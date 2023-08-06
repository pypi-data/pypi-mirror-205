=============
robosignatory
=============

A Fedora Messaging consumer that automatically signs artifacts.

RoboSignatory is composed of multiple consumers:

- TagSigner listens for tags into a specific koji tag, then signs the build and
  moves it to a different koji tag.
- AtomicSigner listens for messages about composed rpmostree trees and signs
  those, optionally updating the tag.
- CoreOSSigner listens for requests to sign CoreOS artefacts, downloads them
  from AWS S3, signs them, and uploads the signature back to S3.

The configuration file should be placed in
``/etc/fedora-messaging/robosignatory.toml`` (see the provided
``robosignatory.toml`` file in this repository for an example).
The part specific to RoboSignatory is in the ``[consumer_config]`` section.

Then the listening service can be activated and started with::

    # systemctl enable fm-consumer@robosignatory.service
    # systemctl start fm-consumer@robosignatory.service


Development
-----------

Run the tests with::

    $ tox

Signing Configuration
---------------------

The only generic part in the configuration is the signing part, for the other
options please check the parts below in this document.

For signing, the one argument you always provide is "backend".
This is the name of a robosignatory.signing.helpers setuptools entry point.

Pre-shipped are "echo" and "sigul".

The other arguments in this section are passed as keyword arguments to the
helper's ``__init__`` method, so are specific for the module you choose to use.


Koji Tag Signer
---------------

You will need to add all the koji "instances" your setup should be aware
of under the ``koji_instances`` section. The url is the link to the kojihub
main url of the instance.

Options contains authentication information.
There are two authmethods available:

- ssl, which takes arguments cert and serverca (both required).
- kerberos, which takes arguments principal, keytab and ccache (all optional).

In the tags part of the instance configuration is the real configuration for
the TagSigner.

It is a list, with each entry being a dict with the tag that should be watched,
a key name (passed to the signing module to indicate which key to use) and
keyid (passed to koji to indicate which signatures need to be written out).
The entry also has a "to" tag, to indicate where builds need to be moved to
after being signed. Each entry can have an optional dict "sidetags" which
specify how a side tag for the respective release and its corresponding "from"
and "to" tags would look like, as well as which Koji users are trusted to ask
RoboSignatory to sign such builds ("trusted_taggers", a list of strings).

Note that "from" and "to" can be the same tag, in this case builds will not be
moved after being signed.

Example:
::
  {
    "from": "f26-pending",
    "to": "f26",
    "key": "fedora-26",
    "keyid": "64dab85d",
    "sidetags": {
        "pattern": "<to>-build-side-<seq_id>",
        "from": "<sidetag>-pending-signing",
        "to": "<sidetag>-testing",
        "trusted_taggers": ["bodhi"]
    }
  }

This example would watch for any builds tagged into the f26-pending tag.
After it sees a build tagged in this tag, it will look up which RPMs need to be
signed, and pass their names together with the koji instance name and key name
to the signing module.

After the signing module acknowledges that it signed the packages, robosignatory
will tell koji to write the signed RPMs out with the keyid.
If that is done and the "from" tag is different from the "to" tag, it will
issue a koji moveBuild operation, moving the build from "f26-pending" to "f26".
After this, it is done signing the package, and continues to the next step.

Analogously, it would work for a side tag build which was e.g. tagged into
"f26-build-side-1234-pending-signing" and move it into
"f26-build-side-1234-testing".


Testing Koji Tag Signer
-----------------------

To test the configuration, you can create the full configuration, and run the
``robosignatory sign-tag`` command, providing the name of the koji instance, the
build NVR and the current tag, and whether or not to skip the tag moving.
This will follow the exact same procedures as outlined in the previous section,
printing a lot of information along the way so you can follow what it's doing
exactly.
