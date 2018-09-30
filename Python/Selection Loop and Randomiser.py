#This python routine loops through the available rows in the MCT and calculates how much the business data requirements have been met.
#This will rerun the routine a configurable number of times, changing the order of accounts randomly to try and get the best fit

#import functions from Python

import mysql.connector
import sys
import datetime
import itertools
import random
import operator

#Set the date and time fore the start of the execution

now=datetime.datetime.now()
starttime = now
print("*************************************")
print("Execution start time:",now.strftime("%Y-%m-%d %H:%M:%S"))
print("*************************************")

#Connect to the mysql database

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="Nottingham14",
  database="migration"
)

#Load MCT into python

#Table = ("mct")
Table = ("mct_volumne")
mycursor = mydb.cursor()
sql = ("select account_id, cust_type,pay_method,bill_freq,fuel,df,df_match from "+Table+" where available = 'Y'")
mycursor.execute(sql)
myresult = mycursor.fetchall()

#Initialise lists for table columns - each column is a seperate list. 

account_id=[]
cust_type=[]
pay_method=[]
bill_freq=[]
fuel=[]
df=[]
df_match=[]

#Load data into lists

#Results={}

for row in myresult:
    #print (row[0],row[1])
    account_id.append(row[0])
    cust_type.append(row[1])
    pay_method.append(row[2])
    bill_freq.append(row[3])
    fuel.append(row[4])
    df.append(row[5])
    df_match.append(row[6])

#Get the total number of rows in the account ID column

maxlength = len(account_id)

#Count the unique variables per column - needs to be configured if more are added

total_count = maxlength
cust_type_res = cust_type.count("res")
cust_type_sme = cust_type.count("sme")
cust_type_b2b = cust_type.count("b2b")
pay_method_dd = pay_method.count("DD")
pay_method_cc =pay_method.count("CC")
pay_method_chq = pay_method.count("CHQ")
bill_freq_M = bill_freq.count("M")
bill_freq_Q = bill_freq.count("Q")
fuel_E = fuel.count("E")
fuel_G = fuel.count("G")
DF_Y = df.count("Y")
DF_N = df.count("N")

#Set the counts for each of the variables
#future improvement would be to load this from a csv directly


total_max = 1000
cust_type_res_val =800
cust_type_sme_val = 100
cust_type_b2b_val = 100
pay_method_dd_val = 800
pay_method_chq_val = 100
pay_method_cc_val = 100
bill_freq_M_val = 500
bill_freq_Q_val = 500
fuel_E_val = 500
fuel_G_val = 500
DF_Y_val = 700
DF_N_val = 300

#Initialise the new lists that are used to hold the selected records

selected_account_list=[]
selected_cust_type=[]
selected_pay_method=[]
selected_bill_frequency=[]
selected_fuel=[]
selected_df=[]
selected_df_match=[]
removed_account_list=[]

#Print a summary of the required fields from the business, compared to the actual available from the MCT

print("\n")
print("Accounts available in MCT = ",total_count)
print("Required Accounts from business = ",total_max)
print("\n")
print("*************************************")
print("Availability Summary from MCT:")
print("*************************************")
print ("Available- Res:",cust_type_res,"SME:",cust_type_sme," B2B:",cust_type_b2b)
print ("Required - Res:",cust_type_res_val,"SME:",cust_type_sme_val," B2B:",cust_type_b2b_val)
print ("Available -DD:",pay_method_dd,"CHQ:",pay_method_chq," CC:",pay_method_cc)
print ("Required - DD:",pay_method_dd_val,"CHQ:",pay_method_chq_val," CC:",pay_method_cc_val)
print ("Available -Monthly:",bill_freq_M,"Quarterly:",bill_freq_Q)
print ("Required - Monthly:",bill_freq_M_val,"Quarterly:",bill_freq_Q_val)
print ("Available -Electric:",fuel_E,"Gas:",fuel_G)
print ("Required - Electric:",fuel_E_val,"Gas:",fuel_G_val)
print ("Available -Dual Fuel:",DF_Y,"Single Fuel:",DF_N)
print ("Required - Dual Fuel:",DF_Y_val,"Single Fuel:",DF_N_val)
print("*************************************")
print("\n")
total_count = 0

