import mysql.connector as m

con = m.connect(username="root", password="Root@123", host="localhost")

cur = con.cursor()

if con.is_connected():
    print("CONNECTION ESTABLISHED")
else:
    print("CONNECTION FAILED")

cur.execute("use bank")

start_acc_id = start_trans_id = 999


def acc_id_generator():
    global start_acc_id
    if start_acc_id == 999:
        return 1000
    else:
        start_acc_id = start_acc_id + 1
        return start_acc_id


def trans_id_generator():
    global start_trans_id
    if start_trans_id == 999:
        return 1000
    else:
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
            balance = float(input("Enter the balance [>10000]: "))
        else:
            balance = 1

        cur.execute(
            "insert into user VALUES( {0}, '{1}', '{2}', {3}, '{4}', {5}, '{6}')".format(
                acc_no, name, dob, aadhar_no, address, balance, acc_type))

        con.commit()

    # DEPOSIT MONEY
    if opt1 == 2:
        pass

    # WITHDRAW MONEY
    if opt1 == 3:
        pass

    # DISPLAY ACCOUNT INFO
    if opt1 == 4:
        pass

    # VIEW ACCOUNTS
    if opt1 == 5:
        pass

    # CLOSE ACCOUNTS
    if opt1 == 6:
        pass

    # MODIFY AN ACCOUNT
    if opt1 == 7:
        pass
