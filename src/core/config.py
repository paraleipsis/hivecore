import json
import os

from dotenv import load_dotenv

load_dotenv()

PUBSUB_CHANNELS = json.loads(os.environ.get("PUBSUB_CHANNELS"))
