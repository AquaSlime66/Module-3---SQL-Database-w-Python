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

# drop all the tables, re-create them
def clear_inventory():
    #drop all the tables
    my_cursor.execute("DROP TABLE card_table")
    my_cursor.execute("DROP TABLE token_table")
    my_cursor.execute("DROP TABLE link_table")

    # re-create the tables
    create_db()
    con.commit()

# filters user input, could have been condensed, but I'm burned out
def FilterInput(user_input):
    menu_range = {"1", "2", "3", "4", "5", "6", "7", "8"}
    return set(user_input).issubset(menu_range)

# automatically insert hard-coded values into the Database, card table, token table, WORK ON link table
def AutoPopulate():
    # insert the demo cards 
    my_cursor.execute("""
        INSERT INTO card_table 
            (id, card_name, card_type, sub_types, conv_cost, colorless_pip, white_pip, blue_pip, black_pip, red_pip, green_pip, activated_abs, trig_abs, stac_trig_abs , power, toughness, scry_link)
                VALUES
                (1, 'Negan the Cold Blooded', 'Legendary Creature', 'Human Rouge', 5, 2, 1, 0, 1, 1, 0, '', 'Whenever an opponent sacrifices a creature, make a treasure token', 'When this creature enters, you and target opponent each secretly choose a creature that player controls. Then those choices are revealed, and that player sacrifices those creatures.', 4, 3, 'https://scryfall.com/card/sld/147/malik-grim-manipulator'),
                (2, 'Mr. House, President and CEO', 'Legendary Artifact Creature', 'Human', 3, 0, 1, 0, 1, 1, 0, '4 T: Roll a six-sided die plus an additional six-sided die for each mana from Treasures spent to activate this ability.', '', 'Whenever you roll a 4 or higher, create a 3/3 colorless Robot artifact creature token. If you rolled 6 or higher, instead create that token and a Treasure token.', 0, 4, 'https://scryfall.com/card/pip/7/mr-house-president-and-ceo'),
                (3, 'The Master, Transcendent', 'Legendary Artifact Creature', 'Mutant', 4, 1, 0, 1, 1, 0, 1, 'Put target creature card in a graveyard that was milled this turn onto the battlefield under your control. Its a green Mutant with base power and toughness 3/3.', '', 'When The Master enters, target player gets two rad counters', 2, 4, 'https://scryfall.com/card/pip/6/the-master-transcendent')
""")
    #insert the demo tokens
    my_cursor.execute("""
        INSERT INTO token_table VALUES
                (1, 'Treasure', 'Artifact', 'Treasure', NULL, NULL, 'T: Sacrifice this artifact: Add 1 mana of any color.'),
                (2, 'Robot', 'Artifact Creature', 'Robot', 3, 3, NULL)
""")
    con.commit()
    
    #insert the connection table
    my_cursor.execute("""
            INSERT INTO link_table (card_id, token_id)
                VALUES
                (2, 1),
                (2, 2),
                (1, 1)     """)
        
    
    con.commit()
    
# determine if the color should be added to total mana calculation
def AddManaCalc(color_int, color):
    # generate a template to build off of
    false_string = ""

    # not all colors have a value, if it doesn't, return the empty template
    if color_int != 0:
        # the colorless color is represented as numbers, not symbols. Return only the provided number
        if color == "colorless":
            false_string = f"{color_int}"
        else:
        # for each count of the color symbol, return a symbol
            for i in range(0, color_int):
                false_string += color
    return false_string

# return a concated string from passed along integer values and color types
def ManaCalculator(colorless_pip, white, blue, black, red, green):
    # craft the generated numbers together into a displayed string

    r_string = ""

    r_string += AddManaCalc(colorless_pip, "colorless")
    r_string += AddManaCalc(white, "W")
    r_string += AddManaCalc(blue, "U")
    r_string += AddManaCalc(black, "B")
    r_string += AddManaCalc(red, "R")
    r_string += AddManaCalc(green, "G")
    
    return r_string

# print off the basics for each item in the database
def RetrieveDB():
    # select every row, display selected variables
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

# print off a false ID for each item (with bare min. basics)
def RetrieveDBMed():
    # create a false id
    false_id = 0
    # display each item from the table, with very dumbed down variables
    for row in my_cursor.execute("SELECT * FROM card_table"):
        print("<------------------------------->")
        false_id += 1
        card_mana = ManaCalculator(row[5], row[6], row[7], row[8], row[9], row[10])

        print(f"Mana Cost:      {card_mana}")
        print(f"Card Name:      {row[1]}")
        print(f"Card Types:     {row[2]} - {row[3]}")
        print(f"Card ID:        {false_id}")
        
        print("<------------------------------->\n")
    
# return the real ID for a value from RetrieveDBMed
def RetrieveDBMedReturn(user_choice):
    # create an empty false and real id, fill later
    false_id = 0
    real_id = 0

    # for each row, generate the false id, compare to the user's chosen false ID
    for row in my_cursor.execute("SELECT * FROM card_table"):
        false_id += 1
        if false_id == user_choice:
            # once you find a match, return the true id
            real_id = int(row[0])
            return real_id
    
    # bad scenario, likely never to occur
    my_cursor.execute("SELECT ID FROM card_table WHERE ID = ?", (real_id,))
    temp_var = my_cursor.fetchone()
    if temp_var is None:
         print("You've broken the program somehow, this likely comes from a very invalid, manually inserted ID.")
         return 404
                
# add a new card to the database
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

