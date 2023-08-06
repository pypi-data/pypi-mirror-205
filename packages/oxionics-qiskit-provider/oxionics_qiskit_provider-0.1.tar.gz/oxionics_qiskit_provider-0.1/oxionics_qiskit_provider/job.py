from __future__ import annotations

import http
import logging
from time import sleep
import typing
from urllib.parse import urljoin

from qiskit import QuantumCircuit
import qiskit.providers
from qiskit.providers import JobError, JobStatus
from qiskit.result import Result
from qiskit.result.models import ExperimentResult, ExperimentResultData

if typing.TYPE_CHECKING:
    from oxionics_qiskit_provider.backend import OxIonicsBackend

log = logging.getLogger(__name__)


class OxIonicsJob(qiskit.providers.JobV1):
    _backend: OxIonicsBackend

    def __init__(
        self, backend: OxIonicsBackend, job_id: str, qobj: QuantumCircuit, **kwargs
    ):
        super().__init__(backend, job_id, **kwargs)
        self.qobj = qobj

    def _get_last_event(self):
        response = self._backend.session.get(
            urljoin(self._backend.api_root, "status"),
            params={"job_id": self._job_id},
        )
        log.debug(
            f"Got response code={response.status_code}, content={response.content}"
        )
        if response.status_code == http.HTTPStatus.OK:
            return response.json()
        elif response.status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR:
            raise JobError(response.json()["message"])
        elif response.status_code == http.HTTPStatus.NOT_FOUND:
            raise ValueError(response.json()["message"])
        else:
            response.raise_for_status()
            raise RuntimeError(
                f"Unexpected result from API call: status={response.status_code}"
            )

    def submit(self):
        """Submits a job for execution.

        :class:`.OxIonicsJob` does not support standalone submission of a job
        object. This can not be called and the Job is only submitted via
        the ``run()`` method of the backend

        Raises:
            NotImplementedError: This method does not support calling
            ``submit()``
        """
        raise NotImplementedError(
            "OxIonics backend doesn't support submitting using "
            "`OxIonicsJob.submit`. Use `OxIonicsBackend.run` instead."
        )

    def cancel(self):
        """Cancels a previously submitted job if it is still queueing"""

        response = self._backend.session.post(
            urljoin(self._backend.api_root, "cancel"),
            params={"job_id": self._job_id},
        )
        log.debug(
            f"Got response code={response.status_code}, content={response.content}"
        )

        if response.status_code == http.HTTPStatus.NOT_FOUND:
            raise ValueError(response.json()["message"])
        elif response.status_code == http.HTTPStatus.INTERNAL_SERVER_ERROR:
            raise JobError(response.json()["message"])
        elif response.status_code != http.HTTPStatus.OK:
            response.raise_for_status()
            raise RuntimeError(
                f"Unexpected result from API call: status={response.status_code}"
            )

    def result(self):
        data = self._get_last_event()
        while data["type"] != "completed":
            sleep(5)
            data = self._get_last_event()
        counts = data["counts"]
        return Result(
            backend_name="oxionics",
            backend_version="0.0.1",  # TODO: Should report this from the backend
            qobj_id=id(self.qobj),
            job_id=self._job_id,
            success=True,
            results=[
                ExperimentResult(
                    shots=sum(counts.values()),
                    success=True,
                    data=ExperimentResultData(
                        counts=counts,
                    ),
                )
            ],
        )

    def status(self):
        try:
            data = self._get_last_event()
        except JobError:
            return JobStatus.ERROR

        status = data["type"]
        if status == "completed":
            return JobStatus.DONE
        elif status == "progress":
            stage = data["stage"]
            if stage == "queued":
                return JobStatus.QUEUED
            elif stage == "processing":
                return JobStatus.RUNNING
            else:
                log.warning(f"Unknown progress stage '{stage}' coerced to queued")
                return JobStatus.QUEUED
        elif status == "accepted":
            return JobStatus.QUEUED
        elif status == "cancelled":
            return JobStatus.CANCELLED
        else:
            log.warning(f"Unknown event type '{status}' coerced to queued status")
            return JobStatus.QUEUED
