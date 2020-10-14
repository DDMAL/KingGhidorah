import re
import string
import unittest

import kingghidorah as kd
from kingghidorah.utils import (
  random_gen,
  create_project,
)


class ProjectTests(unittest.TestCase):
  def setUp(self):
    # self.name = random_gen().replace("/", "_")
    self.name = re.sub(f"[{string.punctuation}]", "", random_gen())

  def test_create_project(self):
    name = self.name
    with create_project(name=name) as p:
      assert p["name"] == name

  def test_delete_project(self):
    name = self.name
    with create_project(name=name) as p:
      assert "delete" in kd.DeleteProject(uuid=p["uuid"])["status"]
  
  def test_get_project(self):
    name = self.name

    with create_project(name=name) as p:
      assert isinstance(kd.GetAllProjects(), list)

      try:
        tmp = kd.GetAllProjects(name=p["name"])[0]
      except:
        raise Exception(name)

      try:
        assert tmp["name"] == name
      except:
        raise Exception("\n" + tmp["name"] + "\n\n" + name)