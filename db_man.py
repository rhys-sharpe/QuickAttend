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
        cur.execute(script)
        self.conn.commit()

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
            attendance[id] = Category[category]
        return attendance

    def _generate_update_block(self, sid: int, section: str, date: datetime.date, attended: Category) -> str:
        return f"UPDATE Attended SET attended = '{attended.name}' WHERE id = {sid} AND class_date = '{date}' AND section = '{section}';"

    def update_record(self, section, new_record: dict[int, Category], current_date):
        '''Writes 'record' to the database.'''
        # updates = record # wat
        
        # old_record - what's read fromm the database
        # new_record - what's passed in from memory
        # additions - what's to be written to the database
        # updates - entries to be changed from their last entry in the database

        additions = {}
        updates = {}
        old_record = self.read_attendance(section, current_date)
        # print(old_record)
        # print(type(old_record))
        # print(not old_record)
        if not old_record:
            additions = self._add_all(section)
        # Loop through update keys, which will either be empty
        # (because there was an old record passed in)
        # or will contain all of the members with their
        # attendance set to a default value (currently, absent)
        # TODO: Fix the above comment (see devlog)
        # print(f"additions is {additions}")
        # print(f"old record is {old_record}")
        for key in new_record.keys():
            if key in old_record.keys():
                if old_record[key] != new_record[key]:
                    # update old key
                    updates[key] = new_record[key]
                # else - they're the same, do nothing
            else:
                # add new key, no need to insert
                additions[key] = new_record[key]
            #     if old_record[key] != new_record[key]: 
            #         updates[key] = new_record[key]
            #     # else, the two records are the same and nothing needs updating
            # else:
            #     updates[key] = new_record[key]

            # # Look for changed keys
            # if key in new_record[key]:
            #     if key not in old_record.keys() or old_record[key] != new_record[key]:
            #         updates[key] = new_record[key]
        # print(f"additions is {additions}")

        # If there are any new people to add, write to the database
        if additions:
            script = f"INSERT INTO Attended(id, class_date, section, attended) VALUES "
            parsed_record_list = [f"({sid}, '{current_date}', '{section}', '{additions[sid].name}')" for sid in additions]
            # print(f"Parsed record list is {parsed_record_list}")
            for value in parsed_record_list:
                script += value
                # Blegh...I hate this but am not sure how to improve it
                if value != parsed_record_list[-1]:
                    script += ", "
                else:
                    script += ";"
            # print(f"script is {script}")
            self._update_db(script)
        
        # If there's any values to change, write to database one at a time
        if updates:
            script = ""
            for key in updates.keys():
                script = self._generate_update_block(key, section, current_date, updates[key]) + " "
                self._update_db(script)


    def _add_all(self, section) -> dict[int, Category]:
        print("No entries found for this date, updating all records...")
        updates = {}
        for key in self.read_roster(section).keys():
            updates[key] = Category.ABSENT
        print(f"from update_all: updates are {updates}")
        return updates



if __name__ == "__main__":
    dbman = DatabaseManager()
    roster = dbman.read_roster('A')
    print(roster)
    print(dbman.read_sections())
    print(dbman.read_attendance('A', '2025-08-30'))
    # print(dbman.update_record('A', {0: Category.PRESENT, 2: Category.ABSENT, 3: Category.TARDY}))
    del dbman
