#Code to show summary of MCT data and select based on criteria#

#Connect to DB#

import sys
import mysql.connector
from Credentials import *

mydb = mysql.connector.connect(
  host=myhost,
  user=myuser,
  passwd=mypasswd,
  database=mydatabase
)

print("Do you want to continue - y/n")
x=input()
if x == "n":
  print("Programme stopped")
  sys.exit
else:
  print("Programme continuing")
