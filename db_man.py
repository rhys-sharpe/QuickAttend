import sqlite3
from category import Category

class DatabaseManager:
    def __init__(self):
        # Set a config file thing for this later
        self.conn = sqlite3.connect("db/db.db")

    def __del__(self):
        self.conn.close()

    def _query_db(self, script) -> list:
        cur = self.conn.cursor()
        cur.execute(script)
        return cur.fetchall()

    def read_roster(self, section: str) -> dict[int, str]:
        '''Return the students registered for this section.'''
        students = {} # Create the dict to return later
       
        script = f"SELECT id, student_name FROM Student\
                WHERE section='{section}'"
        results = self._query_db(script)
        for (id, name) in results:
            students[id] = name
        return students

    def read_sections(self) -> list[str]:
        '''Return the available sections'''
        return [i[0] for i in self._query_db("SELECT label FROM Section;")]


    def read_attendance(self, section, date) -> dict[int, Category]:
        attendance = {}
        script = f"SELECT id, attended FROM Attended\
                   WHERE section = '{section}' AND class_date = '{date}';"
        for (id, category) in self._query_db(script):
            attendance[id] = category
        return attendance


    def update_roster(self, section, record):
        '''Writes 'record' to the database.'''
        updates = {}
        old_record = self.read_attendance(section, datetime.date.today())


if __name__ == "__main__":
    dbman = DatabaseManager()
    roster = dbman.read_roster('A')
    print(roster)
    print(dbman.read_sections())
    print(dbman.read_attendance('A', '2025-08-30'))
