from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.db import models
from django.contrib.auth.models import User
from apps.models import (
    Employee, Client, Company, Owner,
    ConferenceRoom, Booking, Building, Virtual
)

class Command(BaseCommand):
    # args = '<foo bar ...>'
    # help = 'our help string comes here'

    TEST_DATA = {
        User: [ # should have a 'john' user
            {'username': 'john', 'password': 'Pass123$', 'email': 'john@example.com'},
            {'username': 'mary', 'password': 'Pass123$', 'email': 'mary@example.com'}
        ],
        Company:[
            {'user': 'john', 'company': 'KMS Inc.', 'street_number_company':'95', 'street_name_company': 'Speed', 'city_company': 'Lightning', 'state_company': 'McQueen', 'zip_company': '250', 'main_phone_company': '250', 'home_phone_company': '250', 'main_email_company': 'iamspeed@mcqueen.com'},
            {'user': 'john', 'company': 'KYS RN Universe', 'street_number_company':'12', 'street_name_company': 'Tref', 'city_company': 'Acer', 'state_company': 'Gas', 'zip_company': '421', 'main_phone_company': '412', 'home_phone_company': '531', 'main_email_company': 'iamspeed@yours.com'},
        ],
        Employee: [
            {'user': 'john', 'company': 'KMS Inc.', 'name_prefix_employee': 'Ms.', 'last_name_employee': 'Sample', 'middle_name_employee': 'Mars', 'first_name_employee': 'Kim', 'job_title_employee': 'Staff',},
            {'user': 'john', 'company': 'KYS RN Universe', 'name_prefix_employee': 'Mr.', 'last_name_employee': 'Santa', 'middle_name_employee': 'Yranus', 'first_name_employee': 'Kevin', 'job_title_employee': 'Staff',},
        ],
        Owner: [
            {'user': 'john', 'company': 'KMS Inc.', 'name_prefix_owner': 'Mr.', 'last_name_owner': 'Saints', 'middle_name_owner': 'Maer', 'first_name_owner': 'Kimberly', },
            {'user': 'john', 'company': 'KYS RN Universe', 'name_prefix_owner': 'Ms.', 'last_name_owner': 'Saens', 'middle_name_owner': 'Yajger', 'first_name_owner': 'Karlson', },
        ],
        Virtual: [
            {'user': 'john', 'package': 'Gold'},
            {'user': 'john', 'package': 'Silver'},
            {'user': 'john', 'package': 'Bronze'},
        ],
        Client: [
            # The EMPLOYEE unique identifier is set to [lastname]-[middlename]-[firstname]
            {'users':'john', 'name' : 'KMS Holdings' , 'employee':'Sample-Mars-Kim', 'owner': 'Saints-Maer-Kimberly', 'company': 'KMS Inc.', 'virtual': 'Gold',},
            {'users':'john', 'name' : 'The KYS Group' , 'employee':'Santa-Yranus-Kevin', 'owner': 'Saens-Yajger-Karlson', 'company': 'KYS RN Universe', 'virtual': 'Silver',},
        ],
        Building:[
            {'name':'Santa Ana Suites Extension Building', 'address': '92nd Block, Santa Ana, California'},
            {'name':'IKEA Hotel', 'address': '69th Will, This Ever, Come True'},
        ],
        ConferenceRoom: [
            {'name': 'Grande Room', 'building': 'Santa Ana Suites Extension Building'},
            {'name': 'Meeting Room', 'building': 'Santa Ana Suites Extension Building'},
            {'name': 'Staffs Room', 'building': 'IKEA Hotel', 'max_capacity': 50},
            {'name': 'Executives Room', 'building': 'IKEA Hotel', 'seating_capacity': 8},
        ],
        Booking: [
            # The ROOM unique identifier is set to [name]-[building]
            {'client': 'KMS Holdings', 'room': 'Executives Room-IKEA Hotel', 'start_datetime': datetime.now().replace(hour=9)},
            {'client': 'The KYS Group', 'room': 'Executives Room-IKEA Hotel', 'start_datetime': datetime.now().replace(hour=15) + timedelta(days=2), 'end_datetime': datetime.now().replace(hour=15) + timedelta(days=3)},
            {'client': 'The KYS Group', 'room': 'Grande Room-Santa Ana Suites Extension Building', 'start_datetime': datetime.now().replace(hour=17), 'end_datetime': datetime.now().replace(hour=11) + timedelta(days=10)},
        ],
    }

    def handle(self, *args, **options):
        self._create_test_data()


    def _create_test_data(self):
        """Create test users and their related objects."""

        for m, d  in self.TEST_DATA.items():
            model: models.Model = m
            data: list = d
            # TODO
            for obj_dict in data:
                try:
                    if model == models.User or   model == models.Booking:
                        user = getattr(models, model.__name__).objects.get_or_create(**obj_dict)
                except:
                    pass



    def _assert_test(self, data:dict, models_to_populate: list):
        for data_model in data.keys():
            assert data_model in models_to_populate, \
                'Consider checking the models you want to populate.'