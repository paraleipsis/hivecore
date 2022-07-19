import imp
from rest_framework import serializers
import json
from .tasks import redis_instance

class ImageSerializer(serializers.Serializer):
   image = serializers.CharField(required=True)
   node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])
