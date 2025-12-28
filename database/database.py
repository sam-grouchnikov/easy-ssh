import sqlite3

def get_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            name TEXT PRIMARY KEY,
            ssh_path TEXT NOT NULL,
            ssh_psw TEXT,
            wandb_api TEXT NOT NULL,
            wandb_user TEXT NOT NULL,
            wandb_project TEXT NOT NULL,
            git_url TEXT NOT NULL,
            git_user TEXT NOT NULL,
            git_path TEXT NOT NULL,
            status INTEGER NOT NULL DEFAULT 0,
            last_update TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized with Name as Primary Key.")