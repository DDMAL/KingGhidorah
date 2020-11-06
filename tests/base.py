import os
import unittest
import urllib

import kingghidorah as kd
from kingghidorah.utils import random_gen


class KingGhidorahTestCase(unittest.TestCase):
  # Filetypes
  tiff_filetype = [
    i for i in kd.GetAllResourceTypes() if i["extension"] == "tiff"
  ][0]
  rgb_png_filetype = kd.GetAllResourceTypes(mimetype=urllib.parse.quote_plus("rgb+png"))[0]
  rgba_png_filetype = kd.GetAllResourceTypes(mimetype=urllib.parse.quote_plus("rgba+png"))[0]
  hdf5_filetype = kd.GetAllResourceTypes(mimetype=urllib.parse.quote_plus("model+hdf5"))[0]
  gamera_xml_filetype = kd.GetAllResourceTypes(mimetype=urllib.parse.quote_plus("gamera+xml"))[0]
  csv_filetype = kd.GetAllResourceTypes(mimetype=urllib.parse.quote_plus("text/csv"))[0]
  plaintext_filetype = kd.GetAllResourceTypes(mimetype=urllib.parse.quote_plus("text/plain"))[0]
  pyrnn_filetype = kd.GetAllResourceTypes(mimetype=urllib.parse.quote_plus("pyrnn"))[0]

  def setUp(self):
    # Cleanup just in case the workspace is dirty.
    # try:
    #   for p in kd.GetAllProjects():
    #     kd.DeleteProject(uuid=p["uuid"])
    # except kd.exceptions._NoMoreResources:
    #   pass

    self.random_project_name = random_gen()
    self.project = kd.CreateProject(name=self.random_project_name)
    self.path = os.path.dirname(__file__)

    self.workflow = kd.CreateWorkflow(
      name="test",
      project=self.project["uuid"],
    )

  def tearDown(self):
    kd.DeleteProject(uuid=self.project["uuid"])
