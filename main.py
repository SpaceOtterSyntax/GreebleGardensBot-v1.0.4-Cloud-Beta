version = str("""

        GREBBLE GARDENS LITE v1.0.3 Developed by: Raphael Ribeiro Dos Santos 11/9/2024

Version changes:

v1.0.2
* Added list of premade phrases to randomly respond to 'garden' input from user.
* Added random import module and created function to retried random phrase from txt file 'GardenPhrases'.
* Changed Repsone and Format from bot when correct input of the stored keyword in 'Phrase.txt' is given.
* Added Function to check prize status or create txt file: 
    Funciton also limits how many times a user claims the prize to 1x by checking if the prize is 'claimed' or 'unclaimed'.
* Sanitized input to accept anycase from user and convert to lower case.

v1.0.3
* Added function to create initial Phrase.txt that would error on first launch. 
    -(minor bug exist: Phrase txt file created and default phrase set to: NOT SET. but can not be read on initial start with "NOT SET". user must enter the first phrase with slash command.)
    -Fixed bug that could not find Phrase.txt file on first use and would error program in terminal. ( refer to the above change )
* DOT ENV is fuuuuuuked ( bug ) 
* recent testing...  succesful use of bot with sql db was done with this code though some bugs definitely remain. Bugs are noted next to the functions. 
""")
print(version)

#IMPORT NEEDED PACKAGED FOR PYTHON + DISCORD BOT
import discord, os, random
from discord.ext import commands
from discord import app_commands
import sqlite3

#LOADING TOKEN METHOD: TBA 
from dotenv import dotenv_values

# GRAB VALID TOKEN
token = dotenv_values(".env")["TOKEN"]



#SERVER ID / GUILD ID ( CHANGE WHEN DEPLOYING FINAL )
GUILD_ID = discord.Object(id=1299101271453732954)

#############################################################################################
####            SECTION BELOW UNDER CONSTRUCTION > SQL INTERACTION FUNCTIONS         ####  
#############################################################################################
#CREATE TABLE IF NOT EXIST
#CREATE DB IF NOT EXIST ( WORKS )
def create_db():
    try:
        conn = sqlite3.connect('Garden_Scoreboard.db')
        with conn:
            cur = conn.cursor()
            cur.execute(f'''CREATE TABLE IF NOT EXISTS Garden_Scoreboard (username,seedscore)'''), print("found table or table was crated")
            conn.commit(), print("Commit sent, CREATE DB IF NOT EXIST = Garden_Scoreboard\n")
    except sqlite3.Error as error:
        print(f"whoops an ERROR OCCURED:{error}")
create_db()


# SQL COMMUNICATION ( USING WITH STATEMENTS TO AUTO CLOSE ONCE COMPLETE) 
def get_seedbank(): #( NEEDS WORK - /WILL ONLY DISPLAY 1 ROW WHEN REQUESTED THROUGH THE BOT /)
    conn = sqlite3.connect('Garden_Scoreboard.db')
    with conn:
        cur = conn.cursor()
        query = cur.execute("SELECT * FROM Garden_Scoreboard ORDER BY seedscore DESC")
        rows = query.fetchall()
        for row in rows:
            return row
    print("Query results returned successfully")
    
def add_player_to_db(username, seedscore): #( WORKS BUT DUPLICATES ENTRIES CAN BE MADE )
    try:
        conn = sqlite3.connect('Garden_Scoreboard.db')
        with conn:
            cur = conn.cursor()
            sql_values = (username, seedscore)
            sql_query = str("""INSERT INTO Garden_Scoreboard (username, seedscore) VALUES(?, ?)""")
            cur.execute(sql_query, sql_values)
            conn.commit()
    except sqlite3.Error as error:
		    print("Failed to insert info into database, ERROR HERE ->:",error)

def update_seedscore(username, seedscore): #( NOT TESTED )
    try:
        conn = sqlite3.connect('Garden_Scoreboard.db')
        with conn:
            cur = conn.cursor()
            sql_values = (seedscore, username)
            sql_updt_query = str("UPDATE Garden_Scoreboard SET seedscore=? WHERE username == ?")
            cur.execute(sql_updt_query,sql_values)
            conn.commit()
    except sqlite3.Error as error:
        print("Failed to update scoreboard, see error", error)
#############################################################################################
####            SECTION ABOVE UNDER CONSTRUCTION > SQL INTERACTION FUNCTION         ####  
#############################################################################################

# PHRASE OF THE DAY FUNCTIONS
file_path = "Phrase.txt"
if not os.path.exists(file_path):
    with open('Phrase.txt','w') as file:
        file.write('NOTSET')
        print(f"created Phrase.txt file..")

#BOT TO SET THE PHRASE INTO TXT FILE
def writetotxt(phrase):
        with open('Phrase.txt','w') as file:
            file.write(phrase.lower())
        with open('Oldlist.txt','a') as file:
            file.write(phrase + ', \n')
       

#BOT READ THE PHRASE FROM TXT FILE
def open_phrase():
    try:
        with open('Phrase.txt','r') as file:
            content = file.read()
        return content
    except IOError as e:
        print(e)

#GETTING PRIZE STATUS AND WRITING OVER PREV STATUS
file_path = 'Prize_Status.txt'
def writeprizestatus(str):
    with open('Prize_Status.txt','w') as file:
        file.write(str.lower())

