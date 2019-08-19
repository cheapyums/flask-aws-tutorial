from application import db
from application.models import User, Restaurant, Offer, Award

db.create_all()

print("DB created.")
