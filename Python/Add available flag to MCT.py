#Code to show summary of MCT data and select based on criteria#

#Connect to DB#

import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Nottingham14",
  database="migration"
)


#Total accounts in MCT#

mycursor = mydb.cursor()

mycursor.execute("update mct set available = 'Y' where account_id in (select account_id from available_accounts);")
print(mycursor.rowcount," Accounts updated as available in MCT")
mycursor.execute("commit;")




