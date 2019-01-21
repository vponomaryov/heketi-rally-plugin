import json
import time

from kubernetes import client as k_client
from rally.task import atomic
from rally.task import scenario

from heketi_rally_plugin import utils


class OCPScenarioBase(scenario.Scenario):
    """Base class for OCP scenarios."""

    @property
    def client(self):
        """Shortcut for reaching out an OCP client."""
        return self.context["ocp_client"]

    # --- PV ---

    @atomic.action_timer("pv_list")
    def _pv_list(self):
        """Atomic action for listing Persistent Volumes in OCP."""
        return self.client.list_persistent_volume()

    @atomic.action_timer("pv_get")
    def _pv_get(self, name):
        return self.client.read_persistent_volume(name=name)

    # --- PVC ---

    @atomic.action_timer("pvc_create")
    def _pvc_create(self, storage_class,
                    namespace='default', size=1, name_prefix="rally",
                    creation_timeout=120.0, creation_waiting_step=1.7,
                    delete_pvc_if_failed=True):
        """Atomic action for creating Persistent Volume Claim in OCP."""
        if name_prefix and name_prefix[-1] != '-':
            name_prefix += "-"
        name_prefix.replace('_', '-')
        name = "%s%s" % (name_prefix, utils.get_random_str(8))
        if len(name) > 63:
            # TODO(vponomar): write and reuse custom exception
            raise Exception(
                "PVC's 'name' is allowed to be only 63 symbols long.")

        pvc_body = k_client.V1PersistentVolumeClaim(
            api_version="v1",
            kind="PersistentVolumeClaim",
            metadata={
                "name": name,
                "annotations": {
                    "volume.beta.kubernetes.io/storage-class": storage_class,
                },
            },
            spec={
                "accessModes": ["ReadWriteOnce"],
                "resources": {"requests": {"storage": "%sGi" % size}},
            },
        )
        self.client.create_namespaced_persistent_volume_claim(
            namespace=namespace, body=pvc_body)

        # Wait for PVC to be bound to a PV
        time.sleep(creation_waiting_step)
        pvc = self._pvc_get(name=name, namespace=namespace)
        start_time = time.time()
        while (pvc.status.phase.lower() != 'bound' and
               time.time() - start_time < creation_timeout):
            time.sleep(creation_waiting_step)
            pvc = self._pvc_get(name=name, namespace=namespace)
        if pvc.status.phase.lower() == 'bound':
            return pvc

        # Handling situation when timeout has been reached
        try:
            pvc_events = self._event_list(obj_name=name, namespace=namespace)
        except Exception:
            pvc_events = "?"
        if delete_pvc_if_failed:
            self._pvc_delete(name, namespace)
        raise Exception(
            "Failed to wait for PVC to reach the 'Bound' state. "
            "PVC name is '%s' and its status is '%s'. \n"
            "PVC events: %s" % (name, pvc.status.phase, pvc_events))

    @atomic.action_timer("event_list")
    def _event_list(self, obj_name, namespace=None):
        """Atomic action for listing object events based on its name."""
        field_selector = "involvedObject.name=%s" % obj_name
        if namespace:
            return self.client.list_namespaced_event(
                namespace, field_selector=field_selector)
        return self.client.list_event_for_all_namespaces(
            field_selector=field_selector)

    @atomic.action_timer("pvc_get")
    def _pvc_get(self, name, namespace='default'):
        return self.client.read_namespaced_persistent_volume_claim(
            name=name, namespace=namespace)

    @atomic.action_timer("pvc_list")
    def _pvc_list(self, namespace=None):
        """Atomic action for listing Persistent Volumes Claims in OCP."""
        if namespace:
            return self.client.list_namespaced_persistent_volume_claim(
                namespace)
        return self.client.list_persistent_volume_claim_for_all_namespaces()

    @atomic.action_timer("pvc_delete")
    def _pvc_delete(self, name, namespace='default',
                    deletion_timeout=120.0, deletion_waiting_step=1.4):
        self.client.delete_namespaced_persistent_volume_claim(
            name=name, namespace=namespace, body=k_client.V1DeleteOptions())

        # Wait for PV to be absent
        start_time = time.time()
        while time.time() - start_time < deletion_timeout:
            try:
                self._pv_get(name=name)
            except k_client.rest.ApiException as e:
                if int(json.loads(e.body)["code"]) == 404:
                    return
                raise
            time.sleep(deletion_waiting_step)
        raise Exception("Failed to wait for '%s' PV to be deleted." % name)

    def _run(self, storage_classes,
             namespace='default', size=1, name_prefix="rally",
             creation_timeout=120.0, creation_waiting_step=0.7,
             sleep_before_deletion=0.1,
             deletion_timeout=120.0, deletion_waiting_step=0.5,
             delete_pvc_if_failed=True,
             list_pvcs=False, list_pvs=False):
        if len(name_prefix) > 55:
            # TODO(vponomar): write and reuse custom exception
            raise Exception(
                "'name_prefix' is allowed to be only 55 symbols long.")
        if not isinstance(storage_classes, (list, tuple, set)):
            storage_classes = (storage_classes, )
        pvcs = []
        for storage_class in storage_classes:
            pvcs.append(self._pvc_create(
                storage_class=storage_class.strip(),
                namespace=namespace,
                size=size,
                name_prefix=name_prefix,
                creation_timeout=creation_timeout,
                creation_waiting_step=creation_waiting_step,
                delete_pvc_if_failed=delete_pvc_if_failed,
            ))

        if list_pvcs:
            self._pvc_list(namespace=namespace)
        if list_pvs:
            self._pv_list()

        # NOTE(vponomar): we do not use 'grace_period_seconds' from
        #                 kubernetes client because it is integer, not float.
        if sleep_before_deletion > 0:
            time.sleep(sleep_before_deletion)

        for pvc in pvcs:
            self._pvc_delete(
                name=pvc.metadata.name,
                namespace=namespace,
                deletion_timeout=deletion_timeout,
                deletion_waiting_step=deletion_waiting_step,
            )
