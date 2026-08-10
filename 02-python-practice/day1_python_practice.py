import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)


def clean_data(df):
    df = df.drop_duplicates()
    df = df.dropna()
    df = df[df["status"] == "completed"]
    return df


def summarize_by_customer(df):
    summary = df.groupby("customer_id")["amount"].sum().reset_index()
    summary = summary.rename(columns={"amount": "total_spent"})
    return summary


def summarize_by_month(df):
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["month"] = df["order_date"].dt.to_period("M")
    monthly_summary = df.groupby("month")["amount"].sum().reset_index()
    return monthly_summary


def main():
    file_path = "orders.csv"

    df = load_data(file_path)
    cleaned_df = clean_data(df)

    customer_summary = summarize_by_customer(cleaned_df)
    monthly_summary = summarize_by_month(cleaned_df)

    cleaned_df.to_csv("cleaned_orders.csv", index=False)
    customer_summary.to_csv("customer_summary.csv", index=False)
    monthly_summary.to_csv("monthly_summary.csv", index=False)

    print("Pipeline completed successfully.")
    print(customer_summary)
    print(monthly_summary)


if __name__ == "__main__":
    main()