from rest_framework import serializers
import json
from django.conf import settings

redis_instance = settings.REDIS_INSTANCE

def get_choices(docker_object):
   try:
      if docker_object in ('network_plugins', 'volume_plugins'):
         endpoint = json.loads(redis_instance.get('/status'))
      else:
         endpoint = json.loads(redis_instance.get(docker_object))['result']
   except TypeError:
      return ''
   else:
      if docker_object == '/nodes':
         return [node['host'] for node in endpoint if node['items']['Status']['State'] == 'ready']
      elif docker_object == 'network_plugins':
         return endpoint['result'][0]['items']['Plugins']['Network']
      elif docker_object == 'volume_plugins':
         return endpoint['result'][0]['items']['Plugins']['Volume']
      elif docker_object == '/volumes':
         volumes = [vol['items']['Name'] for vol in endpoint]
         volumes.insert(0, "None")
         return volumes
      elif docker_object == '/networks':
         net_name = [net['items']['Name'] for net in endpoint]
         net_id = [net['items']['Id'] for net in endpoint]
         net_host = [net['host'] for net in endpoint]
         net_choices = [':'.join(list(a)) for a in zip(net_name, net_host, net_id)]
         net_choices.insert(0, "None")
         return net_choices
      elif docker_object == '/secrets':
         secret_name = [sec['items']['Spec']['Name'] for sec in endpoint]
         secret_id = [sec['items']['ID'] for sec in endpoint]
         secret_choices = [':'.join(list(a)) for a in zip(secret_name, secret_id)]
         secret_choices.insert(0, "None")
         return secret_choices
      elif docker_object == '/configs':
         config_name = [conf['items']['Spec']['Name'] for conf in endpoint]
         config_id = [conf['items']['ID'] for conf in endpoint]
         config_choices = [':'.join(list(a)) for a in zip(config_name, config_id)]
         config_choices.insert(0, "None")
         return config_choices


class ImageSerializer(serializers.Serializer):
   image = serializers.CharField(required=True)
   node = serializers.ChoiceField(required=True, choices=get_choices('/nodes'))


class BuildImageSerializer(serializers.Serializer):
   tag = serializers.CharField(required=False)
   dockerfile_path = serializers.FileField(required=False)
   dockerfile_field = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)
   node = serializers.ChoiceField(required=True, choices=get_choices('/nodes'))

   def validate(self, data):
      dockerfile_path = data.get('dockerfile_path', None)
      dockerfile_field = data.get('dockerfile_field', None)
      if not dockerfile_path and not dockerfile_field:
         raise serializers.ValidationError("specify Dockerfile")

      return data


class ContainerSerializer(serializers.Serializer):
   container_id = serializers.CharField(required=True)
   container_ip = serializers.CharField(required=True)
   container_signal = serializers.CharField(required=True)
   force = serializers.BooleanField(required=False)


class CreateContainerSerializer(serializers.Serializer):
   # main
   name = serializers.CharField(required=False)
   image = serializers.CharField(required=True)
   ports = serializers.CharField(required=False)

   # for agent
   node = serializers.ChoiceField(required=True, choices=get_choices('/nodes'))

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
   

   network = serializers.ChoiceField(required=True, choices=get_choices('/networks'))
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
   node = serializers.ChoiceField(required=True, choices=get_choices('/nodes'))

   driver = serializers.ChoiceField(required=False, choices=get_choices('network_plugins'))
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
   node = serializers.ChoiceField(required=True, choices=get_choices('/nodes'))

   driver = serializers.ChoiceField(required=False, choices=get_choices('volume_plugins'))
   driver_opts = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   labels = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)


class ConfigsSerializer(serializers.Serializer):
   config_name = serializers.CharField(required=True)


class CreateConfigSerializer(serializers.Serializer):
   name = serializers.CharField(required=True)
   node = serializers.ChoiceField(required=True, choices=get_choices('/nodes'))

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
   node = serializers.ChoiceField(required=True, choices=get_choices('/nodes'))

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
   # node = serializers.ChoiceField(required=True, choices=get_choices('/nodes'))

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
   volume = serializers.ChoiceField(choices=get_choices('/volumes'), required=False) # volume name
   read_only = serializers.BooleanField(required=False)

   # network
   networks = serializers.MultipleChoiceField(choices=get_choices('/networks'), required=False, style={'base_template': 'checkbox_multiple.html'})

   # env
   environment = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   # labels
   labels = serializers.CharField(style={'base_template': 'textarea.html'}, required=False)

   secrets = serializers.MultipleChoiceField(choices=get_choices('/secrets'), style={'base_template': 'checkbox_multiple.html'}, required=False)

   configs = serializers.MultipleChoiceField(choices=get_choices('/configs'), style={'base_template': 'checkbox_multiple.html'}, required=False)

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