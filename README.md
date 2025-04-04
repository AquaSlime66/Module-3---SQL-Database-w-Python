# Overview

This program creates a database that links *Magic, the Gathering* cards to the tokens they create. The user can add new cards, modify existing cards, and delete cards straight from the database. All of the code is contained in a single python file, with execute statements written in SQL. The database is structured inside of one of these statements, but could easily be automatically configured in the schema table when creating a database file through an application like mySQL Workbench.

My goal from this program was to connect a database to a program. At this point in my programming career, I know several different languages and methods of programming, but aside from javascript and HTML, I've never connected any languages together. I'm extremely familar with both SQL and Python, so this project was a great way to assemble both languages together.

The program opens a up a menu from which the user can select any of the previously mentioned options. Once an option has been chosen, executed SQL statements are ran against the database, and selected rows are returned and assigned to local variables in Python for further processing and/or manipulation, as the user chooses.



**{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of how created the Relational Database.}**

[Python + DB Demonstration Video](https://youtu.be/4Nfrew0ufcw)

# Relational Database

The *magic* database holds three tables. A card table, containing information about each card, a token table containing information about each token, and a link table, connecting or joining the two tables together. 
The two tables (card and token) exhibit a many to many relationship. A card can generate many different tokens (although some don't create any), and tokens can come from a multitude of different cards, most are not exclusive to only one card.

### Table Columns
**Card Table**
| Column Name        | Data Type |
|-----------------|------------------------------------------------|
| ID |INT|
|    card_name   | VARCHAR                         |
|card_type    |VARCHAR        |
|sub_types | VARCHAR|
|conv_cost | TINYINT |
| colorless_pip | TINYINT |
| white_pip | TINYINT |
| blue_pip | TINYINT |
| black_pip | TINYINT |
| red_pip | TINYINT |
| green_pip | TINYINT |
| activated_abs | VARCHAR |
| trig_abs | VARCHAR |
| stac_trig_abs | VARCHAR |
| power | TINYINT |
| toughness | TINYINT |
| scry_link | VARCHAR |
****
**Token Table**
| Column Name        | Data Type |
|-----------------|------------------------------------------------|
| ID |INT|
| token_name | VARCHAR |
| type | VARCHAR |
| sub_type | VARCHAR |
| power | TINYINT |
| toughness | TINYINT |
| abilities | VARCHAR |
****
**Link Table**
| Column Name        | Data Type |
|-----------------|------------------------------------------------|
| ID |INT|
|card_id | INT |
|token_id | INT |



# Development Environment

### Tools Used
- Visual Studio Code: Source code editor with built-in terminal(s)
- GitHub: Popular hosting and code repository site (what you're likely viewing the code on)

### Language & Libraries
- Python: Programming Language recognized for it's easy readability and variable versatility.
- SQL: Structured Query Language, language for manipulating relational databases. It can do everything from creating a database to deleting specific rows.
- **Libraries** *import at the top of program, with "import library_name"*
- sqlite3

# Useful Websites

- [SQLite Basic Documentation/Integration](https://docs.python.org/3/library/sqlite3.html)
- [SQLite Advanced Documentation (Less used)](https://docs.python.org/3.9/library/sqlite3.html)
- [ChatGPT]() Used for finding syntax, and variable passing fixes

# Future Work

- **Menu Clean-up:** The menu does function and work as intended, but it's pretty janky. I easily could fix it up, but I got so sucked into the modification part that this task got pushed back. A few clear screens and text formatting would really improve the program's visuals.
- **Improved Column Modification:** I dumped a lot of time into this project, much more than was needed, as I enjoyed it a lot, I love both of these languages. The column modification was something I could not simplify down. I thought the only method was to extract whichever variable the user desired, and manually create a filter to only allow numerical inputs into the field(s). As of the program's upload, modification is only available for three columns, and I'd like it to cover every column we have, aside from primary key values.
- **Allowing User Querying (with limits):** A large part of SQL is filtering and retrieve specific entries or groups that meet a set of criteria. I had a fun sort of stretch goal of allowing to user to sort of build their own query. This would let them find say, all cards that share the "Human" sub-type, or all cards that are artifact creatures. This will be really fun to make (yes, I do plan on making it), but it's honestly enough work to be it's own project. Assembling query strings based on user input AND validating user choice as a correct parameter is a lot of variable manipulation, a LOT.
