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
    roster_dict = {}
    with open(f"class_data/roster.csv", 'r') as roster:
        reader = csv.reader(roster)
        for lines in reader:
            # Does the current line match the current section?
            if lines[2].strip().upper() == section:
                roster_dict[lines[0]] = lines[1]
    return roster_dict
            

### while not 'q', get input ###
# if num typed mark present
# if s write hashmap to csv, overwriting it
def save_attendance(section, current_record):
    # remove already
    updates = {}
    old_record = read_attendance(section, datetime.date.today())
    old_keys = old_record.keys()
    for key in current_record.keys():
        if key not in old_keys or Category[old_record[key]] != current_record[key]:
            if key in old_keys:
                print(f"old_key: {old_record[key]}")
            print(current_record[key])
            updates[key] = current_record[key]
    with open("class_data/record.csv", "a") as file:
        writer = csv.writer(file)
        for id, status in updates.items():
            writer.writerow([id, datetime.date.today(), section, str(status.name)])
    print("Saved!")


def read_attendance(section, date) -> dict[str, str]:
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
                    att_record[line[0]] = line[3]
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
                    

def main():
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
    user_inp = input("Enter a number; s to save; q to quit: ")
    while (user_inp != 'q'):
        if user_inp == 's':
            save_attendance(section, record)
        elif user_inp == 'p':
            print(f"Roster: {roster}")
            print(f"Attended: {record}")
            print(f"Count: {len(record)} / {len(roster)}")
        else:
            if (add_attendee(record, user_inp, Category(int(input("Enter status: "))))):
                print("Added user!")
                #print(f"Added{roster[user_inp]}")
            else:
                print("Invalid, please try again")
        user_inp = input("Enter a number; s to save; q to quit: ")
    else:
        save_attendance(section, record)

### Call main and get lab section, pass to top ###
main()