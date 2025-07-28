from datetime import date
from imap_tools import MailBox, AND
import csv
import joblib
import os
from bs4 import BeautifulSoup
import re
from ..ml_pipline.model_def import train_model
from colorama import Fore, Style

file_name = os.path.normpath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'emails.csv')
)

RECEIPT_KEYWORDS = [
    "receipt", "order confirmation", "payment", "invoice",
    "billed", "your order", "transaction", "purchase",
    "thanks for your order", "your payment"
]

def extract_clean_text(msg):
    raw_text = msg.text or msg.html or ""
    if msg.html:
        soup = BeautifulSoup(msg.html, "html.parser")
        clean_text = soup.get_text(separator=' ', strip=True)
    else:
        clean_text = raw_text.strip()
    return re.sub(r'\s+', ' ', clean_text)  # collapse whitespace

def fetch_bill_emails(server, model, limit, username, password):
  bill_count = 0
  with MailBox(server).login(username, password, "Inbox") as mailbox:
    for msg in mailbox.fetch(reverse=True, limit = limit):
      text = msg.text or msg.html or ""
      prediction = model.predict([text])
      label = f"{Fore.GREEN}BILL{Style.RESET_ALL}" if prediction[0] == 1 else f"{Fore.RED}NOT BILL{Style.RESET_ALL}"
      print(f"📬 {msg.subject} --> {label}")
      if prediction[0] == 1:
        bill_count += 1
  print(f"\n✅ Done! Found {bill_count} eBill(s) out of {limit} email(s) scanned.")


def is_receipt(text):
   text = text.lower()
   return any(keyword in text for keyword in RECEIPT_KEYWORDS)

def fetch_and_save_emails(server, username, password,filename, limit=200):
    with MailBox(server).login(username, password, "Inbox") as mailbox:
        with open(filename, "w", newline='', encoding='utf-8') as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            writer.writerow(["text", "label"])

            for msg in mailbox.fetch(limit=limit, reverse=True):
                clean_text = extract_clean_text(msg)
                if not clean_text:
                    continue
                label = int(is_receipt(clean_text))
                writer.writerow([clean_text, label])
                print(f"Saved: {msg.subject}")

def domain_converter(email):
  inter = email[email.index("@") + 1 :]
  count = 0
  for i in range(-1, -(len(inter) - 1), -1):
     if email[i] == '.':
        if count == 1:
           new = inter[i + 1 :]
           return new
        else:
           count += 1
           
  new = inter     
  return new

def categorize_company(server, model, year, isAll, username, password):
  company_dict = {}
  with MailBox(server).login(username, password, "Inbox") as mailbox:
    if isAll:
        messages = mailbox.fetch()
    else:
        date_from = date(year, 1, 1)
        date_to = date(year + 1, 1, 1)
        messages = mailbox.fetch(AND(date_gte = date_from, date_lt = date_to))
    for msg in messages:
        if isAll or (msg.date.year == year):
          text = (msg.text or msg.html or "").strip()
          prediction = model.predict([text])
          if prediction[0] == 1:
            email_from = domain_converter(msg.from_)
            if email_from in company_dict:
              company_dict[email_from].append(msg.subject)
            else:
              company_dict[email_from] = [msg.subject]
  return company_dict

def stats_summary(server, model, year, isAll, username, password):
  total = 0
  ebill_count = 0
  top_sender = {}
  company_dict_descend = {}
  i = 0
  with MailBox(server).login(username, password, "Inbox") as mailbox:
    if isAll:
        messages = mailbox.fetch()
    else:
        date_from = date(year, 1, 1)
        date_to = date(year + 1, 1, 1)
        messages = mailbox.fetch(AND(date_gte = date_from, date_lt = date_to))
    for msg in messages:
        if isAll or (msg.date.year == year):
          total += 1
  company_dict = categorize_company(server, model, year, isAll, username, password)
  for company in company_dict:
     company_dict_descend[company] = len(company_dict[company])
     ebill_count += len(company_dict[company])
  
  company_dict_descend = {k: v for k, v in sorted(company_dict_descend.items(), key=lambda item: item[1])}

  for domain in company_dict_descend:
    if i == 3:
      break
    top_sender[domain] = company_dict_descend[domain]
    i += 1  
  return total, ebill_count, top_sender
# # Example
# fetch_and_save_emails(MAIL_USERNAME, MAIL_PASSWORD)

# model = train_model()

# model_file = os.path.normpath(
#     os.path.join(os.path.dirname(__file__), '..', '..', 'models', 'email_bill_model.joblib')
# )
# joblib.dump(model, model_file)