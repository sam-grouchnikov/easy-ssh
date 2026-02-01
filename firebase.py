from __future__ import annotations
import time, requests
import keyring
from dataclasses import dataclass
from typing import Any, Dict, Optional

# PUBLIC KEY
API_KEY = "AIzaSyCM5k5OWiIMUPeDqA_hhmHN3mnpuguGvcE"
PROJECT_ID = "easy-ssh"


# ---------- Firestore REST type conversion (write) ----------
def _to_fs_value(v: Any) -> Dict[str, Any]:
    if v is None: return {"nullValue": None}
    if isinstance(v, bool): return {"booleanValue": v}
    if isinstance(v, int) and not isinstance(v, bool): return {"integerValue": str(v)}
    if isinstance(v, float): return {"doubleValue": v}
    if isinstance(v, str): return {"stringValue": v}
    if isinstance(v, dict): return {"mapValue": {"fields": {k: _to_fs_value(val) for k, val in v.items()}}}
    if isinstance(v, (list, tuple)): return {"arrayValue": {"values": [_to_fs_value(x) for x in v]}}
    raise TypeError(f"Unsupported type: {type(v)}")

def to_fs_fields(d: Dict[str, Any]) -> Dict[str, Any]:
    return {k: _to_fs_value(v) for k, v in d.items()}


# ---------- Firestore REST type conversion (read) ----------
def _from_fs_value(v: Dict[str, Any]) -> Any:
    if "stringValue" in v: return v["stringValue"]
    if "integerValue" in v: return int(v["integerValue"])
    if "doubleValue" in v: return float(v["doubleValue"])
    if "booleanValue" in v: return bool(v["booleanValue"])
    if "nullValue" in v: return None
    if "mapValue" in v:
        fields = v["mapValue"].get("fields", {})
        return {k: _from_fs_value(val) for k, val in fields.items()}
    if "arrayValue" in v:
        vals = v["arrayValue"].get("values", [])
        return [_from_fs_value(x) for x in vals]
    raise ValueError(f"Unknown Firestore value: {v}")

def from_fs_doc(doc_json: Dict[str, Any]) -> Dict[str, Any]:
    fields = doc_json.get("fields", {})
    return {k: _from_fs_value(v) for k, v in fields.items()}


@dataclass
class AuthSession:
    uid: str
    id_token: str
    refresh_token: str
    id_token_exp: float


class FirebaseError(RuntimeError):
    pass