#These variable needs to be kept outside all the loops

results =[]
resultsdetail=[]
totalaccountvalue=[]
totaldict={}
dictcount={}

#Make the code iterate z Times, in order to allow the gretest chance of meeting the right criteria from the buiness
bb = 1
z = 10

#This is the first loop that runs through the cycle z times

while bb < z:
    print("*************************************")
    print("*************************************")
    print ("This is cycle:",bb)
    #Initialise the selected lists again, to clear them from the last iteration of the loop
    selected_account_list=[]
    selected_cust_type=[]
    selected_pay_method=[]
    selected_bill_frequency=[]
    selected_fuel=[]
    selected_df=[]
    selected_df_match=[]
    removed_account_list=[]


#Generating a random list of accounts to be tried, this takes the total number of account rows, and reorders them randomly, then uses this to select the position of accounts in the MCT

    account_range = range(0,maxlength)
    y = maxlength - 1
    c={}
    c = random.sample(account_range,y)
    #selected_account_list
   # print("C is:",c)

#Second loop which is going through the index of account rows to be tried
    
    for x in c:
        a = "Y"
        b="N"

#3rd loop which stops processing if the current count has gone over the required total
        
        if total_count < total_max:

#For each account, the rows are added to the seperate selection lists
        
            selected_account_list.append(account_id[x])
            selected_cust_type.append(cust_type[x])
            selected_pay_method.append(pay_method[x])
            selected_bill_frequency.append(bill_freq[x])
            selected_fuel.append(fuel[x])
            selected_df.append(df[x])
            selected_df_match.append(df_match[x])

#Counts are generated for each of the variables in the selection list

           # total_count = len(selected_account_list)
            cust_type_res = selected_cust_type.count("res")
            cust_type_sme = selected_cust_type.count("sme")
            cust_type_b2b = selected_cust_type.count("b2b")
            pay_method_dd = selected_pay_method.count("DD")
            pay_method_cc =selected_pay_method.count("CC")
            pay_method_chq = selected_pay_method.count("CHQ")
            bill_freq_M = selected_bill_frequency.count("M")
            bill_freq_Q = selected_bill_frequency.count("Q")
            fuel_E = selected_fuel.count("E")
            fuel_G = selected_fuel.count("G")
            DF_Y = selected_df.count("Y")
            DF_N = selected_df.count("N")
        
#Fourth loops which check all the variables to see if the count has gone over.

            if cust_type_res > cust_type_res_val:
                a = "N"
            else:
                b ="Y"
            if cust_type_sme > cust_type_sme_val:
                a = "N"
            else:
                b ="Y"
            if cust_type_b2b > cust_type_b2b_val:
                a = "N"
            else:
                b ="Y"


            if pay_method_dd > pay_method_dd_val:
                a = "N"
            else:
                b ="Y"
            if pay_method_cc > pay_method_cc_val:
                a = "N"
            else:
                b ="Y"
            if pay_method_chq > pay_method_chq_val:
                a = "N"
            else:
                b ="Y"


            if bill_freq_M > bill_freq_M_val:
                a = "N"
            else:
                b ="Y"
            if bill_freq_Q > bill_freq_Q_val:
                a = "N"
            else:
                b ="Y"


            if fuel_E > fuel_E_val:
                a = "N"
            else:
                b ="Y"
            if fuel_G > fuel_G_val:
                a = "N"
            else:
                b ="Y"


            if DF_Y > DF_Y_val:
                a = "N"
            else:
                b ="Y"
            if DF_N > DF_N_val:
                a = "N"
            else:
                b ="Y"



            if a=="Y":
                total_count = len(selected_account_list)
            else:
                selected_account_list.remove(account_id[x])
                selected_cust_type.remove(cust_type[x])
                selected_pay_method.remove(pay_method[x])
                selected_bill_frequency.remove(bill_freq[x])
                selected_fuel.remove(fuel[x])
                selected_df.remove(df[x])
                selected_df_match.remove(df_match[x]) 
                total_count = len(selected_account_list)
                removed_account_list.append(account_id[x])
            #print("account removed")
        else:
            b ="Y"
            total_count = len(selected_account_list)
           # print("Success! Account toal reached")
           # print("Accounts selected = ",total_count)
           # print("Required Accounts = ",total_max)
           # print("*************************************")
         #   print("Selected Accounts:",selected_account_list)
           # print("*************************************")
           # print ("Actual   - Res:",cust_type_res,"SME:",cust_type_sme," B2B:",cust_type_b2b)
           # print ("Required - Res:",cust_type_res_val,"SME:",cust_type_sme_val," B2B:",cust_type_b2b_val)
           # print ("Actual -   DD:",pay_method_dd,"CHQ:",pay_method_chq," CC:",pay_method_cc)
           # print ("Required - DD:",pay_method_dd_val,"CHQ:",pay_method_chq_val," CC:",pay_method_cc_val)
           # print ("Actual -   Monthly:",bill_freq_M,"Quarterly:",bill_freq_Q)
           # print ("Required - Monthly:",bill_freq_M_val,"Quarterly:",bill_freq_Q_val)
           # print ("Actual -   Electric:",fuel_E,"Gas:",fuel_G)
           # print ("Required - Electric:",fuel_E_val,"Gas:",fuel_G_val)
           # print ("Actual -   Dual Fuel:",DF_Y,"Single Fuel:",DF_N)
           # print ("Required - Dual Fuel:",DF_Y_val,"Single Fuel:",DF_N_val)
           # print("*************************************")
            #break
         #   print("Accounts not selected:",removed_account_list)

