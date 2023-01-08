import json

import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from models import create_tables, Shop, Publisher, Book, Stock, Sale


server = ''
user = ''
password = ''
database = ''

DSN = f'{server}://{user}:{password}@localhost:5432/{database}'
engine = sq.create_engine(DSN)


Session = sessionmaker(bind=engine)
session = Session()

create_tables(engine)

with open(r'tests_data.json', 'r') as fd:
    data = json.load(fd)

for record in data:
    model = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[record.get('model')]
    session.add(model(id=record.get('pk'), **record.get('fields')))
session.commit()


def get_sales():
    inquiry = input('Please, enter id or name of the publisher: ')
    if inquiry.isdigit():
        for i in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher, Publisher.id == Book.id_publisher).join(Stock, Book.id == Stock.id_book).join(Sale, Stock.id == Sale.id_stock).join(Shop, Shop.id == Stock.id_shop).filter(Publisher.id == inquiry):
            print(f'Book title: {i[0]}, Shop: {i[1]}, Price: {i[2]}, Date of sale: {i[3]}')
    else:
        for i in session.query(Book.title, Shop.name, Sale.price, Sale.date_sale).join(Publisher, Publisher.id == Book.id_publisher).join(Stock, Book.id == Stock.id_book).join(Sale, Stock.id == Sale.id_stock).join(Shop, Shop.id == Stock.id_shop).filter(Publisher.name == inquiry):
            print(f'Book title: {i[0]}, Shop: {i[1]}, Price: {i[2]}, Date of sale: {i[3]}')


if __name__ == '__main__':
    get_sales()

    session.close()