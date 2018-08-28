from rally.common import logging
from rally.task import atomic
from rally.task import scenario

from heketi_rally_plugin import utils


LOG = logging.getLogger(__name__)


class HeketiScenarioBase(scenario.Scenario):
    """Base class for Heketi scenarios."""

    @utils.timeout(300)
    @atomic.action_timer("volume_create")
    def _volume_create(self, volume_options=None, volume_type='file'):
        """Atomic action for 'file' or 'block' volumes creation.

        :param volume_options: dict, contains kwargs which are described here:
            https://github.com/heketi/heketi/blob/master/docs/api/api.md
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        """
        method = "%svolume_create" % ("" if volume_type == "file" else "block")
        try:
            return getattr(self.context["heketi_client"], method)(
                volume_options=volume_options)
        except Exception:
            LOG.error("Create Heketi volume command failed")
            raise

    @utils.timeout(60)
    @atomic.action_timer("volume_list")
    def _volume_list(self, volume_type='file'):
        """Atomic action for listing 'file' or 'block' volumes.

        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of volumes to be listed.
        """
        method = "%svolume_list" % ("" if volume_type == "file" else "block")
        try:
            return getattr(self.context["heketi_client"], method)()
        except Exception:
            LOG.error("List Heketi volumes command failed")
            raise

    @utils.timeout(60)
    @atomic.action_timer("volume_info")
    def _volume_info(self, volume_id, volume_type='file'):
        """Atomic action for getting info of 'file' or 'block' volume.

        :param volume_id: str, ID of a volume to retrieve info about.
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of volume to be taken.
        """
        method = "%svolume_info" % ("" if volume_type == "file" else "block")
        try:
            return getattr(self.context["heketi_client"], method)(volume_id)
        except Exception:
            LOG.error("Get Heketi volume info command failed")
            raise

    @utils.timeout(300)
    @atomic.action_timer("volume_expand")
    def _volume_expand(self, volume_id, expand_size=None, volume_type='file'):
        """Atomic action for 'file' or 'block' volume expansion.

        :param volume_id: str, ID of a volume to retrieve info about.
        :param expand_size: int, size in GiB to be added to the existing volume
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be expanded.
        """
        method = "%svolume_expand" % ("" if volume_type == "file" else "block")
        try:
            return getattr(self.context["heketi_client"], method)(
                volume_id, expand_size=expand_size)
        except Exception:
            LOG.error("Expand Heketi volume command failed")
            raise

    @utils.timeout(300)
    @atomic.action_timer("volume_delete")
    def _volume_delete(self, volume_id, volume_type='file'):
        """Atomic action for deleting 'file' or 'block' volume.

        :param volume_id: str, ID of a volume.
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of volume to be deleted.
        """
        method = "%svolume_delete" % ("" if volume_type == "file" else "block")
        try:
            return getattr(self.context["heketi_client"], method)(volume_id)
        except Exception:
            LOG.error("Delete Heketi volume command failed")
            raise
