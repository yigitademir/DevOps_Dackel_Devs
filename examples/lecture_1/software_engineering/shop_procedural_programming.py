# runcmd: "../venv/Scripts/python" shop_procedural_programming.py
# coding: utf-8

import os
import pandas as pd


def load_transactions_from_folder(path: str) -> None:
    global df
    df = pd.DataFrame()
    for filename in os.listdir(path):
        if filename.endswith('.csv'):
            print(filename)
            append_transactions_from_file(f'{path}/{filename}')
    print(f'{df.shape[0]} transactions loaded')

    # transform data
    df['revenue'] = df['product_price'] * df['quantity']
    df["date"] = pd.to_datetime(df["date"])


def append_transactions_from_file(path: str) -> None:
    global df
    df_temp = pd.read_csv(path, sep=';')
    df = pd.concat([df, df_temp], ignore_index=True)


def print_revenue_per_customer():
    df_total = df[['customer_id', 'revenue']].groupby(['customer_id']).sum().reset_index()
    for index, row in df_total.iterrows():
        print(f"customer_id: {row['customer_id']}, revenue: {row['revenue']} CHF")


def print_revenue_per_month() -> None:
    df_total = df[['date', 'revenue']].groupby(pd.Grouper(key='date', freq='ME')).sum().reset_index()
    for index, row in df_total.iterrows():
        print(f"month: {row['date'].strftime('%Y-%m')}, revenue: {row['revenue']} CHF")


def print_customer_transactions(customer_id: int) -> None:
    print(f"customer_id: {customer_id}")
    df_customer = df[df['customer_id'] == customer_id]
    df_date_revenue_total = df_customer[['date', 'revenue']].groupby(['date']).sum().reset_index()
    df_date_revenue_total
    dict_date_revenue_total = {}
    for index, row in df_date_revenue_total.iterrows():
        dict_date_revenue_total[row['date']] = row['revenue']
    df_customer.sort_values(['date'])
    last_date = None
    for index, row in df_customer.iterrows():
        if last_date != row['date']:
            last_date = row['date']
            revenue_total = dict_date_revenue_total[row['date']]
            print(f"- date: {last_date.strftime('%Y-%d-%m')}, revenue total: {revenue_total} CHF")
        print(f"  - id: {row['product_id']}, name: {row['product_name']}, price: {row['product_price']}, quantity: {row['quantity']}, revenue: {row['revenue']}")


if __name__ == '__main__':

    print('--- Load data ---')
    path = 'data'
    load_transactions_from_folder(path)
    print()

    print('--- Revenue per customer ---')
    print_revenue_per_customer()
    print()

    print('--- Revenue per month: ---')
    print_revenue_per_month()
    print()

    print('--- Revenue for specific customer: ---')
    customer_id = 1234
    print_customer_transactions(customer_id)
    print()
