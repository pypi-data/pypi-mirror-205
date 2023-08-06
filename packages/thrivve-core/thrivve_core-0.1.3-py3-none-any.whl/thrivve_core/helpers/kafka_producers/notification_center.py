import platform
from datetime import datetime

from thrivve_core import ThrivveCore
from thrivve_core.helpers.topics import Topics
from thrivve_core.helpers import kafka_producers


def send_critical_error(message, channel=None):
    channel = channel or "critical-errors"
    send_notification_message(
        channel=channel,
        title="critical",
        color="#df0000",
        message=message,
        emoji=":pleading_face:"
    )


def send_notification_message(
        message, channel="logs", title="Log", color="#32a4a7", emoji=":dizzy_face:"
):
    app = ThrivveCore.get_app()
    channel = "eng-{0}-{1}".format(
        app.config.get("FLASK_ENV")
        if app.config.get("FLASK_ENV") == "production"
        else "development",
        channel,
    )
    datetime_now = datetime.now().strftime("%Y-%m-%d %H:%M")
    message = "Node: {0}\nEnv:{3}\nDate: {1}\n{2}".format(
        platform.node(), datetime_now, message, str(app.config.get("FLASK_ENV"))
    )
    data = {
        "notification_method": "slack",
        "payload": {
            "channel": channel,
            "title": "New {0} in {1} Service".format(
                title, str(app.config.get("SERVICE_NAME"))
            ),
            "text": message,
            "color": color,
            "icon_emoji": emoji,
        },
    }
    app.logger.debug(data)
    kafka_producers.send_topic(topic=Topics.INTERNAL_NOTIFICATION_MESSAGE, datajson=data)



def send_push_notification(
        message, reference_type, user_ids, payload=None, created_by=None
):
    # token = None
    base_payload = dict(
        content_available=True,
        delay_while_idle=False,
        time_to_live=3,
        priority="high",
        sound="sound1",
        title="Thrivve",
        body=message,
        message=message,
        result=payload,
    )
    if payload:
        base_payload.update(payload)

    data = dict(
        message=message,
        reference_type=reference_type,
        user_ids=user_ids,
        payload=base_payload,
        created_by=created_by,
        # language="ar"
    )

    kafka_producers.send_topic(topic=Topics.THRIVVE_SEND_PUSH_NOTIFICATION, datajson=dict(
        function_name='app.business_logic.notification.send_push_notification.execute',
        function_params=data
    ))
