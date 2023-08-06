import os
import logging
import shutil
import tempfile

import robosignatory.utils as utils
from fedora_messaging.api import Message, publish


log = logging.getLogger(__name__)


class XMLSigner:

    __slots__ = ('_signer', '_tmpdir', '_key')

    def __init__(self, config):
        self._signer = utils.get_signing_helper(**config['signing'])
        # Disabling S108 below is OK because self._tmpdir is a top directory
        # where the actual temporary directory will be created with mkdtemp.
        self._tmpdir = '/tmp'  # noqa: S108
        for k, v in config['xml'].items():
            if k == 'tmpdir' and type(v) is str:
                self._tmpdir = v
            elif k == 'key' and type(v) is str:
                self._key = v
            else:
                raise Exception(f'Bad config entry {(k, v)!r}')
        if not hasattr(self, '_key'):
            raise Exception('Key must be specified')
        log.info('XMLSigner ready for service')

    def _sign_object(self, msg, tmpdir):
        input_file = os.path.join(tmpdir, 'input')
        output_file = os.path.join(tmpdir, 'output')
        with open(input_file, 'wb') as f:
            f.write(msg.encode('ascii', 'strict'))
        cmdline = self._signer.build_xml_cmdline(self._key, input_file, output_file)
        ret, stdout, stderr = utils.run_command(cmdline)
        if ret != 0:
            raise Exception(
                'Error signing! Signing output: {}, stdout: '
                '{!r}, stderr: {!r}'.format(ret, stdout, stderr)
            )
        with open(output_file, 'rb') as f:
            signature = f.read().decode('ascii', 'strict')
        log.info('XML file was successfully signed')
        return signature

    def _error(self, msg, error):
        publish(Message(
            topic=f"{msg.topic}.finished",
            # respond with the same body
            body={'body': msg.body, 'error': str(error)}
        ))

    def consume(self, msg):
        log.info('Punji and/or bodhi wants to sign an XML file')

        if type(msg.body) is not str:
            return self._error(msg, 'Refusing to sign non-string')
        # Security check: we must use the same key for signing packages and
        # metadata, but being authorized to sign metadata does not necessarily
        # grant authorization to sign packages.  This check enforces this.
        #
        # RPM packages have two possible signatures: one over just the main
        # header, and one over both the main header and the payload.  RPM checks
        # that the main header header begins with
        # b"\x8e\xad\xe8\x01\x00\x00\x00\x00", so we’re in the clear: it is
        # not possible to abuse this endpoint to sign an RPM.
        if not msg.body.startswith('<?xml version="1.0" '):
            return self._error(msg, 'Refusing to sign object that does not '
                                    'start with XML declaration')
        tmpdir = tempfile.mkdtemp(dir=self._tmpdir,
                                  prefix="robosignatory-")
        try:
            signature = self._sign_object(msg.body, tmpdir)
        except Exception as e:
            log.error(e)
            return self._error(msg, 'Signing failed')
        finally:
            shutil.rmtree(tmpdir)
        publish(Message(
            topic=f"{msg.topic}.finished",
            # respond with the same body
            body={'body': msg.body, 'signature': signature}
        ))
