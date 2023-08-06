import os
import time

from google.cloud import pubsub_v1
import json
import logging

logger = logging.getLogger("whitson tool helper")


class PubsubProducer:
    def __init__(self, project_id=None, topic=None):
        self.publisher = pubsub_v1.PublisherClient()
        self.project_id = project_id
        self.topic = topic or os.environ["GOOGLE_PUBSUB_TOPIC"]
        self.futures = set()

    @property
    def topic_name(self):
        return "projects/{project_id}/topics/{topic}".format(
            project_id=self.project_id,
            topic=self.topic,
        )

    def get_callback(self, f, data):
        def callback(f):
            try:
                logging.debug(f.result())
                self.futures.remove(f)
            except:  # noqa
                logging.error("Please handle {} for {}.".format(f.exception(), data))

        return callback

    def publish(self, payload: dict, encode_json=True, **kwargs):
        logger.debug(f"Publishing to pubsub")
        payload = json.dumps(payload).encode("utf8") if encode_json else payload
        future = self.publisher.publish(self.topic_name, payload, **kwargs)
        self.futures.add(future)
        # Publish failures shall be handled in the callback function.
        future.add_done_callback(self.get_callback(future, payload))
        # Wait for all the publish futures to resolve before exiting.
        while self.futures:
            time.sleep(1)
