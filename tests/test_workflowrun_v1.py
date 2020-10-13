import pytest

import kingghidorah as kd
from kingghidorah.utils import random_gen
from . import base as kdt


class TestWorkflowsV01(kdt.KingGhidorahTestCase):

  def test_create_empty_workflow(self):
    assert self.workflow["name"] == "test"

  def test_delete_workflow(self):
    assert "delete" in kd.DeleteWorkflow(uuid=self.workflow["uuid"])["status"]

  def test_upload_v01_single_job_workflow(self):
    simple = kd.CreateWorkflow(
      name="simple_test",
      project=self.project["uuid"],
      json_workflow=self.path + "/json_workflows/simple.json",
    )
    assert simple["name"] == "simple_test"

  # @pytest.mark.flaky(reruns=5)
  def test_upload_v01_multiple_job_workflow(self):
    complex_workflow = kd.CreateWorkflow(
      name="multiple_test",
      project=self.project["uuid"],
      json_workflow=self.path + "/json_workflows/Full-Workflow.json",
    )
    assert complex_workflow["name"] == "multiple_test"

    files = [
      ("/images/CF-033.png", self.rgb_png_filetype),
      ("/misc/split_features.xml", self.gamera_xml_filetype),
      ("/misc/split_training.xml", self.gamera_xml_filetype),
      ("/misc/back.hdf5", self.hdf5_filetype),
      ("/misc/music.hdf5", self.hdf5_filetype),
      ("/misc/staff.hdf5", self.hdf5_filetype),
      ("/misc/text.hdf5", self.hdf5_filetype),
      ("/misc/csv-square notation test_20190725015554.csv", self.csv_filetype),
      ("/misc/salzinnes_OCR_model_545k.pyrnn", self.pyrnn_filetype),
      ("/misc/CF-033.txt", self.plaintext_filetype),
    ]

    file_links = []
    for f in files:
      file_links.append(
        kd.UploadFile(
          name=self.path + f[0],
          mime_type=f[1]["uuid"],
          project=self.project["uuid"],
        ))

    jn_ip = [
      ("PNG (RGB)", "Image", [file_links[0]["url"]]),
      (
        "Non-Interactive Classifier",
        "GameraXML - Feature Selection",
        [file_links[1]["url"]],
      ),
      (
        "Non-Interactive Classifier",
        "GameraXML - Training Data",
        [file_links[2]["url"]],
      ),
      (
        "Fast Pixelwise Analysis of Music Document",
        "Background model",
        [file_links[3]["url"]],
      ),
      (
        "Fast Pixelwise Analysis of Music Document",
        "Symbol model",
        [file_links[4]["url"]],
      ),
      (
        "Fast Pixelwise Analysis of Music Document",
        "Staff-line model",
        [file_links[5]["url"]],
      ),
      (
        "Fast Pixelwise Analysis of Music Document",
        "Text model",
        [file_links[6]["url"]],
      ),
      ("MEI Encoding", "MEI Mapping CSV", [file_links[7]["url"]]),
      ("Text Alignment", "OCR Model", [file_links[8]["url"]]),
      ("Text Alignment", "Transcript", [file_links[9]["url"]]),
    ]

    resource_assignments = kd.utils.assemble_resource_assignments(
      workflow=kd.GetWorkflow(uuid=complex_workflow["uuid"]),
      port_assignment=jn_ip,
      # resource_assignments={},  # Default value is {} anyway
    )

    running_job = kd.RunWorkflow(
      name="full workflow test...",
      workflow=complex_workflow["uuid"],
      resource_assignments=resource_assignments,
    )
    try:
      assert running_job["name"] == "full workflow test..."
    except KeyError:
      raise Exception(running_job)
