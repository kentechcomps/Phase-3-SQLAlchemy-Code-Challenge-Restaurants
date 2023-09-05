from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, desc, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.associationproxy import association_proxy
from faker import Faker




convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

engine=create_engine('sqlite:///restaurants.db')
Session=sessionmaker(bind=engine)
session=Session()

class Restaurant(Base):
    __tablename__ = 'restaurants'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    reviews=relationship('Review',back_populates='restaurant')
    customers= association_proxy('reviews','customer',creator=lambda us: Review(customer=us))

    def reviews(self):
        return self.reviews
    def customers(self):
        return[review.customer for review in self.reviews]
    
    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(desc(cls.price)).first()
    
    def all_reviews(self):
        return [review.full_review() for review in self.reviews]

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    
    reviews=relationship('Review',back_populates='customer')
    restaurants=association_proxy('reviews','restaurant',creator=lambda gm: Review(restaurant=gm))
    

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

    def favorite_restaurant(self):
        return session.query(Restaurant).join(Review).filter(Review.customer_id==self.id).order_by(desc(Review.star_rating)).first()
    def reviews(self):
        return self.reviews
    def restaurant(self):
        return[review.restaurant for review in self.reviews]


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer)
    comment = Column(Text)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))    
    restaurant = relationship('Restaurant', backref='reviews')
    customer = relationship('Customer', backref='reviews')

    def customer(self):
        return self.customer
    def restaurant(self):
        return self.restaurant
    def full_review(self):
        return f'Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars'

