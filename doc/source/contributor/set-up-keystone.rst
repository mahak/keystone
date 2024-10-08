..
      Copyright 2011-2012 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

.. _dev-environment:

===================
Setting up Keystone
===================

Prerequisites
=============

This document assumes you are using an Ubuntu, Fedora, or openSUSE platform and
that you have the following tools pre-installed on your system:

- python_ 3.11 or later, as the programming language;
- git_, as the version control tool;

.. NOTE::

    Keystone dropped the support of python_ 2.7 in the Ussuri release of Openstack.

**Reminder**: If you are successfully using a different platform, or a
different version of the above, please document your configuration here!

.. _git: http://git-scm.com/

Installing from source
======================

The source install instructions specifically avoid using platform specific
packages. Instead, we recommend using the source for the code and the Python
Package Index (PyPi_) for development environment installations..

.. _PyPi: https://pypi.org/project/pypi

It's expected that your system already has python_, pip_, and git_ available.

.. _python: http://www.python.org
.. _pip: http://www.pip-installer.org/en/latest/installing.html
.. _git: http://git-scm.com/

Clone the keystone repository:

.. code-block:: bash

    $ git clone https://opendev.org/openstack/keystone.git
    $ cd keystone

Prepare dedicated virtual environment (python 3.11 is used here as an example.
Please use any supported version)

.. code-block:: bash

   $ tox -e py311 --notest
   $ source .tox/py311/bin/activate

.. NOTE::

    This step is guaranteed to fail if you do not have the proper binary
    dependencies already installed on your development system. Maintaining a
    list of platform-specific dependencies is outside the scope of this
    documentation, but is within scope of DEVSTACK_.

.. _DEVSTACK: https://docs.openstack.org/devstack/latest

Development environment
=======================

For setting up the Python development environment and running `tox` testing
environments, please refer to the `Project Team Guide: Python Project Guide`_,
the OpenStack guide on wide standard practices around the use of Python.

That documentation will help you configure your development environment and run
keystone tests using `tox`, which uses virtualenv_ to isolate the Python
environment. After running it, notice the existence of a `.tox` directory.

.. _`Project Team Guide: Python Project Guide`: https://docs.openstack.org/project-team-guide/project-setup/python.html
.. _virtualenv: http://www.virtualenv.org/

Deploying configuration files
=============================

You should be able to run keystone after installing via pip. Additional
configuration files are required. The following file is required in order to
run keystone:

* ``keystone.conf``

Configuring Keystone with a sample file
---------------------------------------

Keystone requires a configuration file. Keystone's sample configuration file
``etc/keystone.conf.sample`` is automatically generated based upon all of the
options available within Keystone. These options are sourced from the many
files around Keystone as well as some external libraries.

The sample configuration file will be updated as the end of the development
cycle approaches. Developers should *NOT* generate the config file and propose
it as part of their patches, this will cause unnecessary conflicts.
You can generate one locally using the following command:

.. code-block:: bash

    $ tox -e genconfig

The tox command will place an updated sample config in ``etc/keystone.conf.sample``.
The defaults are enough to get you going, but you can make any changes if
needed.

If there is a new external library (e.g. ``oslo.messaging``) that utilizes the
``oslo.config`` package for configuration, it can be added to the list of libraries
found in ``config-generator/keystone.conf``.

You can also generate sample policy files using ``tox -e genpolicy``. Please refer
to :doc:`../configuration/config-options` for guidance on specific configuration options or to
view a sample paste file.

Bootstrapping a test deployment
===============================

By default an internal sqlite database can be used for local development. Under
certain conditions (i.e. when exception is being raised during runtime) sqlite
switches into the read only mode. After restart it is working again. It is
therefore suggested to use real mysql or postgresql database instead.

Database setup
--------------

Dedicated mysql/postgresql database can be prepared using the script
``tools/test-setup.sh``. In such case be sure to set ``[database].connection``
option in the ``etc/keystone.conf`` file properly.

Initializing Keystone
---------------------

Before using keystone, it is necessary to create the database tables and ensure
the database schemas are up to date. This is can be done as following:

.. code-block:: bash

    $ keystone-manage db_sync

If the above commands result in a ``KeyError``, or they fail on a
``.pyc`` file with the message, ``You can only have one Python script per
version``, then it is possible that there are out-of-date compiled Python
bytecode files in the Keystone directory tree that are causing problems. This
can occur if you have previously installed and ran older versions of Keystone.
These out-of-date files can be easily removed by running a command like the
following from the Keystone root project directory:

.. code-block:: bash

    $ find . -name "*.pyc" -delete


Once the database itself is prepared use to command ``keystone-manage db_sync``
to create necessary objects in a database.

You can use the ``keystone-manage bootstrap`` command to pre-populate the
database with necessary data. It requires ``--bootstrap-password`` parameter to
be given with the password for the admin user.

Initial Sample Data
-------------------

There is an included script which is helpful in setting up some initial sample
data for use with keystone:

.. code-block:: bash

    $ ADMIN_PASSWORD=s3cr3t tools/sample_data.sh

Once run, you can see the sample data that has been created by using the
`python-openstackclient`_ command-line interface:

.. code-block:: bash

    $ export OS_USERNAME=admin
    $ export OS_PASSWORD=s3cr3t
    $ export OS_PROJECT_NAME=admin
    $ export OS_USER_DOMAIN_ID=default
    $ export OS_PROJECT_DOMAIN_ID=default
    $ export OS_IDENTITY_API_VERSION=3
    $ export OS_AUTH_URL=http://localhost:5000/v3
    $ openstack user list

The `python-openstackclient`_ can be installed using the following:

.. code-block:: bash

    $ pip install python-openstackclient

Verifying keystone is set up
----------------------------

Once set up, you should be able to invoke Python and import the libraries:

.. code-block:: bash

    $ .tox/py311/bin/python -c "import keystone"

If you can import keystone without a traceback, you should be ready to move on
to the next sections.


Running Keystone
----------------

You can run keystone using a host of wsgi implementations or web servers. The
following uses ``uwsgi`` (you may first need to install uwsgi for example with
``pip install uwsgi``):

.. code-block:: bash

    $ uwsgi --http-socket :5000 -w "keystone.server.wsgi:initialize_public_application()"

This runs Keystone with the configuration the etc/ directory of the project.
See :doc:`../configuration/config-options` for details on how Keystone is
configured. By default, Keystone is configured with SQL backends.

Depending on use case (i.e. there is an apache webserver deploed in front of
the Keystone to be able to test the federation setup) it may be required to
also expose wsgi socket in the uwsgi (i.e. adding ``-s :5001 -b 65535`` runtime
options).

Interacting with Keystone
=========================

You can also interact with keystone through its REST API. There is a Python
keystone client library `python-keystoneclient`_ which interacts exclusively
through the REST API, and a command-line interface `python-openstackclient`_
command-line interface.

.. _`python-keystoneclient`: https://opendev.org/openstack/python-keystoneclient
.. _`python-openstackclient`: https://opendev.org/openstack/python-openstackclient
