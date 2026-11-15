"""Geometric edge-orientation model for standard ZZ-style EO.

Coordinates: x=R, y=U, z=F.  Edge orientation uses the cubie's primary
sticker (U/D when present, otherwise F/B) against the reference axis of its
current slot (U/D axis for U/D-layer slots, F/B axis for middle-layer slots).
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable

Vec = tuple[int, int, int]
FACE_NORMAL: dict[str, Vec] = {
    "R": (1, 0, 0), "L": (-1, 0, 0), "U": (0, 1, 0),
    "D": (0, -1, 0), "F": (0, 0, 1), "B": (0, 0, -1),
}

def _rotate_vec(v: Vec, axis: int, quarter: int) -> Vec:
    x, y, z = v
    for _ in range(quarter % 4):
        if axis == 0: x, y, z = x, -z, y
        elif axis == 1: x, y, z = z, y, -x
        else: x, y, z = -y, x, z
    return x, y, z

def _turn_parameters(move: str) -> tuple[int, int, int, int]:
    if not move or move[0] not in FACE_NORMAL:
        raise ValueError(f"Unsupported face move: {move!r}")
    face, suffix = move[0], move[1:]
    if suffix not in ("", "'", "2"):
        raise ValueError(f"Unsupported move suffix: {move!r}")
    axis = {"R": 0, "L": 0, "U": 1, "D": 1, "F": 2, "B": 2}[face]
    layer = FACE_NORMAL[face][axis]
    quarter = -1 if layer == 1 else 1
    if suffix == "'": quarter *= -1
    return axis, layer, quarter, 2 if suffix == "2" else 1

@dataclass(frozen=True)
class Edge:
    position: Vec
    stickers: tuple[tuple[str, Vec], ...]
    def sticker_map(self) -> dict[str, Vec]:
        return dict(self.stickers)

@dataclass(frozen=True)
class CubeEdges:
    edges: tuple[tuple[str, Edge], ...]
    @classmethod
    def solved(cls) -> "CubeEdges":
        edges = []
        for a, b in (("U","F"),("U","R"),("U","B"),("U","L"),
                     ("D","F"),("D","R"),("D","B"),("D","L"),
                     ("F","R"),("F","L"),("B","R"),("B","L")):
            na, nb = FACE_NORMAL[a], FACE_NORMAL[b]
            pos = tuple(na[i] + nb[i] for i in range(3))
            edges.append((a+b, Edge(pos, tuple(sorted(((a,na),(b,nb)))))))
        return cls(tuple(edges))
    def _apply_layer(self, axis: int, layer: int, quarter: int, reps: int) -> "CubeEdges":
        out = []
        for identity, edge in self.edges:
            if edge.position[axis] == layer:
                pos, stickers = edge.position, edge.sticker_map()
                for _ in range(reps):
                    pos = _rotate_vec(pos, axis, quarter)
                    stickers = {c:_rotate_vec(n,axis,quarter) for c,n in stickers.items()}
                out.append((identity, Edge(pos, tuple(sorted(stickers.items())))))
            else: out.append((identity, edge))
        return CubeEdges(tuple(out))
    def apply(self, move: str) -> "CubeEdges":
        axis, layer, quarter, reps = _turn_parameters(move)
        return self._apply_layer(axis, layer, quarter, reps)
    def apply_slice(self, move: str) -> "CubeEdges":
        if not move or move[0] not in "MES": raise ValueError(f"Unsupported slice move: {move!r}")
        face = {"M":"L","E":"D","S":"F"}[move[0]]
        axis, _, quarter, reps = _turn_parameters(face + move[1:])
        return self._apply_layer(axis, 0, quarter, reps)
    def apply_sequence(self, moves: Iterable[str]) -> "CubeEdges":
        state = self
        for move in moves: state = state.apply(move)
        return state
    def edge_oriented(self, identity: str) -> bool:
        edge = dict(self.edges)[identity]
        stickers = edge.sticker_map()
        primary = next((stickers[c] for c in ("U","D","F","B") if c in stickers), None)
        if primary is None: raise AssertionError(f"Malformed edge identity: {identity}")
        slot_axis = 1 if edge.position[1] != 0 else 2
        return primary[slot_axis] != 0
    def eo_mask(self) -> int:
        mask = 0
        for i,(identity,_) in enumerate(self.edges):
            if not self.edge_oriented(identity): mask |= 1 << i
        return mask
    def bad_edges(self) -> tuple[str, ...]:
        return tuple(name for name,_ in self.edges if not self.edge_oriented(name))
    def eo_count(self) -> int: return self.eo_mask().bit_count()
    def is_fully_oriented(self) -> bool: return self.eo_mask() == 0

def move_effect(move: str) -> dict[str, object]:
    state = CubeEdges.solved().apply(move)
    return {"move":move,"bad_edges":state.bad_edges(),"bad_count":state.eo_count(),"eo_mask":state.eo_mask()}

def eo_preserving_moves() -> tuple[str, ...]:
    return tuple(f+s for f in "RLUD" for s in ("","'","2")) + ("F2","B2")

def all_face_moves() -> tuple[str, ...]:
    return tuple(f+s for f in "RLUDFB" for s in ("","'","2"))
