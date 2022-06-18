import pandas as pd
import sqlalchemy

#Create db engine
db = sqlalchemy.create_engine('sqlite:///netflix.db')

#create memory db
mem_db = sqlalchemy.create_engine('sqlite:///:memory:')

#Import CSV
data = pd.read_csv("data/netflix_titles.csv")

#Load CSV to db
data.to_sql('netflix_titles', db)