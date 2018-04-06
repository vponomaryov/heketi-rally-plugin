import heketi
import requests


class HeketiClient(heketi.HeketiClient):
    """Extend original Heketi client with block volumes functionality."""

    bv_uri = '/blockvolumes'

    def blockvolume_create(self, volume_options=None):
        req = self._make_request('POST', self.bv_uri, volume_options or {})
        if req.status_code == requests.codes.ok:
            return req.json()

    def blockvolume_list(self):
        req = self._make_request('GET', self.bv_uri)
        if req.status_code == requests.codes.ok:
            return req.json()

    def blockvolume_info(self, volume_id):
        req = self._make_request('GET', "%s/%s" % (self.bv_uri, volume_id))
        if req.status_code == requests.codes.ok:
            return req.json()

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

    def blockvolume_delete(self, volume_id):
        req = self._make_request('DELETE', "%s/%s" % (self.bv_uri, volume_id))
        return req.status_code == requests.codes.NO_CONTENT
