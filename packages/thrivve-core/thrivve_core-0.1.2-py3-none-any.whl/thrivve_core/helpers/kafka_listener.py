import importlib
import json
import os
import time
import traceback

from confluent_kafka import Consumer

from thrivve_core import ThrivveCore
from thrivve_core.app_decorators import handle_exceptions


def start_kafka_listener(topics):
    """
    Start Kafka listener
    """

    app = ThrivveCore.get_app()

    app.logger.info(f"Start Kafka listen to [{' - '.join(topics)}]..")

    consumer = Consumer(
        {
            "bootstrap.servers": app.config.get("BOOTSTRAP_SERVERS"),
            "sasl.username": app.config.get("SASL_USERNAME"),
            "sasl.password": app.config.get("SASL_PASSWORD"),
            "security.protocol": "SASL_SSL",
            "sasl.mechanisms": "PLAIN",
            "group.id": "services_group",
            "auto.offset.reset": "latest",
        }
    )

    consumer.subscribe(topics)

    try:
        while True:

            msg = consumer.poll(timeout=3)

            if msg is None:
                continue

            if msg.error():
                app.logger.error("error: {0}".format(msg.error()))
                continue

            app.logger.info("Got a message..")

            # message_key = msg.key()
            message_payload = json.loads(msg.value())

            app.logger.debug(message_payload)

            if not message_payload:
                continue

            function_name = message_payload.get("function_name")
            function_params = message_payload.get("function_params")
            if not function_name:
                continue

            @handle_exceptions
            def _execute_method():
                function_file, function_call = os.path.splitext(function_name)
                module = importlib.import_module(function_file)
                method = getattr(module, function_call[1:])

                return method(**function_params)

            function_result = _execute_method()
            app.logger.debug(function_result)

            time.sleep(1)

    except KeyboardInterrupt:
        app.logger.debug("Keyboard interrupted..")
    finally:
        app.logger.error(traceback.format_exc())
        consumer.close()
