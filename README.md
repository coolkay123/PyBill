# 📬 PyBill

PyBill is a command-line tool that uses machine learning to automatically classify your Gmail emails as **e-bills** or **non-bills** — and provides statistics, company-wise categorization, and easy summary insights.

---

## 🚀 Features

- 🔍 Classifies emails as bill/not-bill using an ML model
- 🗂️ Categorizes bills by company/domain
- 📊 Shows summary statistics by year or for all time
- 🧠 Allows contributions to retrain the model over time

---

## 🧰 Requirements

- Python 3.8+
- Gmail account with [App Password](https://support.google.com/accounts/answer/185833?hl=en)
- A trained model file (`email_bill_model.joblib`) in the `models/` directory

Install dependencies using:

```bash
pip install -r requirements.txt

## 🔐 Using a `.env` File (Optional)

You can avoid typing your credentials every time by creating a `.env` file in the root of the project:

```dotenv
EMAIL_USERNAME=youremail@gmail.com
EMAIL_PASSWORD=your-app-password
