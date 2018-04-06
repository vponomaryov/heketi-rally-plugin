from rally.common import logging
from rally import consts as rally_consts
from rally import exceptions
from rally.task import context

from heketi_rally_plugin import client as heketi_client

CONTEXT_NAME = "heketi_client"
LOG = logging.getLogger(__name__)


@context.configure(name=CONTEXT_NAME, order=1000)
class HeketiClientContext(context.Context):
    CONFIG_SCHEMA = {
        "type": "object",
        "$schema": rally_consts.JSON_SCHEMA,
        "additionalProperties": False,
        "properties": {
            "server": {
                "type": "string",
            },
            "username": {
                "type": "string",
            },
            "secret": {
                "type": "string",
            },
        }
    }

    def setup(self):
        client = heketi_client.HeketiClient(
            host=self.config.get("server"),
            user=self.config.get("username"),
            key=self.config.get("secret"),
        )
        try:
            if client.hello():
                self.context["heketi_client"] = client
                LOG.debug("Successfully connected to the Heketi server.")
                return
            msg = "Failed to connect to the Heketi server."
        except Exception as e:
            msg = "Can't connect to the Heketi server: %s" % e.message
            if logging.is_debug():
                LOG.exception(msg)
            else:
                LOG.warning(msg)
        raise exceptions.ContextSetupFailure(ctx_name=CONTEXT_NAME, msg=msg)

    def cleanup(self):
        LOG.debug("Nothing to cleanup in Heketi client context. Exiting.")
