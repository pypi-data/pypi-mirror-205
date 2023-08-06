from unittest import mock

import pytest
from fedora_messaging.api import Message
from fedora_messaging.exceptions import Nack

from robosignatory.consumer import Consumer


TEST_CONFIG = {
    "signing": {
        "backend": "echo",
    },
    "koji_instances": {},
    "ostree_refs": {},
    "coreos": {
        "bucket": "testing",
        "key": "testing",
        "aws": {
            "access_key": "testing",
            "access_secret": "testing",
            "region": "us-east-1",
        }
    },
    "xml": {
        "key": "testing",
    }
}


@mock.patch.dict(
    "robosignatory.consumer.fedora_messaging.config.conf",
    {"consumer_config": TEST_CONFIG}
)
class TestConsumers:

    def test_message_handler(self):
        msg = Message(topic="dummy.topic", body={})
        consumer = Consumer()
        handler = mock.Mock()
        consumer.handlers.append(handler)
        consumer(msg)
        handler.consume.assert_called_once_with(msg)

    @mock.patch('robosignatory.consumer.log.exception')
    def test_message_exception(self, error):
        """Test catching an exception when processing messages."""
        msg = mock.Mock()
        # Ensure msg.topic.endswith() throws an exception right away, this way
        # we can forgo mocking out handlers or similar complications.
        msg.topic = None

        with pytest.raises(Nack) as exc:
            Consumer()(msg)

        msg = ("'NoneType' object has no attribute 'endswith': "
               "Unable to handle message: {}".format(msg))
        error.assert_called_once_with(msg)
        assert str(exc.value) == msg

    @mock.patch.dict(
        "robosignatory.consumer.fedora_messaging.config.conf",
        {"consumer_config": {}}
    )
    def test_consumers_disabled(self):
        consumer = Consumer()
        assert len(consumer.handlers) == 0
