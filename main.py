import mysql.connector as m

cur = m.connect(username="root", password="Root@123", host="localhost")

con = cur.connector()

while True:
    opt1 = int(input("CHOOSE FROM THE FOLLOWING OPTIONS:\n[1] Add a new account\n[2]Deposit money\n[3]Withdraw "
                     "money\n[4]Display account info\n[5]View accounts" +
                     "\n[6]Close accounts\n[7] Modify an account"))

    # ADDING A NEW ACCOUNT
    if opt1 == 1:
        pass

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
