from sqlalchemy import create_engine
from models import Base


engine = create_engine('sqlite:///restaurant.db')

# Create the tables in the database
Base.metadata.create_all(engine)