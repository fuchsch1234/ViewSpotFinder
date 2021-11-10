import json
import os.path
import unittest

from handler import find_view_spots


class TestViewSpotFinder(unittest.TestCase):

    def test_mesh_with_one_element(self):
        mesh = {
            'elements': [{'id': 0, 'nodes': [0, 1, 2]}],
            'values': [{'element_id': 0, 'value': 0.0}]
        }

        view_spots = find_view_spots(mesh)
        self.assertListEqual([{'element_id': 0, 'value': 0.0}], view_spots)

    def test_find_single_view_spot(self):
        mesh = {
            'elements': [{'id': 0, 'nodes': [0, 1, 2]}, {'id': 1, 'nodes': [2, 3, 4]}, {'id': 2, 'nodes': [1, 2, 4]}],
            'values': [{'element_id': 0, 'value': 1.0}, {'element_id': 1, 'value': 0.5}, {'element_id': 2, 'value': 0.9}]
        }

        view_spots = find_view_spots(mesh)
        self.assertListEqual([{'element_id': 0, 'value': 1.0}], view_spots)

    def test_find_multiple_view_spots(self):
        mesh = {
            'elements': [{'id': 0, 'nodes': [0, 1, 2]}, {'id': 1, 'nodes': [2, 3, 4]}, {'id': 2, 'nodes': [1, 2, 4]},
                         {'id': 3, 'nodes': [4, 5, 6]}],
            'values': [{'element_id': 0, 'value': 1.0}, {'element_id': 1, 'value': 0.5},
                       {'element_id': 2, 'value': 0.9}, {'element_id': 3, 'value': 1.9}]
        }

        view_spots = find_view_spots(mesh)
        self.assertListEqual([{'element_id': 0, 'value': 1.0}, {'element_id': 3, 'value': 1.9}], view_spots)

    def test_multiple_view_spots_with_plateau(self):
        mesh = {
            'elements': [{'id': 0, 'nodes': [0, 1, 2]}, {'id': 1, 'nodes': [2, 3, 4]}, {'id': 2, 'nodes': [3, 4, 5]}],
            'values': [{'element_id': 0, 'value': 1.0}, {'element_id': 1, 'value': 0.5}, {'element_id': 2, 'value': 0.5}]
        }

        view_spots = find_view_spots(mesh)
        self.assertListEqual([{'element_id': 0, 'value': 1.0}, {'element_id': 2, 'value': 0.5}], view_spots)
