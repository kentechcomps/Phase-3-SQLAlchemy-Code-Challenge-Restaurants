from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, engine_from_config
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    rating = Column(Integer)
    comment = Column(Text)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))

    restaurant = relationship('Restaurant', backref='reviews')
    customer = relationship('Customer', backref='reviews')


    engine = create_engine('sqlite:///Restaurant.db')

# Create a session
Session = sessionmaker(bind=engine_from_config)
session = Session()

# Seed data for restaurants
restaurant1 = Restaurant(name='Restaurant1', price=2)
restaurant2 = Restaurant(name='Restaurant2', price=3)

# Seed data for customers
customer1 = Customer(first_name='John', last_name='Doe')
customer2 = Customer(first_name='Jane', last_name='Smith')

# Add data to the session
session.add_all([restaurant1, restaurant2, customer1, customer2])

# Commit the changes
session.commit()