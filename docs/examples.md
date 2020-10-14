# Examples

## Getting started

```bash
pip install kingghidorah

# Edit the config.py file for your user credentials, and the url for the api
```

## Getting information from Rodan

You can gather all information in Rodan

```python
import kingghidorah as kd

# Get all projects and return them all as a list of dictionaries (each dictionary being a project)
kd.GetAllProjects()
# Returns something like this
# [{
#     'url': 'https://rodan-staging.simssa.ca/api/project/xxxxxxxx-9f1c-482a-xxxx-xxxxxxxxxxxxx/?format=json',
#     'uuid': 'xxxxxxxx-9f1c-482a-xxxx-xxxxxxxxxxxxx',
#     'name': '**',
#     'description': '',
#     'creator': '**',
#     'admins': ['**'],
#     'workers': [],
#     'created': '2020-10-07T13:29:05.802781Z',
#     'updated': '2020-10-07T13:29:24.347581Z',
#     'workflow_count': 2,
#     'resource_count': 19,
#     'resourcelist_count': 0
# }, {
#     'url': 'https://rodan-staging.simssa.ca/api/project/xxxxxxxx-9736-4e5b-xxxx-xxxxxxxxxxxx/?format=json',
#     'uuid': 'xxxxxxxx-9736-4e5b-xxxx-xxxxxxxxxxxx',
#     'name': '**1**',
#     'description': '',
#     'creator': '****',
#     'admins': ['****'],
#     'workers': [],
#     'created': '2020-10-08T15:19:03.754753Z',
#     'updated': '2020-10-08T15:19:15.972080Z',
#     'workflow_count': 3,
#     'resource_count': 48,
#     'resourcelist_count': 0
# }]

# Get all workflows and return them all as a list of dictionaries (each dictionary being a workflow)
kd.GetAllWorkflows()

# The same is true for resources, resource types
kd.GetAllResources()
kd.GetAllResourceTypes()
kd.GetAllInputs()
kd.GetAllOutputs()
kd.GetAllJobs()
```

Or you can gather specific information

```python
import kingghidorah as kd

# Given a project uuid, you can get that specific dictionary too
kd.GetProject(uuid="xxxxxxxx-9736-4e5b-zzzz-xxxxxxxxxxxx")
# {
#     "url": "https://rodan-staging.simssa.ca/api/project/.../",
#     "name": "",
#     "description": "",
#     "creator": "****",
#     "workflows": [
#         {
#             "url": "https://rodan-staging.simssa.ca/api/workflow/.../",
#             "name": "training"
#         },
#     ],
#     "resources": [
#         {
#             "url": "https://rodan-staging.simssa.ca/api/resource/.../",
#             "name": "63_64_original"
#         }
#     ],
#     "resourcelists": [],
#     "created": "2020-10-07T13:29:05.802781Z",
#     "updated": "2020-10-07T13:29:24.347581Z",
#     "admins": [
#         "****"
#     ],
#     "workers": [],
#     "admins_url": "https://rodan-staging.simssa.ca/api/project/.../admins/",
#     "workers_url": "https://rodan-staging.simssa.ca/api/project/.../workers/"
# }

# The same is true for workflows (the uuid for each)
kd.GetWorkflow(uuid="xxxxxxxx-9736-4e5b-aaaa-xxxxxxxxxxxx")
kd.GetResource(uuid="xxxxxxxx-9736-4e5b-bbbb-xxxxxxxxxxxx")
```

## Upload to Rodan

```python
# Get a project, or create a project
project = kd.CreateProject(name="something")

# Get the file format uuid

# If you know the extension in Rodan (tiff)
tiff_filetype = [i for i in kd.GetAllResourceTypes() if i["extension"] == "tiff"][0]
# If you know the Rodan mime type (rgb+png)
rgb_png_filetype = [i for i in kd.GetAllResourceTypes() if i["mimetype"] == "image/rgb+png"][0]
# If you know part of the Rodan mimetype (pyrnn)
pyrnn_filetype = [i for i in kd.GetAllResourceTypes() if "pyrnn" in i["mimetype"]][0]

# Upload a resource
file_ = kd.UploadFile(
  project=project["uuid"],
  name="/the/filepath/to/a/local/file",
  mime_type=tiff_filetype["uuid"],
)

# Modify a resource
kd.ModifyFile(
  uuid=file_["uuid"],
  name="modified the file name",
  description="Modified the description too",
)

# Create a workflow
empty_workflow = kd.CreateWorkflow(
  name="new workflow",
  project=project["uuid"],
)

# Upload a workflow that was exported from Rodan
uploaded_workflow = kd.CreateWorkflow(
  name="you can call it what you want",
  project=project["uuid"],
  json_workflow="/the/filepath/to/a/local/rodan_json_file",
)
```

## Run a workflow

Some parts of this should be familiar now

```python
complex_workflow = kd.CreateWorkflow(
  name="schema v0.2 workflow",
  project=self.project["uuid"],
  json_workflow=self.path + "/json_workflows/v2fast-trainer.json",
)

# Upload files and run the Job
original_layer = kd.UploadFile(
  name="/images/calvo - Halifax_Folio42v_ReducedDim.png",
  mime_type=rgb_png_filetype["uuid"],
  project=project["uuid"],
)

layers = []
for layer in [
    "/images/calvo - pixel - Layer 0.png",
    "/images/calvo - pixel - Layer 1.png",
    "/images/calvo - pixel - Layer 2.png",
    "/images/calvo - pixel - Layer 3.png",
]:
  layers.append(
    kd.UploadFile(
      name=layer,
      mime_type=rgba_png_filetype["uuid"],
      project=project["uuid"],
    ))

jn_ip = [
  # 1
  (
    "Training model for Patchwise Analysis of Music Document",
    "Image",
    [original_layer["url"]],
  ),
  # 2
  (
    "Training model for Patchwise Analysis of Music Document",
    "rgba PNG - Background layer",
    [layers[0]["url"]],
  ),
  # 3
  (
    "Training model for Patchwise Analysis of Music Document",
    "rgba PNG - Music symbol layer",
    [layers[1]["url"]],
  ),
  # 4
  (
    "Training model for Patchwise Analysis of Music Document",
    "rgba PNG - Staff Lines layer",
    [layers[2]["url"]],
  ),
  # 5
  (
    "Training model for Patchwise Analysis of Music Document",
    "rgba PNG - Selected regions",
    [layers[3]["url"]],
  ),
]

resource_assignments = kd.utils.assemble_resource_assignments(
  workflow=kd.GetWorkflow(uuid=complex_workflow["uuid"]),
  port_assignment=jn_ip,
  # resource_assignments={},  # Default value is {} anyway
)

# Run the workflow
running_job = kd.RunWorkflow(
  name="Training on layers...",
  workflow=complex_workflow["uuid"],
  resource_assignments=resource_assignments,
)

# Wait until the job finishes
```
