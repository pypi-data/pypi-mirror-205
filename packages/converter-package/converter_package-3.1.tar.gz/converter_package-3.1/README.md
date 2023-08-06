# Converter

Converter is a subcomponent of the ACCORDION platform. It is being used by the Orchestrator and Lifecycle Manager components in order to translate the application model to K3s configuration files, action models, workflow models and matchmaking models

## Installation

```bash
pip3 install converter-package==2.5
```

## 1. Parse Intermediate Model
```python

nodelist, imagelist, application_version = Parser.ReadFile(jsonResponse)
```
## 2. Create the namespace that describes the appInstanceInfo
```python
 application_instance = ID.generate_k3s_namespace(name, application_version, randomApplicationIntanceID())
```

## 3. How to generate matchmaking model
```python
matchmaking_model = MatchingModel.generate(nodelist, application_instance)
```
## 4. Generate namespace and secrets files for Kubernetes
```python
namespace_yaml = Converter.namespace(application_instance)
secret_yaml = Converter.secret_generation(json_base64_string, application_instance)
```

## 5. Generate deployments, persistenv volumes and services files for Kubernetes
```python
deployment_files, persistent_files, service_files = Converter.tosca_to_k8s(nodelist, imagelist,
                                                                                   application_instance, minicloud,
                                                                                   externalIP, gpu_list)
```
!!! Warning: gpu_model is an optional parameter. Since one or more GPU names may be given to Converter, the parameter has to be a list that would contain application components along with the required GPUs

## 6. Generate the action model
```python
actions_set = ActionModel.generate(nodelist, application_instance)
 ```

## 7. Generate the workflows model
```python
workflows_set = WorkflowModel.generate(nodelist, application_instance)
 ```

## 8. Scale out
```python
json_base64_string, url, name = online_selector('plexus')
intermediate_model = callAppBucket(json_base64_string, url, name)
deployment = Converter.scale_out_to_k8s(componentInfo, intermediate_model)
 ```
## More on Usage
DeployInterface.py is an example of usage for the case of deployment. There is also the ScaleOutInterface.py that presents how to use Converter to create scale out files for ACCORDION, it is available on the ACCORDION's Gitlab


## License
[MIT](https://choosealicense.com/licenses/mit/)