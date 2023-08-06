import abc
import logging
from hashlib import sha256

import pkg_resources
import subprocess
import koji


log = logging.getLogger('robosignatory.utils')


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


def get_rpms(koji_client, build_nvr, build_id, sigkey=None):
    rpms = koji_client.listRPMs(build_id)
    rpminfo = {}
    for rpm in rpms:
        info = {'id': rpm['id']}
        if sigkey:
            sigs = koji_client.queryRPMSigs(rpm_id=rpm['id'],
                                            sigkey=sigkey)
            info['signed'] = len(sigs) != 0
        rpminfo['{}.{}'.format(rpm['nvr'], rpm['arch'])] = info
    return rpminfo


def get_builds_in_tag(koji_client, tag):
    """ Return the list of builds in Koji tag. """

    try:
        rpms, builds = koji_client.listTaggedRPMS(tag, latest=True)
    except koji.GenericError:
        log.exception("Failed to list rpms in tag %r" % tag)
        # If the tag doesn't exist.. then there are no rpms in that tag.
        return []

    return builds


def run_command(command):
    child = subprocess.Popen(
        command,  # noqa: S603
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    stdout, stderr = child.communicate()
    ret = child.wait()
    return ret, stdout, stderr


def get_hash(filepath):
    hasher = sha256()
    with open(filepath, "rb") as f:
        while True:
            content = f.read(1024)
            if not content:
                break
            hasher.update(content)
    return hasher.hexdigest()


def get_signing_helper(backend, *args, **kwargs):
    """ Instantiate and return the appropriate signing backend. """
    points = pkg_resources.iter_entry_points('robosignatory.signing.helpers')
    classes = dict([(point.name, point.load()) for point in points])
    log.debug("Found the following installed signing helpers %r" % classes)
    cls = classes[backend]
    log.debug(f"Instantiating helper {cls!r} from backend key {backend!r}")
    return cls(*args, **kwargs)


class BaseSigningHelper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def build_cmdline(self, *args):
        pass

    @abc.abstractmethod
    def build_sign_cmdline(self, *args):
        pass

    @abc.abstractmethod
    def build_atomic_cmdline(self, *args):
        pass

    @abc.abstractmethod
    def build_coreos_cmdline(self, *args):
        pass

    @abc.abstractmethod
    def build_xml_cmdline(self, *args):
        pass


class EchoHelper(BaseSigningHelper):
    """ A dummy "hello world" helper, used for debugging. """
    def __init__(self, *args, **kwargs):
        log.info(f"Constructing EchoHelper({args!r}, {kwargs!r})")

    def build_cmdline(self, *args, **kwargs):
        result = ['echo', ' '.join(['build_cmdline:', str(args), str(kwargs)])]
        log.info(result)
        return result

    def build_sign_cmdline(self, *args, **kwargs):
        result = ['echo', ' '.join(['build_sign_cmdline:', str(args), str(kwargs)])]
        log.info(result)
        return result

    def build_atomic_cmdline(self, *args, **kwargs):
        result = ['echo', ' '.join(['build_atomic_cmdline:', str(args), str(kwargs)])]
        log.info(result)
        return result

    def build_coreos_cmdline(self, *args, **kwargs):
        result = ['echo', ' '.join(['build_coreos_cmdline:', str(args), str(kwargs)])]
        log.info(result)
        return result

    def build_xml_cmdline(self, *args, **kwargs):
        result = ['echo', ' '.join(['build_xml_cmdline:', str(args), str(kwargs)])]
        log.info(result)
        return result


class SigulHelper(BaseSigningHelper):
    def __init__(self, user, passphrase_file, config_file=None,
                 file_signing_key_passphrase_file=None):
        self.user = user
        self.passphrase_file = passphrase_file
        self.config_file = config_file
        self.file_signing_key_passphrase_file = file_signing_key_passphrase_file

    def build_cmdline(self, *args):
        cmdline = ['sigul', '--batch', '--user-name', self.user,
                   '--passphrase-file', self.passphrase_file]
        if self.config_file:
            cmdline.extend(["--config-file", self.config_file])
        cmdline.extend(args)
        return cmdline

    def build_sign_cmdline(self, key, rpms, koji_instance=None,
                           file_signing_key=None):
        if len(rpms) == 1:
            sigul_cmd = "sign-rpm"
        else:
            sigul_cmd = "sign-rpms"

        command = self.build_cmdline(sigul_cmd, '--store-in-koji',
                                     '--koji-only')
        if koji_instance:
            command.extend(['-k', koji_instance])

        if file_signing_key:
            log.debug('Adding file signing key: %s', file_signing_key)
            if not self.file_signing_key_passphrase_file:
                raise Exception("No passphrase file for file signing key configured")
            command.extend([
                '--file-signing-key', file_signing_key,
                '--file-signing-key-passphrase-file',
                self.file_signing_key_passphrase_file,
            ])

        # TODO: See if this always needs to be set or optional
        # if self.v3:
        command.append('--v3-signature')

        command.append(key)

        return command + rpms

    def build_atomic_cmdline(self, key, checksum, input_file, output_file):
        command = self.build_cmdline('sign-ostree', '--output', output_file,
                                     '--', key, checksum, input_file)
        return command

    def build_coreos_cmdline(self, key, input_file, output_file):
        command = self.build_cmdline('sign-data', '--output', output_file, '--',
                                     key, input_file)
        return command

    def build_xml_cmdline(self, key, input_file, output_file):
        command = self.build_cmdline('sign-data', '--output', output_file, '--',
                                     key, input_file)
        return command
