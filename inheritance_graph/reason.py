from typing import Any, override


def q(x: type[Any]) -> str:
    return x.__qualname__


class Reason:
    def __init__(self) -> None:
        super().__init__()
        self.subreasons: list[Reason] = []

    def text(self) -> str:
        raise NotImplementedError

    def display(self, n: int = 1) -> None:
        for subreason in self.subreasons:
            subreason.display(n + 1)


class APrecedesBReason(Reason):
    def __init__(self,
                 antecedent: type[Any],
                 subsequent: type[Any],
                 **kwargs: object,
                 ) -> None:
        super().__init__(**kwargs)
        self.antecedent = antecedent
        self.subsequent = subsequent


class ProposedBaseClassListReason(APrecedesBReason):
    @override
    def text(self) -> str:
        return (f"{q(self.antecedent)} precedes {q(self.subsequent)} in the "
                "proposed based class list.")


class DirectSubclassReason(APrecedesBReason):
    @override
    def text(self) -> str:
        return (f"{q(self.antecedent)} precedes {q(self.subsequent)} because "
                "it inherits from it directly.")


class PivotedReason(APrecedesBReason):
    def __init__(self,
                 pivot: type[Any],
                 pivot_cause: type[Any] | None,
                 **kwargs: object,
                 ) -> None:
        super().__init__(**kwargs)  # pyright: ignore
        self.pivot = pivot
        self.pivot_cause = pivot_cause

    @override
    def text(self) -> str:
        if self.pivot_cause is None:
            return (f"{q(self.antecedent)} precedes {q(self.subsequent)} in "
                    f"{q(self.pivot)}'s MRO (and {q(self.pivot)} was in the "
                    "proposed based class list) because")
        return (f"{q(self.antecedent)} precedes {q(self.subsequent)} in "
                f"{q(self.pivot_cause)}'s "
                f"base class {q(self.pivot)}'s MRO because")


class SinglePivotedReason(PivotedReason):
    def __init__(self, **kwargs: object) -> None:
        super().__init__(**kwargs)  # pyright: ignore

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
            def add_subreason(x: type[Any]) -> None:
                self.subreasons.append(AInhertisFromBReason(x, self.pivot))
            add_subreason(self.antecedent)
            add_subreason(self.subsequent)


class AInhertisFromBReason(Reason):
    def __init__(self, ancestor: type[Any], child: type[Any], **kwargs: object) -> None:
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

    @override
    def text(self) -> str:
        a = self.ancestor
        c = self.child
        if self.via is None:
            return f"{q(a)} is a base class of {q(c)}"
        return f"{q(self.via)} is a base class of {q(c)} and"
