# Contributing to PyBill

Thanks for your interest in improving PyBill!

## 🧠 Improve the ML Model

To help improve the email classification model:

1. Add labeled emails in `data/your_emails.csv` using this format:
    ```
    message,label
    "This is your electricity bill",1
    "Hello from your friend",0
    ```

2. Run the training script:
    ```bash
    python3 -m src.ml_pipeline.model_def
    ```

3. Test that the new model performs well.

4. Submit a Pull Request with:
    - Your new model (`models/email_bill_model.joblib`)
    - (Optional) Your dataset file, if it does not contain private content

---

## 🛠️ General Contributions

You can also:
- Fix bugs
- Suggest features
- Improve CLI output
- Write tests for `email_handler` or `ui`

---

## 📦 Setup Tips

- Create a virtual environment with:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

- To avoid hardcoding credentials, use a `.env` file (see README)

Happy coding!
