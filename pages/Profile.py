import streamlit as st
import mysql.connector as m
import pandas as pd
from datetime import date as dt
from random import randint as rd
import time
from datetime import date

st.set_page_config(layout="centered")

con = m.connect(username="root", password="Root@123", host="localhost", auth_plugin='mysql_native_password')
cur = con.cursor()
cur.execute("use bank")

try:
    cur.execute("select * from user where acc_id = {0}".format(st.session_state["acc_id"]))
    user_values = cur.fetchall()[0]

    magicEnabled = False

    # functions to generate sequential account,branch,transaction numbers
    cur.execute("SELECT acc_id FROM user;")
    acc_vals = cur.fetchall()
    start_acc_id = acc_vals[-1][0]

    cur.execute("SELECT trans_id FROM transaction;")
    trans_vals = cur.fetchall()
    if len(trans_vals) == 0:
        start_trans_id = 999
    else:
        start_trans_id = trans_vals[-1][0]

    # To take a card with a bank.
    cur.execute("SELECT card_no FROM cards;")
    card_vals = cur.fetchall()
    if len(card_vals) == 0:
        start_card_id = 999
        print(start_card_id)
    else:
        start_card_id = card_vals[-1][0]

    loan_id = cur.fetchall()
    if len(loan_id) == 0:
        start_loan_id = 999
    else:
        start_loan_id = loan_id[-1][0]


    def cvv():
        cv1 = rd(1, 9)
        cv2 = rd(1, 9)
        cv3 = rd(1, 9)
        cv = "{}{}{}".format(cv1, cv2, cv3)
        print("\nDo not share your CVV with anyone. ")
        print(cv)
        return cv


    def card_pin():
        cur.execute("SELECT year(dob) from user where acc_id=1000;")
        dob_yr = cur.fetchall()[0][0]
        # flip year of birth
        c_pin = str(dob_yr)[::-1]
        print(
            "Your pin for card is generated - ****  Use this pin for first transaction and keep it safe. \n Later on you can change your pin. ")
        print(c_pin)
        return c_pin


    def expdate(yr=4):
        """takes the number of years and and adds it to the current date. returns date + number of years provided
        takes yr = 4 as default"""
        curdate = dt.today()

        # checking if the month is single digit
        if curdate.month // 10 == 0:
            month = "0" + str(curdate.month)
        else:
            month = str(curdate.month)

        # checking if the day is single digit
        if curdate.day // 10 == 0:
            day = "0" + str(curdate.day)
        else:
            day = str(curdate.day)

        date = str(curdate.year + yr) + month + day
        return date


    def issue_date(yr=0):
        issdate = dt.today()
        # checking if the month is single digit
        if issdate.month // 10 == 0:
            month = "0" + str(issdate.month)
        else:
            month = str(issdate.month)

        # checking if the day is single digit
        if issdate.day // 10 == 0:
            day = "0" + str(issdate.day)
        else:
            day = str(issdate.day)

        issdt = str(issdate.year + yr) + month + day
        return issdt


    def card_id_generator():
        global start_card_id
        start_card_id = start_card_id + 1
        print(start_card_id)
        return start_card_id


    def acc_id_generator():
        global start_acc_id
        start_acc_id = start_acc_id + 1
        return start_acc_id


    def trans_id_generator():
        global start_trans_id

        start_trans_id = start_trans_id + 1
        return start_trans_id


    def loan_id_generator():
        global start_loan_id
        start_loan_id = start_loan_id + 1
        return start_loan_id


    def deposit_money(deposit_amount):
        today = dt.today()

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
        balance = user_values[8]
        cur.execute(
            "UPDATE user SET balance = balance + {0} WHERE acc_id = {1}".format(deposit_amount,
                                                                                st.session_state["acc_id"]))
        cur.execute(
            "INSERT INTO transaction VALUES({0},{1},'{2}',{3},'{4}')".format(trans_id_generator(),
                                                                             st.session_state["acc_id"], date,
                                                                             deposit_amount, "deposit"))
        con.commit()
        return balance + deposit_amount


    def withdraw_money(withdrawal_amount):
        """takes the withdrawal amount as input and deducts it from the user account
        if withdrawal amount is not available in the user's account, (False,-1) is returned
        if withdrawal amount is available in the user's account,(True, {balance} ) is returned"""

        trans_id = trans_id_generator()
        cur.execute("select acc_id,balance from user where acc_id = {0}".format(st.session_state["acc_id"]))
        acc_details = cur.fetchone()

        today = dt.today()
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

        existing_balance = acc_details[1]
        if withdrawal_amount > existing_balance:
            st.error("Your withdrawal amount " + str(withdrawal_amount) + " It is more than existing balance : " + str(
                existing_balance))
            return False, -1


        else:
            new_balance = existing_balance - withdrawal_amount

            if user_values[9] == "Savings" and new_balance <= 10000:
                st.error(f"{withdrawal_amount} cannot be withdrawn as balance is reaching <= 10000")
                return False, -1
            else:

                cur.execute("UPDATE user SET balance = {0} WHERE acc_id = {1}".format(new_balance, acc_details[0]))
                cur.execute(
                    "INSERT INTO transaction(acc_id,date,trans_amount,trans_type,trans_id) VALUES({0},'{1}',{2},'{3}',{4})".format(
                        acc_details[0], date, withdrawal_amount, 'withdraw', trans_id))
                con.commit()

                return True, new_balance


    if st.session_state["access_granted"]:

        name = user_values[2]

        title, log_out = st.columns([0.85, 0.15])

        with title:
            st.title(f":rainbow[Welcome {name}]")
        with log_out:
            log_out = st.button("Log Out", type="primary", help="Double click to log-out")

        if log_out:
            st.session_state["access_granted"] = False

        acc, loan, card = st.tabs(["Account", "Loan", "Card"])

        # Account functions
        with acc:
            st.header("Access all account related functions here", divider="blue")
            acc_func = st.selectbox("Account Function",
                                    ("View Account Info", "Withdraw Money", "Deposit Money", "Modify Account",
                                     "Close Account"))
            st.divider()

            # View Account Info
            if acc_func == "View Account Info":
                df = pd.DataFrame(
                    [[str(user_values[0]), user_values[1], user_values[2], user_values[3], str(user_values[4]),
                      user_values[5],
                      str(user_values[6]), str(user_values[7]), user_values[8], user_values[9], user_values[10],
                      user_values[11],
                      user_values[12], str(user_values[13]), user_values[14], user_values[15], user_values[16],
                      user_values[17]]],
                    columns=["Account ID", "Password", "Name", "DOB", "Aadhar No", "Address", "Email",
                             "Phone No", "Balance", "Account Type", "Branch ID", "Branch Name",
                             "Pending Loan", "Loan ID", "Pending Loan Amount", "Issued Credit Cards",
                             "Issued Debit Card", "Status"])
                st.dataframe(df)
            # Withdraw Money
            if acc_func == "Withdraw Money":
                w_amt = st.number_input("Withdrawal Amount", min_value=0.01)
                withdraw_button = st.button("Withdraw", type="primary")

                if withdraw_button:
                    success, cur_balance = withdraw_money(w_amt)

                    if success:
                        st.success(f"{w_amt} has been deducted", icon="✅")
                        st.success(f"current balance: {cur_balance}", icon="✅")

            # Deposit Money
            if acc_func == "Deposit Money":
                d_amt = st.number_input("Deposit Amount", min_value=0)
                deposit_button = st.button("Deposit", type="primary")

                if deposit_button:
                    dep_balance = deposit_money(d_amt)

                    st.success(f"{d_amt} has been deposited", icon="✅")
                    st.success(f"current balance: {dep_balance}", icon="✅")

            # Modify Account
            if acc_func == "Modify Account":
                # password, address, email, phone_no
                pwd, adrs, eml, phn = st.tabs(["Password", "Address", "Email", "Phone No"])

                # changing password
                with pwd:
                    new_password_mod = st.text_input("New Password", type="password")
                    old_password = st.text_input("Old Password", type="password")
                    change_password = st.button("Change Password", type="primary", key="password_change_modify")
                    sys_old_password = user_values[1]

                    if change_password:
                        if sys_old_password == old_password:
                            cur.execute("update user set password = {0} where acc_id = {1}".format(new_password_mod,
                                                                                                   st.session_state[
                                                                                                       "acc_id"]))
                            con.commit()
                            st.success("Password has been changed", icon="✅")

                        else:
                            st.error("Old password does not match the new password")

                # changing address
                with adrs:
                    new_address = st.text_input("New Address")
                    change_address = st.button("Change Password", type="primary", key="change_address")

                    if change_address:
                        if new_address == "":
                            st.error("Please enter a valid address")

                        else:
                            cur.execute("update user set address = '{0}' where acc_id = {1}".format(new_address,
                                                                                                    st.session_state[
                                                                                                        "acc_id"]))
                            con.commit()
                            st.success("Address has been changed", icon="✅")

                # changing the email
                with eml:
                    new_email = st.text_input("New Email")
                    change_email = st.button("Change Email", type="primary", key="change_email")

                    if change_email:
                        if new_email == "":
                            st.error("Please enter a valid email")

                        else:
                            cur.execute("update user set email = '{0}' where acc_id = {1}".format(new_email,
                                                                                                  st.session_state[
                                                                                                      "acc_id"]))
                            con.commit()
                            st.success("Email has been changed", icon="✅")

                with phn:
                    new_phone = st.text_input("New Phone No")
                    change_phone = st.button("Change Phone", type="primary", key="change_phone")

                    if change_phone:
                        if len(new_phone) != 10:
                            st.error("Please enter a valid phone no")
                        else:
                            try:
                                phone_no = int(new_phone)
                                cur.execute("update user set phone_no = '{0}' where acc_id = {1}".format(new_phone,
                                                                                                         st.session_state[
                                                                                                             "acc_id"]))
                                con.commit()
                                st.success("Phone Number has been changed", icon="✅")



                            except ValueError:
                                st.error("Please enter a valid phone no")

            # close Account
            if acc_func == "Close Account":
                btn_state = False
                st.warning(":red[Account needs bank approval to re-activate once de-activated]", icon="⚠️")
                new_password_cls = st.text_input("Password")
                close_acc = st.button("Close Account", key="close_acc", disabled=btn_state)

                sys_old_password = user_values[1]

                if close_acc:
                    if sys_old_password == sys_old_password:
                        cur.execute("update user set status = '{0}' where acc_id = {1}".format("Deactivated",
                                                                                               st.session_state[
                                                                                                   "acc_id"]))
                        con.commit()
                        st.success("Account has been closed permanently, Log-out for changes to be permanent")
                        st.session_state["access_granted"] = False
                    else:
                        st.error("Incorrect Password")
        # Loan Functions
        with loan:
            st.header("Access all loan related options here", divider="blue")
            loan_func = st.selectbox("Loan Function", ("Avail Loan", "Loan Details", "Pay Off Installment"))
            st.divider()

            # applying for a loan
            if loan_func == "Avail Loan" and user_values[14] == 0:
                interest = 0
                try:
                    l_amt = float(st.number_input("Loan Amount", min_value=10000, max_value=10000000))
                except ValueError:
                    st.error("Please enter a valid loan amount")
                l_type = st.selectbox("Loan Type", ["Housing - 7.5%", "Car - 9%", "Personal - 15%"])
                dur = st.selectbox("Loan Duration", [5, 10, 15, 20, 25, 30])
                acc_id = st.session_state["acc_id"]
                loan_id = loan_id_generator()
                loan_start_date = dt.today()
                l_e_dt = expdate(dur)
                overdue = 0
                fine_amt = 0
                pending_loan_amt = l_amt

                if l_type == "Housing":
                    interest = 7.5
                elif l_type == "Car":
                    interest = 9
                elif l_type == "Personal":
                    interest = 15

                total_interest = l_amt * dur * (interest / 100)
                total_payable = l_amt + total_interest
                emi = total_payable / (dur * 12)

                get_loan = st.button("Get a Loan", key="get_loan")

                if get_loan:
                    x5 = "INSERT INTO loan VALUES({0},{1},{2},'{3}',{4},'{5}','{6}',{7},{8},{9},{10},{11});".format(
                        loan_id,
                        acc_id,
                        l_amt,
                        l_type,
                        interest,
                        loan_start_date,
                        l_e_dt,
                        dur,
                        overdue,
                        fine_amt,
                        pending_loan_amt,
                        emi)
                    x6 = "update user set balance = balance +{0},loan_id = {1},pending_loan = {2},pending_loan_amt = {3} where acc_id = {4}".format(
                        l_amt, loan_id, True, l_amt, acc_id)

                    cur.execute(x5)
                    con.commit()
                    cur.execute(x6)
                    con.commit()

                    with st.spinner("Processing..."):
                        time.sleep(5)
                    st.success("Loan Sanctioned")

                    end = date(int(l_e_dt[:4]), int(l_e_dt[4:6]), int(l_e_dt[6:]))
                    loan_info = pd.DataFrame([[l_amt, l_type, l_e_dt, fine_amt]],
                                             columns=["Loan Amount", "Loan Type", "Loan End Date",
                                                      "Fine Amount (if overdue)"])
                    st.dataframe(loan_info)

            elif loan_func == "Avail Loan" and user_values[14] != 0:
                st.error("*Cannot Issue Loan* - You have an outstanding loan")

            # Loan details
            if loan_func == "Loan Details":
                cur.execute("select * from loan where acc_id = {0}".format(st.session_state["acc_id"]))

                loan_details = cur.fetchall()[0]

                today = dt.today()

                exp_date = loan_details[6]
                fine = loan_details[2] * 0.1

                if today > exp_date and loan_details[10] > 0:
                    cur.execute("update loan set overdue = {0},fine_amt = {1} where acc_id = {2}".format(True, fine,
                                                                                                         loan_details[
                                                                                                             1]))

                    con.commit()

                    with st.container(border=True):
                        st.title(":red[OVERDUE LOAN]")
                        st.subheader(f":orange[Please contact the bank to pay ]:red[ Fine: 1000]")



                else:
                    st.title(":green[Overdue Loans: False]")

                loan_df = pd.DataFrame([loan_details],
                                       columns=["Loan Id", "Account Id", "Loan Amount", "Loan Type", "Interest",
                                                "Loan Start Date", "Loan End Date", "Duration", "Overdue",
                                                "Fine Amount",
                                                "Pending Loan Amount", "EMI"])
                st.dataframe(loan_df)

            # pay of installment
            if loan_func == "Pay Off Installment":

                cur.execute("select pending_loan_amt from loan where acc_id = {0}".format(st.session_state["acc_id"]))
                pay_pending_loan = int(cur.fetchall()[0][0])

                if pay_pending_loan > 0:
                    installment_amt = st.slider("Select the amount you want to pay", min_value=0,
                                                max_value=pay_pending_loan,
                                                value=0, step=1)
                else:
                    installment_amt = 0
                    st.success("No loans issued")

                pay_installment = st.button("Pay installment", key="pay_installment")

                pay = True
                pending_loan = user_values[13]
                if pay_installment and installment_amt != 0:
                    # checkin if there are any pending loans
                    if pending_loan == 0:
                        st.error("You have no pending loans")
                        pay = False
                    # checking for insufficient funds
                    balance = user_values[8]
                    if installment_amt >= balance - 10000 and user_values[9] == "Savings":
                        st.error("Insufficient Funds - balance dropping below Rs.10000")
                        pay = False
                        # sufficient funds regardless of account
                    if installment_amt >= user_values[8]:
                        st.error("Insufficient Funds")
                        pay = False

                    if pay:
                        # updating new balance
                        cur.execute(
                            "update user set balance = balance - {0},pending_loan_amt = pending_loan_amt - {1} where acc_id = {2}".format(
                                installment_amt, installment_amt,
                                st.session_state[
                                    "acc_id"]))
                        con.commit()
                        # updating pending loan amount in loan table
                        cur.execute(
                            "update loan set pending_loan_amt = pending_loan_amt - {0} where acc_id = {1}".format(
                                installment_amt, st.session_state["acc_id"]))
                        con.commit()
                        # recording the transaction

                        cur.execute(
                            "insert into transaction values({0},{1},'{2}',{3},'{4}')".format(trans_id_generator(),
                                                                                             st.session_state[
                                                                                                 "acc_id"],
                                                                                             date.today(),
                                                                                             installment_amt,
                                                                                             "withdraw"))

                        con.commit()

                        if pending_loan == 1 and pay_pending_loan - installment_amt == 0:
                            # changing the user's pending loan status if the user has paid off their loan
                            cur.execute(
                                "update user set pending_loan = {0},loan_id = {1} where acc_id = {2}".format(0, 0, st.session_state[
                                    "acc_id"]))
                            st.success("Loan has been paid off in full")
                            con.commit()
                            st.balloons()
                        else:
                            st.warning(
                                f"Installment has been paid. Pending Loan Amount: {pay_pending_loan - installment_amt}")
                elif pay_installment and installment_amt == 0:
                    st.error("Enter a valid amount")
                else:
                    pass
        # card functions
        with card:
            st.header("Apply for Debit or Credit card", divider="blue")
            card_func = st.selectbox("", ("Debit Card", "Credit Card"))
            st.divider()

            # Applying for a debit card
            if card_func == "Debit Card":
                # displaying card info
                with st.container(border=True):
                    st.header(":rainbow[Debit Card]", )
                    st.write("Available for citizens above the age of 18")

                # checking if user is eligible
                cur.execute("SELECT year(dob) from user where user.acc_id={0}".format(st.session_state["acc_id"]))
                dob_yr = cur.fetchall()[0][0]
                currentYear = dt.today().year

                # if the user is eligible
                if currentYear - int(dob_yr) >= 18 and user_values[16] <= 0:
                    avail_debit_card = st.button(":green[YOU'RE ELIGIBLE: APPLY FOR DEBIT CARD] ", key="debit_card",
                                                 use_container_width=True)
                    # st.toast("CONGRATULATIONS!! YOU ARE ELIGIBLE FOR A DEBIT CARD !!")
                    if "issue_debit_card" not in st.session_state.keys():
                        st.session_state["issue_debit_card"] = False

                    if avail_debit_card: st.session_state["issue_debit_card"] = True

                    if st.session_state["issue_debit_card"]:
                        with st.container(border=True):
                            st.header(":rainbow[Card Info]")
                            st.write("Validity: 4 years")
                            st.write("Max withdrawal Limit: Rs.10000 per day")
                            st.write(":orange[Free for the year 2024]")

                        confirm_debit_card = st.button(":green[Confirm Debit Card]", key="confirm_debit_card")

                        if confirm_debit_card:
                            card_no = card_id_generator()
                            card_type = "Debit"
                            max_limit = -1
                            iss_date = expdate(0)
                            exp_date = expdate()
                            pin = card_pin()
                            ccv = cvv()
                            cashback = 0
                            x1 = "INSERT INTO cards values({0},'{1}',{2},'{3}','{4}',{5},{6},{7},{8});".format(
                                st.session_state["acc_id"], card_type,
                                card_no,
                                iss_date, exp_date, pin,
                                ccv,
                                max_limit, cashback)
                            x2 = "update user set no_debit_cards = {0} where acc_id = {1}".format(1, st.session_state[
                                "acc_id"])
                            cur.execute(x1)
                            con.commit()
                            cur.execute(x2)
                            con.commit()

                            st.session_state["issue_debit_card"] = False
                            with st.spinner("Processing...."):
                                time.sleep(5)
                            st.balloons()
                            with st.container(border=True):
                                st.title(f":rainbow[{user_values[2]}]")

                                c1, c2, c3 = st.columns(3)

                                with c1:
                                    st.subheader(f"Card No: {card_no}")
                                with c2:
                                    st.subheader(f"Issue Date: {iss_date}")
                                with c3:
                                    st.subheader(f"Expiry Date: {exp_date}")

                                c4, c5 = st.columns(2)

                                with c4:
                                    st.subheader(f"Pin: {pin}")
                                with c5:
                                    st.subheader(f"CVV: {ccv}")

                            debit_card_info = pd.DataFrame([[str(card_no), iss_date, exp_date, pin, ccv]],
                                                           columns=["Card No", "Issue Date", "Expiry Date", "Pin",
                                                                    "CVV"])

                            st.dataframe(debit_card_info)
                else:
                    st.error("Sorry, you're not eligible for a debit card")

            # applying for a credit card
            elif card_func == "Credit Card":
                with st.container(border=True):
                    st.header(":rainbow[Credit Card]", )
                    st.write("Available for citizens above the age of 18")

                # checking if user is eligible
                cur.execute("SELECT year(dob) from user where user.acc_id={0}".format(st.session_state["acc_id"]))
                dob_yr = cur.fetchall()[0][0]
                currentYear = dt.today().year

                if currentYear - int(dob_yr) >= 18 and user_values[15] <= 4:
                    avail_credit_card = st.button(":green[YOU'RE ELIGIBLE: APPLY FOR CREDIT CARD] ", key="credit_card",
                                                  use_container_width=True)
                    # st.toast("CONGRATULATIONS!! YOU ARE ELIGIBLE FOR A DEBIT CARD !!")
                    if "issue_credit_card" not in st.session_state.keys():
                        st.session_state["issue_credit_card"] = False

                    if avail_credit_card: st.session_state["issue_credit_card"] = True

                    if st.session_state["issue_credit_card"]:
                        with st.container(border=True):
                            st.header(":rainbow[Card Info]")
                            st.write("Validity: 4 years")
                            st.write("Max withdrawal Limit: Rs.2,00,000")
                            st.write("Cashback: 2%")
                            st.write(":orange[Free for year 2024]")
                            st.write(":red[Late Fee: 10% of every transaction]")

                        confirm_credit_card = st.button(":green[Confirm Credit Card]", key="confirm_credit_card")

                        if confirm_credit_card:
                            card_no = card_id_generator()
                            acc_id = st.session_state["acc_id"]
                            credit_card_type = 'Credit'
                            credit_exp_date = expdate()
                            credit_iss_date = issue_date(0)
                            max_limit = 50000
                            credit_pin = card_pin()
                            credit_ccv = cvv()
                            cashback = 0.02

                            x3 = "INSERT INTO cards values({0},'{1}',{2},{3},{4},{5},{6},{7},{8});".format(acc_id,
                                                                                                           credit_card_type,
                                                                                                           card_no,
                                                                                                           credit_iss_date,
                                                                                                           credit_exp_date,
                                                                                                           credit_pin,
                                                                                                           credit_ccv,
                                                                                                           max_limit,
                                                                                                           cashback)

                            x4 = "update user set no_credit_cards = no_credit_cards + {0} where acc_id={1}".format(1,
                                                                                                                   acc_id)

                            cur.execute(x3)
                            con.commit()
                            cur.execute(x4)
                            con.commit()

                            st.session_state["issue_credit_card"] = False

                            with st.spinner("Processing...."):
                                time.sleep(5)
                            st.balloons()
                            with st.container(border=True):
                                st.title(f":rainbow[{user_values[2]}]")
                                col1, col2, col3 = st.columns(3)

                                with col1:
                                    st.subheader(f"Card No: {card_no}")

                                with col2:
                                    # st.subheader(f"Issue Date: {credit_iss_date}")
                                    st.subheader(f"Expiry Date: {credit_exp_date}")

                                with col3:
                                    st.subheader(f"CVV: {credit_ccv}")

                                col4, col5, col6 = st.columns(3)

                                with col4:
                                    st.subheader(f"Cashback: {cashback}")
                                with col5:
                                    st.subheader(f"Max-limit: {max_limit}")
                                with col6:
                                    st.subheader(f"Pin: {credit_pin}")

                            credit_card_info = pd.DataFrame(
                                [[str(card_no), credit_iss_date, credit_exp_date, credit_ccv, cashback, max_limit,
                                  credit_pin]],
                                columns=["Card",
                                         "Card Issue Date", "Card Expiry Date", "CVV", "Cashback", "Max Limit",
                                         "Credit Pin"])

                            st.dataframe(credit_card_info)
                else:
                    st.error("Sorry, you're not eligible for a credit card")
    else:
        st.title("Please log in to access the options")

except KeyError:
    st.title("Please log in to access the options")
