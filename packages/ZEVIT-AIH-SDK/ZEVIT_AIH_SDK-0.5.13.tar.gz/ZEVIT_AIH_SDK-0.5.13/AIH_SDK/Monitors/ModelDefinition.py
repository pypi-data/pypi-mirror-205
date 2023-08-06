from AIH_SDK.Monitors.MonitorsObject import MonitorsObject


class ModelDefinition(MonitorsObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'ModelDefinitions'
        self._version = api_version

    def get(self, name: str=None, version: str=None, parameters: dict={}):
        if not name:
            return super().get(parameters=parameters)
        elif not version:
            return self._client._get(self._api, f'{self._endpoint}/{name}/versions')
        else:
            return self._client._get(self._api, f'{self._endpoint}/{name}/versions/{version}')
    
    def delete(self, name: str=None, version: str=None, parameters: dict={}):
        return self._client._delete(self._api, f'{self._endpoint}/{name}/versions/{version}')