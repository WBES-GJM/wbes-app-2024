'''
This file includes all custom helper functions
'''

import calendar, json, typing
from django.db.models import Q
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect, JsonResponse
from django.db import models


class JsonResponseHelper():
    
    @staticmethod
    def error(message):
        pass
    
    @staticmethod
    def serialize(model_instance: models.Model, mode: str='simple'):
        if mode == 'simple':
            return {'id': model_instance.pk, 'name': str(model_instance)}
        elif mode == 'all':
            pass
        else:
            pass
    
class ModelInstanceGetter():
    
    @staticmethod
    def get_instance(model: models.Model, instance_id: int):
        try:
            return model.objects.get(id=instance_id)
        except model.DoesNotExist:
            return None
        
    def search_instance(model: models.Model, fields: typing.List[typing.Tuple[str, type]]):
        pass