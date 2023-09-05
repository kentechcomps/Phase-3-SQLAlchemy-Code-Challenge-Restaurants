from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, engine_from_config
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from faker import Faker
import random
from models import Restaurant , Customer , Review
Base = declarative_base()

if __name__ == '__main__':

    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    print("seeding....")
    fake = Faker()
    restaurants=[]
    for i in range(5):
        restaurant=Restaurant(
            name=fake.name(),
            price=fake.pyint()
        )
        session.add(restaurant)
        session.commit()
        restaurants.append(restaurant)
    
    customers=[]
    for i in range(5):
        customer=Customer(
            first_name=fake.name(),
            last_name=fake.name()
        )
        session.add(customer)
        session.commit()
        customers.append(customer)

    reviews=[]
    for restaurant in restaurants:
        for i in range(random.randint(1,5)):
            customer=random.choice(customers)

            review=Review(
                comment=fake.sentence(),
                star_rating=random.randint(0,10),
                restaurant_id=restaurant.id,
                customer_id=customer.id
            )
            if restaurant not in customer.restaurants:
                customer.reviews.append(review)
                session.commit()
            
           
    session.bulk_save_objects(reviews)
    session.commit()
    session.close()   