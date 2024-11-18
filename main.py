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
    (minor bug exist: Phrase txt file created and default phrase set to: NOT SET. but can not be read on initial start with "NOT SET". user must enter the first phrase with slash command.)
* Fixed bug that would search for Phrase.txt file on first use and would error program in terminal. ( refer to the above change )

* testing connection to db ... 

""")
print(version)

#IMPORT NEEDED PACKAGED FOR PYTHON + DISCORD BOT
import discord, os, random
from discord.ext import commands
from discord import app_commands
from dotenv import dotenv_values

from cogs import SQLBasics

token = dotenv_values(".env")["TOKEN"]


print("bot token is valid, bot loading...")
#SERVER ID / GUILD ID ( CHANGE WHEN DEPLOYING FINAL )
GUILD_ID = discord.Object(id=1299101271453732954)

#SQL COMMUNICATION
def get_seedbank(request):
    if request == "seedbank":
        content = SQLBasics("show seedbank")
        print(content)      
        return content
    else:
        print("nothing happened sadly")


# PHRASE OF THE DAY FUNCTIONS
file_path = "Phrase.txt"
with open('Phrase.txt','w') as file:
    file.write('NOTSET')
    print(f"created Phrase.txt file..")

#BOT TO SET THE PHRASE INTO TXT FILE
def writetotxt(phrase):
        with open('Phrase.txt','w') as file:
            file.write(phrase.lower())
            #print(f"A Phrase was entered into the txt file: {phrase}") #FOR DEBUGING IO 
        with open('Oldlist.txt','a') as file:
            file.write(phrase + ', \n')
        #print(f"Phrase added to old list: {phrase}") #FOR DEBUGING IO

#FOR BOT READ THE PHRASE FROM TXT FILE
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
    
#GET GARDEN PHRASE LIST
def Random_Garden_Phrases():
    with open('GardenPhrases.txt', 'r')as file:
        content = file.readlines()
        content = [content.strip() for content in content]
        random_phrase = random.choice(content)
        return random_phrase

#APP/BOT CLIENT GETS CREATED
class Client(commands.Bot):
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

#### SLASH COMMANDS ####
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

# SLASH COMMAND /SEEDBANK
@client.tree.command(name="seedbank", description="Show current seedscore", guild=GUILD_ID)
async def seedbank(interaction: discord.Interaction):
    get_seedbank("seedbank")
    await interaction.response.send_message(f"You have requested for thy seeds!\n {get_seedbank}")

# RUNNING THE CLIENT USING DOT ENV
client.run('token')
