from AIH_SDK.Monitors.MonitorsObject import MonitorsObject
from AIH_SDK import AIHExceptions as AIHE


class Monitor(MonitorsObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        self._endpoint = 'Monitors'
        self._version = api_version


class MonitorJob(MonitorsObject):
    
    def __init__(self, api_version='1.0'):
        super().__init__()
        api_version = '1.0'
        self._endpoint = 'MonitorJobs'
    

    def update_status(self, status: str=None, monitorjob_id: str=None):
        if not monitorjob_id:
            if type(self.value) == dict:
                monitorjob_id = self.get_value('id')
            else:
                raise AIHE.AIHException(f'This method is not supported for self.value of type {type(self.value)}')
        
        self._client._put(self._api, f'{self._endpoint}/{monitorjob_id}/{status}', "")
