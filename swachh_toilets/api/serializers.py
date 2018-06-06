from rest_framework_mongoengine import serializers as mongoserializers
from swachh_toilets.utils import (
                today_name_in_short_form,
                haversine
        )
from swachh_toilets.models import SwachhToilet
from rest_framework import serializers


class ToiletSerializer(mongoserializers.DocumentSerializer):
    title = serializers.SerializerMethodField(read_only=True)
    url = serializers.SerializerMethodField(read_only=True)
    picture_url = serializers.SerializerMethodField(read_only=True)
    comments_url = serializers.SerializerMethodField(read_only=True)
    opened = serializers.SerializerMethodField(read_only=True)
    open_hours = serializers.SerializerMethodField(read_only=True)
    opened_from = serializers.SerializerMethodField(read_only=True)
    opened_untill = serializers.SerializerMethodField(read_only=True)
    distance_away = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SwachhToilet
        fields = (
                'id', 'title', 'address', 'latitude', 'longitude',
                'category', 'picture_url', 'opened', 'open_hours',
                'opened_from', 'opened_untill', 'distance_away',
                'url', 'comments_url'
                )

    def get_title(self, obj):
        return obj.title()

    def get_url(self, obj):
        return obj.get_api_url(self.context.get('request'))

    def get_picture_url(self, obj):
        return obj.image

    def get_day_name(self, obj):
        return today_name_in_short_form()

    def get_comments_url(self, obj):
        return obj.get_comments_api_url(self.context.get('request'))

    def get_opened(self, obj):
        return obj.opened_today()

    def get_open_hours(self, obj):
        if obj.opened_today() and obj.opened_all_the_day():
            return '24 Hours'

    def get_opened_from(self, obj):
        return obj.opening_time

    def get_opened_untill(self, obj):
        return obj.closing_time

    def get_distance_away(self, obj):
        request = self.context.get('request')
        latitude = float(request.GET.get('latitude'))
        longitude = float(request.GET.get('longitude'))

        distance = haversine(longitude, latitude, obj.longitude, obj.latitude)
        return str(round(distance, 1)) + ' KM'
