import unittest

import kingghidorah as kd
from kingghidorah.utils import (
  random_gen,
  create_project,
)


class ProjectTests(unittest.TestCase):

  def test_create_project(self):
    name = random_gen()
    with create_project(name=name) as p:
      assert p["name"] == name

  def test_delete_project(self):
    name = random_gen()
    with create_project(name=name) as p:
      assert "delete" in kd.DeleteProject(uuid=p["uuid"])["status"]
