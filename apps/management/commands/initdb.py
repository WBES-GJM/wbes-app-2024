from typing import List, Dict
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
            {'id': 10, 'username': 'john', 'password': 'Pass123$'},
            {'id': 11, 'username': 'mary', 'password': 'Pass123$'}
        ],
        Company:[
            {'id': 1, 'user': 'john', 'company': 'KMS Inc.', 'street_number_company':'95', 'street_name_company': 'Speed', 'city_company': 'Lightning', 'state_company': 'McQueen', 'zip_company': '250', 'main_phone_company': '250', 'home_phone_company': '250', 'main_email_company': 'iamspeed@mcqueen.com', 'timestamp': datetime.now()},
            {'id': 2, 'user': 'john', 'company': 'KYS RN Universe', 'street_number_company':'12', 'street_name_company': 'Tref', 'city_company': 'Acer', 'state_company': 'Gas', 'zip_company': '421', 'main_phone_company': '412', 'home_phone_company': '531', 'main_email_company': 'iamspeed@yours.com', 'timestamp': datetime.now()},
        ],
        Employee: [
            {'id': 1, 'user': 'john', 'company': 'KMS Inc.', 'name_prefix_employee': 'Ms.', 'last_name_employee': 'Sample', 'middle_name_employee': 'Mars', 'first_name_employee': 'Kim', 'job_title_employee': 'Staff', 'timestamp': datetime.now()},
            {'id': 2, 'user': 'john', 'company': 'KYS RN Universe', 'name_prefix_employee': 'Mr.', 'last_name_employee': 'Santa', 'middle_name_employee': 'Yranus', 'first_name_employee': 'Kevin', 'job_title_employee': 'Staff', 'timestamp': datetime.now()},
        ],
        Owner: [
            {'id': 1, 'user': 'john', 'company': 'KMS Inc.', 'name_prefix_owner': 'Mr.', 'last_name_owner': 'Saints', 'middle_name_owner': 'Maer', 'first_name_owner': 'Kimberly', 'timestamp': datetime.now() },
            {'id': 2, 'user': 'john', 'company': 'KYS RN Universe', 'name_prefix_owner': 'Ms.', 'last_name_owner': 'Saens', 'middle_name_owner': 'Yajger', 'first_name_owner': 'Karlson', 'timestamp': datetime.now() },
        ],
        Virtual: [
            {'id': 1, 'user': 'john', 'package': 'Gold'},
            {'id': 2, 'user': 'john', 'package': 'Silver'},
            {'id': 3, 'user': 'john', 'package': 'Bronze'},
        ],
        Client: [
            # The EMPLOYEE unique identifier is set to [lastname]-[middlename]-[firstname]
            {'id': 1, 'user':'john', 'name' : 'KMS Holdings' , 'employee':'Sample-Mars-Kim', 'owner': 'Saints-Maer-Kimberly', 'company': 'KMS Inc.', 'virtual': 'Gold', },
            {'id': 2, 'user':'john', 'name' : 'The KYS Group' , 'employee':'Santa-Yranus-Kevin', 'owner': 'Saens-Yajger-Karlson', 'company': 'KYS RN Universe', 'virtual': 'Silver',  },
        ],
        Building:[
            {'id': 1, 'name':'Santa Ana Suites Extension Building', 'address': '92nd Block, Santa Ana, California'},
            {'id': 2, 'name':'IKEA Hotel', 'address': '69th Will, This Ever, Come True'},
        ],
        ConferenceRoom: [
            {'id': 1, 'name': 'Grande Room', 'building': 'Santa Ana Suites Extension Building'},
            {'id': 2, 'name': 'Meeting Room', 'building': 'Santa Ana Suites Extension Building'},
            {'id': 3, 'name': 'Staffs Room', 'building': 'IKEA Hotel', 'max_capacity': 50},
            {'id': 4, 'name': 'Executives Room', 'building': 'IKEA Hotel', 'seating_capacity': 8},
        ],
        Booking: [
            # The ROOM unique identifier is set to [name]-[building]
            {'id': 1, 'client': 'KMS Holdings', 'room': 'Executives Room-IKEA Hotel', 'start_datetime': datetime.now().replace(hour=9)},
            {'id': 2,'client': 'The KYS Group', 'room': 'Executives Room-IKEA Hotel', 'start_datetime': datetime.now().replace(hour=15) + timedelta(days=2), 'end_datetime': datetime.now().replace(hour=15) + timedelta(days=3)},
            {'id': 3,'client': 'The KYS Group', 'room': 'Grande Room-Santa Ana Suites Extension Building', 'start_datetime': datetime.now().replace(hour=17), 'end_datetime': datetime.now().replace(hour=11) + timedelta(days=10)},
        ],
    }

    def handle(self, *args, **options):
        self._create_test_data()

    def _create_test_data(self):
        """Create test users and their related objects."""

        for m, d  in self.TEST_DATA.items():
            model: models.Model = m
            data: List[Dict] = d

            replace_all = False

            for obj_dict in data:
                
                new_obj: models.Model = model()
                save = True
                with_id = False

                for fname, value in obj_dict.items():
                    if not model._meta.get_field(fname):
                        continue
                    with_id = fname == 'id' or with_id
                    
                    if fname == 'user':
                        value = User.objects.get(username=value)
                    elif fname == 'employee':
                        name = value.split('-')
                        value = Employee.objects.get(
                            last_name_employee=name[0], 
                            middle_name_employee=name[1], 
                            first_name_employee=name[2]
                        )
                    elif fname == 'owner':
                        name = value.split('-')
                        value = Owner.objects.get(
                            last_name_owner=name[0], 
                            middle_name_owner=name[1], 
                            first_name_owner=name[2]
                        )
                    elif fname == 'client':
                        value = Client.objects.get(name=value)
                    elif fname == 'company' and model is not Company:
                        value = Company.objects.get(company=value)
                    elif fname == 'building':
                        value = Building.objects.get(name=value)
                    elif fname == 'room':
                        rname = value.split('-')
                        value = ConferenceRoom.objects.get(name=rname[0], building__name=rname[1])
                    elif fname == 'virtual':
                        value = Virtual.objects.get(package=value)
                    setattr(new_obj, fname, value)
                    print(f'Added new {model._meta.model_name}' )
                        
                if replace_all or not with_id:
                    new_obj.save()
                    continue

                existing_obj = self._validate_obj(new_obj)
                while existing_obj:
                    ans = self._duplicate_ask(new_obj)
                    if  ans == 'r' or ans == 'replace':
                        break
                    elif ans == 'ra':
                        replace_all = True
                        break
                    elif ans ==  'i' or ans == 'ignore':
                        save = False
                        break

                if save:
                    new_obj.save()

    def _validate_obj(self, new_obj: models.Model) -> models.Model:
        model = new_obj._meta.model
        existing_obj = None
        try:
            existing_obj: models.Model = model.objects.get(unique_identifier=new_obj.unique_identifier)
        except AttributeError:
            try:
                existing_obj: models.Model = model.objects.get(id=new_obj.pk)
            except model.DoesNotExist:
                return None
        return existing_obj

    def _duplicate_ask(self, new_obj: models.Model) -> bool:
        model = new_obj._meta.model
        ans = input('Duplicate object with the same name found in model: ' + model._meta.model_name \
                        + '.\nWhat would you like to do for this record? '\
                        + '[replace/ignore - r/i] (or if you want to replace all duplicates, enter [ra]): ')
        return ans