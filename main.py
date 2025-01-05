import csv
import datetime

### Read in csv of names and numbers, return tuple of hashmaps num-person and person-attended ####
def read_roster(section: str):
    roster_dict = {}
    with open(f"data/roster.csv", 'r') as roster:
        reader = csv.reader(roster)
        for lines in reader:
            # Does the current line match the current section?
            if lines[2] == section:
                roster_dict[lines[0]] = lines[1]
    return roster_dict
            

### while not 'q', get input ###
# if num typed mark present
# if s write hashmap to csv, overwriting it
def save_attendance(section, current_record):
    # remove already
    filtered_record = {}
    old_record = read_attendance(section, datetime.date.today())
    for key in current_record:
        if key not in old_record.keys():
            filtered_record[key] = current_record[key]
    with open(f"data/lab-record-{section}.csv", "a") as file:
        writer = csv.writer(file)
        for id, name in filtered_record.items():
            writer.writerow([datetime.date.today(), id, name])
    print("Saved!")

def read_attendance(section, date):
    att_record = {}
    with open(f"data/lab-record-{section}.csv", "r") as file:
        reader = csv.reader(file)
        for line in reader:
            # skip blank lines
            if len(line)>0:
                if line[0] == str(date):
                    att_record[line[1]] = line[2]
    return att_record

def add_attendee(roster, record, user_inp) -> bool:
    try:
        user_inp = user_inp.strip()
        record[user_inp] = roster[user_inp]
        return True
    except KeyError:
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
                if line[0] == inp.strip().upper():
                    return line[0]
    return "n/a"
                    

def main():
    # Get the current section
    section = get_section(input("What section? "))
    while section != "n/a":
        section = get_section(input("Sorry, that was an invalid section. Try again: "))
    
    # Get the roster for the current section
    roster = read_roster(section)
    [print(key, val) for key, val in roster.items()]
    # initialize an empty dict of id numbers and names to record who was there
    record = read_attendance(section, datetime.date.today())
    user_inp = input("Enter a number; s to save; q to quit: ")
    while (user_inp != 'q'):
        if user_inp == 's':
            save_attendance(section, record)
        elif user_inp == 'p':
            print(f"Roster: {roster}")
            print(f"Attended: {record}")
            print(f"Count: {len(record)} / {len(roster)}")
        else:
            if (add_attendee(roster, record, user_inp)):
                print("Added user!")
                #print(f"Added{roster[user_inp]}")
            else:
                print("Invalid, please try again")
        user_inp = input("Enter a number; s to save; q to quit: ")
    else:
        save_attendance(section, record)

### Call main and get lab section, pass to top ###
main()