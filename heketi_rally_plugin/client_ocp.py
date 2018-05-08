from kubernetes import client


class OCPClient(object):
    def __getattr__(self, attr):
        return getattr(client.CoreV1Api(), attr)
