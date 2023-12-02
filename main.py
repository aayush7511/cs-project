# important libraries
import simple_colors as sc
import datetime
from datetime import datetime
# connecting to sql
import mysql.connector as m

con = m.connect(username="root", password="Root@123", host="localhost")

cur = con.cursor()

if con.is_connected():
    print("CONNECTION ESTABLISHED")
else:
    print("CONNECTION FAILED")
# using the database
cur.execute("use bank")

# functions to generate sequential account and transaction numbers
cur.execute("SELECT acc_id FROM user;")
acc_vals = cur.fetchall()
start_acc_id = acc_vals[-1][0]

cur.execute("SELECT trans_id FROM transaction;")
trans_vals = cur.fetchall()
if len(trans_vals) == 0:
    start_trans_id = 999
else:
    start_trans_id = trans_vals[-1][0]


def acc_id_generator():
    global start_acc_id
    start_acc_id = start_acc_id + 1
    return start_acc_id


def trans_id_generator():
    global start_trans_id

    start_trans_id = start_trans_id + 1
    return start_trans_id


while True:
    opt1 = int(input("CHOOSE FROM THE FOLLOWING OPTIONS:\n[1]Add a new account\n[2]Deposit money\n[3]Withdraw "
                     "money\n[4]Display account info\n[5]View accounts" +
                     "\n[6]Close accounts\n[7]Modify an account\nENTER YOUR OPTION NO: "))

    # ADDING A NEW ACCOUNT
    if opt1 == 1:
        acc_no = acc_id_generator()
        name = input("Enter your name: ")
        dob = input("Enter your dob [yyyymmdd]: ")
        aadhar_no = float(input("Enter your aadhar no: "))
        address = input("Enter the address: ")
        acc_type = input("Enter the account type: ")

        if acc_type == "saving":
            # checking if savings account has sufficient balance to be created
            balance = float(input("Enter the balance [>10000]: "))
            if balance < 10000:
                print("Enter sufficient balance amount")
            else:
                cur.execute(
                    "INSERT INTO user VALUES( {0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}')".format(
                        acc_no, name, dob, aadhar_no, address, balance, acc_type))

        else:
            # all checking accounts have a balance of 1 when created
            balance = 1

            cur.execute(
                "INSERT INTO user VALUES( {0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}')".format(
                    acc_no, name, dob, aadhar_no, address, balance, acc_type))

        con.commit()

    # DEPOSIT MONEY
    if opt1 == 2:
        val = int(input("Enter your account number: "))
        amount = float(input("Enter the amount you would like to deposit: "))
        today = datetime.date.today()

        # checking if the month is single digit
        if today.month // 10 == 0:
            month = "0" + str(today.month)
        else:
            month = str(today.month)

        # checking if the day is single digit
        if today.day // 10 == 0:
            day = "0" + str(today.day)
        else:
            day = str(today.day)

        date = str(today.year) + month + day

        # checking if the amount is negative or zero
        if amount <= 0:
            print("Enter a valid amount")
        else:
            # getting the account numbers
            acc_nums = []
            for t in acc_vals:
                acc_nums.append(t[0])

            if val in acc_nums:
                # adding deposit amount to balance
                cur.execute("UPDATE user SET balance = balance + {0} WHERE acc_id = {1}".format(amount, val))

                # adding deposit as a transaction to transaction table
                cur.execute(
                    "INSERT INTO transaction VALUES({0},{1},'{2}',{3},'{4}')".format(trans_id_generator(), val, date,
                                                                                     amount, "deposit"))
                con.commit()
            else:
                print(sc.red("Please enter a valid account number", ["bold"]))

    # WITHDRAW MONEY
    # column names used user(acc_id,name,birthday,aadhar_no,address,acc_type,balance)
    #transaction(trans_id, acc_id,trans_date,trans_amt,trans_type)
    if opt1 == 3:
        acc_no = int(input("Enter your account number: "))
        cur.execute("select acc_id,balance from user where acc_id = {0}".format(acc_no))
        acc_details = cur.fetchone()
        if acc_details is None:
            print("Account Number is not correct")
        else:
            withdrawal_amount = int(input("Enter amount to withdraw: "))
            existing_balance  = acc_details[1]
            if withdrawal_amount > existing_balance:
                print("Your withdrawal amount " + str(withdrawal_amount)  + " It is more than existing balance : " + str(existing_balance))
            else:
                new_balance = existing_balance - withdrawal_amount
                cur.execute("UPDATE user SET balance = {0} WHERE acc_id = {1}".format(new_balance,  acc_details[0]))
                cur.execute("INSERT INTO transaction(acc_id,trans_date,trans_amt,trans_type) VALUES({0},'{1}',{2},'{3}')".format(acc_details[0], datetime.now(),withdrawal_amount,'withdraw'))
                print("Your current available balance  " + str(new_balance))
                con.commit()

    # DISPLAY ACCOUNT INFO
    if opt1 == 4:
        acc_no = int(input("Enter your account number: "))
        cur.execute("select acc_id, name, acc_type, balance from user where acc_id = {0}".format(acc_no))
        acc_details = cur.fetchone()
        if acc_details is None:
            print("Account Number is not correct")
        else:
            print(acc_details[0])
            print("account number: "  + str(acc_details[0]))
            print("name: " + acc_details[1] )
            print("account type: " + acc_details[2])
            print("balance: " + str(acc_details[3]))


    # VIEW ACCOUNTS
    if opt1 == 5:
        pass

    # CLOSE ACCOUNTS
    if opt1 == 6:
        pass

    # MODIFY AN ACCOUNT
    if opt1 == 7:
        pass
