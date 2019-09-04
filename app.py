from flask import Flask
from yumsapp.core.utils import convertUTCToTimezone

# Elastic Beanstalk initalization
application = Flask(__name__)
application.debug = True
# change this to your own value
application.secret_key = 'cC1YCIWOj9GgWspgNEo2'


def format_valueIfNone(value, valueIfNone=""):
    if value is None:
        return valueIfNone
    return value

def format_datetime(value,timezone=None,format="%m-%d-%Y",valueIfNone=""):
    if value is None:
        return valueIfNone
    if timezone is None:
        return value.strftime(format)
    return convertUTCToTimezone(value, timezone).strftime(format)

'''
    if format == 'full':
        format="EEEE, d. MMMM y 'at' HH:mm"
    elif format == 'medium':
        format="EE dd.MM.y HH:mm"
    return babel.dates.format_datetime(value, format)
'''


application.jinja_env.filters['datetime'] = format_datetime
application.jinja_env.filters['valueIfNone'] = format_valueIfNone