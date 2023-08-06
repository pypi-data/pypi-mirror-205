# Introduction 
This project makes it possible to easily interact with the objects in ZEVIT's Asset Integrity Hub.

Project is structured as follows:

```
AIH_SDK
├── AIHClient
├── Assets
│   ├── Equipment
│   ├── MainSystem
│   └── Plant
├── DataProcessing
│   ├── Job
│   ├── JobConfiguration
│   └── JobDefinition
├── Files
│   ├── DataType
│   └── File
├── Designations
│   ├── Design
│   ├── Schema
│   └── Structure
├── Risks
│   ├── Mitigation
│   ├── Risk
│   └── RiskAssessmentResult
├── Monitors
│   ├── Monitor
│   ├── Model
│   └──  ModelDefinition
├── Maintenance
│   ├── Deviation
│   ├── WorkItem
│   └── Activity
│   ├── WorkTemplate
│   └── ActivityTemplate
│   └── Input
│   └── Media
│   └── MediaReference
├── Signals
│   ├── Channel
│   └── Signal
├── Workitems
│   ├── Annotation
│   ├── Assessment
│   ├── AssignedElement
│   ├── Failure
│   ├── Media
│   ├── MediaReference
│   ├── PanoramaImage
│   ├── PanoramicTour
│   └── WorkorderItem
```

# Getting Started
1.	Install by: pip install AIH_SDK
2.	Initialize AIHClient by: AIH_SDK.AIHClient.AIHClient(environment_to_connect_to, client_id, client_secret, Location)
3.	Get objects from APIs. Example of getting a main system: from AIH_SDK.Assets import MainSystem; mainsystem = MainSystem().get(guid)
4.	Objects support CRUD operation in form of post, get, put, and delete.

# Object design
Objects store the information fetched from the APIs in the self.value of the object

self.value can either be a dict containing one instance or be a list containing multiple dicts, representing multiple objects.

All objects contain the following methods:
* get()
* put()
* post()
* delete()
* copy()
* get_value()
* set_value()
* update_values()
* to_dataframe()
* get_keys()
* filter()
* from_dataframe()
* from_dict()
* from_list()
* join()

Methods that modifies the object operate inplace, but also return the object itself to allow chaining of methods.

# API version
All AIH api's are versioned. If not value is specified the latest spi version is selected by default. To specify the version of an api add the argument api_version when creating the instance of you object for example: MainSystem(api_version='1.4').get(). Please see the documentation to see active versions. 

# PropertyDefinitions
Many Modules in AIH uses property definitions to customize data models to specific usecases. The python sdk supports assigning property values to an object (like a mainsystem) but also creating new property definitions with associated categories and classifications. 