# print the smaller database display
def FalseDisplay():
    print("Review the Database and pick an item: \nNOTE: ID's are only placeholders")
    RetrieveDBMed()

    # retrieve the count of all items in the DB, assign it to a variable
    my_cursor.execute("SELECT COUNT(*) FROM card_table")
    table_extent = int(my_cursor.fetchone()[0])

    # ask the user for a false ID based on the display
    while True:
        entry_input = int(input("Enter here: "))
        # if the user's selection is outside of the selection of the DB, tell them
        if entry_input > table_extent or entry_input < 0:
            print("Your selection is outside the scope of the database, please try again.\n")
        else:
        # break the loop if the false ID is valid
            break
    
    # retrieve the true/real item id
    true_id = int(RetrieveDBMedReturn(entry_input))
    # return the true id
    return true_id

# delete an entry
def DeleteEntry():
    # retrieve the entry's ID from FalseDisplay
    true_id = int(FalseDisplay())

    # select the chosen line, assign it to a fetchable value
    my_cursor.execute("SELECT card_name from card_table WHERE id =?", (true_id,))
    temp_confirm = my_cursor.fetchone()[0]

    # ask the user to confirm deletion
    confirm_del = input(f"Are you sure you want to delete: {temp_confirm}\n1. Yes\n2. No")
    if confirm_del == "1":
        # on confirmation, delete based on the extracted ID
        my_cursor.execute("DELETE FROM card_table WHERE id = ?", (true_id,))
        # select the ID, assign to fetched variable
        my_cursor.execute("SELECT ID FROM card_table WHERE id = ?", (true_id,))
        temp_var = my_cursor.fetchone()

        # check to see if the query was empty
        # it needs to be empty, that means it's been deleted
        if temp_var is None:
            print("Card successfully deleted! ")
        else:
            print("Deletion failed! Try again. ")
    # commit the changes
    con.commit()

# update an entry
def EditEntry():
    # call the FalseDisplay function
    true_id = int(FalseDisplay())

    # select the chosen row, fetch it as selected_row
    my_cursor.execute("SELECT * FROM card_table WHERE id = ?", (true_id,))
    selected_row = my_cursor.fetchone()
    
    print("As of now, the Database can only handle limited edits:\nPlease enter the ID of the item you'd like to modify")
    
    # show the user the 3 editable variables, ask them to choose one of them, deny further progress until a valid selection has been made
    while True:
        print(f"1. Card Name:       {selected_row[1]}\n2. Card Type(s):    {selected_row[2]}\n3. Subtype(s):      {selected_row[3]}")
        user_choice = int(input("Enter the number for the item you'd like to edit: "))
        if (user_choice > 3 or user_choice < 0):
            print("Error: input is outside of the menu range (only 1-3)")
        else: 
            break
    
        # based on user choice, generate the changed value
    if user_choice == 1:
        selected_value = "card_name"
    elif user_choice == 2:
        selected_value = "card_type"
    else:
        selected_value = "sub_types"
    
    new_item = input(f"\nWhat would you like to the change the card's {selected_value} to? ")

    # generate a false query string with the selected value, then pass it directly into an executable string
    temp_sql_string = f"UPDATE card_table SET {selected_value} = ? WHERE id = ?"
    my_cursor.execute(temp_sql_string, (new_item, true_id))

    # commit changes
    con.commit()


    # print(selected_row[1])
    # false_id = 0
    # for thing in selected_row:
    #     false_id += 1
    #     print(f"ID: {false_id}      {thing}")

# show off the join
def JoinDisplay():
    print("NOTE: This line connects a single card to some tokens, it is static and has no user interaction, but does complete the join")
    print("The join also assumes that the database is in it's default state, if it's not, please go back and run option 6 + 7")
    temp_input = int(input("Do you need to go back?\n1. Yes\n 2. No "))
    if temp_input == 1:
        return
    
    # my_cursor.execute("SELECT id FROM card_table WHERE card_name = 'Mr. House, President and CEO'")
    # house_id = int(my_cursor.fetchone()[0])

    my_cursor.execute("""
            SELECT card_table.card_name, token_table.token_name
            FROM link_table
            JOIN card_table ON card_table.id = link_table.card_id 
            JOIN token_table ON token_table.id = link_table.token_id
                      """)
    
    results = my_cursor.fetchall()

    for row in results:
        print(f"Card:    {row[0]}")
        print(f"Token:   {row[1]}")
        print("<-------------------------->")
    

    #fetch all from selection 


print("This project lets the user view, add, and execute pre-planned queries from a locally downloaded or created database. \nThis database in particular stores information about Magic the Gathering cards, but with some changes, could hold literally anything else.")

while prog_status:
    # PrintMenu()
    print("\nPlease Select one of the Following Options:")
    print("1. Add a new card to the database")
    print("2. Display the current Database")
    print("3. Edit an Card")
    print("4. Delete a Card")
    print("5. Choose a card and display it's token(s) (demonstrate join)")
    print("6. Drop all Tables (basically reset the Database)")
    print("7. Populate Database with Test Inserts\n(Debugging ONLY, do not use this option unless you've reset with option 6.)")
    print("8. Quit Program")
    # 

    # CHANGE the insert statements 1 -> Add a new card to the database  2 -> Display DB

    user_choice = input("")

    #checks first to see if the input is a digit, and then runs it through a range of menu options
    if user_choice.isdigit() and FilterInput(user_choice):
        match user_choice:
            case "1":
                print("\nPlease only input numbers for entries that require numerical responses\n")
                AddCardEntry()
                print("\nSee your new card in the database!\n")
                RetrieveDB()
            # Display the DB
            case "2":
                # retrieve the display function
                RetrieveDB()
            case "3":
                EditEntry()
            case "4":
                DeleteEntry()
            case "5":
                JoinDisplay()
            case "6":
                clear_inventory()
            case "7":
                AutoPopulate()
            case "8":
                prog_status = False
            

                

    else:
        #remember to ADD the specified range of the files
        print("Please input a valid number or a number within the menu's range")
    