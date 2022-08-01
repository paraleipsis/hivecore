from email.policy import default
from random import choices
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

   network_plugins = json.loads(redis_instance.get('/status'))['result'][0]['items']['Plugins']['Network']
   driver = serializers.ChoiceField(required=False, choices=network_plugins)
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


class VolumesSerializer(serializers.Serializer):
   volume_id = serializers.CharField(required=True)


class CreateVolumeSerializer(serializers.Serializer):
   name = serializers.CharField(required=True)
   node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])

   volume_plugins = json.loads(redis_instance.get('/status'))['result'][0]['items']['Plugins']['Volume']
   driver = serializers.ChoiceField(required=False, choices=volume_plugins)
   driver_opts = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   labels = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)


class ConfigsSerializer(serializers.Serializer):
   config_name = serializers.CharField(required=True)


class CreateConfigSerializer(serializers.Serializer):
   name = serializers.CharField(required=True)
   node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])

   data_path = serializers.FileField(required=False)
   data_field = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   def validate(self, data):
      data_path = data.get('data_path', None)
      data_field = data.get('data_field', None)
      if not data_path and not data_field:
         raise serializers.ValidationError("specify config")

      return data

   labels = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)


class SecretsSerializer(serializers.Serializer):
   secret_name = serializers.CharField(required=True)


class CreateSecretSerializer(serializers.Serializer):
   name = serializers.CharField(required=True)
   node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])

   data_path = serializers.FileField(required=False)
   data_field = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   def validate(self, data):
      data_path = data.get('data_path', None)
      data_field = data.get('data_field', None)
      if not data_path and not data_field:
         raise serializers.ValidationError("specify secret")

      return data

   labels = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)


class ServicesSerializer(serializers.Serializer):
   service_name = serializers.CharField(required=True)


class CreateServiceSerializer(serializers.Serializer):
   service_name = serializers.CharField(required=True)
   # node = serializers.ChoiceField(required=True, choices=[node['host'] for node in json.loads(redis_instance.get('/nodes'))['result']])

   image = serializers.CharField(required=True)

   ports = serializers.CharField(required=False)

   # replicated mode
   scheduling_mode = serializers.ChoiceField(choices=['replicated', 'global'])
   replicas = serializers.IntegerField(min_value=1, required=False, default=1, initial=1)

   # login
   hostname = serializers.CharField(required=False)
   working_dir = serializers.CharField(required=False)
   open_stdin = serializers.BooleanField(required=False)
   tty = serializers.BooleanField(required=False)

   # volumes
   container_path = serializers.CharField(required=False) # path in container
   VOL_CHOISES = [net['items']['Name'] for net in json.loads(redis_instance.get('/volumes'))['result']]
   VOL_CHOISES.insert(0, "None")
   volume = serializers.ChoiceField(choices=VOL_CHOISES, required=False) # volume name
   read_only = serializers.BooleanField(required=False)

   # network
   NET_CHOISES = [net['items']['Name'] for net in json.loads(redis_instance.get('/networks'))['result']]
   NET_CHOISES.insert(0, "None")
   networks = serializers.MultipleChoiceField(choices=NET_CHOISES, required=False, style={'base_template': 'checkbox_multiple.html'})

   # env
   environment = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   # labels
   labels = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   secret = [net['items']['Spec']['Name'] for net in json.loads(redis_instance.get('/secrets'))['result']]
   secret_id = [net['items']['ID'] for net in json.loads(redis_instance.get('/secrets'))['result']]
   SEC_CHOISES = [':'.join(list(a)) for a in zip(secret, secret_id)]
   secrets = serializers.MultipleChoiceField(choices=SEC_CHOISES, style={'base_template': 'checkbox_multiple.html'}, required=False)

   config = [net['items']['Spec']['Name'] for net in json.loads(redis_instance.get('/configs'))['result']]
   config_id = [net['items']['ID'] for net in json.loads(redis_instance.get('/configs'))['result']]
   CONF_CHOISES = [':'.join(list(a)) for a in zip(config, config_id)]
   configs = serializers.MultipleChoiceField(choices=CONF_CHOISES, style={'base_template': 'checkbox_multiple.html'}, required=False)

   # restart policy
   restart_condition = serializers.ChoiceField(choices=['none', 'on-failure', 'any'])
   restart_delay = serializers.IntegerField(min_value=0, required=False, default=5, initial=5)
   max_attempts = serializers.IntegerField(min_value=0, required=False, default=0, initial=0)
   restart_window = serializers.IntegerField(min_value=0, required=False, default=0, initial=0)

   # update config
   update_parallelism = serializers.IntegerField(min_value=0, required=False, default=1, initial=1)
   update_delay = serializers.IntegerField(min_value=0, required=False, default=0, initial=0)
   failure_action = serializers.ChoiceField(choices=['continue', 'pause'])
   update_order = serializers.ChoiceField(choices=['start-first', 'stop-first'])