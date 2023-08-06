from copy import copy
import math
from urllib.parse import urljoin

from qiskit import QuantumCircuit
from qiskit.circuit import Barrier, Measure, Parameter
from qiskit.circuit.library import RXGate, RXXGate, RYGate
import qiskit.providers
from qiskit.transpiler import Target
import requests
from requests.utils import default_user_agent

from oxionics_qiskit_provider.job import OxIonicsJob


class OxIonicsBackend(qiskit.providers.BackendV2):
    def __init__(self, token, api_root):
        super().__init__()
        # This target definition makes transpile work, which is probably
        # expected for a qiskit backend, but we don't require transpilation,
        # and we might recompile against a different target server side.
        self._target = Target(num_qubits=6)
        theta = Parameter("theta")
        self._target.add_instruction(RXGate(theta))
        self._target.add_instruction(RYGate(theta))
        self._target.add_instruction(RXXGate(math.pi / 2))
        self._target.add_instruction(Measure())
        self._target.add_instruction(Barrier(self._target.num_qubits))

        self.api_root = api_root
        self.session = requests.Session()
        # TODO get our version from somewhere
        self.session.headers[
            "User-Agent"
        ] = f"OxIonicsQisKitBacked/0.1 {default_user_agent()}"
        self.session.headers["Authorization"] = f"Bearer {token}"
        self.options.set_validator("shots", (1, 200))

    @property
    def target(self):
        return self._target

    @property
    def max_circuits(self):
        return 1

    @classmethod
    def _default_options(cls):
        return qiskit.providers.Options(
            shots=50,
        )

    def run(self, run_input, **options):
        if not isinstance(run_input, QuantumCircuit):
            raise ValueError(f"OxIonics backend doesn't support running {run_input!r}")

        opts = copy(self.options)
        opts.update_options(**options)

        body = {
            "shots": opts.shots,
            "qasm": run_input.qasm(),
        }

        response = self.session.post(
            urljoin(self.api_root, "submit"),
            json=body,
        )
        response.raise_for_status()

        return OxIonicsJob(self, response.json()["job_id"], run_input)
