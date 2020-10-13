# Create or Upload

.. autofunction:: kingghidorah.CreateProject
.. autofunction:: kingghidorah.CreateWorkflow
.. autofunction:: kingghidorah.UploadFile

### Initiate tasks

.. autofunction:: kingghidorah.RunWorkflow

```python

# Get filetype uuid from Rodan
self.rgb_png_filetype = [
  i for i in kd.GetAllResourceTypes() if i["mimetype"] == "image/rgb+png"
][0]
# If you're unsure what the mime type is in Rodan (because they don't follow the official standard), you can search for one this way.
self.pyrnn_filetype = [
  i for i in kd.GetAllResourceTypes() if "pyrnn" in i["mimetype"]
][0]

# Upload a file
original_upload = kd.UploadFile(
  name=self.path + "/images/calvo - Halifax_Folio42v_ReducedDim.png",
  mime_type=self.rgb_png_filetype["uuid"],
  project=self.project["uuid"],
)

# Job Names and Input Ports association
jn_ip = [
  # (Job name, Input Port Name, Resource URL)
  ("PNG (RGB)", "Image", [original_upload["url"]]),
  ("MEI Encoding", "MEI Mapping CSV", [csv_upload["url"]]),
  ("Text Alignment", "OCR Model", [ocropus_upload["url"]]),
  ("Text Alignment", "Transcript", [transcript_upload["url"]]),
  ("Fast Pixelwise Analysis of Music Document", "Background model", [background_upload["url"]]),
  ("Fast Pixelwise Analysis of Music Document", "Text model", [text_upload["url"]]),
  ("Fast Pixelwise Analysis of Music Document", "Staff-line model", [staff_upload["url"]]),
  ("Fast Pixelwise Analysis of Music Document", "Symbol model", [music_upload["url"]]),
  ("Classifier", "GameraXML - Feature Selection", [features_upload["url"]]),
  ("Classifier", "GameraXML - Training Data", [training_upload["url"]]),
]

# Create a workflow by uploading a json file.
tmp = kd.CreateWorkflow(
  name="simple_test",
  project=self.project["uuid"],
  json_workflow=self.path + "/json_workflows/simple.json",
)

# Assign the resources to their input ports
resource_assignments = kd.utils.assemble_resource_assignments(
  workflow=kd.GetWorkflow(uuid=tmp["uuid"]),
  port_assignment=jn_ip,
  # resource_assignments={},  # Default value is {} anyway
)

# You'll be able to initiate it.
kd.RunWorkflow(
  name = wf_name,
  workflow = workflow_uuid,
  resource_assignments = resource_assignments,
)
```