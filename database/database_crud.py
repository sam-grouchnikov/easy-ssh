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
def get_project(project_name):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE name = ?", (project_name,))
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


# database/database_crud.py

def update_project(project_name, **kwargs):
    if not kwargs:
        return

    conn = get_connection()
    try:
        cursor = conn.cursor()

        fields = ", ".join(f"{key} = ?" for key in kwargs.keys())

        values = list(kwargs.values())

        values.append(project_name)

        cursor.execute(f"UPDATE projects SET {fields} WHERE name = ?", values)

        conn.commit()
    finally:
        conn.close()


# -------- DELETE --------
def delete_project(project_name):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM projects WHERE name = ?", (project_name,))
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