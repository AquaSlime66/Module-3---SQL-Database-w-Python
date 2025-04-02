# import the sqlite library
import sqlite3
#connect to the magic.db database, if it doesn't exist in the PWD
#it's summoned to the directory from nowhere
con = sqlite3.connect("magic.db")

# declare a new cursor
my_cursor = con.cursor()

# function to summon the database tables, if it already exits, don't create it
def create_db():
    my_cursor.execute("CREATE TABLE IF NOT EXISTS card_table(id INT PRIMARY KEY, card_name VARCHAR(50), card_type VARCHAR(60), sub_types VARCHAR(60), conv_cost TINYINT, colorless_pip TINYINT, white_pip TINYINT, blue_pip TINYINT, black_pip TINYINT, red_pip TINYINT, green_pip TINYINT, activated_abs VARCHAR(200), trig_abs VARCHAR(200), stac_trig_abs VARCHAR(200), power TINYINT, toughness TINYINT, scry_link VARCHAR(100))")

    my_cursor.execute("CREATE TABLE IF NOT EXISTS token_table(id INT PRIMARY KEY, token_name VARCHAR(50), type VARCHAR(80), sub_type VARCHAR(80), power INT, toughness INT, abilities VARCHAR(200))")

    my_cursor.execute("CREATE TABLE IF NOT EXISTS link_table(card_id INT, token_id INT)")

# summon THE DATABASE and initialize loop status
create_db()
prog_status = True

def clear_inventory():
    #drop all the tables
    my_cursor.execute("DROP TABLE card_table")
    my_cursor.execute("DROP TABLE token_table")
    my_cursor.execute("DROP TABLE link_table")

    # re-create the tables
    create_db()

def PrintMenu():
    print("\nPlease Select one of the Following Options:")
    print("1. Populate Database with Test Inserts\n(Debugging ONLY, do not use this option unless you've reset)")
    print("2. Display the current Database")
    print("3. Quit Program")
    print("4. Drop all Tables (basically reset the Database)")
    return

def FilterInput(user_input):
    menu_range = {"1", "2", "3", "4", "5", "6", "7"}
    return set(user_input).issubset(menu_range)


def AutoPopulate():
    #insert the demo cards 
    my_cursor.execute("""
        INSERT INTO card_table VALUES
                (1, 'Negan the Cold Blooded', 'Legendary Creature', 'Human Rouge', 5, 2, 1, 0, 1, 1, 0, NULL, 'Whenever an opponent sacrifices a creature, make a treasure token', 'When this creature enters, you and target opponent each secretly choose a creature that player controls. Then those choices are revealed, and that player sacrifices those creatures.', 4, 3, 'https://scryfall.com/card/sld/147/malik-grim-manipulator'),
                (2, 'Mr. House, President and CEO', 'Legendary Artifact Creature', 'Human', 3, 0, 1, 0, 1, 1, 0, '4 T: Roll a six-sided die plus an additional six-sided die for each mana from Treasures spent to activate this ability.', NULL, 'Whenever you roll a 4 or higher, create a 3/3 colorless Robot artifact creature token. If you rolled 6 or higher, instead create that token and a Treasure token.', 0, 4, 'https://scryfall.com/card/pip/7/mr-house-president-and-ceo'),
                (3, 'The Master, Transcendent', 'Legendary Artifact Creature', 'Mutant', 4, 1, 0, 1, 1, 0, 1, 'Put target creature card in a graveyard that was milled this turn onto the battlefield under your control. It’s a green Mutant with base power and toughness 3/3.', NULL, 'When The Master enters, target player gets two rad counters', 2, 4, 'https://scryfall.com/card/pip/6/the-master-transcendent')
""")
    #insert the demo tokens
    my_cursor.execute("""
        INSERT INTO token_table VALUES
                (1, 'Treasure', 'Artifact', 'Treasure', NULL, NULL, 'T: Sacrifice this artifact: Add 1 mana of any color.'),
                (2, 'Robot', 'Artifact Creature', 'Robot', 3, 3, NULL)
""")
    
    # commit the changes
    con.commit()
    
# determine if the color should be added to total mana calculation
def AddManaCalc(color_int, color):
    false_string = ""

    if color_int != 0:
        if color == "colorless":
            false_string = f"{color_int}"
        else:
            for i in range(0, color_int):
                false_string += color
    return false_string

def ManaCalculator(colorless_pip, white, blue, black, red, green):
    r_string = ""

    r_string += AddManaCalc(colorless_pip, "colorless")
    r_string += AddManaCalc(white, "W")
    r_string += AddManaCalc(blue, "U")
    r_string += AddManaCalc(black, "B")
    r_string += AddManaCalc(red, "R")
    r_string += AddManaCalc(green, "G")
    
    return r_string


    
def RetrieveDB():
    for row in my_cursor.execute("SELECT * FROM card_table"):
        print("<------------------------------->")
        card_mana = ManaCalculator(row[5], row[6], row[7], row[8], row[9], row[10])

        print(f"Mana Cost:      {card_mana}")
        print(f"Card Name:      {row[1]}")
        print(f"Card Types:     {row[2]} - {row[3]}")
        print(f"Power/Toughness:{row[14]}/{row[15]}")
        print(f"Activated Ab.   {row[11]}")
        print("~-----------------------------~")
        print(f"Triggered Ab.   {row[12]}")
        print("~-----------------------------~")
        print(f"Static Trig.    {row[13]}")
        
        print("<------------------------------->\n")

