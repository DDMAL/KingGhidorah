# Quickstart

## Getting started

### Installation

Install with pip or poetry
```bash
pip install kingghidorah
```

### Configuration

You need a configuration file which declares the API, user credentials, and proxy if needed.

```json
// config.json
{
  "domain": "http://localhost/api/",
  "username": "rodan",
  "password": "rodan",
  "proxy": ""
}
```

## Getting information from Rodan

- Specify a configuration file at the top of your script.
  ```python
  import kingghidorah as kd

  kd.set_conf("./config.json")
  ```

  .. note:: If you've git-cloned KingGhidorah, installed, and edited the config.json from the git repository, you can omit this. The `set_conf` function is useful for running the same workflow on multiple Rodan APIs to test for errors.

- You can gather all information in Rodan.

  ```python
  import kingghidorah as kd

  kd.set_conf("./config.json")

  # Get all projects and return them all as a list of dictionaries (each dictionary being a project)
  kd.GetAllProjects()
  ```

  - KingGhidorah will always return either a **list** or a **dictionary**. `GetAllProjects` will return the following:

    ```python
    [{
        'url': 'https://localhost/api/project/xxxxxxxx-9f1c-482a-xxxx-xxxxxxxxxxxxx/?format=json',
        'uuid': 'xxxxxxxx-9f1c-482a-xxxx-xxxxxxxxxxxxx',
        'name': '**',
        'description': '',
        'creator': '**',
        'admins': ['**'],
        'workers': [],
        'created': '2020-10-07T13:29:05.802781Z',
        'updated': '2020-10-07T13:29:24.347581Z',
        'workflow_count': 2,
        'resource_count': 19,
        'resourcelist_count': 0
    }, {
        'url': 'https://localhost/api/project/xxxxxxxx-9736-4e5b-xxxx-xxxxxxxxxxxx/?format=json',
        'uuid': 'xxxxxxxx-9736-4e5b-xxxx-xxxxxxxxxxxx',
        'name': '**1**',
        'description': '',
        'creator': '****',
        'admins': ['****'],
        'workers': [],
        'created': '2020-10-08T15:19:03.754753Z',
        'updated': '2020-10-08T15:19:15.972080Z',
        'workflow_count': 3,
        'resource_count': 48,
        'resourcelist_count': 0
    }]
    ```

  - Other functions to get information

    ```python
    # Get all workflows and return them all as a list of dictionaries (each dictionary being a workflow)
    kd.GetAllWorkflows()

    # The same is true for resources, resource types
    kd.GetAllResources()
    kd.GetAllResourceTypes()
    kd.GetAllInputs()
    kd.GetAllOutputs()
    kd.GetAllJobs()
    ```

  - You can also search for something like all the projects with "hello" in their name.

    ```python
    kd.GetAllProjects(name="hello")
    ```

- If you know the UUID of something, you can get the specific object, which will return a python dictionary.

  ```python
  import kingghidorah as kd

  # Given a project uuid, you can get that specific dictionary too
  kd.GetProject(uuid="xxxxxxxx-9736-4e5b-zzzz-xxxxxxxxxxxx")
  ```

  - Output:

    ```python
    {
        "url": "https://rodan-staging.simssa.ca/api/project/.../",
        "name": "",
        "description": "",
        "creator": "****",
        "workflows": [
            {
                "url": "https://rodan-staging.simssa.ca/api/workflow/.../",
                "name": "training"
            },
        ],
        "resources": [
            {
                "url": "https://rodan-staging.simssa.ca/api/resource/.../",
                "name": "63_64_original"
            }
        ],
        "resourcelists": [],
        "created": "2020-10-07T13:29:05.802781Z",
        "updated": "2020-10-07T13:29:24.347581Z",
        "admins": [
            "****"
        ],
        "workers": [],
        "admins_url": "https://rodan-staging.simssa.ca/api/project/.../admins/",
        "workers_url": "https://rodan-staging.simssa.ca/api/project/.../workers/"
    }
    ```

- Other commonly used options are also available

  ```python
  # The same is true for workflows (the uuid for each)
  kd.GetWorkflow(uuid="xxxxxxxx-9736-4e5b-aaaa-xxxxxxxxxxxx")
  kd.GetResource(uuid="xxxxxxxx-9736-4e5b-bbbb-xxxxxxxxxxxx")
  ```

## Upload to Rodan

```python
import kingghidorah as kd

# set config
kd.set_conf("./config.json")

# Get a project, or create a project
project = kd.CreateProject(name="something")

# Get the file format uuid

# If you know the extension in Rodan (tiff)
tiff_filetype = [i for i in kd.GetAllResourceTypes() if i["extension"] == "tiff"][0]
# Search by the contents of the Mimetype
tiff_filetype = kd.GetAllResourceTypes(mimetype="tiff")[0]
# Warning: if you're looking for rgb+png for example, you need to urlencode your search:
import urllib
rgb_png_filetype = kd.GetAllResourceTypes(mimetype=urllib.parse.quote_plus("png+png"))[0]
# You can still do things you own way.
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
import kingghidorah as kd

# set config
kd.set_conf("./config.json")

complex_workflow = kd.CreateWorkflow(
  name="schema v0.2 workflow",
  project=project["uuid"],
  json_workflow=path + "/json_workflows/v2fast-trainer.json",
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
    "rgba PNG - Layer 0",
    [layers[1]["url"]],
  ),
  # 4
  (
    "Training model for Patchwise Analysis of Music Document",
    "rgba PNG - Layer 1",
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
