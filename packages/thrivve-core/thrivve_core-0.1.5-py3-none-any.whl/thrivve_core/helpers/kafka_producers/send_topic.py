from thrivve_core.helpers.kafka_producer import Producer


def send_topic(topic, producer_version=2, **kwargs):
    kwargs.update(producer_version=producer_version)

    Producer().send_topic(topic, kwargs)
