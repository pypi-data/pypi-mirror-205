from AIH_SDK.Monitors.MonitorsObject import MonitorsObject
from AIH_SDK import AIHExceptions as AIHE


class Classification(MonitorsObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Classifications'
        self._version = api_version
        
    def get_elements(self, classification_id=None):
        if not classification_id:
            if type(self.value) == dict:
                classification_id = self.get_value('id')
            else:
                raise AIHE.AIHException(f'This method is not supported for self.value of type {type(self.value)}')

        return ClassificationElement(classification_id).get()


class ClassificationElement(MonitorsObject):

    _classification_id = None

    def __init__(self, classification_id, api_version='1.0'):
        self._classification_id = classification_id
        super().__init__()
        self._version = api_version
        self._endpoint = f'Classifications/{self._classification_id}/Elements'