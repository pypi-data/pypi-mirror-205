import json
import random
import string
import traceback

from confluent_kafka import Producer as kafka_Producer
from thrivve_core import ThrivveCore


class Producer:
    app = None

    def __init__(self):
        self.app = ThrivveCore.get_app()
        self._producer = (
            None
            if not self.app or self.app.config.get("FLASK_ENV") == "local"
            else kafka_Producer(
                {
                    "sasl.mechanisms": "PLAIN",
                    "request.timeout.ms": 20000,
                    "bootstrap.servers": self.app.config.get("BOOTSTRAP_SERVERS"),
                    "retry.backoff.ms": 500,
                    "sasl.username": self.app.config.get("SASL_USERNAME"),
                    "sasl.password": self.app.config.get("SASL_PASSWORD"),
                    "security.protocol": "SASL_SSL",
                }
            )
        )

    def send_topic(self, topic, datajson):

        if not self.app:
            return True

        self.app.logger.debug(datajson)
        is_test_kafka = self.app.config.get("IS_TEST_KAFKA")

        if is_test_kafka and datajson.get("producer_version") == 2:
            self.app.logger.debug("Test Kafka is enabled")
            try:
                from app.kafka.test import execute
                execute(json.dumps(datajson.get('datajson')))

            except Exception:
                self.app.logger.error(traceback.format_exc())
            return True

        if self._producer is None:
            self.app.logger.debug(
                "Can not send Kafka message, this is {} environment".format(
                    self.app.config.get("FLASK_ENV")
                )
            )
            return True

        def acked(err, msg):
            """Delivery report handler called on
            successful or failed delivery of message
            """
            if err is not None:

                self.app.logger.error("Failed to deliver message: {0}".format(err))

            else:
                self.app.logger.debug(
                    "Produced record to topic {0} partition [{1}] @ offset {2}".format(
                        msg.topic(), msg.partition(), msg.offset()
                    )
                )
                # is_success = True

        # record_key = "alice"
        record_key = str(random.choices(string.digits, k=5))

        self._producer.produce(
            topic, key=record_key, value=json.dumps(datajson), on_delivery=acked
        )
        self._producer.poll(0)
        self._producer.flush()

        return True
