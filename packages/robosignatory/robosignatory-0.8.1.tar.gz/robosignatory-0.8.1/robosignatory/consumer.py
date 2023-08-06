import logging

import fedora_messaging

from .tag import TagSigner
from .atomic import AtomicSigner
from .coreos import CoreOSSigner
from .xml import XMLSigner


log = logging.getLogger('robosignatory')


class Consumer:
    """All messages are received by this class's __call__() method."""

    def __init__(self):
        log.info('Initializing Robosignatory consumer')
        self.config = fedora_messaging.config.conf["consumer_config"]
        self.handlers = []
        for handler_class in (TagSigner, AtomicSigner, CoreOSSigner, XMLSigner):
            if handler_class.is_enabled(self.config):
                self.handlers.append(handler_class(self.config))

    def __call__(self, msg):
        """
        Callback method called by fedora-messaging consume.

        The handlers decide whether they want to process the message.

        In case of duplicate messages, robosignatory will just try to re-sign
        the object, which will have no effect (except wasted cyles but that
        should not be a major problem).

        Args:
            msg (fedora_messaging.api.Message): The message received from the broker.
        """
        log.info('Received message from fedora-messaging with topic: %s', msg.topic)

        try:
            for handler in self.handlers:
                handler.consume(msg)
        except Exception as e:
            error_msg = f'{e}: Unable to handle message: {msg}'
            log.exception(error_msg)
            raise fedora_messaging.exceptions.Nack(error_msg) from e
