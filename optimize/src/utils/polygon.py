import numpy as np
from scipy.spatial import ConvexHull
from src.utils import polygon_x

def _shoelace(vertices):
    """ The shoelace algorithm for polgon area """
    area = 0.0
    n = len(vertices)
    for i in range(n):
        j = (i + 1) % n
        area += (vertices[j][0] - vertices[i][0]) * \
                (vertices[j][1] + vertices[i][1])
    return area

def area(polygons):
    if type(polygons[0]) == np.ndarray:
        return sum(polygon_x.area(p) for p in polygons)
    else:
        return sum(abs(_shoelace(p))/2 for p in polygons)

def centroid(polygons):
    xmin, ymin = float('inf'), float('inf')
    xmax, ymax = float('-inf'), float('-inf')
    for poly in polygons:
        for x, y in poly:
            xmin = min(xmin, x)
            ymin = min(ymin, y)
            xmax = max(xmax, x)
            ymax = max(ymax, y)
    xc = (xmin + xmax) / 2
    yc = (ymin + ymax) / 2
    return (xc, yc)

def bounding_box(polygons):
    bbox = [ float('inf'), float('inf'), float('-inf'), float('-inf')  ]
    for poly in polygons:
        if len(poly) < 3:
            raise ValueError('Polygon must have more than two points.')
        for x,y in polygon:
            bbox[0] = min(bbox[0], x)
            bbox[1] = min(bbox[1], y)
            bbox[2] = max(bbox[2], x)
            bbox[3] = max(bbox[3], y)
    return bbox

def convex_hull(polygons):
    poly_arr = np.array(polygons, dtype='f')
    return (poly_arr[ ConvexHull(poly_arr).vertices ]).tolist()

def pround(polygons):
    return [[(round(x), round(y)) for x,y in poly] for poly in polygons]

import time
from collections import defaultdict, Counter
from itertools import combinations
def merge_polygons(polygons):
    """ Assumes polygons **share identical integer vertices.**
    """
    if len(polygons) == 1:
        return polygns[0]
    # try:
    start = time.time()
    edge_faces = Counter()
    for pi, poly in enumerate(polygons):
        for vi, v in enumerate(poly):
            v_n = poly[(vi+1)%len(poly)]
            edge_faces[(min(v, v_n), max(v, v_n))] += 1
    outside_edges = set(e for e, c in edge_faces.items() if c == 1)
    vert_neighbors = defaultdict(set)
    for v1, v2 in outside_edges:
        vert_neighbors[v1].add(v2)
        vert_neighbors[v2].add(v1)
    outside_verts = list(vert_neighbors.keys())
    if len(outside_verts) == 0: # TODO fix this.
        return []
    vert = next(iter(outside_verts))
    start_vert = vert
    added = set()
    polygon = []
    while True:
        assert vert not in added
        polygon.append(vert)
        added.add(vert)
        options = [ v for v in vert_neighbors[ vert ] if v not in added ]
        if len(options) == 0:
            break
        vert = options[0]
    assert len(polygon) == len(outside_verts), (len(polygon), len(outside_verts), polygons)
    # print('Merged %i polygns in %f'%(len(polygons), time.time() - start))
    return polygon
    # except Exception as e:
    #     print("Failed to merge")
    #     print("SIZES:", [ len(p) for p in polygons ])
    #     for (i, p1), (j, p2) in combinations(enumerate(polygons), 2):
    #         print(i, j, len(set(p1) & set(p2)))
    #     raise e
