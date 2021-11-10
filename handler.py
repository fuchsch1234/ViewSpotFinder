import json
from operator import itemgetter


def combine_mesh(mesh: dict) -> list:
    """Combines the elements and values array from a mesh into a single elements array, where every element
    contains its id, list of nodes and height value.

    :param mesh: Mesh received in request body.
    :returns: List of elements that combine id, list of nodes and value.
    """
    elements = sorted(mesh['elements'], key=itemgetter('id'))
    values = sorted(mesh['values'], key=itemgetter('element_id'))

    transformed_mesh = []
    for (element, value) in zip(elements, values):
        element['value'] = value['value']
        transformed_mesh.append(element)

    return transformed_mesh


def find_view_spot(body: dict) -> list:
    """Finds view spots in a given mesh.

    A view spot is defined as an element that has no neighbors with a higher value than itself. Two elements are
    said to be neighbors if they share at least one node.

    View spots are found by first recording the maximum value of all elements that are connected to each node.
    Next this mapping from node to maximum element value is used to select all elements that have no neighbor with a
    greater value.
    Finally view spots that are neighbors with the exact same value are filtered out and only one of the neighbors
    is selected.

    :param body: Input data received from request.
    :returns: List of view spots that contains element_id and value for each view spot."""
    combined_mesh = combine_mesh(body)

    # First pass over all elements.
    # For each node store the maximum value of all elements that are neighbors at this node.
    max_nodes_values = {}
    for element in combined_mesh:
        for node in element['nodes']:
            max_nodes_values[node] = max(max_nodes_values.get(node, element['value']), element['value'])

    # Collect all elements that have no neighbors with a greater value using the max_nodes_values dict
    # from the first pass over all elements.
    view_spot_candidates = []
    for element in combined_mesh:
        if all([element['value'] >= max_nodes_values[node] for node in element['nodes']]):
            view_spot_candidates.append(element)

    # Only take one view spot candidate when multiple elements with the same height are neighbors.
    # At this point all elements that are neighbors in the view_spot_candidate list are guaranteed
    # to have the same value.
    view_spots = []
    marked_nodes = set()
    for candidate in view_spot_candidates:
        # Check if there already is a view spot that shares a node with the current candidate.
        if not any(marked_nodes.intersection(candidate['nodes'])):
            view_spots.append({'element_id': candidate['id'], 'value': candidate['value']})
        # Mark candidate's nodes as already used by a view spot.
        # This is true either directly if the current candidate is a view spot or transitively
        # when this candidate is a neighbor to an view spot.
        for node in candidate['nodes']:
            marked_nodes.add(node)

    return view_spots


def handle_find_view_spot(event, context):
    view_spots = find_view_spot(event)
    # Sort view spots by value in descending order.
    view_spots = sorted(view_spots, key=itemgetter('value'), reverse=True)
    # If parameter N is part of request, return only first N view spots.
    if 'N' in event:
        # Ensure all view spots are returned if there are less than N view spots.
        view_spots = view_spots[:min(event['N'], len(view_spots))]
    response = {
        "statusCode": 200,
        "body": json.dumps(view_spots)
    }

    return response
