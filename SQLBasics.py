def main(cmd):
	import sqlite3, os
	
	# CONNECTING TO DB AND GETTING CURSOR
	conn = sqlite3.connect('Garden_Scoreboard.db')
	print("connecting to database...") 
	cur = conn.cursor()
	print('''Successfully Connected to SQLite, You've Got Cursor!\n''')

	#CREATE DB IF NOT EXIST 
	def create_db():
		try:
			cur.execute(f'''CREATE TABLE IF NOT EXISTS Garden_Scoreboard (id,username,seedscore)'''), print("found table or table was crated")
			conn.commit(), print("Commit sent, CREATE DB IF NOT EXIST = Garden_Scoreboard\n")
	
		except sqlite3.Error as error:
			print(f"whoops an ERROR OCCURED:{error}")
	create_db()
	
	# FUTURE FEATURE TBA ( OPTIONAL NAME OPTION RQST FROM USER AS A LIVE PROGRAM )

	file_path = 'Garden_Scoreboard.db'

	#REQUEST LEADERBOARD BY RANKING > to < 
	def show_seedbank():
		cur = conn.cursor()
		query = cur.execute("SELECT username, seedscore FROM Garden_Scoreboard ORDER BY seedscore DESC")
		rows = query.fetchall()
		print("-- Grebble Gardens Seed Scoreboard -- \n",)
		for row in rows:
			return print(row)
		
		#return print("-- Grebble Gardens Seed Scoreboard -- \n",query.fetchall())
		
	#INSERT FUNCTION
	# 		INSERTING MULTIPLE VALUES INTO SQL DB FROM QUERY STRING
	def insertodb():
		#	DESIRED VALUES TO BE ENTERED
		sql_values = []

		discord_id = input("Enter discord_id: ")
		sql_values.append(discord_id)

		username = input("Enter username: ")
		sql_values.append(username)

		seedscore = input("Enter seedscore: ")
		sql_values.append(seedscore)

		#	SQL QUERT TO BE PASSED
		sql_query = str("""INSERT INTO Garden_Scoreboard (id, username, seedscore) VALUES(?, ?, ?)""")

		print(sql_values)
		try:
			cur.execute(sql_query, sql_values)
			conn.commit()
			print("Executed INSERT query...")

		except sqlite3.Error as error:
			print("Failed to insert info into database, ERROR HERE ->:",error)

		finally:
			if conn:
				print("End Func > insertodb ")
	

	#UPDATE FUNCTION
	def updatedb_score():
		username = input("Enter username: ")
		updt_seedscore = input("Enter new score:")
		
		sql_updt_query = str("UPDATE Garden_Scoreboard SET seedscore=? WHERE username == ?")
		try:
			cur.execute(sql_updt_query,(updt_seedscore, username))
			conn.commit()
			print("Executed UPDATE query...")
		except sqlite3.Error as error:
			print(f"An ERROR OCCURRED UPDATING: {error}")
		finally:
			if conn:
				print("End Func > Update score - Closing DB")
				return
	######## 
	#DELETE TBA
	########
	#CONDITIONAL STATEMENTS FOR INPUT RECEIVED
	if cmd == str("show seedbank"):
		print("requesting Scoreboard...\n")
		return show_seedbank()
	
	elif cmd == str("insert"):
		print("You are entering info into the database and will need to provied 3 values, discord_id, discord_username, seedscore.\n")
		insertodb()

	elif cmd == str("update score"):
		print("score update func loading.\n")
		updatedb_score()
	else:
		return 

if __name__ == __name__:
	loadscreen = "Loading SQLBasics Project...\n" 
	version = (''' \n Welcome to my SQLBasics Project, and this is my SQL Databse using Python and Sqlite3. \n  			Version 1.0.1 First Edition \n''')
	try:
		print(loadscreen)
		print(version)
		cmd = input("ENTER COMMAND FOR DATABASE: ")
		main(cmd)
	except Exception as error:
		print(f"Program closed there was an error: {error}")
	finally:
		closing_prg_msg = ("CLOSING >> SQLBasics by Raphael Dos Santos - version 1.0.1")
		print(closing_prg_msg)
		


