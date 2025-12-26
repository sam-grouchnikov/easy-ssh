from database.database import get_connection

# -------- CREATE --------

def add_project(
    db,
    name,
    ssh_path,
    ssh_password_encrypted,
    wandb_api_key_encrypted,
    wandb_user,
    wandb_project,
    github_repo_url,
    github_user,
    git_local_path,
    status,
    last_time
):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO projects (
            name,
            ssh_path,
            ssh_password_encrypted,
            wandb_api_key_encrypted,
            wandb_user,
            wandb_project,
            github_repo_url,
            github_user,
            git_local_path,
            status,
            last_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        ssh_path,
        ssh_password_encrypted,
        wandb_api_key_encrypted,
        wandb_user,
        wandb_project,
        github_repo_url,
        github_user,
        git_local_path,
        status,
        last_time
    ))
    db.commit()
    return cursor.lastrowid


# -------- READ --------

def get_project(db, project_id):
    cursor = db.cursor()
    cursor.execute(
        "SELECT * FROM projects WHERE id = ?",
        (project_id,)
    )
    return cursor.fetchone()


def get_all_projects(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM projects")
    return cursor.fetchall()


# -------- UPDATE --------

def update_project(db, project_id, **kwargs):

    if not kwargs:
        return  # prevent invalid SQL

    cursor = db.cursor()
    fields = ", ".join(f"{key} = ?" for key in kwargs.keys())
    values = list(kwargs.values()) + [project_id]

    cursor.execute(
        f"UPDATE projects SET {fields} WHERE id = ?",
        values
    )
    db.commit()


def delete_project(db, project_id):
    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM projects WHERE id = ?",
        (project_id,)
    )
    db.commit()