import sqlite3
from category import Category
import datetime

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

    def _update_db(self, script):
        cur = self.conn.cursor()

    def read_roster(self, section: str) -> dict[int, tuple[str, str]]:
        '''Return the students registered for this section.'''
        students = {} # Create the dict to return later
       
        script = f"SELECT id, first_name, last_name FROM Student\
                WHERE section='{section}'"
        results = self._query_db(script)
        for (id, first_name, last_name) in results:
            students[id] = (first_name, last_name)
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


    def update_record(self, section, record):
        '''Writes 'record' to the database.'''
        updates = {}
        old_record = self.read_attendance(section, datetime.date.today())
        if not old_record:
            self._update_all
        for key in record.keys():
            # Look for changed keys
            if old_record[key] != record[key]:
                updates[key] = record[key]
        script = f"INSERT INTO Attended(id, class_date, section, attended) VALUES"
        parsed_record_list = [f"({sid}, {datetime.date.today()}, {section}, {cat})" for sid, cat in updates]
        for value in parsed_record_list:
            script += value
            # Blegh...I hate this but am not sure how to improve it
            if value != parsed_record_list[-1]:
                script += ", "
        self._update_db(script)

    def _update_all(self):

        pass



if __name__ == "__main__":
    dbman = DatabaseManager()
    roster = dbman.read_roster('A')
    print(roster)
    print(dbman.read_sections())
    print(dbman.read_attendance('A', '2025-08-30'))
    del dbman
