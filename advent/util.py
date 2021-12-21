GRID_NEIGHBOR_DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]
GRID_NEIGHBOR_DIRECTIONS_DIAGONALS = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
    (-1, -1),
    (1, 1),
    (-1, 1),
    (1, -1),
]


def grid_neighbors(r, c, grid, diagonals=False):
    """
    returns neighbors of a given point in a grid. excludes diagonals by default
    """

    m, n = len(grid), len(grid[0])
    directions = (
        GRID_NEIGHBOR_DIRECTIONS_DIAGONALS if diagonals else GRID_NEIGHBOR_DIRECTIONS
    )
    for y, x in directions:
        nr, nc = r + y, c + x

        if 0 <= nr < m and 0 <= nc < n:
            yield nr, nc
