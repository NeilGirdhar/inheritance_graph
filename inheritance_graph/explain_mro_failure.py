from more_itertools import pairwise
from networkx import DiGraph, simple_cycles

__all__ = ['mro_check']


class Reason:

    def __init__(self, reason_str, subreasons=[]):
        self.reason_str = reason_str
        self.subreasons = subreasons

    def display(self, n=1):
        print("  " * n, self.reason_str, "because" if self.subreasons else "")
        for subreason in self.subreasons:
            subreason.display(n + 1)


def _qs(bases):
    return str(list(base.__qualname__ for base in bases))


def _why(c, a, b):
    "Why does a precede b in c?"
    assert a in c.__mro__
    assert b in c.__mro__
    if issubclass(a, b):
        assert False
        return [Reason(f"{a.__qualname__} is a subclass of {b.__qualname__}")]
    reasons = []
    for base in c.__bases__:
        if a in base.__mro__ and b in base.__mro__:
            reasons.append(Reason(f"{a.__qualname__} precedes "
                                  f"{b.__qualname__} in {c.__qualname__}'s "
                                  f"base class {base.__qualname__}",
                                  _why(base, a, b)))
    if not reasons:
        a_s = [base
               for base in c.__bases__
               if a in base.__mro__]
        b_s = [base
               for base in c.__bases__
               if b in base.__mro__]
        reasons.append(Reason(f"{a.__qualname__} is found in "
                              f"{c.__qualname__}'s base classes "
                              f"{_qs(a_s)} and "
                              f"{b.__qualname__} is found in "
                              f"{c.__qualname__}'s base classes {_qs(b_s)}"))
    return reasons


def _process(g, iterable_of_pairs, reason_str, c):
    for a, b in iterable_of_pairs:
        if g.has_edge(a, b):
            continue
        why = [] if c is None else _why(c, a, b)
        reason = Reason(f"{a.__qualname__} precedes {b.__qualname__} "
                        f"{reason_str}",
                        why)
        g.add_edge(a, b, reason=reason)


def mro_check(proposed_base_class_list):
    g = DiGraph()
    _process(g, pairwise(proposed_base_class_list),
             "in the attempt to inherit from "
             f"{_qs(proposed_base_class_list)}",
             None)
    for proposed_base in proposed_base_class_list:
        for base in proposed_base.__mro__:
            for bases_base in base.__bases__:
                _process(g, [(base, bases_base)],
                         f"due to direct inheritance", None)
        _process(g, pairwise(proposed_base.__mro__),
                 f"in {proposed_base.__qualname__}'s MRO", proposed_base)
    for cycle in simple_cycles(g):
        print("Cycle found:")
        for a, b in pairwise(cycle + [cycle[0]]):
            for edge in g.edges(a, data=True):
                if edge[1] == b:
                    edge[2]['reason'].display()
