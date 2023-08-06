# <h1 style='color:purple'>Solarflare</h1>

The purpose of this code is to provide a set of functions and a class, named Daystar, to facilitate calculations related to the position of the sun in the sky, such as the sunrise and sunset times, the position of the sun in the ecliptic and equatorial coordinates, the sidereal time, and the hour angle. The code imports two standard Python modules, math and datetime, to perform the necessary calculations. The code is intended to be used in formal settings where precise astronomical calculations are required, such as in scientific research or engineering applications. The Daystar class provides a convenient interface for performing multiple calculations related to the position of the sun at a given location, allowing the user to specify the latitude, longitude, and optionally, the height above sea level. You may modify the code and/or create pull requests, but you must grant the same permission to others, and include an [MIT license](https://opensource.org/license/mit/) with it.

PLEASE NOTE: THIS HAS BEEN A QUESTION ASKED MANY, MANY TIMES!! IF YOU SEE A SUNSET/RISE TIME THAT LOOKS IMPOSSIBLE, IT IS BECAUSE IT IS IN YOUR LOCAL TIME!!

## Documentation
### Descriptions of Functions (at solarflare.py)
- `sin(x)`, `cos(x)`, `tan(x)`, `acos(x)`, `asin(x)`, `atan2(y, x)`: these functions provide trigonometric operations in degrees rather than radians. 

- `julian_date(date=datetime.datetime.now())`: calculates the Julian date of a given date and time. The Julian date is the number of days since noon (12:00) on January 1, 4713 BCE, in the Julian calendar.

- `mean_anomaly(date=datetime.datetime.now())`: calculates the mean anomaly of the Sun for a given date and time. The mean anomaly is the angular distance between the perihelion (the point in the orbit of a planet or other celestial body where it is closest to the Sun) and the current position of the planet or body (in this case earth) in its orbit, measured in degrees.

- `equation(date=datetime.datetime.now())`: calculates the equation of center, which is the difference between the true anomaly (the angle between the perihelion and the current position of the planet or body in its orbit, measured at the Sun) and the mean anomaly. This is used in the calculation of the ecliptical coordinates.

- `true_anomaly(date=datetime.datetime.now())`: calculates the true anomaly of the Sun for a given date and time, taking into account the equation of center.

- `ecliptical_longitude(date=datetime.datetime.now())`: calculates the ecliptical longitude of the Sun for a given date and time. The ecliptical longitude is the angular distance between the vernal equinox (the point on the celestial sphere where the ecliptic intersects the celestial equator, corresponding to the position of the Sun at the spring equinox) and the current position of the Sun in its orbit, measured in degrees.

- `declination(date=datetime.datetime.now())`: calculates the declination of the Sun for a given date and time. The declination is the angular distance between the equator and the current position of the Sun in the sky, measured in degrees.

- `right_ascension(date=datetime.datetime.now())`: calculates the right ascension of the Sun for a given date and time. The right ascension is the angular distance between the vernal equinox and the current position of the Sun in the sky, measured in degrees.

- `sidereal_time(longitude, time=datetime.datetime.now())`: calculates the sidereal time for a given longitude and date and time. The sidereal time is the time elapsed since the vernal equinox, measured in hours.

- `solar_transit(longitude, date=datetime.datetime.now())`: calculates the Julian date of the solar transit (the moment when the Sun is at its highest point in the sky) for a given longitude and date and time.

- `suntimes(latitude, longitude, date=datetime.datetime.now())`: calculates the Julian dates of sunrise and sunset for a given latitude, longitude, and date and time.

- `sunrise(latitude, longitude, date=datetime.datetime.now())`: returns the date and time of sunrise for a given latitude, longitude, and date and time.

- `sunset(latitude, longitude, date=datetime.datetime.now())`: returns the date and time of sunset for a given latitude, longitude, and date and time.

- `hour_angle(longitude, date=datetime.datetime.now())`: calculates the hour angle of the Sun for a given longitude and date and time. 

