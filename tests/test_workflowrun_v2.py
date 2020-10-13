import pytest

import kingghidorah as kd
from kingghidorah.utils import random_gen
from . import base as kdt


class TestWorkflowsV02(kdt.KingGhidorahTestCase):

  def test_upload_v02_multiple_job_workflow(self):
    """
		If you see this test fail, try running it alone.
			pytest tests/test_workflowrun_v2.py::TestWorkflowsV02::test_upload_v02_multiple_job_workflow

    Either the problem is in the code or the tests are not cleaning up well.
		"""

    complex_workflow = kd.CreateWorkflow(
      name="schema v0.2 workflow",
      project=self.project["uuid"],
      json_workflow=self.path + "/json_workflows/v2fast-trainer.json",
    )
    assert complex_workflow["name"] == "schema v0.2 workflow"

    # Upload files and run the Job
    original_layer = kd.UploadFile(
      name=self.path + "/images/calvo - Halifax_Folio42v_ReducedDim.png",
      mime_type=self.rgb_png_filetype["uuid"],
      project=self.project["uuid"],
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
          name=self.path + layer,
          mime_type=self.rgba_png_filetype["uuid"],
          project=self.project["uuid"],
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

    running_job = kd.RunWorkflow(
      name="Training on layers...",
      workflow=complex_workflow["uuid"],
      resource_assignments=resource_assignments,
    )
    try:
      assert running_job["name"] == "Training on layers..."
    except KeyError:
      raise Exception(running_job)
