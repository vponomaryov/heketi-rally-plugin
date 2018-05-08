import time

from rally.task import scenario

from heketi_rally_plugin import scenario_base


@scenario.configure(name="Heketi.volume_create_delete")
class HeketiVolumeCreateDeleteScenario(scenario_base.HeketiScenarioBase):
    def run(self, size=1, volume_type='file', sleep_before_deletion=0):
        """File/Block volume creation and deletion scenario.

        :param size: int, size of a volume in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param sleep_before_deletion: float/int, time in seconds to sleep
            after volume creation and deletion.
        """
        vol = self._volume_create({"size": int(size)}, volume_type=volume_type)
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)
        self._volume_delete(vol["id"], volume_type=volume_type)


@scenario.configure(name="Heketi.volume_create_expand_delete")
class HeketiVolumeCreateExpandDeleteScenario(scenario_base.HeketiScenarioBase):
    def run(self, size=1, expand_size=1, volume_type='file',
            sleep_before_entension=0, sleep_before_deletion=0):
        """File/Block volume creation, expansion and deletion scenario.

        :param size: int, size in GiB of a volume for 'create' operation
        :param expand_size: int, size of a storage to be added to a volume
            in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param sleep_before_entension: float/int, time in seconds to sleep
            before volume expansion.
        :param sleep_before_deletion: float/int, time in seconds to sleep
            before volume deletion.
        """
        # TODO(vponomar): remove raising of the following exception when
        #                 "expansion of block volume" feature is implemented
        #                 in Heketi.
        if volume_type != "file":
            raise NotImplementedError(
                "'expand block volume' feature is absent yet in Heketi.")

        vol = self._volume_create({"size": int(size)}, volume_type=volume_type)
        if sleep_before_entension > 0:
            time.sleep(sleep_before_entension)
        self._volume_expand(
            vol["id"], {"expand_size": int(expand_size)},
            volume_type=volume_type)
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)
        self._volume_delete(vol["id"], volume_type=volume_type)


@scenario.configure(name="Heketi.volume_create_get_delete")
class HeketiVolumeCreateGetDeleteScenario(scenario_base.HeketiScenarioBase):
    def run(self, size=1, volume_type='file', sleep_before_deletion=0):
        """File/Block volume creation, getting and deletion scenario.

        :param size: int, size of a volume in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param sleep_before_getting: float/int, time in seconds to sleep
            before getting a volume.
        :param sleep_before_deletion: float/int, time in seconds to sleep
            before volume deletion.
        """
        vol = self._volume_create({"size": int(size)}, volume_type=volume_type)
        self._volume_info(vol["id"], volume_type=volume_type)
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)
        self._volume_delete(vol["id"], volume_type=volume_type)


@scenario.configure(name="Heketi.volume_list")
class HeketiVolumeListScenario(scenario_base.HeketiScenarioBase):
    def run(self, volume_type='file'):
        """File/Block volume listing scenario.

        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of volumes to be listed.
        """
        self._volume_list(volume_type=volume_type)
