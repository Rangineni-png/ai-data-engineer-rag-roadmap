import pandas as pd
import logging
from pathlib import Path


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


BASE_DIR = Path(__file__).parent
CUSTOMERS_FILE = BASE_DIR / "customers.csv"
ORDERS_FILE = BASE_DIR / "orders.csv"
OUTPUT_DIR = BASE_DIR / "output"


def load_csv(file_path):
    try:
        logging.info(f"Loading file: {file_path}")
        return pd.read_csv(file_path)
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except Exception as e:
        logging.error(f"Error loading file {file_path}: {e}")
        raise


def clean_orders(orders_df):
    logging.info("Cleaning orders data")

    orders_df = orders_df.drop_duplicates()
    orders_df = orders_df.dropna(subset=["amount"])
    orders_df = orders_df[orders_df["status"] == "completed"]

    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])

    return orders_df


def validate_customer_ids(customers_df, orders_df):
    logging.info("Validating customer IDs")

    valid_customer_ids = set(customers_df["customer_id"])
    order_customer_ids = set(orders_df["customer_id"])

    invalid_ids = order_customer_ids - valid_customer_ids

    if invalid_ids:
        logging.warning(f"Invalid customer IDs found in orders: {invalid_ids}")

    return invalid_ids


def create_customer_summary(customers_df, orders_df):
    logging.info("Creating customer summary")

    order_summary = (
        orders_df
        .groupby("customer_id")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "total_spent"})
    )

    customer_summary = customers_df.merge(
        order_summary,
        on="customer_id",
        how="left"
    )

    customer_summary["total_spent"] = customer_summary["total_spent"].fillna(0)

    return customer_summary


def create_monthly_summary(orders_df):
    logging.info("Creating monthly revenue summary")

    orders_df["month"] = orders_df["order_date"].dt.to_period("M").astype(str)

    monthly_summary = (
        orders_df
        .groupby("month")["amount"]
        .sum()
        .reset_index()
        .rename(columns={"amount": "monthly_revenue"})
    )

    return monthly_summary


def save_output(df, file_name):
    OUTPUT_DIR.mkdir(exist_ok=True)
    output_path = OUTPUT_DIR / file_name

    logging.info(f"Saving output file: {output_path}")
    df.to_csv(output_path, index=False)


def main():
    customers_df = load_csv(CUSTOMERS_FILE)
    orders_df = load_csv(ORDERS_FILE)

    clean_orders_df = clean_orders(orders_df)

    invalid_customer_ids = validate_customer_ids(customers_df, clean_orders_df)

    customer_summary = create_customer_summary(customers_df, clean_orders_df)
    monthly_summary = create_monthly_summary(clean_orders_df)

    save_output(clean_orders_df, "clean_orders.csv")
    save_output(customer_summary, "customer_summary.csv")
    save_output(monthly_summary, "monthly_summary.csv")

    logging.info("Pipeline completed successfully")

    if invalid_customer_ids:
        logging.warning("Pipeline completed with data quality warnings")


if __name__ == "__main__":
    main()