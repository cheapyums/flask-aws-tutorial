from dateutil import tz

def convertUTCToTimezone(dt, timeZone):
    from_zone = tz.gettz('UTC')
    utc = dt.replace(tzinfo=from_zone)
    to_zone = tz.gettz(timeZone)
    return utc.astimezone(to_zone)