#Code to show summary of MCT data and select based on criteria#

#Connect to DB#

import mysql.connector
from Credentials import *

mydb = mysql.connector.connect(
  host=myhost,
  user=myuser,
  passwd=mypasswd,
  database=mydatabase
)

print(mydb)

#Total accounts in MCT#

mycursor = mydb.cursor()

table = "mct_volumne"

mycursor.execute("select count(*) from" + table + ";")

myresult = mycursor.fetchall()
for x in myresult:
  print("This is the total number of accounts in the MCT table:")
  print(x)

#MCT Analysis#

mycursor = mydb.cursor()

mycursor.execute("select cust_type,pay_method,bill_freq,fuel,df, count(*) from "+table+" group by cust_type,pay_method,bill_freq,fuel,df order by cust_type,pay_method,bill_freq,fuel,df;")

myresult = mycursor.fetchall()
print("MCT Analysis:")
field_name = [field[0] for field in mycursor.description]
print(field_name)
for x in myresult:
  print(x)


#Cleanse Analysis#
#Total clean accounts#
mycursor = mydb.cursor()

mycursor.execute("select count(*) from "+table+" where dc_1 = 'N' and dc_2 = 'N'"
                 "and dc_3 = 'N' and dc_4 = 'N' and dc_5 = 'N' and dc_6 = 'N' and dc_7 = 'N' and dc_8 = 'N' and dc_9 = 'N' and dc_10 = 'N';")

myresult = mycursor.fetchall()
for y in myresult:
  print("This is the total number of clean accounts in the MCT table:")
  print(y)

#Cleanse Summary#

mycursor = mydb.cursor()

mycursor.execute("select reference, count(*) from cleanse_exclusion_data where type = 'dc' group by reference order by count(*) desc;")

myresult = mycursor.fetchall()
print("Cleanse Rule Summary:")
field_name = [field[0] for field in mycursor.description]
print(field_name)
for y in myresult:
  print(y)


#Cleanse Config and values#

mycursor = mydb.cursor()

mycursor.execute("select t2.dc_id, t2.Status, count(*) from cleanse_config t2 left outer join cleanse_exclusion_data t1 on t2.dc_id = t1.reference group by t2.dc_id order by t2.status;")

myresult = mycursor.fetchall()
print("Cleanse Rule Status and Counts:")
field_name = [field[0] for field in mycursor.description]
print(field_name)
for y in myresult:
  print(y)

#Exclusions Analysis#
#Exclusions Total#

mycursor = mydb.cursor()

mycursor.execute("select count(*) from "+table+" where exc_1 = 'N' and exc_2 = 'N' and exc_3 = 'N' and exc_4 = 'N' and exc_5 = 'N' and exc_6 = 'N' and exc_7 = 'N' and exc_8 = 'N' and exc_9 = 'N' and exc_10 = 'N';")

myresult = mycursor.fetchall()
for y in myresult:
  print("This is the total number of non excluded accounts in the MCT table:")
  print(y)


#Exclusion Summary#

mycursor = mydb.cursor()

mycursor.execute("select reference, count(*) from cleanse_exclusion_data where type = 'exc' group by reference order by count(*) desc;")

myresult = mycursor.fetchall()
print("Exclusion Rule Summary:")
field_name = [field[0] for field in mycursor.description]
print(field_name)
for y in myresult:
  print(y)


#Cleanse Config and values#

mycursor = mydb.cursor()

mycursor.execute("select t2.exc_id, t2.Status, count(*) from exclusion_config t2 left outer join cleanse_exclusion_data t1 on t2.exc_id = t1.reference group by t2.exc_id order by t2.status;")

myresult = mycursor.fetchall()
print("Exclusion Rule Status and Counts:")
field_name = [field[0] for field in mycursor.description]
print(field_name)
for y in myresult:
  print(y)





#Clean and non excluded accounts total - all exclusion and cleanse rules#

mycursor = mydb.cursor()

mycursor.execute("select count(*) from "+table+" where exc_1 = 'N' and exc_2 = 'N' and exc_3 = 'N' and exc_4 = 'N' and exc_5 = 'N' and exc_6 = 'N' and exc_7 = 'N' and exc_8 = 'N' and exc_9 = 'N' and exc_10 = 'N' and dc_1 = 'N' and dc_2 = 'N' and dc_3 = 'N'and dc_4 = 'N' and dc_5 = 'N' and dc_6 = 'N' and dc_7 = 'N' and dc_8 = 'N' and dc_9 = 'N' and dc_10 = 'N';")

myresult = mycursor.fetchall()
for y in myresult:
  print("This is the total number of clean and non excluded accounts in the MCT table (including Active and Inactive rules):")
  print(y)


#Clean and non excluded accounts total - Active rules only#

mycursor = mydb.cursor()

mycursor.execute("select count(*) from "+table+" where account_id not in ( select j1.account_id from ((select t1.account_id account_id from cleanse_config t2 left outer join cleanse_exclusion_data t1 on t2.dc_id = t1.reference and t2.status = 'Active') Union (select t1.account_id account_id from exclusion_config t2 left outer join cleanse_exclusion_data t1 on t2.exc_id = t1.reference and t2.status = 'Active')) j1 where j1.account_id is not null order by j1.account_id) and df_match not in  ( select j1.account_id from ((select t1.account_id account_id from cleanse_config t2 left outer join cleanse_exclusion_data t1 on t2.dc_id = t1.reference and t2.status = 'Active') Union (select t1.account_id account_id from exclusion_config t2 left outer join cleanse_exclusion_data t1 on t2.exc_id = t1.reference and t2.status = 'Active')) j1 where j1.account_id is not null order by j1.account_id);")

myresult = mycursor.fetchall()
for y in myresult:
  print("This is the total number of clean and non excluded accounts in the MCT table (Active rules only). Dual Fuel pairing failues have also been removed:")
  print(y)

#Available count check#

mycursor = mydb.cursor()

mycursor.execute("select count(*) from available_accounts;")

myresult = mycursor.fetchall()
for y in myresult:
  print("This is the count from the available_accounts table. It should equal the number above:")
  print(y)

#Available count check - MCT#

mycursor = mydb.cursor()

mycursor.execute("select count(*) from "+table+" where available = 'Y';")

myresult = mycursor.fetchall()
for y in myresult:
  print("This is the available count from the MCT table. It should equal the number above if the update has been successful:")
  print(y)


#Selection profile from Business#

mycursor = mydb.cursor()

mycursor.execute("select * from selection_summary order by filter, variable;")

myresult = mycursor.fetchall()
print("Selection profile from Business")
field_name = [field[0] for field in mycursor.description]
print(field_name)
for y in myresult:
  print(y)



