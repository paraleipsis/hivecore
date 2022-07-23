from cgi import print_form
from requests import request
from rest_framework import serializers
import json
from .tasks import redis_instance

class ImageSerializer(serializers.Serializer):
   image = serializers.CharField(required=True)
   node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])


class BuildImageSerializer(serializers.Serializer):
   tag = serializers.CharField(required=False)
   dockerfile_path = serializers.FileField(required=False)
   dockerfile_field = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
   node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])

   def validate(self, data):
      dockerfile_path = data.get('dockerfile_path', None)
      dockerfile_field = data.get('dockerfile_field', None)
      if not dockerfile_path and not dockerfile_field:
         raise serializers.ValidationError("specify Dockerfile")

      return data


class ContainerSerializer(serializers.Serializer):
   container_id = serializers.CharField(required=True)


class CreateContainerSerializer(serializers.Serializer):
   # main
   name = serializers.CharField(required=False)
   image = serializers.CharField(required=True)
   ports = serializers.CharField(required=False)

   # for agent
   node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])

   # container settings

   # login
   command = serializers.CharField(required=False)
   entrypoint = serializers.CharField(required=False)
   working_dir = serializers.CharField(required=False)
   stdin_open = serializers.BooleanField(required=False)
   tty = serializers.BooleanField(required=False)

   # volumes
   volumes = serializers.CharField(required=False)

   # network
   net = [net['items']['Name'] for net in json.loads(redis_instance.get('/networks'))['result']]
   net_id = [net['items']['Id'] for net in json.loads(redis_instance.get('/networks'))['result']]
   host = [net['host'] for net in json.loads(redis_instance.get('/networks'))['result']]
   NET_CHOISES = [':'.join(list(a)) for a in zip(net, host, net_id)]
   NET_CHOISES.insert(0, "None")

   network = serializers.ChoiceField(required=True, choices=NET_CHOISES)
   hostname = serializers.CharField(required=False)
   domainname = serializers.CharField(required=False)
   mac_address = serializers.CharField(required=False)
   ipv4_address = serializers.CharField(required=False)
   ipv6_address = serializers.CharField(required=False)

   # env
   environment = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   # labels
   labels = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   # restart
   restart_policy = serializers.ChoiceField(choices=['no', 'on-failure', 'always', 'unless-stopped'])


class NetworkSerializer(serializers.Serializer):
   network_id = serializers.CharField(required=True)


class CreateNetworkSerializer(serializers.Serializer):
   name = serializers.CharField(required=True)
   node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])
   driver = serializers.ChoiceField(required=False, choices=['bridge', 'overlay'])
   options = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   # ipv4 config
   subnet = serializers.CharField(required=False)
   gateway = serializers.CharField(required=False)

   def validate(self, data):
      subnet = data.get('subnet', None)
      gateway = data.get('gateway', None)

      driver = data.get('driver', None)
      options = data.get('options', None)

      if gateway and not subnet:
         raise serializers.ValidationError("specify subnet")

      if options and not driver:
         raise serializers.ValidationError("specify driver")

      return data

   labels = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
   scope = serializers.ChoiceField(required=False, choices=['local', 'global', 'swarm'])
   internal = serializers.BooleanField(required=False)