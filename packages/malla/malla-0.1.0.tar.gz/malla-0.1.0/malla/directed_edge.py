"""
Directed edge data structure for triangle meshes

This module implements the directed edge data structure for triangle
meshes.

CLASSES
-------
mesh
    main class representing a triangle mesh
vertex
    a class representing a single mesh vertex
half_edge
    a class representing a single half edge
"""

from dataclasses import dataclass
from typing import Generator

@dataclass
class vertex:
    """
    A class representing a mesh vertex

    Attributes
    ----------
    data : any
        user-defined data associated with the vertex
    half_edge : int
        index of a mesh half_edge starting at the vertex
    """

    data: any = None
    half_edge: int = -1


@dataclass
class half_edge:
    """A class representing a half_edge"""

    dst: int
    mate: int = -1


class mesh:
    """A class representing a triangle mesh

    This is an implementation of the Directed Edge data sructure for
    triangle meshes.

    Attributes
    ----------
    vertices : List[vertex]
        The list of all mesh vertices
    half_edges : List[half_edge]
        The list of all half edges in the mesh. Faces are coded by this
        list, so there is not need for a face container.

    Methods
    -------
    next(he: int) -> int
        returns the half edge next to he in the same face
    prev(he: int) -> int:
        returns the half edge previous to he in the same face
    face(he: int) -> int:
        returns the face to which half edge he belongs to
    vertex(self, v: int) -> vertex:
        returns the mesh vertex of index v
    half_edge(self, he: int) -> half_edge:
        returns the mesh half edge of index he
    number_of_vertices(self) -> int:
        returns the number of mesh vertices
    number_of_faces(self) -> int:
        returns the number of mesh faces
    vertex_neighbors(self, v: int):
        generator yielding the indices of vertices neighbors to vertex v
    vertex_neighboring_faces(self, v: int):
        generator yielding the indices of faces incident to vertex v
    face_neighbors(self, f: int):
        generator yielding the indices of faces neighbors to face f
    """

    def __init__(self, vertices, faces):
        self.vertices = [ vertex(v) for v in vertices ]
        self.half_edges = []
        self._half_edges_map = {}
        for f in faces:
            self.__add_face(f)
        for i in range(len(self.vertices)):
            self.__assert_vertex_half_edge(i)
        self._half_edges_map = None

    @staticmethod
    def next(he: int) -> int:
        if he % 3 == 2:
            return he - 2
        else:
            return  he + 1;

    @staticmethod
    def prev(he:int ) -> int:
        if he % 3 == 0:
            return he + 2
        else:
            return he - 1;

    @staticmethod
    def face(he: int) -> int:
        return int(he/3)

    def vertex(self, v: int) -> vertex:
        return self.vertices[v]

    def half_edge(self, he: int) -> half_edge:
        return self.half_edges[he]

    def number_of_vertices(self) -> int:
        return len(self.vertices)

    def number_of_faces(self) -> int:
        return int(len(self.half_edges)/3)

    def vertex_neighbors(self, v: int) -> Generator[int, None, None]:
        he = self.vertex(v).half_edge
        if he != -1:
            v0 = self.half_edge(he).dst
            yield v0
            while True:
                hn = self.half_edge(self.prev(he)).mate
                if hn == -1:
                    yield self.half_edge(self.next(he)).dst
                    break
                else:
                    he = hn
                vi = self.half_edge(he).dst
                if vi == v0:
                    break
                else:
                    yield vi

    def vertex_neighboring_faces(self, v: int) -> Generator[int, None, None]:
        hf = self.vertex(v).half_edge
        if hf != -1:
            he = hf
            yield self.face(he)
            while True:
                hn = self.half_edge(self.prev(he)).mate
                if hn == -1:
                    break
                else:
                    he = hn
                if he == hf:
                    break
                else:
                    yield self.face(he)

    def face_neighbors(self, f: int) -> Generator[int, None, None]:
        hf = 3*f
        for i in range(3):
            h = hf+i
            mate = self.half_edge(h).mate
            if mate > -1:
                yield self.face(mate)

    def __add_face(self, f: any) -> None:
        self.__put_half_edge(f[0], f[1])
        self.__put_half_edge(f[1], f[2])
        self.__put_half_edge(f[2], f[0])

    def __put_half_edge(self, vi: int, vj: int) -> None:
        pair = (vi, vj)
        if pair in self._half_edges_map:
            print("Error  : wrong orientation on mesh. Quitting ...")
            exit()
        h = len(self.half_edges)
        he = half_edge(vj)
        self.half_edges.append(he)
        if self.vertices[vi].half_edge == -1:
            self.vertices[vi].half_edge = h
        self._half_edges_map[pair] = h
        other_pair = (vj, vi)
        if other_pair in self._half_edges_map:
            self.__link(h, self._half_edges_map[other_pair]);

    def __link(self, he1: int, he2: int) -> None:
        if he1 != -1:
            self.half_edges[he1].mate = he2
        if he2 != -1:
            self.half_edges[he2].mate = he1

    def __assert_vertex_half_edge(self, v: int) -> None:
        first = self.vertices[v].half_edge
        if first != -1:
            mate  = self.half_edges[first].mate
            if mate != -1:
                current = self.next(mate)
                while current != first:
                    mate = self.half_edges[current].mate
                    if mate != -1:
                        current = self.next(mate)
                    else:
                        self.vertices[v].half_edge = current
                        current = first
        else:
            print("Warning : vetex %d is isolated." % v)

