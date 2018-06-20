import time

from rally.task import scenario

from heketi_rally_plugin import scenario_heketi_base as scenario_base
from heketi_rally_plugin import utils


def _get_volume_options(size=1, name_prefix="rally"):
    volume_options = {}
    if name_prefix:
        if name_prefix[-1] != '-':
            name_prefix += "-"
        name_prefix.replace('_', '-')
        name = "%s%s" % (name_prefix, utils.get_random_str(14))
        volume_options["name"] = name
    volume_options["size"] = int(size)
    return volume_options


@scenario.configure(name="Heketi.volume_create_delete")
class HeketiVolumeCreateDeleteScenario(scenario_base.HeketiScenarioBase):
    def run(self, size=1, volume_type='file',
            name_prefix="rally", sleep_before_deletion=0):
        """File/Block volume creation and deletion scenario.

        :param size: int, size of a volume in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param name_prefix: str, custom string to be used as prefix
            for volume names.
        :param sleep_before_deletion: float/int, time in seconds to sleep
            after volume creation and deletion.
        """
        volume_options = _get_volume_options(size, name_prefix)
        vol = self._volume_create(volume_options, volume_type=volume_type)
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)
        self._volume_delete(vol["id"], volume_type=volume_type)


@scenario.configure(name="Heketi.volume_create_expand_delete")
class HeketiVolumeCreateExpandDeleteScenario(scenario_base.HeketiScenarioBase):
    def run(self, size=1, expand_size=1, volume_type='file',
            name_prefix="rally",
            sleep_before_entension=0, sleep_before_deletion=0):
        """File/Block volume creation, expansion and deletion scenario.

        :param size: int, size in GiB of a volume for 'create' operation
        :param expand_size: int, size of a storage to be added to a volume
            in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param name_prefix: str, custom string to be used as prefix
            for volume names.
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

        volume_options = _get_volume_options(size, name_prefix)
        vol = self._volume_create(volume_options, volume_type=volume_type)
        if sleep_before_entension > 0:
            time.sleep(sleep_before_entension)
        self._volume_expand(
            vol["id"], {"expand_size": int(expand_size)},
            volume_type=volume_type)
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)
        self._volume_delete(vol["id"], volume_type=volume_type)


@scenario.configure(name="Heketi.volume_create_expand_list_delete")
class HeketiVolumeCreateExpandListDeleteScenario(
        scenario_base.HeketiScenarioBase):
    def run(self, size=1, expand_size=1, volume_type='file',
            name_prefix="rally",
            sleep_before_entension=0, sleep_before_deletion=0):
        """File/Block volume creation, expansion, listing and deletion scenario

        :param size: int, size in GiB of a volume for 'create' operation
        :param expand_size: int, size of a storage to be added to a volume
            in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param name_prefix: str, custom string to be used as prefix
            for volume names.
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

        volume_options = _get_volume_options(size, name_prefix)
        vol = self._volume_create(volume_options, volume_type=volume_type)
        if sleep_before_entension > 0:
            time.sleep(sleep_before_entension)
        self._volume_expand(
            vol["id"], {"expand_size": int(expand_size)},
            volume_type=volume_type)
        self._volume_list(volume_type=volume_type)
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)
        self._volume_delete(vol["id"], volume_type=volume_type)


@scenario.configure(name="Heketi.volume_create_expand_get_delete")
class HeketiVolumeCreateExpandGetDeleteScenario(
        scenario_base.HeketiScenarioBase):
    def run(self, size=1, expand_size=1, volume_type='file',
            name_prefix="rally",
            sleep_before_entension=0, sleep_before_deletion=0):
        """File/Block volume creation, expansion, getting and deletion scenario

        :param size: int, size in GiB of a volume for 'create' operation
        :param expand_size: int, size of a storage to be added to a volume
            in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param name_prefix: str, custom string to be used as prefix
            for volume names.
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

        volume_options = _get_volume_options(size, name_prefix)
        vol = self._volume_create(volume_options, volume_type=volume_type)
        if sleep_before_entension > 0:
            time.sleep(sleep_before_entension)
        self._volume_expand(
            vol["id"], {"expand_size": int(expand_size)},
            volume_type=volume_type)
        self._volume_info(vol["id"], volume_type=volume_type)
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)
        self._volume_delete(vol["id"], volume_type=volume_type)


@scenario.configure(name="Heketi.volume_create_get_delete")
class HeketiVolumeCreateGetDeleteScenario(scenario_base.HeketiScenarioBase):
    def run(self, size=1, volume_type='file',
            name_prefix="rally", sleep_before_deletion=0):
        """File/Block volume creation, getting and deletion scenario.

        :param size: int, size of a volume in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param name_prefix: str, custom string to be used as prefix
            for volume names.
        :param sleep_before_getting: float/int, time in seconds to sleep
            before getting a volume.
        :param sleep_before_deletion: float/int, time in seconds to sleep
            before volume deletion.
        """
        volume_options = _get_volume_options(size, name_prefix)
        vol = self._volume_create(volume_options, volume_type=volume_type)
        self._volume_info(vol["id"], volume_type=volume_type)
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)
        self._volume_delete(vol["id"], volume_type=volume_type)


@scenario.configure(name="Heketi.volume_create_list_delete")
class HeketiVolumeCreateListDeleteScenario(scenario_base.HeketiScenarioBase):
    def run(self, size=1, volume_type='file',
            name_prefix="rally", sleep_before_deletion=0):
        """File/Block volume creation, listing and deletion scenario.

        :param size: int, size of a volume in GiB
        :param volume_type: str, choices are 'file' and 'block'. Defines
            the type of a volume to be created.
        :param name_prefix: str, custom string to be used as prefix
            for volume names.
        :param sleep_before_getting: float/int, time in seconds to sleep
            before getting a volume.
        :param sleep_before_deletion: float/int, time in seconds to sleep
            before volume deletion.
        """
        volume_options = _get_volume_options(size, name_prefix)
        vol = self._volume_create(volume_options, volume_type=volume_type)
        self._volume_list(volume_type=volume_type)
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


@scenario.configure(name="Heketi.volume_create_delete_file_and_block_volumes")
class HeketiVolumeCreateDeleteFileAndBlockVolumesScenario(
        scenario_base.HeketiScenarioBase):
    def run(self, size=1, name_prefix="rally", sleep_before_deletion=0):
        """File and Block volumes creation and deletion scenario.

        :param size: int, size of a volume in GiB
        :param name_prefix: str, custom string to be used as prefix
            for volume names.
        :param sleep_before_deletion: float/int, time in seconds to sleep
            after volume creation and deletion.
        """
        volume_options = _get_volume_options(size, name_prefix)
        vols = []
        step = self.context["iteration"] % 2 or -1
        try:
            for volume_type in ('file', 'block')[::step]:
                vols.append(
                    (self._volume_create(volume_options,
                                         volume_type=volume_type),
                     volume_type)
                )
            if sleep_before_deletion > 0:
                time.sleep(sleep_before_deletion)
        finally:
            for vol in vols:
                self._volume_delete(vol[0]["id"], volume_type=vol[1])
