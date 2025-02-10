# Greeble-Gardens-Bot-v1.0.4-Beta

                GREBBLE GARDENS LITE v1.0.4-Beta 
        Developed by: Raphael Ribeiro Dos Santos 11/9/2024

Version changes:
v1.0.4-Beta 
BIG UPDATE!
* Replaced DOT ENV for token mangmnt - DOTENV was bugged for me, replaced with aws parameter store to secure string on the cloud.
* Uploaded code to aws platform for 24/7 use! 
* Changed Token auth to integrate with aws ec2 services.
* Removed import fx for PrettyTables -> TableStyle

v1.0.3
* Added function to create initial Phrase.txt that would error on first launch. 
    -(minor bug exist: Phrase txt file created and default phrase set to: NOT SET. but can not be read on initial start with "NOT SET". user must enter the first phrase with slash command.)
    -Fixed bug that could not find Phrase.txt file on first use and would error program in terminal. ( refer to the above change )

v1.0.2
* Added list of premade phrases to randomly respond to 'garden' input from user.
* Added random import module and created function to retried random phrase from txt file 'GardenPhrases'.
* Changed Repsone and Format from bot when correct input of the stored keyword in 'Phrase.txt' is given.
* Added Function to check prize status or create txt file: 
    Funciton also limits how many times a user claims the prize to 1x by checking if the prize is 'claimed' or 'unclaimed'.
* Sanitized input to accept anycase from user and convert to lower case.
