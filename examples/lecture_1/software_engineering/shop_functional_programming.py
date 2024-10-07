# runcmd: "../../venv/Scripts/python" shop_functional_programming.py
# coding: utf-8

import os
import csv
import datetime
import copy


class Product:

    @staticmethod
    def get_instance(id, name, price, quantity) -> dict:
        return {
            'id': id,
            'name': name,
            'price': price,
            'quantity': quantity
        }

    @staticmethod
    def get_revenue(product: dict) -> int:
        return product['price'] * product['quantity']

    @classmethod
    def get_string(cls, product) -> None:
        return f"id: {product['id']}, name: {product['name']}, price: {product['price']}, quantity: {product['quantity']}, revenue: {cls.get_revenue(product)}"


class Transaction:

    @staticmethod
    def get_instance(date) -> dict:
        return {
            'date': date,
            'list_product': [],
        }

    @staticmethod
    def get_revenue(transaction) -> int:
        revenue = 0
        for product in transaction['list_product']:
            revenue += Product.get_revenue(product)
        return revenue

    @classmethod
    def get_string(cls, transaction) -> None:
        info = f"- date: {transaction['date'].strftime('%Y-%m-%d')}, revenue total: {cls.get_revenue(transaction)} CHF"
        for product in transaction['list_product']:
            info += f'\n  - {Product.get_string(product)}'
        return info


class Customer:

    @staticmethod
    def get_instance(id) -> dict:
        return {
            'id': id,
            'list_transaction': [],
        }

    @staticmethod
    def add_transaction_data(customer: dict, row: dict) -> dict:
        customer = copy.deepcopy(customer)

        # find or create transaction object
        transaction = None
        dt = datetime.datetime.strptime(row['date'], '%Y-%m-%d')
        for trans in customer['list_transaction']:
            if trans['date'] == dt:
                transaction = trans
                break
        if transaction is None:
            transaction = Transaction.get_instance(dt)
            customer['list_transaction'].append(transaction)

        # create product and add to transactino
        product = Product.get_instance(
            int(row['product_id']),
            row['product_name'],
            int(row['product_price']),
            int(row['quantity'])
        )
        transaction['list_product'].append(product)
        return customer

    @staticmethod
    def get_revenue_total(customer: dict) -> int:
        revenue_total = 0
        for transaction in customer['list_transaction']:
            revenue_total += Transaction.get_revenue(transaction)
        return revenue_total

    @staticmethod
    def get_revenue_per_month(customer: dict) -> dict:
        dict_month_revenue = {}
        for transaction in customer['list_transaction']:
            month = datetime.datetime.strftime(transaction['date'], '%Y-%m')
            if month not in dict_month_revenue:
                dict_month_revenue[month] = 0
            dict_month_revenue[month] += Transaction.get_revenue(transaction)
        return dict_month_revenue

    @staticmethod
    def print_transactions(customer: dict) -> None:
        for transaction in customer['list_transaction']:
            print(Transaction.get_string(transaction))


class Shop:

    LIST_TRANSACTION_COLUMN = [
        'customer_id',
        'date',
        'product_id',
        'product_name',
        'product_price',
        'quantity'
    ]

    @staticmethod
    def get_instance() -> dict:
        return {
            'dict_customer': {}
        }

    @classmethod
    def load_transactions_from_folder(cls, shop: dict, path: str) -> dict:
        shop = copy.deepcopy(shop)
        cnt_transactions = 0
        for filename in os.listdir(path):
            if filename.endswith('.csv'):
                print(filename)
                shop_updated, cnt_transactions_in_file = cls.load_transactions_from_file(shop, f'{path}/{filename}')
                shop = shop_updated
                cnt_transactions += cnt_transactions_in_file
        print(f'{cnt_transactions} transactions loaded')
        return shop

    @classmethod
    def load_transactions_from_file(cls, shop: dict, path: str) -> (dict, int):
        shop = copy.deepcopy(shop)

        with open(path, mode='r', encoding='utf-8') as fin:
            csv_reader = csv.DictReader(fin, delimiter=';')

            # validate data structure
            for fieldname in cls.LIST_TRANSACTION_COLUMN:
                assert fieldname in csv_reader.fieldnames, f'Missing column "{fieldname}".'

            # parse transactions
            cnt_transactions = 0
            for row in csv_reader:

                # find or create customer object
                customer = None
                customer_id = int(row['customer_id'])
                if customer_id not in shop['dict_customer']:
                    customer = Customer.get_instance(customer_id)
                else:
                    customer = shop['dict_customer'][customer_id]

                # add transaction data
                customer = Customer.add_transaction_data(customer, row)
                shop['dict_customer'][customer_id] = customer  # new instance needs to be set
                cnt_transactions += 1

            return shop, cnt_transactions

    @staticmethod
    def print_revenue_per_customer(shop: dict) -> None:
        for customer in shop['dict_customer'].values():
            print(f"customer_id: {customer['id']}, revenue: {Customer.get_revenue_total(customer)} CHF")

    @staticmethod
    def print_revenue_per_month(shop: dict) -> None:
        dict_month_revenue_total = {}
        for customer in shop['dict_customer'].values():
            dict_month_revenue_customer = Customer.get_revenue_per_month(customer)
            for month, revenue in dict_month_revenue_customer.items():
                if month not in dict_month_revenue_total:
                    dict_month_revenue_total[month] = 0
                dict_month_revenue_total[month] += revenue

        for month in sorted(dict_month_revenue_total.keys()):
            print(f'month: {month}, revenue: {dict_month_revenue_total[month]} CHF')

    def print_customer_transactions(shop: dict, customer_id) -> None:
        assert customer_id in shop['dict_customer'], f'Customer ID not found "{customer_id}"'
        customer = shop['dict_customer'][customer_id]
        print(f'customer_id: {customer_id}')
        Customer.print_transactions(customer)


if __name__ == '__main__':

    shop = Shop.get_instance()

    print('--- Load data ---')
    path = 'data'
    shop = Shop.load_transactions_from_folder(shop, path)
    print()

    print('--- Revenue per customer ---')
    Shop.print_revenue_per_customer(shop)
    print()

    print('--- Revenue per month: ---')
    Shop.print_revenue_per_month(shop)
    print()

    print('--- Revenue for specific customer: ---')
    customer_id = 1234
    Shop.print_customer_transactions(shop, customer_id)
    print()
