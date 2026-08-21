from astropy.time import Time, TimeDelta
from freezegun import freeze_time
from unittest import TestCase

from dspp_reader.tools.site import Site


class TestSite(TestCase):
    site_id = 'site'
    name = 'My Site'
    latitude = -30.169166
    longitude = -70.804
    elevation = 2174.
    timezone = 'America/Santiago'
    sun_altitude = -10

    site = Site(id=site_id,
                name=name,
                latitude=latitude,
                longitude=longitude,
                elevation=elevation,
                timezone=timezone)

    def test_site_attributes(self):
        self.assertEqual(self.site.id, self.site_id)
        self.assertEqual(self.site.name, self.name)
        self.assertAlmostEqual(self.site.latitude.value, self.latitude, places=3)
        self.assertAlmostEqual(self.site.longitude.value, self.longitude, places=3)
        self.assertEqual(self.site.elevation.value, self.elevation)
        self.assertEqual(self.site.timezone, self.timezone)

    @freeze_time("2026-08-20 12:00:00", tz_offset=0)
    def test_get_time_range(self):

        next_period_start, next_period_end, time_to_next_start, time_to_next_end = self.site.get_time_range(
            sun_altitude=self.sun_altitude)

        self.assertIsInstance(next_period_start, Time)
        self.assertIsInstance(next_period_end, Time)
        self.assertIsInstance(time_to_next_start, TimeDelta)
        self.assertIsInstance(time_to_next_end, TimeDelta)
