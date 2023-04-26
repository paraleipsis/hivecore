# in cycle:

# 1. listen to PubSub Channel anf receive object of UUID and SSH Channel to connect;

# 2. establish STREAM connection to WS router on Reverse SSH Server that in turn
# should establish a WebSocket connection to hivecore-agent aiohttp server to report
# application by some endpoint;

# 3. receive data;

# 4. Kafka Stream - Faust: send received data to appropriate topics.
