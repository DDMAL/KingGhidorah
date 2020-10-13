import os
import unittest

import kingghidorah as kd
from kingghidorah.utils import random_gen


class KingGhidorahTestCase(unittest.TestCase):

  def setUp(self):
    # Cleanup just in case the workspace is dirty.
    try:
      for p in kd.GetAllProjects():
        kd.DeleteProject(uuid=p["uuid"])
    except kd.exceptions._NoMoreResources:
      pass

    self.random_project_name = random_gen()
    self.project = kd.CreateProject(name=self.random_project_name)
    self.path = os.path.dirname(__file__)

    # Filetypes
    self.tiff_filetype = [
      i for i in kd.GetAllResourceTypes() if i["extension"] == "tiff"
    ][0]
    self.rgb_png_filetype = [
      i for i in kd.GetAllResourceTypes() if i["mimetype"] == "image/rgb+png"
    ][0]
    self.rgba_png_filetype = [
      i for i in kd.GetAllResourceTypes() if i["mimetype"] == "image/rgba+png"
    ][0]
    self.hdf5_filetype = [
      i for i in kd.GetAllResourceTypes() if i["mimetype"] == "keras/model+hdf5"
    ][0]
    self.gamera_xml_filetype = [
      i for i in kd.GetAllResourceTypes() if i["mimetype"] == "application/gamera+xml"
    ][0]
    self.csv_filetype = [
      i for i in kd.GetAllResourceTypes() if i["mimetype"] == "text/csv"
    ][0]
    self.plaintext_filetype = [
      i for i in kd.GetAllResourceTypes() if i["mimetype"] == "text/plain"
    ][0]
    self.pyrnn_filetype = [
      i for i in kd.GetAllResourceTypes() if "pyrnn" in i["mimetype"]
    ][0]

    self.workflow = kd.CreateWorkflow(
      name="test",
      project=self.project["uuid"],
    )

  def tearDown(self):
    kd.DeleteProject(uuid=self.project["uuid"])
