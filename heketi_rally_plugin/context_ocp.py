import os

from openshift import config as ocp_config
from rally.common import logging
from rally import consts as rally_consts
from rally import exceptions
from rally.task import context

from heketi_rally_plugin import client_ocp

CONTEXT_NAME = "ocp_client"
LOG = logging.getLogger(__name__)


@context.configure(name=CONTEXT_NAME, order=1000)
class OCPClientContext(context.Context):
    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": rally_consts.JSON_SCHEMA,
        "additionalProperties": False,
        "properties": {
            "config_path": {
                "type": "string",
            },
        }
    }

    DEFAULT_CONFIG = {
        "config_path": "~/.kube/config",
    }

    def setup(self):
        ocp_config.load_kube_config(
            os.path.expanduser(self.config.get("config_path")))
        client = client_ocp.OCPClient()
        try:
            if client.list_node():
                self.context["ocp_client"] = client
                LOG.debug("Successfully connected to the OCP server.")
                return
            msg = "Failed to connect to the OCP server."
        except Exception as e:
            msg = "Can't connect to the OCP server: %s" % e.message
            if logging.is_debug():
                LOG.exception(msg)
            else:
                LOG.warning(msg)
        raise exceptions.ContextSetupFailure(ctx_name=CONTEXT_NAME, msg=msg)

    def cleanup(self):
        LOG.debug("Nothing to cleanup in OCP client context. Exiting.")