file_path = 'Prize_Status.txt'
def prize_status():
    try:
        if not os.path.exists(file_path):
            with open('Prize_Status.txt','w') as file:
                file.write('unclaimed'.lower())
        else:
            with open('Prize_Status.txt','r') as file:
                content = file.read()
                return content
    except IOError as e:
        print(f"there was an error: {e}")
    else: 
        print(f"check for txt file, if not found one will be created and set to unclaimed status")
    
#GET GARDEN PHRASE LIST FROM TXT FILE
def Random_Garden_Phrases():
    with open('GardenPhrases.txt', 'r')as file:
        content = file.readlines()
        content = [content.strip() for content in content]
        random_phrase = random.choice(content)
        return random_phrase

#APP/BOT CLIENT GETS CREATED
class Client(commands.Bot):
    # BOT READY, CHECKING SYNCED COMMANDS w/ ERROR HANDLING
    async def on_ready(self):
        #these print commands go-to terminal not response to discord.
        print('Logged on as', self.user)
        print(f'''Bot Ready''')
        # VERIFY SLASH COMMANDS ARE UPDATED ON LAUNCH
        try:
            guild = discord.Object(id=1299101271453732954)
            synced = await self.tree.sync(guild=guild)
            print(f'Synched {len(synced)} commands to your guild {guild.id}')
        except Exception as e:
            print(f'Error syncing commands: {e}')
    
    # WAITING ON MESSAGES IN DISCORD FROM USERS AND USING CONDITION STATEMENTS
    async def on_message(self, message):
        prize_stat = prize_status() 
        phrase = str(open_phrase())
        GardenPhrases = str(Random_Garden_Phrases())
                
        if message.author == self.user:
            return
        elif prize_stat == 'claimed' and message.content.lower() == (f"!{phrase}"):
            await message.channel.send(f'''Sorry, But there is no quest at this time...''')
        elif prize_stat == 'unclaimed' and message.content.lower() == (f"!{phrase}"):
            print(f"a user has found the keyword")
            writeprizestatus('claimed')
            await message.channel.send(f'''**Congratulations**, **{message.author}**! \n It seems you've solved Thoughts' riddle and uncovered the secret phrase. Can you guess what happens next? Go and fetch what the elusive Draik seeks and return it to his lair, if you've been successful you'll receive something worth your time... You have three days. _Fetch the item that was the secret phrase and send it to Quill to receive your reward! If you don't complete the quest in time, it will silently reset. Good luck!_ \n Don't know what you're looking at? Go here: _https://www.grundos.cafe/~Thoughts/_''')
        elif message.content.startswith(('garden','Garden','GARDEN')):
            await message.channel.send(f"{GardenPhrases}")
        else: 
            print(f"Else happened here... Bot misunderstood or ignored input.")
            return 

# SETUP TO RUN THE CLIENT
intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=intents)

#############################################################################################
#### SLASH COMMANDS ####
#############################################################################################

#SLASH COMMAND /SAY HELLO
@client.tree.command(name="hello", description="say hello!", guild=GUILD_ID)
async def sayHello(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message(f"HEEEEYYYY GARDEN LOVER..{user.mention}")

# SLASH COMMAND /SETPHRASE
@client.tree.command(name="setphrase", description="For admins to set challenge phrase", guild=GUILD_ID)
async def setphrase(interaction: discord.Interaction, phrase: str):
    writetotxt(phrase)
    writeprizestatus('unclaimed')
    await interaction.response.send_message(f"You have set the challenge phrase to: !{phrase}, and quest has been reset.")

#############################################################################################
####            SECTION BELOW UNDER CONSTRUCTION > SQL INTERACTION COMMANDS         ####  
#############################################################################################
# SLASH COMMAND /SEEDBANK
@client.tree.command(name="seedbank", description="Show current Garden seeds Scoreboard", guild=GUILD_ID)
async def seedbank(interaction: discord.Interaction):
    try:
        results = get_seedbank()
        await interaction.response.send_message(f"-- Grebble Gardens Seed Scoreboard -- \n {results}")
    except ValueError as e:
        return e

# SLASH COMMAND /INSERT PLAYER AND SCORE ( USERNAME + AMOUNT )
@client.tree.command(name="add_player", description="Adds new player to the scoreboard by username.", guild=GUILD_ID)
async def add_player(interaction: discord.Interaction, user: discord.Member, add_seedscore: int):
    username = str(user)
    seedscore = add_seedscore
    add_player_to_db(username, seedscore)
    await interaction.response.send_message(f"You have requested to add a player and give em my seeds! \n {username} has been added and given {seedscore} seeds.")



@client.tree.command(name="update_player_score", description="Updates the players seedscore by username and score to be updated", guild=GUILD_ID)
async def update_score(interaction: discord.Interaction, user: discord.Member, updtd_seedscore: int):
    username = str(user)
    seedscore = updtd_seedscore
    update_seedscore(username, seedscore)
    await interaction.response.send_message(f"You have updated {username}'s seedscore to {seedscore}")
#############################################################################################
####            SECTION ABOVE UNDER CONSTRUCTION > SQL INTERACTION COMMANDS         ####
#############################################################################################

# RUNNING THE CLIENT USING DOT ENV
client.run(token)