#Calculate percentage actual against required value

    total_count_pc = (total_count / total_max) * 100
    cust_type_res_pc = (cust_type_res / cust_type_res_val) * 100
    cust_type_sme_pc = (cust_type_sme / cust_type_sme_val) * 100
    cust_type_b2b_pc = (cust_type_b2b / cust_type_b2b_val) * 100
    pay_method_dd_pc = (pay_method_dd / pay_method_dd_val) * 100
    pay_method_chq_pc = (pay_method_chq / pay_method_chq_val) * 100
    pay_method_cc_pc = (pay_method_cc / pay_method_cc_val) * 100
    bill_freq_M_pc = (bill_freq_M / bill_freq_M_val) * 100
    bill_freq_Q_pc = (bill_freq_Q / bill_freq_Q_val) * 100
    fuel_E_pc = (fuel_E / fuel_E_val) * 100
    fuel_G_pc = (fuel_G / fuel_G_val) * 100
    DF_Y_pc = (DF_Y / DF_Y_val) * 100
    DF_N_pc = (DF_N / DF_N_val) * 100

#Calculate overall data set score

    actual_store=[total_count,cust_type_res,cust_type_sme,cust_type_b2b,pay_method_dd,pay_method_chq,pay_method_cc,bill_freq_M,bill_freq_Q,fuel_E,fuel_G,DF_Y,DF_N]
    required_store=[total_max,cust_type_res_val,cust_type_sme_val,cust_type_b2b_val,pay_method_dd_val,pay_method_chq_val,pay_method_cc_val,bill_freq_M_val,bill_freq_Q_val,fuel_E_val,fuel_G_val,DF_Y_val,DF_N_val]
    total_actual = sum(actual_store)
    total_required = sum(required_store)
    overall_score = (total_actual / total_required) * 100

#Print the final counts with actual and required        
    variance = total_max - total_count
    if variance == 0:
        print("Success! Count Reached")
    else:
        print("Count Not Reached")    

    print("Accounts selected = ",total_count)
    print("Required Accounts = ",total_max)
    variance = total_max - total_count
    print("Variance of ",variance)
    #print("Selected Accounts:",selected_account_list)
    print("*************************************")
    print ("Actual   - Res:",cust_type_res,"SME:",cust_type_sme," B2B:",cust_type_b2b)
    print ("Required - Res:",cust_type_res_val,"SME:",cust_type_sme_val," B2B:",cust_type_b2b_val)
    print ("Actual -   DD:",pay_method_dd,"CHQ:",pay_method_chq," CC:",pay_method_cc)
    print ("Required - DD:",pay_method_dd_val,"CHQ:",pay_method_chq_val," CC:",pay_method_cc_val)
    print ("Actual -   Monthly:",bill_freq_M,"Quarterly:",bill_freq_Q)
    print ("Required - Monthly:",bill_freq_M_val,"Quarterly:",bill_freq_Q_val)
    print ("Actual -   Electric:",fuel_E,"Gas:",fuel_G)
    print ("Required - Electric:",fuel_E_val,"Gas:",fuel_G_val)
    print ("Actual -   Dual Fuel:",DF_Y,"Single Fuel:",DF_N)
    print ("Required - Dual Fuel:",DF_Y_val,"Single Fuel:",DF_N_val)
    print("*************************************")
    #print("Removed Accounts:",removed_account_list)

