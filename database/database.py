import sqlite3

def get_connection():
    return sqlite3.connect('app.db')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            local_path TEXT NOT NULL,
            ssh_user TEXT NOT NULL,
            ssh_ip TEXT NOT NULL,
            ssh_password_encrypted TEXT NOT NULL,
            ssh_port INTEGER NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS github_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            repo_url TEXT,
            branch TEXT,
            github_token_encrypted TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wandb_settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER NOT NULL,
            wandb_api_key_encrypted TEXT,
            entity TEXT,
            project_name TEXT,
            FOREIGN KEY (project_id) REFERENCES projects(id)
        );
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized.")
