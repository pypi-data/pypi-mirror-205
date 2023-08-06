OxIonics Qiskit Provider
========================

A provider and backend for Qiskit, which executes quantum circuits on the
Oxford Ionics ion traps.

Usage
-----

Unlike with most Qiskit backends, the Oxford Ionics backend doesn't require that
the circuit has been transpiled before being passed to `OxIonicsBackend.run`.
This is because the OxIonics API accepts arbitrary QASM.


### Create a backend

An authentication token is required:

```python
from oxionics_qiskit_provider import OxIonicsProvider

provider = OxIonicsProvider("my_token")
backend = provider.get_backend()
```

### Run circuits on the backend

```python
from qiskit.circuit.random import random_circuit

qx = random_circuit(1, 3)

job = backend.run(qx)
results = job.results()
```
