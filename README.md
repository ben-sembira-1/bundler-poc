# bundler-poc

## How to use
1. Create a venv and enter into it
1. `pip install -r requirements.txt` (Only pydantic)
1. run `python3 package_bundle.py dragonfly` or `python3 package_bundle.py eagle`

The output will look like this:
```
(.venv) user@user:~/clones/bundler-poc$ python3 package_bundle.py eagle

----------------------
Packing module Chrome
===
~ Removing /home/ben-sembira/clones/bundler-poc/modules/Chrome/.deps
---
Fetching https://path/to/google-chrome-stable-v3.4.1.msi to /home/ben-sembira/clones/bundler-poc/modules/Chrome/.deps/google-chrome.msi
Validating hash of /home/ben-sembira/clones/bundler-poc/modules/Chrome/.deps/google-chrome.msi
---
Fetching https://path/to/google-translate-v1.2.8.exe to /home/ben-sembira/clones/bundler-poc/modules/Chrome/.deps/google-translate.exe
Validating hash of /home/ben-sembira/clones/bundler-poc/modules/Chrome/.deps/google-translate.exe
---
Copying /home/ben-sembira/clones/bundler-poc/entities/eagle/chrome/auto-tabs.yaml to /home/ben-sembira/clones/bundler-poc/modules/Chrome/.deps/background_image.yaml
---
Copying /home/ben-sembira/clones/bundler-poc/entities/eagle/chrome/background.jpeg to /home/ben-sembira/clones/bundler-poc/modules/Chrome/.deps/background_image.jpeg
---
self.parameters=ChromeParameters(dark_mode=True, installation_path=PosixPath('C:\\Program Files (x86)\\Google Chrome'))
----------------------

----------------------
Packing module MissionPlanner
===
~ Removing /home/ben-sembira/clones/bundler-poc/modules/MissionPlanner/.deps
---
Fetching https://path/to/MissionPlanner-v1.3.74.msi to /home/ben-sembira/clones/bundler-poc/modules/MissionPlanner/.deps/MissionPlanner.msi
Validating hash of /home/ben-sembira/clones/bundler-poc/modules/MissionPlanner/.deps/MissionPlanner.msi
---
Copying /home/ben-sembira/clones/bundler-poc/entities/eagle/mission-planner/config.xml to /home/ben-sembira/clones/bundler-poc/modules/MissionPlanner/.deps/config.xml
---
self.parameters=MissionPlannerParameters(installation_path=PosixPath('C:\\Program Files (x86)\\Mission Planner'))
----------------------

----------------------
Packing module LogsShortcuts
===
~ Removing /home/ben-sembira/clones/bundler-poc/modules/LogsShortcuts/.deps
---
self.parameters=LogsShortcutsParameters(log_paths=[PosixPath('C:\\AppData\\Google Chrome\\Logs'), PosixPath('C:\\AppData\\Google Chrome\\Experimental\\Light Rendering\\Logs')])
----------------------
```

## Things to think about

