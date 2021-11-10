import json
import unittest

from handler import handle_find_view_spots


class TestHandleFindViewSpots(unittest.TestCase):

    def test_returns_no_more_than_N_view_spots(self):
        mesh = {
            'elements': [{'id': 0, 'nodes': [0, 1, 2]}, {'id': 1, 'nodes': [2, 3, 4]}, {'id': 2, 'nodes': [1, 2, 4]},
                         {'id': 3, 'nodes': [4, 5, 6]}],
            'values': [{'element_id': 0, 'value': 1.0}, {'element_id': 1, 'value': 0.5},
                       {'element_id': 2, 'value': 0.9}, {'element_id': 3, 'value': 1.9}],
            'N': 1
        }

        response = handle_find_view_spots(mesh, None)
        view_spots = json.loads(response['body'])
        self.assertListEqual([{'element_id': 3, 'value': 1.9}], view_spots)

    def test_returns_all_view_spots_if_N_greater_than_number_of_view_spots(self):
        mesh = {
            'elements': [{'id': 0, 'nodes': [0, 1, 2]}, {'id': 1, 'nodes': [2, 3, 4]}, {'id': 2, 'nodes': [1, 2, 4]},
                         {'id': 3, 'nodes': [4, 5, 6]}],
            'values': [{'element_id': 0, 'value': 1.0}, {'element_id': 1, 'value': 0.5},
                       {'element_id': 2, 'value': 0.9}, {'element_id': 3, 'value': 1.9}],
            'N': 5
        }

        response = handle_find_view_spots(mesh, None)
        view_spots = json.loads(response['body'])
        self.assertListEqual([{'element_id': 3, 'value': 1.9}, {'element_id': 0, 'value': 1.0}], view_spots)

    def test_returns_all_view_spots_if_N_is_missing(self):
        mesh = {
            'elements': [{'id': 0, 'nodes': [0, 1, 2]}, {'id': 1, 'nodes': [2, 3, 4]}, {'id': 2, 'nodes': [1, 2, 4]},
                         {'id': 3, 'nodes': [4, 5, 6]}],
            'values': [{'element_id': 0, 'value': 1.0}, {'element_id': 1, 'value': 0.5},
                       {'element_id': 2, 'value': 0.9}, {'element_id': 3, 'value': 1.9}]
        }

        response = handle_find_view_spots(mesh, None)
        view_spots = json.loads(response['body'])
        self.assertListEqual([{'element_id': 3, 'value': 1.9}, {'element_id': 0, 'value': 1.0}], view_spots)
