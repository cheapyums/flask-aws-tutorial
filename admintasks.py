#from flask import Flask, render_template, request, send_file, session

from datetime import datetime
import random

from app import application
from application import db
from application.models import Restaurant, Offer, Award

from coupon_encoder import CouponEncoder

@application.route("/admin/restaurant/add")
def addRestaurant():
    r = Restaurant("mama-coco","Mama Coco","fC4We0ggwe4tsftswoh", None, None, "12:30","2:00", "7:00", "8:00")
    db.session.add(r)
    db.session.commit()
    db.session.close()
    return ""

@application.route("/admin/<restaurant>/offer/add")
def addOffer(restaurant):
    res = Restaurant.query.filter_by(code=restaurant).first()
    if res is None:
        return "Error: Invalid Restaurant"
    o = Offer("welcome",restaurant,10,10,5,5,"2019/8/19","2019/8/24","ACTIVE")
    try:
        db.session.add(o)
        db.session.commit()
        db.session.close()
    except:
        db.session.rollback()
        return "Error: Invalid Offer Code"
    return ""

@application.route("/admin/<restaurant>/offer/<offerCode>/issueaward")
def issueAward(restaurant, offerCode):
    off = Offer.query.filter_by(code=offerCode, restaurant_code=restaurant).first()
    if off is None:
        return "Error: Invalid Offer.  Offer does not exist."

    if off.valid_end_date < datetime.now().date():
        return "Error: Offer Expired."

    if off.status != "ACTIVE":
        return "Error: Offer is not Active."

    c = CouponEncoder('10BEH8G426RADWZVF9JPKX5QMC3YTN7S')

    while True:
        awardCode =  c.encode(random.randrange(1,150000000), num_digits=8)
        awd = Award(awardCode, restaurant, offerCode, None, datetime.now())
        try:
            db.session.add(awd)
            db.session.commit()
            db.session.close()
            return ""
        except:
            db.session.rollback()
            print "Error: Award Code already Exists.  Generating new code."