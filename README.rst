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

Useful utilities
================

Bunch of Ansible playbooks is available for doing following actions:

- Restart VMWare VMs
- Restart 'glusterd' services
- Disable and enable Heketi node
- Disable and enable Heketi device

Examples of commands to run these playbooks:

1) Restart of VMWare VMs::

    $ tox -e ansible -- ansible-playbook \
        -e vcenter_host='vcenter-hostname' \
        -e vcenter_username='someUserName' \
        -e vcenter_password='someCoolPassword' \
        -e vcenter_vm_names="nodename1,nodename2" \
        -e vm_downtime_in_seconds=13 \
        ansible-playbooks/vmware-vms-restart.yaml

2) Restart 'glusterd' services::

    $ tox -e ansible -- ansible-playbook \
        -i "username@hostname,hostname2" \
        -e downtime_in_seconds=3 \
        ansible-playbooks/glusterd-restart.yaml 

3) Disable Heketi node::

    $ tox -e ansible -- ansible-playbook \
        -i username@hostname, \
        -e heketi_server=http://hostname:8080 \
        -e heketi_user=admin \
        -e heketi_secret=admin \
        -e heketi_node_id=FooNodeID \
        ansible-playbooks/heketi-node-disable.yaml

4) Enable Heketi node::

    $ tox -e ansible -- ansible-playbook \
        -i username@hostname, \
        -e heketi_server=http://hostname:8080 \
        -e heketi_user=admin \
        -e heketi_secret=admin \
        -e heketi_node_id=FooNodeID \
        ansible-playbooks/heketi-node-enable.yaml

5) Disable Heketi device::

    $ tox -e ansible -- ansible-playbook \
        -i "username@hostname," \
        -e heketi_server=http://hostname:8080 \
        -e heketi_user=admin \
        -e heketi_secret=admin \
        -e heketi_device_id=FooDeviceID \
        ansible-playbooks/heketi-device-disable.yaml

6) Enable Heketi device::

    $ tox -e ansible -- ansible-playbook \
        -i "username@hostname," \
        -e heketi_server=http://hostname:8080 \
        -e heketi_user=admin \
        -e heketi_secret=admin \
        -e heketi_device_id=FooDeviceID \
        ansible-playbooks/heketi-device-enable.yaml