class FirebaseClient:
    """
    Desktop-safe Firebase access:
    - Email/password login via Auth REST
    - Firestore via REST with Bearer idToken (Security Rules apply)
    - Stores refresh token in OS keychain via keyring
    """

    KEYRING_SERVICE = "easy-ssh"
    KEYRING_REFRESH = "firebase_refresh_token"

    def __init__(self, api_key: str, project_id: str):
        self.api_key = api_key
        self.project_id = project_id
        self._session: Optional[AuthSession] = None

    # ---- AUTH ----
    def sign_in(self, email: str, password: str) -> AuthSession:
        # documented signInWithPassword endpoint :contentReference[oaicite:4]{index=4}
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        data = self._post_json(url, payload)
        return self._set_session(data, persist_refresh=True)

    def sign_up(self, email: str, password: str) -> AuthSession:
        url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={self.api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        data = self._post_json(url, payload)
        return self._set_session(data, persist_refresh=True)

    def try_restore_session(self) -> bool:
        rt = keyring.get_password(self.KEYRING_SERVICE, self.KEYRING_REFRESH)
        if not rt:
            return False
        id_token, uid, expires_in = self._refresh(rt)
        self._session = AuthSession(
            uid=uid,
            id_token=id_token,
            refresh_token=rt,
            id_token_exp=time.time() + int(expires_in) - 60,
        )
        return True

    def sign_out(self) -> None:
        self._session = None
        try:
            keyring.delete_password(self.KEYRING_SERVICE, self.KEYRING_REFRESH)
        except Exception:
            pass

    def uid(self) -> str:
        self._require_session()
        return self._session.uid

    def _ensure_id_token(self) -> str:
        self._require_session()
        assert self._session is not None
        if time.time() < self._session.id_token_exp:
            return self._session.id_token
        id_token, uid, expires_in = self._refresh(self._session.refresh_token)
        self._session.uid = uid
        self._session.id_token = id_token
        self._session.id_token_exp = time.time() + int(expires_in) - 60
        return self._session.id_token

    def _refresh(self, refresh_token: str) -> tuple[str, str, str]:
        # token flow described in Identity Platform REST usage :contentReference[oaicite:5]{index=5}
        url = f"https://securetoken.googleapis.com/v1/token?key={self.api_key}"
        r = requests.post(url, data={"grant_type": "refresh_token", "refresh_token": refresh_token}, timeout=15)
        if not r.ok:
            raise FirebaseError(f"Refresh failed: {r.text}")
        j = r.json()
        return j["id_token"], j["user_id"], j["expires_in"]

    def _set_session(self, j: Dict[str, Any], persist_refresh: bool) -> AuthSession:
        expires_in = int(j.get("expiresIn", "3600"))
        sess = AuthSession(
            uid=j["localId"],
            id_token=j["idToken"],
            refresh_token=j["refreshToken"],
            id_token_exp=time.time() + expires_in - 60,
        )
        self._session = sess
        if persist_refresh:
            keyring.set_password(self.KEYRING_SERVICE, self.KEYRING_REFRESH, sess.refresh_token)
        return sess

    def _post_json(self, url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        r = requests.post(url, json=payload, timeout=15)
        if r.ok:
            return r.json()
        try:
            msg = r.json().get("error", {}).get("message", r.text)
        except Exception:
            msg = r.text
        raise FirebaseError(msg)

    def _require_session(self) -> None:
        if self._session is None:
            raise FirebaseError("Not signed in.")

    # ---- FIRESTORE ----
    def get_doc(self, doc_path: str) -> Dict[str, Any]:
        # Firestore REST accepts Firebase ID tokens; rules apply :contentReference[oaicite:6]{index=6}
        id_token = self._ensure_id_token()
        url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents/{doc_path}"
        r = requests.get(url, headers={"Authorization": f"Bearer {id_token}"}, timeout=15)
        if not r.ok:
            raise FirebaseError(r.text)
        return r.json()

    def set_doc(self, doc_path: str, data: Dict[str, Any]) -> Dict[str, Any]:
        id_token = self._ensure_id_token()
        url = f"https://firestore.googleapis.com/v1/projects/{self.project_id}/databases/(default)/documents/{doc_path}"
        body = {"fields": to_fs_fields(data)}
        r = requests.patch(url, json=body, headers={"Authorization": f"Bearer {id_token}"}, timeout=15)
        if not r.ok:
            raise FirebaseError(r.text)
        return r.json()


# ----- convenience for YOUR config doc -----
DEFAULT_CONFIG = {
    "user": "",
    "email": "",
    "ssh_user": "",
    "ssh_ip": "",
    "ssh_psw": "",
    "ssh_port": 22,
    "git_url": "",
    "git_pat": "",
    "wandb_user": "",
    "wandb_proj": "",
    "wandb_api": ""
}

def config_doc_path(uid: str) -> str:
    return f"users/{uid}/config/main"

if __name__ == "__main__":
    from pprint import pprint

    fb = FirebaseClient(API_KEY, PROJECT_ID)

    print("=== Firebase Desktop Test ===")

    email = input("Email: ").strip()
    password = input("Password: ").strip()

    # ---- Sign in ----
    try:
        session = fb.sign_in(email, password)
        uid = fb.uid()
        print(f"\n✅ Signed in successfully")
        print(f"UID: {uid}")
    except Exception as e:
        print("\n❌ Sign-in failed")
        print(e)
        raise SystemExit(1)

    # ---- Config document path ----
    doc_path = config_doc_path(uid)

    # ---- Load or create config ----
    try:
        print("\n📥 Loading config from Firestore...")
        doc = fb.get_doc(doc_path)
        config = from_fs_doc(doc)
        print("Config loaded:")
        pprint(config)
    except Exception:
        print("\n⚠️ Config not found, creating default config...")
        fb.set_doc(doc_path, DEFAULT_CONFIG)
        config = DEFAULT_CONFIG.copy()
        print("Default config created.")

    # ---- Modify one field ----
    print("\n✏️ Updating test field...")
    config["user"] = "test-user"
    fb.set_doc(doc_path, config)

    # ---- Read back ----
    print("\n📥 Re-loading config after update...")
    doc = fb.get_doc(doc_path)
    updated_config = from_fs_doc(doc)

    print("\n✅ Final config from Firestore:")
    pprint(updated_config)

    print("\n🎉 Test complete — Firebase Auth +")

# if __name__ == "__main__":
#     from pprint import pprint
#
#     fb = FirebaseClient(API_KEY, PROJECT_ID)
#
#     email = input("Email: ").strip()
#     password = input("Password: ").strip()
#
#     fb.sign_in(email, password)
#     uid = fb.uid()
#
#     path = config_doc_path(uid)
#
#     # Load current config
#     doc = fb.get_doc(path)
#     config = from_fs_doc(doc)
#
#     print("\nCurrent config:")
#     pprint(config)
#
#     # ---- MODIFY WHAT YOU WANT HERE ----
#     config["ssh_user"] = "ubuntu"
#     config["ssh_ip"] = "1.2.3.4"
#     config["ssh_port"] = 22
#     config["git_url"] = "https://github.com/yourname/repo"
#
#     # Save back to Firestore
#     fb.set_doc(path, config)
#
#     print("\n✅ Config updated successfully.")
