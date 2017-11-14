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
