import csv
import os
from swachh_toilets.models import SwachhToilet
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Process CSV file and Import swachh toilets to DB'

    def add_arguments(self, parser):
        parser.add_argument('input_file', type=str)

    def handle(self, *args, **options):
        input_files = options['input_file']
        absolute_path = os.path.dirname(__file__) + '/' + input_files

        if not os.path.exists(absolute_path):
            raise CommandError(f'{input_files} does not exists')

        self.read_csv(absolute_path)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully imported file {input_files}')
        )

    def read_csv(self, file):
        csvfile = open(file, 'r', encoding="utf8")
        reader = csv.DictReader(csvfile)
        headers = [
                'QCI ID', 'State', 'City', 'Toilet ID', 'Address', 'Category',
                'Open Days', 'Opening Time', 'Closing Time', 'Image',
                'Latitude', 'Longitude', 'Type', 'Seats',
                'Differently Abled Friendly', 'Child Friendly', 'Fee',
                'Cost', 'Gender', 'Category Code', 'Type'
            ]

        for row in reader:
            data = {}
            for header in headers:
                formatted_header = header.lower().replace(' ', '_')
                data[formatted_header] = row[header]

            if SwachhToilet.objects.filter(qci_id=data['qci_id']):
                print(f'Toilet QCI ID: {data["qci_id"]} already indexed')
            else:
                self.save(data)
                print(f'Toilet: {data["qci_id"]} indexed')

    def save(self, data):
        differntly_abled_friedly = False
        if data['differently_abled_friendly'] == 'Yes':
            differntly_abled_friedly = True
        child_friendly = data['child_friendly']

        swachh_toilet = SwachhToilet(
            qci_id=data.get('qci_id', None).strip(),
            toilet_id=data.get('toilet_id').strip(),
            address=data.get('address', None).strip(),
            latitude=float(data.get('latitude').strip()),
            longitude=float(data.get('longitude').strip()),
            location=[
                        float(data.get('longitude').strip()),
                        float(data.get('latitude').strip())
                    ],
            state=data.get('state', None).strip(),
            city=data.get('city', None).strip(),
            category=data.get('category', None).strip(),
            category_code=data.get('category_code', None).strip(),
            type=data.get('type', None).strip(),
            open_days=data.get('open_days').strip(),
            opening_time=str(data['opening_time']).strip(),
            closing_time=str(data['closing_time']).strip(),
            seats=int(data['seats']) if data['seats'] else None,
            gender=data.get('gender').strip(),
            child_friendly=True if child_friendly == 'Yes' else False,
            differntly_abled_friedly=differntly_abled_friedly,
            fee_type=data.get('fee'),
            cost=data['cost'].strip() if data['cost'].strip() != '' else None,
            image=data.get('image', None) if data['image'] != '' else None
            ).save()

        return swachh_toilet
