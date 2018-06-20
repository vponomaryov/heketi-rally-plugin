from rally.task import scenario

from heketi_rally_plugin import scenario_ocp_base as scenario_base


@scenario.configure(name="OCP.pv_list")
class OCPPVListScenario(scenario_base.OCPScenarioBase):
    def run(self):
        """PV listing scenario."""
        self._pv_list()


@scenario.configure(name="OCP.pvc_list")
class OCPPVCListScenario(scenario_base.OCPScenarioBase):
    def run(self, namespace=None):
        """PVC listing scenario."""
        self._pvc_list(namespace=namespace)


@scenario.configure(name="OCP.pvc_create_delete")
class OCPPVCCreatePVCDeleteScenario(scenario_base.OCPScenarioBase):
    def run(self, storage_classes, namespace='default', size=1,
            name_prefix="rally",
            creation_timeout=120.0, creation_waiting_step=0.7,
            sleep_before_deletion=0.1,
            deletion_timeout=120.0, deletion_waiting_step=0.5,
            delete_pvc_if_failed=True):
        """PVC creation and deletion."""
        self._run(
            storage_classes=storage_classes,
            namespace=namespace,
            size=size,
            name_prefix=name_prefix,
            creation_timeout=creation_timeout,
            creation_waiting_step=creation_waiting_step,
            sleep_before_deletion=sleep_before_deletion,
            deletion_timeout=deletion_timeout,
            deletion_waiting_step=deletion_waiting_step,
            delete_pvc_if_failed=delete_pvc_if_failed,
            list_pvcs=False, list_pvs=False)


@scenario.configure(name="OCP.pvc_create_pvclist_delete")
class OCPPVCCreatePVCListPVCDeleteScenario(scenario_base.OCPScenarioBase):
    def run(self, storage_classes, namespace='default', size=1,
            name_prefix="rally",
            creation_timeout=120.0, creation_waiting_step=0.7,
            sleep_before_deletion=0.1,
            deletion_timeout=120.0, deletion_waiting_step=0.5,
            delete_pvc_if_failed=True):
        """PVC creation and deletion."""
        self._run(
            storage_classes=storage_classes,
            namespace=namespace,
            size=size,
            name_prefix=name_prefix,
            creation_timeout=creation_timeout,
            creation_waiting_step=creation_waiting_step,
            sleep_before_deletion=sleep_before_deletion,
            deletion_timeout=deletion_timeout,
            deletion_waiting_step=deletion_waiting_step,
            delete_pvc_if_failed=delete_pvc_if_failed,
            list_pvcs=True, list_pvs=False)


@scenario.configure(name="OCP.pvc_create_pvlist_delete")
class OCPPVCCreatePVListPVCDeleteScenario(scenario_base.OCPScenarioBase):
    def run(self, storage_classes, namespace='default', size=1,
            name_prefix="rally",
            creation_timeout=120.0, creation_waiting_step=0.7,
            sleep_before_deletion=0.1,
            deletion_timeout=120.0, deletion_waiting_step=0.5,
            delete_pvc_if_failed=True):
        """PVC creation and deletion."""
        self._run(
            storage_classes=storage_classes,
            namespace=namespace,
            size=size,
            name_prefix=name_prefix,
            creation_timeout=creation_timeout,
            creation_waiting_step=creation_waiting_step,
            sleep_before_deletion=sleep_before_deletion,
            deletion_timeout=deletion_timeout,
            deletion_waiting_step=deletion_waiting_step,
            delete_pvc_if_failed=delete_pvc_if_failed,
            list_pvcs=False, list_pvs=True)
