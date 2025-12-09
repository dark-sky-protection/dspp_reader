import astropy.units as u
import datetime

from astropy.time import Time
from astropy.coordinates import EarthLocation
from pytz import timezone as tz
from astroplan import Observer

class Site(object):
    def __init__(self,id, name, latitude, longitude, elevation, timezone,):
        self.id = id
        self.name = name
        self.latitude = latitude * u.deg
        self.longitude = longitude * u.deg
        self.elevation = elevation * u.m
        self.timezone = timezone
        self.location = EarthLocation.from_geodetic(self.longitude, self.latitude, self.elevation)
        self.observer = Observer(
            name=self.name,
            location=self.location,
            timezone=tz(self.timezone),
            description=self.name)

    def get_time_range(self):
        now = Time(datetime.datetime.now(datetime.UTC))
        # now = Time("2024-12-02 09:00:00")
        reference_time = now
        next_sunset = self.observer.sun_set_time(reference_time, which='next', horizon=-10 * u.deg)
        next_sunrise = self.observer.sun_rise_time(reference_time, which='next', horizon=-10 * u.deg)
        time_to_sunset = next_sunset - now
        time_to_sunrise = next_sunrise - now
        return next_sunset, next_sunrise, time_to_sunset, time_to_sunrise
