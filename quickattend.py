import datetime
from db_man import DatabaseManager
from category import Category
from enum import Enum
from cmd_mod import Cmd

cmds = {'q': 0, 'quit': 0, 'a': 1, 'add': 1, "set-date": 2, "save-record": 3, "show": 4, "help": 5}

def add_record(roster, new_entries):
    # first_names = [x[0] for x in roster.values()]
    added_val = False
    while not added_val:
        fn_input = input("Enter the first name of a student: ").strip()
        if fn_input == "quit" or fn_input == "q":
            added_val = True
            continue
        for id, (fn, ln) in roster.items():
            if fn == fn_input:
                try:
                    att_input = Category[input("Enter status: ").strip().upper()]
                    new_entries[id] = att_input
                    added_val = True
                    break
                except KeyError:
                    print("Status not recognized; please try again.")
                    break
        if not added_val:
            print("Could not find student, please try again.")
    return new_entries
            
        
    # while (student := input("Enter the first name of a student: ").strip() not in first_names):
    #     print("Name not found; try again")
    # new_entries[]

def save_record(dbman, section, new_entries, current_date):
    dbman.update_record(section, new_entries, current_date)

def display_record(dbman, roster, section, new_entries, current_date):
    dbman.update_record(section, new_entries, current_date)    
    saved_record: dict[int, Category] = dbman.read_attendance(section, current_date)
    print(f"\n CURRENT RECORD \n")
    [print(roster[key], val) for key, val in saved_record.items()]              

def set_date(date_str: str) -> datetime.date:
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def print_help():
    print(f"Potential commands: ")
    [print(f"{key}: {Cmd(val).name}") for key, val in cmds.items()]

def validate_section(dbman: DatabaseManager, inp: str) -> str:
    '''Get the class section inputted by the user.
    Returns 'n/a' if the input string matches no section.'''
    valid_sections = [s.strip().upper() for s in dbman.read_sections()]
    inp_processed = inp.strip().upper()
    for section in valid_sections:
        if section == inp_processed:
            return section
    else:
        return "n/a"
    

def run_interface():
    '''Main user interface function.'''
    dbman = DatabaseManager()
    current_date = datetime.date.today()

    # Got some help from Copilot for streamlining this one...
    while (section := validate_section(dbman, input("What section? "))) == "n/a":
        print("Invalid section, try again.")
    
    # Get the roster for the current section
    roster = dbman.read_roster(section)
    # [print(key, val) for key, val in roster.items()]
    
    # Get all the values already entered into the database
    saved_record: dict[int, Category] = dbman.read_attendance(section, current_date)
    new_entries: dict[int, Category] = {}

    while (user_cmd := input("Enter a command (help for all examples): ")) != 0:
        try:
            user_cmd = Cmd(cmds[user_cmd])
        except KeyError:
            print("Did not recognize command; please try again")
            continue
        match user_cmd:
            case Cmd.QUIT:
                break
            case Cmd.ADD_RECORD:
                new_entries = add_record(roster, new_entries)
            case Cmd.SET_DATE:
                current_date = set_date(input("Input the date to edit: "))
                print(f"Date is set to {current_date}")
            case Cmd.SAVE_RECORD:
                save_record(dbman, section, new_entries, current_date)
            case Cmd.DISPLAY_RECORD:
                display_record(dbman, roster, section, new_entries, current_date)
            case Cmd.HELP:
                print_help() 

if __name__ == "__main__":     
    run_interface()
   



