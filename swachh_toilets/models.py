from datetime import datetime
from django_mongoengine import Document, fields
from rest_framework.reverse import reverse as api_reverse
from swachh_toilets.utils import (
                today_name_in_short_form,
                week_days_in_short_format
        )


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

    def title(self):
        return 'Swachh Public Toilet'

    def get_api_url(self, request=None):
        return api_reverse(
            "api-public-toilets:detail-toilet",
            kwargs={'pk': str(self.pk)},
            request=request
        )

    def get_comments_api_url(self, request=None):
        return self.get_api_url(request) + '/comments'

    def opened_today(self):
        days = week_days_in_short_format()

        open_days_from_db = self.open_days

        if open_days_from_db == 'Monday to Friday':
            open_days = days[:5]
        if open_days_from_db == 'Monday to Saturday':
            open_days = days[:6]
        elif open_days_from_db == 'Tuesday,Wednesday,Thursday,\
                                    Friday,Saturday,Sunday':
            open_days = days[1:7]
        else:
            open_days = days

        if today_name_in_short_form() in open_days:
            return True

    def opened_all_the_day(self):
        return (self.opening_time == '00:00' and
                self.closing_time == '23:59'
                )


'''
Sample data to insert

 SwachhToilet(qci_id="textss", toilet_id="tessts",
 address="new hdfc", latitude=12.34, longitude=77.34,
 location=[77.34, 12.34], state="Karnataka", city="Bangalore",
 category="Public Toilet", category_code='PTB', type="toilet",
 opening_time="00:00", closing_time="21:00",
 image="test.jpeg").save()
 '''
