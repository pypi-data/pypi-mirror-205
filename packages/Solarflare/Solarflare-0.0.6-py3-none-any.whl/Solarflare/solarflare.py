# 1. TIME
# For these calculations, it is convenient to use Julian dates.
import datetime
from decimal import Decimal, getcontext
import math

# set the precision for Decimal module
getcontext().prec = 50 # good precision, fast results

def julian_date(date=datetime.datetime.now()):
    time = date.timestamp() * 1000
    tzoffset = date.utcoffset().total_seconds() // 60 if date.utcoffset() else 0
    return Decimal((time / 86400000) - (tzoffset / 1440) + 2440587.5)

J1970 = Decimal('2440588')
dayMs = Decimal('86400000')
# this is the inverse of the Julian Date function

def fromJulian(j):
    return datetime.datetime.fromtimestamp(float((Decimal(j) + Decimal('0.5') - J1970) * (dayMs / Decimal('1000.0'))))


#2. Math Tools
# degree input trigonometry functions
def sin(x): return Decimal(math.sin(math.radians(x)))
def cos(x): return Decimal(math.cos(math.radians(x)))
def tan(x): return Decimal(math.tan(math.radians(x)))
def acos(x): return Decimal(math.degrees(math.acos(x)))
def asin(x): return Decimal(math.degrees(math.asin(x)))
def atan2(y, x): return Decimal(math.degrees(math.atan2(y, x)))


#3. The Mean Anomaly using Decimal for Accuracy
def mean_anomaly(date=datetime.datetime.now()):
    J = Decimal(julian_date(date))
    J200 = Decimal('2451545')
    M0 = Decimal('357.5291')
    M1 = Decimal('0.98560028')
    return (M0 + M1 * (J - J200)) % Decimal('360')

#4. Equation of Center
def equation(date=datetime.datetime.now()):
    C1, C2, C3 = Decimal('1.9148'), Decimal('0.0200'), Decimal('0.0003')
    M = Decimal(mean_anomaly(date))
    C = C1 * sin(M) + C2 * sin(M * 2) + C3 * sin(M * 3)
    return C

#5. True Anomaly
def true_anomaly(date=datetime.datetime.now()):
    return equation(date) + mean_anomaly(date)

#6. Perihelion and Obliquity
II = Decimal('102.9373')
e = Decimal('23.4393')

#7. Ecliptical Coordinates
def ecliptical_longitude(date=datetime.datetime.now()):
    L = mean_anomaly(date) + II
    Lsun = Decimal(Decimal(L) + Decimal('180'))
    long = Lsun + Decimal(equation(date))
    return long % Decimal('360.0')

#8. Equatorial Coordinates
def right_ascension(date=datetime.datetime.now()):
    long = ecliptical_longitude(date)
    ra = atan2(sin(long) * cos(e), cos(long))
    return ra

def declination(date=datetime.datetime.now()):
    long = ecliptical_longitude(date)
    dec = asin(sin(long) * sin(e))
    return dec

#9. The Observer
def sidereal_time(longitude, date=datetime.datetime.now()):
    lw = -longitude
    theta1, theta2 = Decimal('280.1470'), Decimal('360.9856235')
    theta = (theta1 + theta2 * (julian_date(date) - Decimal('2451545')) - Decimal(lw)) % Decimal('360')
    return theta

#10. Solar Transit
def solar_transit(longitude, date=datetime.datetime.now()):
    L = mean_anomaly(date) + II
    Lsun = Decimal(Decimal(L) + Decimal('180'))
    J, J2000, J0, lw = julian_date(date), Decimal('2451545'), Decimal('0.0009'), -longitude
    nx = ((J - J2000 - J0) / Decimal('1.0000000')) - Decimal(lw)/Decimal('360')
    jx = J + Decimal('1.0000000') * (round(nx) - nx)
    jtransit = jx + Decimal('0.0053') * sin(mean_anomaly(date)) - Decimal('0.0068') * sin(Decimal('2') * Lsun)
    return jtransit

#11. Sunrise and Sunset
def suntimes(latitude, longitude, date=datetime.datetime.now()):
    try:
        ht = acos((sin(Decimal('-0.83')) - sin(Decimal(latitude)) * sin(declination(date)))/ cos(Decimal(latitude)) * cos(declination(date)))
        Jrise = solar_transit(longitude, date) - (ht/Decimal('360')) * Decimal('1.0000000')
        Jset = solar_transit(longitude, date) + (ht / Decimal('360')) * Decimal('1.0000000')
        return (Jrise - Decimal('0.00247222222'), Decimal('0.00247222222') + Jset)
    except:
        return (None, None)


def sunrise(latitude, longitude, date=datetime.datetime.now()):
    try:
        return fromJulian(suntimes(latitude, longitude, date)[0])
    except:
        return None

def sunset(latitude, longitude, date=datetime.datetime.now()):
    try:
        return fromJulian(suntimes(latitude, longitude, date)[1])
    except:
        return None


#12. Horizontal Coordinates
def hour_angle(longitude, date=datetime.datetime.now()):
    return sidereal_time(longitude, date) - right_ascension(date)

def azimuth(latitude, longitude, date=datetime.datetime.now()):
    H = hour_angle(longitude, date)
    dec = declination(date)
    A = atan2(sin(H), cos(H) * sin(latitude) - tan(dec) * cos(latitude))
    return A + Decimal('180')

def altitude(latitude, longitude, date=datetime.datetime.now()):
    H = hour_angle(longitude, date)
    delta = declination(date)
    sinh = sin(delta) * sin(latitude) + cos(delta) * cos(latitude) * cos(H)
    return asin(sinh)


#13. Seasons
def spring():
    date = datetime.datetime(datetime.datetime.now().year, 1, 1)
    for i in range(365):
        if round(ecliptical_longitude(date)) == 0:
            return date - datetime.timedelta(days=1)
        else:
            date += datetime.timedelta(days = 1)

def summer():
    date = datetime.datetime(datetime.datetime.now().year, 1, 1)
    for i in range(365):
        if round(ecliptical_longitude(date)) == 90:
            return date
        else:
            date += datetime.timedelta(days=1)

def autumn():
    date = datetime.datetime(datetime.datetime.now().year, 1, 1)
    for i in range(365):
        if round(ecliptical_longitude(date)) == 180:
            return date - datetime.timedelta(days=1)
        else:
            date += datetime.timedelta(days=1)

def winter():
    date = datetime.datetime(datetime.datetime.now().year, 1, 1)
    for i in range(365):
        if round(ecliptical_longitude(date)) == 270:
            return date
        else:
            date += datetime.timedelta(days=1)

