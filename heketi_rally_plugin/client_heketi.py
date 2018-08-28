try:
    import http.client as http_client
except ImportError:
    # Python 2
    import httplib as http_client
import requests
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
    """Extend original Heketi client with block volumes functionality."""

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
    def blockvolume_create(self, volume_options=None):
        req = self._make_request('POST', self.bv_uri, volume_options or {})
        if req.status_code == requests.codes.ok:
            return req.json()

    @wrap_sys_stdout
    def blockvolume_list(self):
        req = self._make_request('GET', self.bv_uri)
        if req.status_code == requests.codes.ok:
            return req.json()

    @wrap_sys_stdout
    def blockvolume_info(self, volume_id):
        req = self._make_request('GET', "%s/%s" % (self.bv_uri, volume_id))
        if req.status_code == requests.codes.ok:
            return req.json()

    @wrap_sys_stdout
    def blockvolume_expand(self, volume_id, expand_size=None):
        # TODO(vponomar): remove raising of the following exception when
        #                 "expansion of block volume" feature is implemented
        #                 in Heketi.
        raise NotImplementedError(
            "'expand block volume' feature is absent yet in Heketi.")
        uri = '%s/%s/expand' % (self.bv_uri, volume_id)
        req = self._make_request('POST', uri, expand_size)
        if req.status_code == requests.codes.ok:
            return req.json()

    @wrap_sys_stdout
    def blockvolume_delete(self, volume_id):
        req = self._make_request('DELETE', "%s/%s" % (self.bv_uri, volume_id))
        return req.status_code == requests.codes.NO_CONTENT
