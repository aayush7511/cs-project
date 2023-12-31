import streamlit as st
import mysql.connector as m
import regex as re
import pandas as pd
from datetime import date


st.set_page_config(layout="centered")

con = m.connect(username="root", password="Root@123", host="localhost", auth_plugin='mysql_native_password')
cur = con.cursor()

if con.is_connected():
    pass
else:
    st.error("CONNECTION FAILED")
cur.execute("use bank")
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


def acc_id_generator():
    global start_acc_id
    start_acc_id = start_acc_id + 1
    return start_acc_id


def trans_id_generator():
    global start_trans_id

    start_trans_id = start_trans_id + 1
    return start_trans_id


dict_branch = {"Akshaynagar": 101, "Koramangala": 102, "HSR Layout": 103, "BTM Layout": 104, "Vijaya Bank Layout": 105,
               "Indira Nagar": 106}


def create_acc(n1, p1, dob1, adhr1, adrs1, eml1, ph_no, actype, b_name, bal):
    acc_id = acc_id_generator()
    branch_id = dict_branch[branch_name]

    cur.execute(
        "insert into user values ({0},'{1}','{2}','{3}',{4},'{5}','{6}',{7}, {8},'{9}',{10},'{11}',{12},{13}, {14}, {15}, {16}, '{17}')".format(
            acc_id, p1, n1, dob1, adhr1, adrs1, eml1, ph_no, bal, actype, branch_id, b_name, 0, False, 0, 0, 0, "Active"
        ))
    con.commit()

    user_vals = pd.DataFrame(
        [[str(acc_id), name, password, dob, str(aadhar_no), address, email, str(phone_no), acc_type, str(branch_id),
          branch_name, balance]],
        columns=["Account Id", "Name", "Password", "Date Of Birth", "Aadhar No", "Address", "Email", "Phone No",
                 "Account Type", "Branch ID", "Branch Name", "Balance"])

    st.dataframe(user_vals)


if "access_granted" not in st.session_state.keys():
    st.session_state["access_granted"] = False
if "acc_id" not in st.session_state.keys():
    st.session_state["username"] = 0
if "password" not in st.session_state.keys():
    st.session_state["password"] = 0

st.title(":rainbow[Welcome to Stratton Oakmont Bank]")
login, acc = st.tabs(["Login", "Create Account"])

with login:
    log_acc_id = st.number_input("Account ID", min_value=0, step=1)
    log_password = st.text_input("Password", type="password")

    login_button = st.button("Login", key="login", type="primary")

    sys_password = None
    login_auth = {"username": False}

    cur.execute("select acc_id,password,status from user")
    vals = cur.fetchall()

    if login_button:
        for i in vals:
            # checking if the account exists in the table
            if i[0] == log_acc_id:
                sys_password = i[1]
                # checking is the user entered password and the stored password are same
                if log_password == sys_password:
                    # checking if the account is de-activated

                    if i[2] == "Deactivated":
                        st.error("Account has been De-activated: Contact your branch")
                        break
                    else:
                        st.session_state["access_granted"] = True
                        st.session_state["acc_id"] = log_acc_id
                        st.session_state["password"] = sys_password
                        st.success("Access Granted")
                        break
        else:
            st.error("Username and password do not match")

with acc:
    name = st.text_input("Full Name", key="name")
    password = prompt = st.text_input("Password", key="password_key", type="password")
    dob = st.text_input("Date Of Birth", placeholder="YYYYMMDD", key="dob")
    aadhar_no = st.text_input("Aadhar_No", placeholder="XXXXXXXXXX", key="aadhar")
    address = st.text_input("Address", key="address")
    email = st.text_input("Email", placeholder="example@gmail.com", key="email")
    phone_no = st.text_input("Phone No", placeholder="XXX-XXX-XXXX", key="phone")
    acc_type = st.radio("Account Type", ["Savings", "Checking"])
    branch_name = st.selectbox("Branch Name", (
        "Koramangala", "Akshaynagar", "HSR Layout", "BTM Layout", "Vijaya Bank Layout", "Indira Nagar"),
                               placeholder="Please select an option...")
    balance = st.number_input("Balance", min_value=0, key="balance")

    submit_button = st.button("SUBMIT", key="submit", type="primary")

    if submit_button:

        dict_check = {"name": False, "pass": False, "dob": False, "aadhar_no": False, "email": False, "phone_no": False,
                      "Balance": False, "address": False}

        # empty name
        if name != "":
            words = name.split()
            only_words = True
            for i in words:
                if not i.isalpha():
                    only_words = False

            # if the words in name are only letters
            if only_words:
                dict_check["name"] = True
            else:
                st.toast("Name must be only characters ")
        else:
            st.toast("Name must be at least one character and only characters ")

        # password - 8 digits and alphanumeric
        if len(password) >= 8 and password.isalnum():
            dict_check["pass"] = True
        else:
            st.toast("Password must be alpha numeric and 8 digits")

        # wrong date format
        if re.match(pattern="^[0-9]{8}$", string=dob):
            # checking if the date is valid
            try:
                age = date(int(dob[:4]) + 18, int(dob[4:6]), int(dob[6:]))
                if age <= date.today():
                    dict_check["dob"] = True
                else:
                    st.error("You must be 18")

            except ValueError:
                st.toast("Date entered is not a valid date")
        else:
            st.toast("Date is in the wrong format")

        domains = ["@gmail.com", "@hotmail.com", "aol.com", "msn.com", "wanadoo.fr", "live.com", "greenmailed.com",
                   "rediffmail.com", "outlook.com", ]

        # empty email
        if email != "" and "@" in email:
            domain = email.find("@")
            domain = email[domain:]

            # valid domain name
            if domain in domains:
                dict_check["email"] = True
            else:
                st.toast("Please enter a valid domain name")
        else:
            st.toast("Please enter a valid email")

        # aadhar no
        if len(aadhar_no) != 10:
            st.toast("Please enter a valid aadhar no")
        else:
            try:
                aadhar_no = int(aadhar_no)
                aadhar_no = str(aadhar_no)
                dict_check["aadhar_no"] = True
            except ValueError:
                st.toast("Please enter a valid aadhar no")

        # phone no
        if len(phone_no) != 10:
            st.toast("Please enter a valid Phone no")
        else:
            try:
                phone_no = int(phone_no)
                dict_check["phone_no"] = True
            except ValueError:
                st.toast("Please enter a valid phone no")

        # balance
        if acc_type == "Savings" and balance < 10000:
            st.toast("Minimum balance of 10000 is required for savings account")
        else:
            dict_check["Balance"] = True

        # empty address
        if address == "":
            st.toast("Enter a valid address")
        else:
            dict_check["address"] = True

        st.write(dict_check.values())
        # if all values are correct
        if all(dict_check.values()):

            cur.execute("select aadhar_no from user")
            aadhar = cur.fetchall()
            flag_exist = False

            # checking if the user exist
            for i in aadhar:
                if int(aadhar_no) == i[0]:
                    flag_exist = True
                    break

            if flag_exist:
                st.error("Account already exits with this aadhar no")
            else:
                create_acc(name, password, dob, aadhar_no, address, email, phone_no, acc_type, branch_name, balance)
                st.success(
                    "Account created! Please download the information in the table above for future login purposes")
                st.balloons()
