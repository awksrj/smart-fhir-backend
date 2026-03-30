class BaseAdapter:
    def fetch_patients(self, name=None):
        raise NotImplementedError

    def fetch_observations(self, patient_id):
        raise NotImplementedError

    def normalize_patient(self, data):
        raise NotImplementedError

    def normalize_observation(self, data):
        raise NotImplementedError