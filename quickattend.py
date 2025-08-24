import csv
import datetime
from enum import Enum

# TODO: Build a function to read this in later
class Category(Enum):
    PRESENT = 0
    EXCUSED = 1
    TARDY = 2
    ABSENT = 3

### Read in csv of names and numbers, return tuple of hashmaps num-person and person-attended ####
def read_roster(section: str):
    '''Read the class roster from a CSV.'''
    roster_dict = {}
    with open(f"class_data/roster.csv", 'r') as roster:
        reader = csv.reader(roster)
        for lines in reader:
            # Does the current line match the current section?
            if lines[2].strip().upper() == section:
                roster_dict[lines[0]] = lines[1]
    return roster_dict
            
def write_roster(updated_roster, section):
    with open("class_data/record.csv", "a") as file:
        writer = csv.writer(file)
        for id, status in updated_roster.items():
            writer.writerow([id, datetime.date.today(), section, str(status.name)])


def bulk_update(section, date, old_record):
    '''Triggered each new class period. Bulk-marks students as absent unless specified otherwise.
    TODO: Set default in config later.'''
    print("entering bulk update")
    roster = read_roster(section)
    recorded_keys = old_record.keys()
    updated_record = old_record
    for id in roster.keys():
        if id not in recorded_keys:
            updated_record[id] = Category.ABSENT
    return updated_record

def save_attendance(section, current_record):
    '''Writes the current attendance dict to a CSV.
    If no entries have been added for this date and section, then all students will be marked as absent through
    the bulk_update function. This does not affect '''
    # remove already
    updates = {}
    old_record = read_attendance(section, datetime.date.today())
    old_keys = old_record.keys()
    for key in current_record.keys():
        # Check and see if this key is missing. If it is, then bulk_update has not yet run or a student has been hot-swapped in.
        # The latter should not happen.
        # This will mark all students as absent, then update the current one. Should only ever run once in the for-loop.
        if key not in old_keys:
             updates = bulk_update(section, datetime.date.today(), old_record)
        # else if old_record[key] != current_record[key]:
            # if key in old_keys:
            #     print(f"old_key: {old_record[key]}")
            # print(current_record[key])
        updates[key] = current_record[key]
    print(updates)
    write_roster(updates, section)
    print("Saved!")


def read_attendance(section, date) -> dict[str, Category]:
    '''
    Create a dictionary mapping student names to their attendance status.
    Selects only for the specified section and date (like a WHERE query).
    '''
    att_record = {}
    with open("class_data/record.csv", "r") as file:
        reader = csv.reader(file)
        for line in reader:
            # skip blank lines
            if len(line) > 0:
                # check if it's for the right section & date
                if line[2].strip() == section and line[1] == str(date):
                    # map current name to attendance status
                    print(f"line is {line}")
                    att_record[line[0]] = Category[line[3]]
    return att_record

def add_attendee(record, user_inp, status: str) -> bool:
    '''
    Add the specified user to the record dictionary.
    :param record: The record dictionary to add to/check.
    :param user_inp: the id NUMBER of the user to add.
    :param status: What to mark the student as. Should be one of the types defined in categories.csv.
    :return True if the operation succeeded; False if there is no such ID in the record.
    '''
    try:
        user_inp = user_inp.strip()
        record[user_inp] = status
        return True
    except KeyError:
        # Key user_inp does not exist in record, aborting
        return False

# TODO: Is this whole thing too complciated?
def get_section(inp: str) -> str:
    '''Get the class section inputted by the user.
    Returns 'n/a' if the input string matches no section.'''
    with open(f"system_data/sections.csv") as sections:
        reader = csv.reader(sections)
        for line in reader:
            # Skip blank lines
            if len(line) > 0:
                # Search for correct section
                curr_section = line[0].strip().upper()
                if curr_section == inp.strip().upper():
                    return curr_section
    return "n/a"
                    

def get_attendance():
    '''Main user interface function.'''
    # Get the current section
    section = get_section(input("What section? "))
    while section == "n/a":
        section = get_section(input("Sorry, that was an invalid section. Try again: "))
    
    # TODO: GET DATE HERE

    # Get the roster for the current section
    roster = read_roster(section)
    [print(key, val) for key, val in roster.items()]
    # initialize an empty dict of id numbers and statuses to record who was there
    record = read_attendance(section, datetime.date.today())
    # [print(key, val) for key, val in record.items()]
    user_inp = input("Enter a number; s to save; p to print; q to quit: ")
    while (user_inp != 'q'):
        if user_inp == 's':
            save_attendance(section, record)
        elif user_inp == 'p':
            print(f"Roster: {roster}")
            print(f"Attended: {record}")
            print(f"Count: {len(record)} / {len(roster)}")
        else:
            inp_status = Category(int(input("Enter status: ")))
            if (add_attendee(record, user_inp, inp_status)):
                print(f"Added user{roster[user_inp]} with status {inp_status}")
            else:
                print("Invalid, please try again")
        user_inp = input("Enter a number; s to save; q to quit: ")
    else:
        save_attendance(section, record)

### Execute user interface if not used as a package ###
if __name__ == "__main__":
    get_attendance()