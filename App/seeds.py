from faker import Faker
import random
from models import Restaurant , Customer , Review, session

fake = Faker()



if __name__ == '__main__':
    session.query(Restaurant).delete()
    session.query(Customer).delete()
    session.query(Review).delete()

    print("seeding....")
    restaurants=[]
    for i in range(10):
            restaurant=Restaurant(
                name=fake.name(),
                price=random.randint(1000, 50000)
            )
            session.add(restaurant)
            session.commit()
            restaurants.append(restaurant)
        
    customers=[]
    for i in range(10):
            customer=Customer(
                first_name=fake.first_name(),
                last_name=fake.last_name()
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
                # if restaurant not in customer.restaurants:
                #     customer.reviews.append(review)
                #     session.commit()
                # reviews.append(review)
                
            
                session.add(review)
    session.commit()
               