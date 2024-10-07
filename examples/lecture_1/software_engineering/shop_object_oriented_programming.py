# runcmd: "../venv/Scripts/python" shop_object_oriented_programming.py
# coding: utf-8

import os
import csv
import datetime


class Product:
    def __init__(self, id, name, price, quantity) -> None:
        self.id: int = id
        self.name: str = name
        self.price: int = price
        self.quantity: int = quantity

    def get_revenue(self) -> int:
        return self.price * self.quantity

    def __str__(self) -> None:
        return f'id: {self.id}, name: {self.name}, price: {self.price}, quantity: {self.quantity}, revenue: {self.get_revenue()}'


class Transaction:
    def __init__(self, date) -> None:
        self.date: datetime.datetime.date = date
        self.list_product: list[Product] = []

    def get_revenue(self) -> int:
        revenue = 0
        for product in self.list_product:
            revenue += product.get_revenue()
        return revenue

    def __str__(self) -> None:
        info = f"- date: {self.date.strftime('%Y-%m-%d')}, revenue total: {self.get_revenue()} CHF"
        for product in self.list_product:
            info += f'\n  - {product}'
        return info


class Customer:
    def __init__(self, id) -> None:
        self.id: int = id
        self.list_transaction: list[Transaction] = []

    def add_transaction_data(self, row: dict) -> None:

        # find or create transaction object
        transaction = None
        dt = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
        for trans in self.list_transaction:
            if trans.date == dt:
                transaction = trans
                break
        if transaction is None:
            transaction = Transaction(dt)
            self.list_transaction.append(transaction)

        # create product and add to transactino
        product = Product(
            int(row['product_id']),
            row['product_name'],
            int(row['product_price']),
            int(row['quantity'])
        )
        transaction.list_product.append(product)

    def get_revenue_total(self) -> int:
        revenue_total = 0
        for transaction in self.list_transaction:
            revenue_total += transaction.get_revenue()
        return revenue_total

    def get_revenue_per_month(self) -> dict:
        dict_month_revenue = {}
        for transaction in self.list_transaction:
            month = datetime.datetime.strftime(transaction.date, '%Y-%m')
            if month not in dict_month_revenue:
                dict_month_revenue[month] = 0
            dict_month_revenue[month] += transaction.get_revenue()
        return dict_month_revenue

    def print_transactions(self) -> None:
        for transaction in self.list_transaction:
            print(transaction)


class Shop:

    LIST_TRANSACTION_COLUMN = [
        'customer_id',
        'date',
        'product_id',
        'product_name',
        'product_price',
        'quantity'
    ]

    def __init__(self) -> None:
        self.dict_customer = {}

    def load_transactions_from_folder(self, path: str) -> None:
        cnt_transactions = 0
        for filename in os.listdir(path):
            if filename.endswith('.csv'):
                print(filename)
                cnt_transactions += self.load_transactions_from_file(f'{path}/{filename}')
        print(f'{cnt_transactions} transactions loaded')

    def load_transactions_from_file(self, path: str) -> int:
        with open(path, mode='r', encoding='utf-8') as fin:
            csv_reader = csv.DictReader(fin, delimiter=';')

            # validate data structure
            for fieldname in self.LIST_TRANSACTION_COLUMN:
                assert fieldname in csv_reader.fieldnames, f'Missing column "{fieldname}".'

            # parse transactions
            cnt_transactions = 0
            for row in csv_reader:

                # find or create customer object
                customer = None
                customer_id = int(row['customer_id'])
                if customer_id not in self.dict_customer:
                    customer = Customer(customer_id)
                    self.dict_customer[customer_id] = customer
                else:
                    customer = self.dict_customer[customer_id]

                # add transaction data
                customer.add_transaction_data(row)
                cnt_transactions += 1

            return cnt_transactions

    def print_revenue_per_customer(self) -> None:
        for customer in self.dict_customer.values():
            print(f'customer_id: {customer.id}, revenue: {customer.get_revenue_total()} CHF')

    def print_revenue_per_month(self) -> None:
        dict_month_revenue_total = {}
        for customer in self.dict_customer.values():
            dict_month_revenue_customer = customer.get_revenue_per_month()
            for month, revenue in dict_month_revenue_customer.items():
                if month not in dict_month_revenue_total:
                    dict_month_revenue_total[month] = 0
                dict_month_revenue_total[month] += revenue

        for month in sorted(dict_month_revenue_total.keys()):
            print(f'month: {month}, revenue: {dict_month_revenue_total[month]} CHF')

    def print_customer_transactions(self, customer_id) -> None:
        assert customer_id in self.dict_customer, f'Customer ID not found "{customer_id}"'
        customer = self.dict_customer[customer_id]
        print(f'customer_id: {customer_id}')
        customer.print_transactions()


if __name__ == '__main__':

    shop = Shop()

    print('--- Load data ---')
    path = 'data'
    shop.load_transactions_from_folder(path)
    print()

    print('--- Revenue per customer ---')
    shop.print_revenue_per_customer()
    print()

    print('--- Revenue per month: ---')
    shop.print_revenue_per_month()
    print()

    print('--- Revenue for specific customer: ---')
    customer_id = 1234
    shop.print_customer_transactions(customer_id)
    print()
