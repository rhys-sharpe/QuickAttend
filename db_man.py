import sqlite3

class DatabaseManager:
    def __init__(self):
        # Set a config file thing for this later
        self.conn = sqlite3.connect("db/db.db")

    def __del__(self):
        self.conn.close()

    def read_roster(self, section: str) -> dict[int, str]:
        '''Return the students registered for this section.'''
        students = {} # Create the dict to return later
        script = f"SELECT id, student_name FROM Student\
                WHERE section='{section}'"
        cur = self.conn.cursor()
        cur.execute(script)
        for (id, name) in cur.fetchall():
            students[id] = name
        return students

    def read_sections(self) -> list[str]:
        '''Return the available sections'''
        sections = []
        script = f"SELECT label FROM Section"
        cur = self.conn.cursor()
        cur.execute(script)
        return [i[0] for i in cur.fetchall()]

if __name__ == "__main__":
    dbman = DatabaseManager()
    roster = dbman.read_roster('A')
    print(roster)
    print(dbman.read_sections())