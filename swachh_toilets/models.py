from datetime import datetime
from django_mongoengine import Document, fields


class SwachhToilet(Document):

    qci_id = fields.StringField(max_length=100, unique=True)
    toilet_id = fields.StringField(max_length=100, unique=True)
    address = fields.StringField()
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    location = fields.PointField()
    state = fields.StringField(blank=True)
    city = fields.StringField()
    category = fields.StringField(blank=True)
    category_code = fields.StringField(blank=True)
    type = fields.StringField(blank=True)
    opening_time = fields.StringField(blank=True)
    closing_time = fields.StringField(blank=True)
    open_days = fields.StringField(default='All Seven Days')
    seats = fields.IntField(default=0)
    gender = fields.StringField(default='Gents and Ladies')
    child_friendly = fields.BooleanField(default=False)
    differntly_abled_friedly = fields.BooleanField(default=False)
    fee_type = fields.StringField(default='Free of Charge')
    cost = fields.StringField(blank=True)
    image = fields.StringField(blank=True)
    timestamp = fields.DateTimeField(default=datetime.now)
    comments = fields.ListField(fields.DictField(), blank=True, default=None)

    meta = {
        'collection': 'swachh_toilets'
    }

    def __str__(self):
        return self.qci_id


'''
Sample data to insert

 SwachhToilet(qci_id="textss", toilet_id="tessts",
 address="new hdfc", latitude=12.34, longitude=77.34,
 location=[77.34, 12.34], state="Karnataka", city="Bangalore",
 category="Public Toilet", category_code='PTB', type="toilet",
 opening_time="00:00", closing_time="21:00",
 image="test.jpeg").save()
 '''