### Hard pydantic errors
Currently because the pydantic type of the json is a list of modules that pydantic needs to match to real classes, if there is an error in the model the errors are overwhelming and it is hard to understand where in the configuration structure the problem is. For example, I switched the boolean value of `"dark_mode" =  true` to `"dark_mode" = "dark"` and this is the error:
```
Traceback (most recent call last):
  File "/home/ben-sembira/clones/bundler-poc/package_bundle.py", line 63, in <module>
    main()
  File "/home/ben-sembira/clones/bundler-poc/package_bundle.py", line 59, in main
    pack_all(entity)
  File "/home/ben-sembira/clones/bundler-poc/package_bundle.py", line 39, in pack_all
    bundle = load_bundle_from_json(Path(f"{entity}_configurations.json"))
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ben-sembira/clones/bundler-poc/package_bundle.py", line 35, in load_bundle_from_json
    return BundleConfiguration(**json.loads(json_raw))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/ben-sembira/clones/bundler-poc/.venv/lib/python3.12/site-packages/pydantic/main.py", line 176, in __init__
    self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 11 validation errors for BundleConfiguration
modules.0.Chrome.parameters.dark_mode
  Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value='dark', input_type=str]
    For further information visit https://errors.pydantic.dev/2.7/v/bool_parsing
modules.0.MissionPlanner.name
  Assertion failed, 

Could not find module named 'Chrome'.
>>> IMPORTANT: If you received this error you can ignore other pydantic errors.

 [type=assertion_error, input_value='Chrome', input_type=str]
    For further information visit https://errors.pydantic.dev/2.7/v/assertion_error
modules.0.MissionPlanner.url_dependencies.msi
  Field required [type=missing, input_value={'installer_msi': {'url':....exe', 'hash': 'a193d'}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
modules.0.MissionPlanner.configuration_files.config_xml
  Field required [type=missing, input_value={'background_image': {'pa...chrome/auto-tabs.yaml'}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
modules.0.Neptune.name
  Assertion failed, 

Could not find module named 'Chrome'.
>>> IMPORTANT: If you received this error you can ignore other pydantic errors.

 [type=assertion_error, input_value='Chrome', input_type=str]
    For further information visit https://errors.pydantic.dev/2.7/v/assertion_error
modules.0.Neptune.configuration_files
  Input should be None [type=none_required, input_value={'background_image': {'pa...chrome/auto-tabs.yaml'}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.7/v/none_required
modules.0.Neptune.url_dependencies.installation_tar
  Field required [type=missing, input_value={'installer_msi': {'url':....exe', 'hash': 'a193d'}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
modules.0.LogsShortcuts.name
  Assertion failed, 

Could not find module named 'Chrome'.
>>> IMPORTANT: If you received this error you can ignore other pydantic errors.

 [type=assertion_error, input_value='Chrome', input_type=str]
    For further information visit https://errors.pydantic.dev/2.7/v/assertion_error
modules.0.LogsShortcuts.parameters.log_paths
  Field required [type=missing, input_value={'dark_mode': 'dark', 'in...s (x86)\\Google Chrome'}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.7/v/missing
modules.0.LogsShortcuts.url_dependencies
  Input should be None [type=none_required, input_value={'installer_msi': {'url':....exe', 'hash': 'a193d'}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.7/v/none_required
modules.0.LogsShortcuts.configuration_files
  Input should be None [type=none_required, input_value={'background_image': {'pa...chrome/auto-tabs.yaml'}}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.7/v/none_required
```
The relevant error inside all of this is:
```
modules.0.Chrome.parameters.dark_mode
  Input should be a valid boolean, unable to interpret input [type=bool_parsing, input_value='dark', input_type=str]
```

A solution for it can be to move from a list of modules to a strict object that includes strict modules:

Instead of:
```python
ModulesAvailable = Union[Chrome, MissionPlanner, Neptune, LogsShortcuts]
Entity = Literal["eagle", "dragonfly"]

class BundleConfiguration(BaseModel):
    entity: Entity
    modules: List[ModulesAvailable]
```
```json
{
  "entity": "eagle",
  "modules": [
    {
      "name": "Chrome",
      "url_dependencies": {...},
      "parameters": {...},
      "configuration_files": {...}
    },
    {
      "name": "MissionPlanner",
      "url_dependencies": {...},
      "parameters": {...},
      "configuration_files": {...}
    },
    {
      "name": "LogsShortcuts",
      "module": "logs-shortcut",
      "parameters": {...},
      "url_dependencies": null,
      "configuration_files": null
    }
  ]
}
```
We can have:
```python
Entity = Literal["eagle", "dragonfly"]

class BundleConfiguration(BaseModel):
    entity: Entity
    modules: Union[EagleModules, DragonflyModules]

class EagleModules(BaseModel):
  chrome: Chrome
  mission_planner: MissionPlanner
  logs_shortcuts: LogsShortcuts

class DragonflyModules(BaseModel):
  neptune: Neptune
  mission_planner: MissionPlanner
  logs_shortcuts: LogsShortcuts
```
```json
{
  "entity": "eagle",
  "modules": {
    "chrome": {
      "url_dependencies": {...},
      "parameters": {...},
      "configuration_files": {...}
    },
    "mission_planner": {
      "url_dependencies": {...},
      "parameters": {...},
      "configuration_files": {...}
    },
    "logs_shortcuts": {
      "module": "logs-shortcut",
      "parameters": {...},
      "url_dependencies": null,
      "configuration_files": null
    }
  }
}
```

### Installation scripts

Currently the installation scripts are powershell scripts. This fact makes the installation part of the code to not use the types in the bundle phase.
Options:
- Transfer all powershell installation from powershell to python (hard)
- Make the powershell scripts get as arguments all the paths and parameters from a python script
- Just keep it like that, and think about it later
