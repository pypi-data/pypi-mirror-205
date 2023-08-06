from qiskit import IBMQ, transpile, Aer

from ..utilities import JobResponse


class QiskitFaaS:

    def __init__(self, backend_data):
        self.token = backend_data.get("token")
        self.device_name = backend_data.get("deviceName")
        # self.hub = backend_data.get("hub")
        # self.device_type = backend_data.get("deviceType")
        self.hub = None
        self.device_type = 'QUANTUM_SIMULATOR'
        self.backend = self.get_qiskit_backend()

    def init_ibmq_provider(self):
        if IBMQ.active_account():
            if IBMQ.active_account().get("token") == self.token:
                provider = IBMQ.get_provider(hub=self.hub)
            else:
                IBMQ.disable_account()
                provider = IBMQ.enable_account(token=self.token, hub=self.hub)
        else:
            provider = IBMQ.enable_account(self.token, hub=self.hub)
        return provider

    def get_qiskit_backend(self):
        if self.device_type == "QUANTUM_MACHINE":
            ibmq = self.init_ibmq_provider()
            return ibmq.get_backend(self.device_name)
        else:
            return Aer.get_backend(self.device_name)

    def transpile_circuit(self, circuit):
        return transpile(circuit, self.backend)

    def run_job(self, circuit, shots):
        # Transpile circuit to adapt with backend basis gate
        qc = self.transpile_circuit(circuit)
        job = self.backend.run(qc, shots=shots)
        return job

    def submit_job(self, qcircuit, shots) -> JobResponse:
        if self.device_type == "QUANTUM_SIMULATOR":
            try:
                job = self.run_job(qcircuit, shots)
                job_result = dict(job.result().get_counts())
                job_status = "DONE"
            except Exception:
                job_result = {}
                job_status = "ERROR"
            return JobResponse(
                provider_job_id="Internal-Qiskit-Simulation-Job",
                job_status=job_status,
                job_result=job_result,
            )
        return JobResponse()
