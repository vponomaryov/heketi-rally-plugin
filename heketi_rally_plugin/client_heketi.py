try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
import sys

import heketi
from rally.common import logging


http_client.HTTPConnection.debuglevel = 1
LOG = logging.getLogger(__name__)


class StdoutLogger(object):
    def write(self, message):
        if message.strip():
            LOG.debug(message)

    def flush(self):
        return


stdout_logger = StdoutLogger()


def wrap_sys_stdout(f):
    def wrapped_f(*args, **kwargs):
        sys.stdout = stdout_logger
        result = f(*args, **kwargs)
        sys.stdout = sys.__stdout__
        return result
    return wrapped_f


class HeketiClient(heketi.HeketiClient):
    """Extend original Heketi client with API calls verbose logging."""

    bv_uri = '/blockvolumes'

    @wrap_sys_stdout
    def volume_create(self, *args, **kwargs):
        return super(HeketiClient, self).volume_create(*args, **kwargs)

    @wrap_sys_stdout
    def volume_list(self, *args, **kwargs):
        return super(HeketiClient, self).volume_list(*args, **kwargs)

    @wrap_sys_stdout
    def volume_info(self, *args, **kwargs):
        return super(HeketiClient, self).volume_info(*args, **kwargs)

    @wrap_sys_stdout
    def volume_expand(self, *args, **kwargs):
        return super(HeketiClient, self).volume_expand(*args, **kwargs)

    @wrap_sys_stdout
    def volume_delete(self, *args, **kwargs):
        return super(HeketiClient, self).volume_delete(*args, **kwargs)

    @wrap_sys_stdout
    def block_volume_create(self, *args, **kwargs):
        return super(HeketiClient, self).block_volume_create(*args, **kwargs)

    @wrap_sys_stdout
    def block_volume_list(self, *args, **kwargs):
        return super(HeketiClient, self).block_volume_list(*args, **kwargs)

    @wrap_sys_stdout
    def block_volume_info(self, *args, **kwargs):
        return super(HeketiClient, self).block_volume_info(*args, **kwargs)

    @wrap_sys_stdout
    def block_volume_expand(self, *args, **kwargs):
        # TODO(vponomar): remove raising of the following exception when
        #                 "expansion of block volume" feature is implemented
        #                 in Heketi.
        raise NotImplementedError(
            "'expand block volume' feature is absent yet in Heketi.")

    @wrap_sys_stdout
    def block_volume_delete(self, *args, **kwargs):
        return super(HeketiClient, self).block_volume_delete(*args, **kwargs)
