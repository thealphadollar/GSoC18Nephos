from tests.base import BaseTestCase

class TestControllers(BaseTestCase):
  def test_root(self):
    """
    Test the root
    """
    response = self.app.test_client().get('/')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, b'Hello World!')

  def test_channels_view(self):
    """
    Test if Channel works properly
    """
    response = self.app.test_client().get('/channels')
    self.assertEqual(response.status_code, 200)
    self.assert_template_used('channels.html')

  def test_channels_api(self):
    """
    Test if Channel works properly
    """
    d = [
  {
    "channel_id": 1,
    "name": "tve1",
    "ip": "239.255.20.1:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 2,
    "name": "la_2",
    "ip": "239.255.20.2:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 3,
    "name": "antena_3",
    "ip": "239.255.20.3:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 4,
    "name": "cuatro",
    "ip": "239.255.20.4:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 5,
    "name": "tele_5",
    "ip": "239.255.20.5:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 6,
    "name": "la_sexta",
    "ip": "239.255.20.6:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 7,
    "name": "intereconomia",
    "ip": "239.255.20.7:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 8,
    "name": "tve_24horas",
    "ip": "239.255.20.8:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 9,
    "name": "marca_tv",
    "ip": "239.255.20.9:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 10,
    "name": "navarra_tv",
    "ip": "239.255.20.10:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 11,
    "name": "navarra_tv2",
    "ip": "239.255.20.11:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 12,
    "name": "xplora",
    "ip": "239.255.20.12:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 13,
    "name": "13tv",
    "ip": "239.255.20.13:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 14,
    "name": "bbc_world_news",
    "ip": "239.255.20.14:1234",
    "country_code": "spa",
    "lang": "eng",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 15,
    "name": "cnn_international",
    "ip": "239.255.20.15:1234",
    "country_code": "spa",
    "lang": "eng",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 16,
    "name": "al_jazzeera",
    "ip": "239.255.20.16:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 17,
    "name": "france_24",
    "ip": "239.255.20.17:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 18,
    "name": "russia_today",
    "ip": "239.255.20.18:1234",
    "country_code": "spa",
    "lang": "rus",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 19,
    "name": "cctv",
    "ip": "239.255.20.19:1234",
    "country_code": "spa",
    "lang": "spa",
    "timezone": "spa",
    "status": "up"
  },
  {
    "channel_id": 20,
    "name": "bloomberg_europe",
    "ip": "239.255.20.20:1234",
    "country_code": "EU",
    "lang": "eng",
    "timezone": "spa",
    "status": "up"
  }
]
    response = self.app.test_client().get('/channels')
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, d)