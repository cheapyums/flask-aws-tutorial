from application import db


class Restaurant(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(128))
    timezone = db.Column(db.String(50))
    password = db.Column(db.String(30))
    bf_start = db.Column(db.Time)
    bf_end = db.Column(db.Time)
    lu_start = db.Column(db.Time)
    lu_end = db.Column(db.Time)
    di_start = db.Column(db.Time)
    di_end = db.Column(db.Time)
    status = db.Column(db.String(30))

    def __init__(self, code, name, timezone, password, bf_start, bf_end, lu_start, lu_end, di_start, di_end, status="ACTIVE"):
        self.code = code
        self.name = name
        self.timezone = timezone
        self.password = password
        self.bf_start = bf_start
        self.bf_end = bf_end
        self.lu_start = lu_start
        self.lu_end = lu_end
        self.di_start = di_start
        self.di_end = di_end
        self.status = status


class Offer(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    restaurant_code = db.Column(db.String(30), primary_key=True)
    max_customers = db.Column(db.Integer)
    min_offer_percent = db.Column(db.Integer)
    off_peak_bonus =  db.Column(db.Integer)
    random_offer_bonus = db.Column(db.Integer)
    valid_start_date = db.Column(db.Date)
    valid_end_date = db.Column(db.Date)
    status = db.Column(db.String(30))

    def __init__(self, code, restaurant_code, max_customers, min_offer_percent, off_peak_bonus, random_offer_bonus, valid_start_date, valid_end_date, status):
        self.code = code
        self.restaurant_code = restaurant_code
        self.max_customers = max_customers
        self.min_offer_percent = min_offer_percent
        self.off_peak_bonus = off_peak_bonus
        self.random_offer_bonus = random_offer_bonus
        self.valid_start_date = valid_start_date
        self.valid_end_date = valid_end_date
        self.status = status


class Award(db.Model):
    code = db.Column(db.String(30), primary_key=True)
    restaurant_code = db.Column(db.String(30), primary_key=True)
    offer_code = db.Column(db.String(30))
    customers = db.Column(db.Integer)
    status = db.Column(db.String(30))
    award_ts = db.Column(db.DateTime)
    redemption_ts = db.Column(db.DateTime)
    offer_percent = db.Column(db.Integer)

    def __init__(self, code, restaurant_code, offer_code,customers, award_ts, status = "ISSUED", redemption_ts = None, offer_percent = None):
        self.code = code
        self.restaurant_code = restaurant_code
        self.offer_code = offer_code
        self.customers = customers
        self.award_ts = award_ts
        self.status = status
        self.redemption_ts = redemption_ts
        self.offer_percent = offer_percent

class User(db.Model):
    username = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(128))
    password = db.Column(db.String(30))

    def __init__(self, username, name, password):
        self.username = username
        self.name = name
        self.password = password
