==============================================
Heketi plugin for Rally [benchmarking] project
==============================================

What is it?
===========

This is plugin for `Rally`_ project.

.. _Rally: https://rally.readthedocs.io/en/latest/

With this tool you'll be able to generate load for Heketi, using various
scenarios which create, expand and delete Gluster 'file' and 'block' volumes.

How to use this plugin
======================

Run following command once to create DB instance for Rally project::

    $ tox -e heketi -- rally db create

Then, create deployment for our Heketi plugin::

    $ tox -e heketi -- rally deployment create --name heketi

Now, take some sample from 'samples/' dir, update it according to your needs
and run it using following command::

    $ tox -e heketi -- rally task start scenario-file-name.yaml

For more details read `Rally`_ project docs.
