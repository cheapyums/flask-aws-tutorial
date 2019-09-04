from flask import render_template, request, send_file, session, redirect, flash
from application import db
from application.models import Restaurant, Offer, Award, RestaurantLead, ConsumerLead
from datetime import datetime
import qrcode
import cStringIO
import random
import re
from app import application
from yumsapp.core.utils import convertUTCToTimezone


import admintasks


#@application.route("/tst")
#def tst():
#    return render_template("test.html")


@application.route("/act", methods=['GET', 'POST'])
def info():
    if request.method == "GET":
        return render_template("restaurant_lead.html", data={})
    if request.method == "POST":
        data = {
            "restaurant": request.form.get("restaurant", ""),
            "manager": request.form.get("manager", ""),
            "zipcode": request.form.get("zipcode", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", "")
        }

        error = False
        if data["restaurant"] == "":
            error = True
            flash("Please provide the name of your restaurant")
        if data["manager"] == "":
            error = True
            flash("Please provide your name")

        if data["email"] == "" or (not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", data["email"])):
            error = True
            flash("Please provide a valid email address.")

        if data["email"] == "" and data["phone"] == "":
            error = True
            flash("In order for us to contact you, please provide either your email or your phone number")
        if error:
            return render_template("restaurant_lead.html", data=data)

        lead = RestaurantLead(data["restaurant"],data["manager"], data["email"], data["phone"], data["zipcode"])
        db.session.add(lead)
        db.session.commit()
        db.session.close()

        return render_template("message.html", message = "Thank you very much. We will be contacting you shortly!")

@application.route("/eat", methods=['GET', 'POST'])
def clientinfo():
    if request.method == "GET":
        return render_template("consumer_lead.html", data={})
    if request.method == "POST":
        data = {
            "name": request.form.get("name", ""),
            "zipcode": request.form.get("zipcode", ""),
            "email": request.form.get("email", ""),
        }

        error = False
        if data["name"] == "":
            error = True
            flash("Please provide your name")

        if not re.match(r"[^@\s]+@[^@\s]+\.[a-zA-Z0-9]+$", data["email"]):
            error = True
            flash("Please provide a valid email address.")

        if data["zipcode"] == "":
            error = True
            flash("Please provide your zip code so we can identify offers near you.")

        if error:
            return render_template("consumer_lead.html", data=data)

        lead = ConsumerLead(data["name"],data["email"], data["zipcode"])
        db.session.add(lead)
        db.session.commit()
        db.session.close()
        return render_template("message.html", message="Thank you very much. We will be contacting you shortly!")


@application.route("/host")
def host():
    return request.host

@application.route("/a/<restaurant>/award/<awardCode>", methods=['GET', 'POST'])
def viewAward(restaurant, awardCode):
    db.session.connection(execution_options={'isolation_level': "READ COMMITTED"})
    awd = Award.query.filter_by(code=awardCode, restaurant_code=restaurant).first()
    if awd is None:
        print "Award not found"
        return ""

    off = Offer.query.filter_by(code=awd.offer_code, restaurant_code=restaurant).first()
    if off is None:
        print "Offer not found"
        return ""

    res = Restaurant.query.filter_by(code=restaurant).first()
    if res is None:
        print "Restaurant not found"
        return ""

    if awd.customers is None:
        if request.method == "GET":
            return render_template('pre_award.html', maxCustomers=off.max_customers,updateURL="/a/{0}/award/{1}".format(restaurant, awardCode))
        if request.method == "POST":
            cust = int(request.form.get("customers", 0))
            if 0 < cust <= off.max_customers:
                awd.customers = cust
                db.session.commit()
            else:
                return render_template('pre_award.html', maxCustomers=off.max_customers, updateURL="/a/{0}/award/{1}".format(restaurant, awardCode))

    hours = ""
    if res.bf_start is not None and res.bf_end is not None:
        hours = "{0} - {1}".format(res.bf_start.strftime("%-I:%M %p"), res.bf_end.strftime("%-I:%M %p"))
    if res.lu_start is not None and res.lu_end is not None:
        if hours != "":
            hours = "{0} / ".format(hours)
        hours = "{0}{1} - {2}".format(hours,res.lu_start.strftime("%-I:%M %p"), res.lu_end.strftime("%-I:%M %p"))
    if res.di_start is not None and res.di_end is not None:
        if hours != "":
            hours = "{0} / ".format(hours)
        hours = "{0}{1} - {2}".format(hours,res.di_start.strftime("%-I:%M %p"), res.di_end.strftime("%-I:%M %p"))

    data={
        "minPercent": off.min_offer_percent,
        "maxPercent": off.min_offer_percent + off.off_peak_bonus + off.random_offer_bonus,
        "startDate": off.valid_start_date.strftime("%-m/%-d/%y"),
        "endDate": off.valid_end_date.strftime("%-m/%-d/%y"),
        "peakPercent": off.min_offer_percent,
        "offPeakPercent": off.min_offer_percent + off.off_peak_bonus,
        "hours": hours,
        "customers":awd.customers,
        "status": awd.status
    }
    if awd.status == "REDEEMED":
        data["discount"]= awd.offer_percent
        data["redemptionDate"] = convertUTCToTimezone(awd.redemption_ts, res.timezone).date().strftime("%-m/%-d/%y")
        data["redemptionTime"] = convertUTCToTimezone(awd.redemption_ts, res.timezone).time().strftime("%-I:%M %p")

    db.session.close()
    if request.method == "POST":
        return redirect("/a/{0}/award/{1}".format(restaurant, awardCode))
    return render_template("award.html", restaurant=restaurant, awardCode=awardCode, data=data)


@application.route("/a/<restaurant>/qrcode/<awardCode>")
def QRCode(restaurant, awardCode):
    db.session.connection(execution_options={'isolation_level': "READ COMMITTED"})
    awd = Award.query.filter_by(code=awardCode, restaurant_code=restaurant).first()
    if awd is None:
        return ""

    off = Offer.query.filter_by(code=awd.offer_code, restaurant_code=restaurant).first()
    if off is None:
        return ""

    if awd.customers is None:
        return ""

    img_buf = cStringIO.StringIO()
    img = qrcode.make("http://www.yumsapp.com/r/{0}/redemption/{1}".format(restaurant,awardCode))
    img.save(img_buf)
    img_buf.seek(0)
    return send_file(img_buf, mimetype='image/png')

@application.route("/r/signin", methods=['GET', 'POST'])
def signIn():
    db.session.connection(execution_options={'isolation_level': "READ COMMITTED"})
    if "restaurant" in session and session["loggedIn"] is True:
        restaurant = session["restaurant"]
        res = Restaurant.query.filter_by(code=restaurant).first()
        if res is None:
            return render_template("signin.html", path="/r/signin")
        return "You are now logged in as {0}".format(res.name)

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        res = Restaurant.query.filter_by(code=username).first()
        if res is None:
            return redirect("/r/signin")
        if res.password == password:
            session["restaurantName"] = res.name
            session["restaurant"] = username
            session["loggedIn"] = True
            return redirect("/r/{0}".format(username))
        else:
            return redirect("/r/signin")
    return render_template("signin.html", path="/r/signin")

@application.route("/r/signout")
def signOut():
    db.session.connection(execution_options={'isolation_level': "READ COMMITTED"})
    if "restaurant" in session:
        del session["restaurant"]
    if "restaurantName" in session:
        del session["restaurantName"]
    session["loggedIn"] = False
    return redirect("/")

@application.route("/r/<restaurant>")
def restaurantMain(restaurant):
    db.session.connection(execution_options={'isolation_level': "READ COMMITTED"})
    if "restaurant" not in session or "loggedIn" not in session:
        return redirect("/r/signin")

    #List all awards
    data = []
    offers = Offer.query.filter_by(restaurant_code = restaurant).all()
    res = Restaurant.query.filter_by(code=restaurant).first()
    for offer in offers:
        awards = Award.query.filter_by(restaurant_code=restaurant, offer_code=offer.code).all()
        d = {}
        d["offer"] = offer
        d["awards"] = awards
        data.append(d)

    return render_template("restaurant_main.html", data=data, restaurant=res)

@application.route("/r/<restaurant>/award/<awardCode>")
def viewRestaurantAward(restaurant, awardCode):
    db.session.connection(execution_options={'isolation_level': "READ COMMITTED"})
    if not restaurantIsSignedIn(restaurant):
        return redirect("/r/signin")

    awd = Award.query.filter_by(code=awardCode, restaurant_code=restaurant).first()
    res = Restaurant.query.filter_by(code=restaurant).first()
    if awd is None or res is None:
        return render_template("message.html", message="This offer is not valid in this establishment.")

    message =request.args.get("message",None)
    return render_template("award_details.html", award = awd, restaurant=res, message=message)


@application.route("/r/<restaurant>/redemption/<awardCode>")
def redeemOffer(restaurant, awardCode):
    db.session.connection(execution_options={'isolation_level': "READ COMMITTED"})
    if not restaurantIsSignedIn(restaurant):
        return redirect("/r/signin")

    awd = Award.query.filter_by(code=awardCode, restaurant_code=restaurant).first()
    if awd is None:
        return render_template("message.html", message="This offer is not valid in this establishment.")

    off = Offer.query.filter_by(code=awd.offer_code, restaurant_code=restaurant).first()
    if off is None:
        return render_template("message.html", message="This offer is not valid in this establishment.")

    res = Restaurant.query.filter_by(code=restaurant).first()
    if res is None:
        return render_template("message.html", message="This offer is not valid in this establishment.")

    if awd.status == "REDEEMED":
        dt = convertUTCToTimezone(awd.redemption_ts, res.timezone)
        return redirect("/r/{0}/award/{1}?message={2}".format(restaurant, awardCode, "This award has already been processed in the past. The award details are shown here."))

    now = convertUTCToTimezone(datetime.utcnow(), res.timezone)

    # Check to see if the award is currently valid based on the start and end dates
    if now.date() < off.valid_start_date or now.date() > off.valid_end_date:
        return "This offer is not currently valid.  This offer is only valid from {0} to {1}.".format(off.valid_start_date.strftime("%-m/%-d/%y"), off.valid_end_date.strftime("%-m/%-d/%y"))

    # Offer is valid.  Now let us set up all the offer details

    print "Current Time is {0}".format(now)
    print now.time()

    isPeak = False
    if res.bf_start is not None and res.bf_end is not None:
        if res.bf_start <= now.time() < res.bf_end:
            print "Breakfast Rush Hour"
            isPeak = True
    if res.lu_start is not None and res.lu_end is not None:
        if res.lu_start <= now.time() < res.lu_end:
            print "Lunch Rush Hour"
            isPeak = True
    if res.di_start is not None and res.di_end is not None:
        if res.di_start <= now.time() < res.di_end:
            print "Dinner Rush Hour"
            isPeak = True

    print isPeak

    print "Minimum Offer % : {0}".format(off.min_offer_percent)
    print "Offpeak Bonus % : {0}".format(off.off_peak_bonus)
    print "Random Offer Bonus % : {0}".format(off.random_offer_bonus)
    bonus = random.randrange(0, off.random_offer_bonus+1)
    print "Bonus {0}".format(bonus)

    offerValue = off.min_offer_percent
    if not isPeak:
        offerValue = offerValue + off.off_peak_bonus
    offerValue = offerValue + bonus
    print "Total Offer Value = {0}".format(offerValue)

    awd.redemption_ts = datetime.utcnow()
    awd.status = "REDEEMED"
    awd.offer_percent = offerValue
    db.session.commit()
    db.session.close()

    return redirect("/r/{0}/award/{1}?message={2}".format(restaurant,awardCode,"Award has been accepted"))


@application.route('/', methods=['GET', 'POST'])
@application.route('/index', methods=['GET', 'POST'])
def index():
    return render_template("index.html")


def restaurantIsSignedIn(restaurant):
    if "restaurant" not in session or "loggedIn" not in session:
        return False

    if session["restaurant"] != restaurant or session["loggedIn"] != True:
        return False

    return True


if __name__ == '__main__':
    application.run(host='0.0.0.0')