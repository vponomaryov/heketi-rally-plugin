import time

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
class OCPPVCCreateDeleteScenario(scenario_base.OCPScenarioBase):
    def run(self, storage_class, namespace='default', size=1,
            name_prefix="rally",
            creation_timeout=120.0, creation_waiting_step=0.7,
            sleep_before_deletion=0.1,
            deletion_timeout=120.0, deletion_waiting_step=0.5,
            delete_pvc_if_failed=True):
        """PVC creation and deletion."""
        pvc = self._pvc_create(
            storage_class=storage_class,
            namespace=namespace,
            size=size,
            name_prefix=name_prefix,
            creation_timeout=creation_timeout,
            creation_waiting_step=creation_waiting_step,
            delete_pvc_if_failed=delete_pvc_if_failed,
        )

        # NOTE(vponomar): we do not use 'grace_period_seconds' from
        #                 kubernetes client because it is integer, not float.
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)

        self._pvc_delete(
            name=pvc.metadata.name,
            namespace=namespace,
            deletion_timeout=deletion_timeout,
            deletion_waiting_step=deletion_waiting_step,
        )
