from database.database_crud import get_all_projects

projects = get_all_projects()

for item in projects:
    print(dict(item))