import pytest

import kingghidorah as kd
from kingghidorah.utils import random_gen
from . import base as kdt
import time

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
      json_workflow=self.path + "/json_workflows/simple_workflow.json",
    )
    assert complex_workflow["name"] == "multiple_test"

    files = [
      ("/images/doge.png", self.rgb_png_filetype),
    ]

    file_links = []
    for f in files:
      file_links.append(
        kd.UploadFile(
          name=self.path + f[0],
          mime_type=f[1]["uuid"],
          project=self.project["uuid"],
        ))
    time.sleep(5)

    jn_ip = [
      ("PNG (RGB)", "Image", [file_links[0]["url"]])
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