def RetrieveDBMed():
    false_id = 0
    for row in my_cursor.execute("SELECT * FROM card_table"):
        print("<------------------------------->")
        false_id += 1
        card_mana = ManaCalculator(row[5], row[6], row[7], row[8], row[9], row[10])

        print(f"Mana Cost:      {card_mana}")
        print(f"Card Name:      {row[1]}")
        print(f"Card Types:     {row[2]} - {row[3]}")
        print(f"Card ID:        {false_id}")
        
        print("<------------------------------->\n")

def RetrieveDB_Detailed():
    print("Test Line")     

def AddCardEntry():

    # retrive the number of items in the DB, attempt to find a new ID from the count
    my_cursor.execute("SELECT COUNT(*) FROM card_table;")

    # convert the amount of items in the database from a tuple? into a integar, add 1 to it, as this will be the next item 
    table_count = int(my_cursor.fetchone()[0])
    table_count += 1

    # open a loop, sees if the ID already exists in the database. If it does, loop again and add 1 to the count until a new ID is found
    entry_loop = True
    while entry_loop:
        my_cursor.execute("SELECT ID FROM card_table WHERE id = ?", (table_count,))
        temp_var = my_cursor.fetchone()
        if temp_var is not None:
            # FAILED KEY
            table_count += 1
        else:
            # SLICK key
            entry_loop = False
            print("worked")

    # retirve the number, ensure nothing else has key, then assign it
    # loop through until key success

    # autopopulate the key
    card_name = input("What's your card's name? ")
    types = input("What's your card's type? ")
    sub_types = input("What are your card's subtypes? ")
    color_count = int(input("How much colorless/generic mana is required for this spell (numbers ONLY)? "))
    white_pip = int(input("How much white mana does the spell cost (numbers ONLY)? "))
    blue_pip = int(input("How much blue mana does the spell cost (numbers ONLY)? "))
    black_pip = int(input("How much black mana does the spell cost (numbers ONLY)? "))
    red_pip = int(input("How much red mana does the spell cost (numbers ONLY)? "))
    green_pip = int(input("How much green mana does the spell cost (numbers ONLY)? "))
    conv_cost = int(color_count) + (white_pip) + int(blue_pip) + int(black_pip) + int(red_pip) + green_pip
    power = int(input("What is your creature's power (numbers ONLY)? "))
    toughness = int(input("What is your creature's toughness (numbers ONLY)? "))
    link = input("What's the scryfall link to your card? ")
    act_abs = input("What are your creature's activated abilites? ")
    trig = input("What are your creature's triggered abilities? ")
    stat_trig = input("What are your creature's static triggered abilities? ")
    
    # you've got all the variables to add a new card to the database... let's input them
    my_cursor.execute("""INSERT INTO card_table 
                      (id, card_name, card_type, sub_types, conv_cost, colorless_pip, white_pip, blue_pip, black_pip, red_pip, green_pip, activated_abs, trig_abs, stac_trig_abs, power, toughness, scry_link)
                      VALUES
                      (?,?,?,?,?,?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                      """, (table_count, card_name, types, sub_types, conv_cost, color_count, white_pip, blue_pip, black_pip, red_pip, green_pip, act_abs, trig, stat_trig, power, toughness, link))

    con.commit()

def DeleteEntry():
    print("Review the Database and pick an item: \nNOTE: ID's are only placeholders")
    RetrieveDBMed()

    my_cursor.execute("SELECT COUNT(*) FROM card_table")
    table_extent = int(my_cursor.fetchone()[0])

    while True:
        entry_input = int(input("Enter here: "))
        if entry_input > table_extent or entry_input < 0:
            print("Your selection is outside the scope of the database, please try again.\n")
        else:
            break


        


        
    #retirve loop and add to count??

print("This project lets the user view, add, and execute pre-planned queries from a locally downloaded or created database. \nThis database in particular stores information about Magic the Gathering cards, but with some changes, could hold literally anything else.")

while prog_status:
    # PrintMenu()
    print("\nPlease Select one of the Following Options:")
    print("1. Populate Database with Test Inserts\n(Debugging ONLY, do not use this option unless you've reset)")
    print("2. Display the current Database")
    print("3. Quit Program")
    print("4. Drop all Tables (basically reset the Database)")
    print("5. Choose a card and display it's token(s) (demonstrate join)")
    print("6. Add a new card to the database")
    print("7. Test current statement")

    user_choice = input("")

    #checks first to see if the input is a digit, and then runs it through a range of menu options
    if user_choice.isdigit() and FilterInput(user_choice):
        match user_choice:
            case "1":
                AutoPopulate()
            # Display the DB
            case "2":
                # retrieve the display function
                RetrieveDB()
            case "3":
                prog_status = False
            case "4":
                clear_inventory()
            case "5":
                RetrieveDB()
            case "6":
                print("\nPlease only input numbers for entries that require numerical responses\n")
                AddCardEntry()
                print("\nSee your new card in the database!\n")
                RetrieveDB()
            case "7":
                DeleteEntry()
        


                

    else:
        #remember to ADD the specified range of the files
        print("Please input a valid number or a number within the menu's range")
    