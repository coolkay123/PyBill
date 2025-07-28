#!/usr/bin/env python3 
import sys
import joblib
import sys
from ..email_handler.fetcher import fetch_bill_emails, categorize_company, stats_summary
from imap_tools import MailBox, MailboxLoginError
from datetime import datetime
from getpass import getpass
from dotenv import load_dotenv
import os
load_dotenv()

username = os.getenv("EMAIL_USERNAME")
password = os.getenv("EMAIL_PASSWORD")

FILENAME = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'email_bill_model.joblib')
)
model = joblib.load(FILENAME)

# Map email domains to IMAP servers
imap_servers = {
    "gmail.com": "imap.gmail.com",
    "yahoo.com": "imap.mail.yahoo.com",
    "outlook.com": "imap-mail.outlook.com",
    "hotmail.com": "imap-mail.outlook.com",
    "icloud.com": "imap.mail.me.com",
}


def int_input(message):
  while True:
      try:
        i = int(input(message))
        break
      except:
        print("Please enter an integer\n")
  return i

def year_int(message):
  current_year = datetime.now().year
  while True:
        year = input(message).strip()
        isAll = (year.lower() == 'all')
        if  not isAll:
          try:
            year = int(year)
            if not (1970 <= year <= current_year):
               print(f"Please enter a valid year between 1970 and {current_year} (inclusive)\n")
            else:
              break
          except:
            print("Please enter in correct format")
        else:
          break
  return year, isAll

if __name__ == "__main__":
  print("Welcome to PyBill!!")
  while True:
    if not username:
      username = input("Enter your email: ")
    if not password:
      password = getpass("Enter your app password: ")

    # Extract domain and lookup IMAP server
    domain = username.split('@')[-1].lower()
    imap_server = imap_servers.get(domain)

    if not imap_server:
        imap_server = input(f"IMAP server for {domain} not found. Please enter it manually: ")

    # Attempt connection
    try:
        with MailBox(imap_server).login(username, password, "INBOX") as mailbox:
            print("✅ Connected to mailbox!")
            break
    except MailboxLoginError:
        print("❌ Login failed. Please check your email or app password and try again.")

  while True:
    print("Please enter the option number of the feature in order to use it (ex. -> 1)")
    print("1. Classifies whether email is an eBill or not")
    print("2. Categorize by Company")
    print("3. View Summary Stats")
    print("4. Exit")

    i = int_input("Enter option: ")
    if (i == 1):
      limit = int_input("Enter the number of email(s) you want to display: ")
      print("Loading...")
      fetch_bill_emails(imap_server, model, limit, username, password)
      print('\n')

    
    elif (i == 2):
      year, isAll = year_int("Enter the year (Type 'All' for all the emails): ")
      print("Loading...")
      company_dict = categorize_company(imap_server, model, year, isAll, username, password)
      for company in company_dict:
        print(company + " -> " + str(len(company_dict[company])) + " emails")

    elif (i == 3):
      year, isAll = year_int("Enter the year you want to see the summary of (Type 'All' for all the emails): ")
      print("Loading...")
      total, ebill_count, top_sender = stats_summary(imap_server, model, year, isAll, username, password)
      print("Total email(s) scanned:", total)
      print("Total number of email(s) which were an eBill:", ebill_count)
      print("Top sender domains:")
      for domain in top_sender:
        print(f"    {domain} ({top_sender[domain]} email(s))")

    elif (i == 4):
      print("Thanks for using PyBill! 👋")
      break
    
    else:
      print("Please enter a integer between 1 and 4")
    print("\n")