import pandas as pd

REQUIRED_COLUMNS = ["date", "description", "expense/income", "amount"]

def load_and_validate_csv(file):
    df = pd.read_csv(file)
    df.columns = [c.strip().lower() for c in df.columns]
    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing column: {col}")
    return df

def clean_financial_data(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
    df["expense/income"] = df["expense/income"].astype(str).str.strip().str.capitalize()

    df = df.dropna(subset=["date", "amount"])
    df = df[df["expense/income"].isin(["Income", "Expense"])]
    df = df[df["amount"] > 0]

    return df.reset_index(drop=True)
