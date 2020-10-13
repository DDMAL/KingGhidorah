import os
import unittest

import pytest

import kingghidorah as kd
from kingghidorah.utils import (
  create_resource,
  random_gen,
)


class ResourceTests(unittest.TestCase):

  def setUp(self):
    self.random_project_name = random_gen()
    self.project = kd.CreateProject(name=self.random_project_name)
    self.path = os.path.dirname(__file__)

    # Filetypes
    self.tiff_filetype = [
      i for i in kd.GetAllResourceTypes() if i["extension"] == "tiff"
    ][0]

  def tearDown(self):
    kd.DeleteProject(uuid=self.project["uuid"])

  def test_create_resource(self):
    assert (kd.UploadFile(
      project=self.project["uuid"],
      name=self.path + "/images/test.tif",
      mime_type=self.tiff_filetype["uuid"],
    )["name"] == "test")

  def test_modify_resource(self):
    with create_resource(
        name=self.path + "/images/test.tif",
        project=self.project["uuid"],
        mime_type=self.tiff_filetype["uuid"],
    ) as f:
      tmp = kd.ModifyFile(
        uuid=f["uuid"],
        name="modify this file",
        description="and description too.",
      )
      assert tmp["name"] == "modify this file"
      assert tmp["description"] == "and description too."

  def test_delete_resource(self):
    with create_resource(
        name=self.path + "/images/test.tif",
        project=self.project["uuid"],
        mime_type=self.tiff_filetype["uuid"],
    ) as f:
      assert kd.DeleteFile(uuid=f["uuid"])["status"]
