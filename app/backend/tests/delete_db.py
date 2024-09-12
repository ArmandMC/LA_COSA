import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from settings import settings

def delete_db(enn2end = bool):
    if enn2end:
        db_filename = os.path.join("..", settings.Db_TEST_FILEANAME)
    else:
        db_filename = settings.DB_FILEANAME
    
    try:
        # Attempt to delete the file
        os.remove(db_filename)
        print(f"{db_filename} has been deleted successfully.")
    except FileNotFoundError:
        print(f"{db_filename} does not exist.")
    except Exception as e:
        print(f"An error occurred while deleting {db_filename}: {e}")

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        print("Usage: python delete_db.py end2end\n or python delete_db.py")
        sys.exit(1)
    if len(sys.argv) == 2 and sys.argv[1] == "end2end":
        delete_db(True)
    elif len(sys.argv) == 1:
        delete_db(False)
    else:
        print("Usage: python delete_db.py end2end\n or python delete_db.py")
        sys.exit(1)