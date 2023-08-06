import os
from google.cloud import pubsub_v1 as pubsub
import google.api_core.exceptions
from google.cloud.pubsub_v1.subscriber.message import Message
import logging
import json
import traceback


logger = logging.getLogger("whitson tool helper")


class PubsubConsumer:
    def __init__(
        self, process_func, google_project_name, subscription=None, to_dict=False
    ):
        self.decode_json = to_dict
        self.process_func = process_func
        self.subscription = (
            subscription or os.environ["PVT_UTILS_GOOGLE_PUBSUB_SUBSCRIPTION"]
        )
        self.google_project_name = google_project_name
        self.subscriber = pubsub.SubscriberClient()

    @property
    def subscription_path(self):
        if self.subscriber:
            return self.subscriber.subscription_path(
                self.google_project_name, self.subscription
            )
        else:
            raise Exception("Pubsub subscriber not yet instantiated")

    def work(self):
        while True:
            logger.info(f"Pulling subscription {self.subscription_path}")
            try:
                response = self.subscriber.pull(
                    subscription=self.subscription_path, max_messages=1
                )
            except google.api_core.exceptions.DeadlineExceeded as e:
                logger.debug(e)
                continue
            except Exception as e:
                logger.error(e)
                raise
            for received_message in response.received_messages:
                msg = received_message.message
                logger.info(
                    f"Received PubSub message {msg.message_id}",
                    {"pubsub_msg_id": msg.message_id},
                )
                data = json.loads(msg.data.decode("utf8")) if self.decode_json else msg
                try:
                    self.process_func(data)
                except Exception as e:
                    logger.error(e)
                    logger.error(traceback.format_exc())
                    logger.warning(f"ACKING UNPROCESSED MESSAGE: {msg.message_id}")
                else:
                    logger.info(f"ACKING MESSAGE: {msg.message_id}")
                self.subscriber.acknowledge(
                    subscription=self.subscription_path,
                    ack_ids=[received_message.ack_id],
                )

    def process_msg(self, msg: Message):
        try:
            logger.debug(f"Received PubSub message (id: {msg.message_id})")
            data = json.loads(msg.data.decode("utf8")) if self.decode_json else msg
            logger.debug(data)
            self.process_func(data)
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            logger.warning(f"ACKING UNPROCESSED MESSAGE: {msg.message_id}")
            msg.ack()
        else:
            msg.ack()
