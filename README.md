# Coding Challenge: View Spot Finder

## How to run

Run with serverless:

```shell
serverless invoke local --function findViewSpots -p <input-file>
```

Run unit tests with pytest:

```shell
pytest tests
```

## Task

Given a mesh of nodes (vertices) and elements defined by three nodes and a value denoting its height,
and an integer N find the first N view spots by view spot height.

A view spot is any element that has no neighboring element that has a greater value.
Two elements are said to be neighboring if they share at least one node.

# Solution

All view spots can be found with a runtime linear in the number of elements, by first iterating over all elements
and keeping track of all nodes and the maximum value any neighboring element has.
With this data all elements that are potential view spots can be found in a second iteration over all elements
by comparing their value to the maximum value of its nodes.
At last the potential view spots must be filtered for neighboring view spots with the same height. Of these only
one view spot shall be selected.