#print the percentage match results

   # print("*************************************")
    print("Percentage Stats against Required Target:")
    print("*************************************")
    print("Total Account Match:",total_count_pc,"%")
    print("Customer Type RES Match:",cust_type_res_pc,"%")
    print("Customer Type SME Match:",cust_type_sme_pc,"%")
    print("Customer Type B2B Match:",cust_type_b2b_pc,"%")
    print("Payment Type DD Match:",pay_method_dd_pc,"%")
    print("Payment Type CHQ Match:",pay_method_chq_pc,"%")
    print("Payment Type CC Match:",pay_method_cc_pc,"%")
    print("Bill Frequency Monthly Match:",bill_freq_M_pc,"%")
    print("Bill Frequency Quarterly Match:",bill_freq_Q_pc,"%")
    print("Fuel Type Electric Match:",fuel_E_pc,"%")
    print("Fuel Type Gas Match:",fuel_G_pc,"%")
    print("Dual Fuel Match:",DF_Y_pc,"%")
    print("Single Fuel Match:",DF_N_pc,"%")
    print("*************************************")
    print("Total data match score:",overall_score,"%")

#Add results and run into dictionary
#summarise the % results for each run and save the account IDs
    
    overall_score = str(overall_score)
    bb = str(bb)
    total_count = str(total_count)
    selected_account_list = str(selected_account_list)
    dictinput = "Run " + bb + ": "
    resultsinput = "Run " + bb + ": " + overall_score
    resultsinput2 = "Run " + bb + ": " + selected_account_list
    resultsinput3 = "Run " + bb + ": " + total_count + " accounts"
    results.append(resultsinput)
    resultsdetail.append(resultsinput2)
    totalaccountvalue.append(resultsinput3)

    totaldict[dictinput]=overall_score

    dictcount[dictinput]=total_count

    print("\n")
    print("\n")
    bb = int(bb)
    total_count = int(total_count)
    bb = bb + 1

    if variance == 0:
        print("*************************************")
        print("*************************************")
        print("Success - program stopping")
        now=datetime.datetime.now()
        endtime = now
        print("*************************************")
        print("*************************************")
        break
        sys.quit()
    

#Shows the total count and score for each run in a column
print("\n")
print("Summary of Results:")
print("*************************************")
g = len(results)
for m in range(g):
    print(results[m])
print("*************************************")    
j = len(totalaccountvalue)
for m in range(j):
    print(totalaccountvalue[m])
print("*************************************")
#Works out the best run for score and count

best_run = max(totaldict.items(), key=operator.itemgetter(1))[0]
dict_val = totaldict.get(best_run)
print("Highest % Match -  ",best_run,dict_val)
#print(totaldict)
most_accounts = max(dictcount.items(), key=operator.itemgetter(1))[0]
dict_val = dictcount.get(most_accounts)

print("Highest Accounts -  ",most_accounts,dict_val)
#print(dictcount)
#This will print out all the selected accounts for all runs, commented out deliverably if being run at high volume - code to be adjusted so only the best outcome is returned

#d = len(resultsdetail)
#for m in range(d):
  #  print(resultsdetail[m])

#Log the end date and calculate the run time

now=datetime.datetime.now()
endtime = now
print("*************************************")
print("Execution End time:",now.strftime("%Y-%m-%d %H:%M:%S"))
duration = endtime - starttime
print(duration)
print("*************************************")

