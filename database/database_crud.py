from database.database import get_connection

# -------- CREATE --------
def add_project(
    name,
    ssh_path,
    ssh_password,
    wandb_api_key,
    wandb_user,
    wandb_project,
    github_repo_url,
    github_user,
    git_local_path,
    status,
    last_time
):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects (
                name,
                ssh_path,
                ssh_psw,
                wandb_api,
                wandb_user,
                wandb_project,
                git_url,
                git_user,
                git_path,
                status,
                last_update
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            name,
            ssh_path,
            ssh_password,
            wandb_api_key,
            wandb_user,
            wandb_project,
            github_repo_url,
            github_user,
            git_local_path,
            status,
            last_time
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


# -------- READ --------
def get_project(project_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        return cursor.fetchone()
    finally:
        conn.close()


def get_all_projects():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects")
        return cursor.fetchall()
    finally:
        conn.close()


# -------- UPDATE --------
def update_project(project_id, **kwargs):
    if not kwargs:
        return  # prevent invalid SQL

    conn = get_connection()
    try:
        cursor = conn.cursor()
        fields = ", ".join(f"{key} = ?" for key in kwargs.keys())
        values = list(kwargs.values()) + [project_id]

        cursor.execute(f"UPDATE projects SET {fields} WHERE id = ?", values)
        conn.commit()
    finally:
        conn.close()


# -------- DELETE --------
def delete_project(project_id):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        conn.commit()
    finally:
        conn.close()

def delete_all_projects():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects")
        conn.commit()
    finally:
        conn.close()
