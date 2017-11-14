from abc import abstractmethod

from ipromise import AbstractBaseClass, implements


def q(x):
    return x.__qualname__


def _qs(bases):
    return str(list(base.__qualname__ for base in bases))


class Reason(AbstractBaseClass):

    def __init__(self):
        self.subreasons = []

    @abstractmethod
    def text(self):
        raise NotImplementedError

    def display(self, n=1):
        print("  " * n, self.text())
        for subreason in self.subreasons:
            subreason.display(n + 1)


class APrecedesBReason(Reason):

    def __init__(self, antecedent, subsequent, **kwargs):
        super().__init__(**kwargs)
        self.antecedent = antecedent
        self.subsequent = subsequent


class ProposedBaseClassListReason(APrecedesBReason):

    @implements(Reason)
    def text(self):
        return (f"{q(self.antecedent)} precedes {q(self.subsequent)} in the "
                "proposed based class list.")


class DirectSubclassReason(APrecedesBReason):

    @implements(Reason)
    def text(self):
        return (f"{q(self.antecedent)} precedes {q(self.subsequent)} because "
                "it inherits from it directly.")


class PivotedReason(APrecedesBReason):

    def __init__(self, pivot, pivot_cause, **kwargs):
        super().__init__(**kwargs)
        self.pivot = pivot
        self.pivot_cause = pivot_cause

    @implements(Reason)
    def text(self):
        if self.pivot_cause is None:
            return (f"{q(self.antecedent)} precedes {q(self.subsequent)} in "
                    f"{q(self.pivot)}'s MRO (and {q(self.pivot)} was in the "
                    "proposed based class list) because")
        else:
            return (f"{q(self.antecedent)} precedes {q(self.subsequent)} in "
                    f"{q(self.pivot_cause)}'s "
                    f"base class {q(self.pivot)}'s MRO because")


class SinglePivotedReason(PivotedReason):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        a = self.antecedent
        b = self.subsequent

        assert a in self.pivot.__mro__
        assert b in self.pivot.__mro__

        for base in self.pivot.__bases__:
            if a in base.__mro__ and b in base.__mro__:
                self.subreasons.append(SinglePivotedReason(
                    antecedent=a,
                    subsequent=b,
                    pivot=base,
                    pivot_cause=self.pivot))
        if not self.subreasons:
            def add_subreason(x):
                self.subreasons.append(AInhertisFromBReason(x, self.pivot))
            add_subreason(self.antecedent)
            add_subreason(self.subsequent)


class AInhertisFromBReason(Reason):

    def __init__(self, ancestor, child, **kwargs):
        super().__init__(**kwargs)
        self.ancestor = ancestor
        self.child = child

        assert ancestor in child.__mro__
        if ancestor in child.__bases__:
            self.via = None
        else:
            for base in self.child.__bases__:
                if ancestor in base.__mro__:
                    self.via = base
                    self.subreasons.append(
                        AInhertisFromBReason(ancestor, base))
                    break

    @implements(Reason)
    def text(self):
        a = self.ancestor
        c = self.child
        if self.via is None:
            return f"{q(a)} is a base class of {q(c)}"
        return f"{q(self.via)} is a base class of {q(c)} and"
