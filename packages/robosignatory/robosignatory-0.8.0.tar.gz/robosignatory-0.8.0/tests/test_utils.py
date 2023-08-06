import unittest

from pytest import raises

import robosignatory.utils


class TestUtils(unittest.TestCase):

    def test_no_such_helper(self):
        with raises(KeyError):
            robosignatory.utils.get_signing_helper(backend='wat', )

    def test_get_sigul_helper(self):
        helper = robosignatory.utils.get_signing_helper(
            backend='sigul',
            user='ralph',
            passphrase_file='/tmp/wide-open.txt',
        )
        assert type(helper) == robosignatory.utils.SigulHelper
        assert helper.file_signing_key_passphrase_file is None

    def test_get_sigul_helper_with_fsk(self):
        helper = robosignatory.utils.get_signing_helper(
            backend='sigul',
            user='ralph',
            passphrase_file='/tmp/wide-open.txt',
            file_signing_key_passphrase_file='/tmp/wide-closed.txt',
        )
        assert type(helper) == robosignatory.utils.SigulHelper
        assert helper.file_signing_key_passphrase_file == '/tmp/wide-closed.txt'

    def test_simple_echo_helper(self):
        helper = robosignatory.utils.get_signing_helper(
            backend='echo',
            user='ralph',
            passphrase_file='/tmp/wide-open.txt',
        )
        cmdline = helper.build_cmdline('wat')
        assert cmdline == ["echo", "build_cmdline: ('wat',) {}"]

    def test_simple_echo_helper_with_fsk(self):
        helper = robosignatory.utils.get_signing_helper(
            backend='echo',
            user='ralph',
            passphrase_file='/tmp/wide-open.txt',
            file_signing_key_passphrase_file='/tmp/wide-closed.txt',
        )
        cmdline = helper.build_cmdline('wat')
        assert cmdline == ["echo", "build_cmdline: ('wat',) {}"]
