import qiskit.providers

from oxionics_qiskit_provider.backend import OxIonicsBackend


class OxIonicsProvider(qiskit.providers.ProviderV1):
    def __init__(
        self,
        token,
        api_root="https://api.oxionics.com/",
    ):
        self._backed = OxIonicsBackend(token, api_root)

    def backends(self, name=None, **kwargs):
        return [self._backed]
