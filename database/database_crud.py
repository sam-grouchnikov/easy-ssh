from database.database import get_connection


def add_ssh_profile(name, host, port, username, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO ssh_profiles (name, host, port, username, password) 
        VALUES (?, ?, ?, ?, ?)
        
        """, (name, host, port, username, password)
    )

    conn.commit()
    conn.close()

# CRUD for projects

def add_project(db, name, local_path, ssh_user, ssh_ip, ssh_password, ssh_port):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO projects (name, local_path, ssh_user, ssh_ip, ssh_password, ssh_port)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (name, local_path, ssh_user, ssh_ip, ssh_password, ssh_port))
    db.commit()
    return cursor.lastrowid

def get_project(db, project_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
    return cursor.fetchone()

def get_all_projects(db):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM projects")
    return cursor.fetchall()

def update_project(db, project_id, **kwargs):
    cursor = db.cursor()
    fields = ", ".join(f"{key} = ?" for key in kwargs)
    values = list(kwargs.values())
    values.append(project_id)
    cursor.execute(f"UPDATE projects SET {fields} WHERE id = ?", values)
    db.commit()

def delete_project(db, project_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    db.commit()

# CRUD for Github setting
def add_github_settings(db, project_id, repo_url, branch, github_token_encrypted):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO github_settings (project_id, repo_url, branch, github_token_encrypted)
        VALUES (?, ?, ?, ?)
    """, (project_id, repo_url, branch, github_token_encrypted))
    db.commit()
    return cursor.lastrowid

def get_github_settings(db, project_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM github_settings WHERE project_id = ?", (project_id,))
    return cursor.fetchone()

def update_github_settings(db, project_id, **kwargs):
    cursor = db.cursor()
    fields = ", ".join(f"{key} = ?" for key in kwargs)
    values = list(kwargs.values())
    values.append(project_id)
    cursor.execute(f"UPDATE github_settings SET {fields} WHERE project_id = ?", values)
    db.commit()

def delete_github_settings(db, project_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM github_settings WHERE project_id = ?", (project_id,))
    db.commit()

# CRUD for WandB

def add_wandb_settings(db, project_id, wandb_api_key_encrypted, entity, project_name):
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO wandb_settings (project_id, wandb_api_key_encrypted, entity, project_name)
        VALUES (?, ?, ?, ?)
    """, (project_id, wandb_api_key_encrypted, entity, project_name))
    db.commit()
    return cursor.lastrowid

def get_wandb_settings(db, project_id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM wandb_settings WHERE project_id = ?", (project_id,))
    return cursor.fetchone()

def update_wandb_settings(db, project_id, **kwargs):
    cursor = db.cursor()
    fields = ", ".join(f"{key} = ?" for key in kwargs)
    values = list(kwargs.values())
    values.append(project_id)
    cursor.execute(f"UPDATE wandb_settings SET {fields} WHERE project_id = ?", values)
    db.commit()

def delete_wandb_settings(db, project_id):
    cursor = db.cursor()
    cursor.execute("DELETE FROM wandb_settings WHERE project_id = ?", (project_id,))
    db.commit()
