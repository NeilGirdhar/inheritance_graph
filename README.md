# Inheritance Graph
A tool to help debug inheritance failures.

# Example

    from inheritance_graph import mro_check

    class Dec:
        pass

    class Dif:
        pass

    class E:
        pass

    class R(E):
        pass

    class Err(Dif, R):
        pass

    class B(E, Dec, Dif):
        pass

    mro_check((B, Err))

displays

    Cycle found:
       Dif precedes R in Err's MRO (and Err was in the proposed based class list) because
         Dif is a base class of Err
         R is a base class of Err
       R precedes E because it inherits from it directly.
       E precedes Dec in B's MRO (and B was in the proposed based class list) because
         E is a base class of B
         Dec is a base class of B
       Dec precedes Dif in B's MRO (and B was in the proposed based class list) because
         Dec is a base class of B
         Dif is a base class of B
