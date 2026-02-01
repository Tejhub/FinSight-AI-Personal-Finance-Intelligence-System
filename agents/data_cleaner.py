from utils import load_and_validate_csv, clean_financial_data

class DataCleaningAgent:
    def run(self, file):
        df = load_and_validate_csv(file)
        return clean_financial_data(df)
