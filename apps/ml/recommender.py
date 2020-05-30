from abc import ABC, abstractmethod


class Recommender(ABC):
    @property
    def endpoint_name(self):
        raise NotImplementedError

    @property
    def algorithm_name(self):
        raise NotImplementedError

    @property
    def owner(self):
        raise NotImplementedError

    @property
    def description(self):
        raise NotImplementedError

    @property
    def version(self):
        raise NotImplementedError

    @property
    def status(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def pre_calculate(cls):
        pass

    @abstractmethod
    def preprocessing(self, input_data):
        pass

    @abstractmethod
    def predict(self, input_data):
        pass

    @abstractmethod
    def postprocessing(self, prediction):
        pass

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction
