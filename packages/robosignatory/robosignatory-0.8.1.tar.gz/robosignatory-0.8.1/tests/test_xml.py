import logging
from unittest import mock

from fedora_messaging.api import Message
from fedora_messaging.testing import mock_sends

from robosignatory.xml import XMLSigner


TEST_CONFIG = {
    "signing": {
        "backend": "echo",
    },
    "koji_instances": {},
    "ostree_refs": {},
    "xml": {
        'key': 'testing',
    },
}

XML_MESSAGE = Message(
    topic="org.fedoraproject.prod.robosignatory.xml-sign",
    body='<?xml version="1.0" encoding="UTF-8"?>')

INVALID_MESSAGE = Message(
    topic="org.fedoraproject.prod.robosignatory.xml-sign",
    body='\0<?xml version="1.0" encoding="UTF-8"?>')


class TestXML:

    def setup_method(self):
        self.consumer = XMLSigner(TEST_CONFIG)

    def _get_response_message(self, source_msg, failed=False, failure_msg="Signing failed", sig=""):
        body = {
            'body': source_msg.body,
            'error': failure_msg,
        } if failed else {
            'body': source_msg.body,
            'signature': sig,
        }
        return Message(
            topic=source_msg.topic + ".finished",
            body=body
        )

    @mock.patch('robosignatory.xml.utils.run_command')
    def test_xml_sign(self, run_command):
        run_command.return_value = 0, "", ""
        expected_response = self._get_response_message(XML_MESSAGE, failed=True)
        with mock_sends(expected_response):
            self.consumer.consume(XML_MESSAGE)
        run_command.assert_called()

    @mock.patch('robosignatory.xml.utils.run_command')
    def test_wrong_xml(self, run_command):
        run_command.return_value = 0, "", ""
        expected_response = self._get_response_message(
            INVALID_MESSAGE,
            failed=True,
            failure_msg='Refusing to sign object that does not start with XML declaration'
        )
        with mock_sends(expected_response):
            self.consumer.consume(INVALID_MESSAGE)
        run_command.assert_not_called()

    @mock.patch('robosignatory.coreos.utils.run_command')
    def test_signing_failed(self, run_command):
        run_command.return_value = 1, "stdout", "stderr"
        expected_response = self._get_response_message(XML_MESSAGE, failed=True)
        with mock_sends(expected_response):
            self.consumer.consume(XML_MESSAGE)

        run_command.assert_called()

    @mock.patch('robosignatory.coreos.utils.run_command')
    def test_no_signature(self, run_command):
        run_command.return_value = 0, "stdout", "stderr"
        expected_response = self._get_response_message(XML_MESSAGE, failed=True)

        with mock_sends(expected_response):
            self.consumer.consume(XML_MESSAGE)

        run_command.assert_called()

    @mock.patch('robosignatory.xml.utils.run_command')
    def test_wrong_topic(self, run_command, caplog):
        """Test message with an unsupported topic"""
        caplog.set_level(logging.DEBUG)
        msg = Message(topic="something.unrelated", body={})
        self.consumer.consume(msg)
        assert len(caplog.records) == 0
        run_command.assert_not_called()

    def test_disabled(self):
        assert XMLSigner.is_enabled({}) is False
