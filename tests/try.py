from imap_tools import MailBox, AND
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
import csv
import pandas as pd
import joblib

MAIL_PASSWORD = "zjwa iqjm hpfm ngtk"
MAIL_USERNAME = "koulkayaan@gmail.com"
# Load the model
model = joblib.load("/Users/kayaankoul/untitled v1/models/email_bill_model.joblib")

# with MailBox("imap.gmail.com").login(MAIL_USERNAME, MAIL_PASSWORD, "Inbox") as mailbox:
#     for msg in mailbox.fetch(reverse=True, limit = 300):
#       text = msg.text or msg.html or ""
#       prediction = model.predict([text])
#       print(f"📬 {msg.subject} --> {'BILL' if prediction[0] == 1 else 'NOT BILL'}")

texts = ['Hi Alex,  Thanks for your recent purchase from Books & Beyond! Your order #12345 for "The Midnight Library" by Matt Haig ($15.99) and "Project Hail Mary" by Andy Weir ($14.50) has been successfully processed.  Total charged: $30.49  Your books are on their way and should arrive within 3-5 business days. You can track your order here: [Tracking Link]  We appreciate your business!  Sincerely, The Books & Beyond Team', 'Subject: Payment Confirmation: Invoice #INV-2025-07-001 for Web Design Services  Dear Mr. Harrison,  This email confirms receipt of your payment for Invoice #INV-2025-07-001, covering web design services completed on July 10, 2025.  Amount received: $1,500.00  Thank you for your prompt payment. We value your business and look forward to working with you again.  Best regards, Sarah Chen Creative Digital Solutions', "Hi Maria,  I hope you're having a good week.  Just wanted to confirm the time for our meeting next Tuesday. Is 10:00 AM still good for you, or would an afternoon slot work better?  Let me know!  Best, David", "Hey Team,  Just a friendly reminder about our weekend hike this Saturday, July 19th! We're meeting at the trailhead for Mount Royal Park at 8:30 AM sharp.  Remember to bring plenty of water, snacks, and appropriate footwear. The weather looks great, so it should be a fun one!  See you Saturday, Chris", "Hello Pat,  This is a receipt for your recent grocery order from FreshBite, placed on July 15, 2025.  Items purchased:  Organic Apples (1 bag) - $4.99  Whole Wheat Bread (1 loaf) - $3.50  Milk (1 gallon) - $4.00  Chicken Breast (1.5 lbs) - $9.75  Subtotal: $22.24 Delivery Fee: $5.00 Tax: $1.36 Total: $28.60  Your order is scheduled for delivery between 4:00 PM - 5:00 PM today.  Thank you for choosing FreshBite!", "Dear Valued Supporter,  Thank you for your generous donation of $50.00 to the Green Earth Foundation on July 15, 2025. Your contribution will directly support our efforts in reforestation and conservation.  Your transaction ID is GE20250715-007.  A formal tax receipt will be mailed to your address within 7-10 business days. We are deeply grateful for your commitment to a healthier planet.  With sincere thanks, The Green Earth Foundation Team", "Hi Jamie,  Your tickets for \"Inside Out 2\" at Cineplex Downtown on July 15, 2025, at 7:00 PM are confirmed!  Number of tickets: 2 (Adult) Total amount paid: $28.00  Your e-tickets are attached to this email. Please have them ready for scanning at the theater. Enjoy the show!  Thanks, Cineplex", "Dear Valued Users,  Please be advised that our website will undergo scheduled maintenance on Friday, July 18th, from 12:00 AM to 4:00 AM EDT. During this time, you may experience brief interruptions in service.  We apologize for any inconvenience this may cause and appreciate your understanding as we work to improve our platform.  Thank you, The Support Team Global Solutions Inc."]

for text in texts:
  prediction = model.predict([text])
  print(f"📬  --> {'BILL' if prediction[0] == 1 else 'NOT BILL'}")