from __future__ import annotations
from collections.abc import Iterable
from typing import Any

from more_itertools import pairwise
from networkx import DiGraph, simple_cycles

from .reason import DirectSubclassReason, ProposedBaseClassListReason, SinglePivotedReason

__all__ = ['mro_check']


def _add_edges(g: DiGraph[Any],
               iterable_of_pairs: Iterable[tuple[type[Any], type[Any]]],
               reason_cls: type[Any],
               **kwargs: Any
               ) -> None:
    for a, b in iterable_of_pairs:
        if g.has_edge(a, b):
            continue
        reason = reason_cls(antecedent=a, subsequent=b, **kwargs)
        g.add_edge(a, b, reason=reason)


def mro_check(proposed_base_class_list: list[type[Any]]) -> None:
    g = DiGraph()

    _add_edges(g, pairwise(proposed_base_class_list),
               ProposedBaseClassListReason)

    for proposed_base in proposed_base_class_list:
        for base in proposed_base.__mro__:
            for bases_base in base.__bases__:
                _add_edges(g, [(base, bases_base)], DirectSubclassReason)

    for proposed_base in proposed_base_class_list:
        _add_edges(g, pairwise(proposed_base.__mro__),
                   SinglePivotedReason,
                   pivot=proposed_base,
                   pivot_cause=None)

    for cycle in simple_cycles(g):
        for a, b in pairwise([*cycle, cycle[0]]):
            for edge in g.edges(a, data=True):
                if edge[1] == b:
                    edge[2]['reason'].display()
