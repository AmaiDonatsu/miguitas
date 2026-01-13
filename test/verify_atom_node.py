from miguitas.tools.models.atom.Atom import Atom

def test_atom_node():
    print("Verificando Atom como Nodo...")
    
    # Hidrógeno
    h = Atom("Hidrógeno", "H", 1)
    print(f"\n{h}")
    assert h.available_spaces == 1, f"Error en Hidrógeno: se esperaba 1, se obtuvo {h.available_spaces}"
    
    # Carbono
    c = Atom("Carbono", "C", 6)
    print(f"\n{c}")
    assert c.available_spaces == 4, f"Error en Carbono: se esperaba 4, se obtuvo {c.available_spaces}"
    
    # Oxígeno
    o = Atom("Oxígeno", "O", 8)
    print(f"\n{o}")
    assert o.available_spaces == 2, f"Error en Oxígeno: se esperaba 2, se obtuvo {o.available_spaces}"

    # Neón (Gases nobles - octeto completo)
    ne = Atom("Neón", "Ne", 10)
    print(f"\n{ne}")
    assert ne.available_spaces == 0, f"Error en Neón: se esperaba 0, se obtuvo {ne.available_spaces}"

    print("\n¡Todas las verificaciones pasaron!")

if __name__ == "__main__":
    try:
        test_atom_node()
    except AttributeError as e:
        print(f"\nFallo esperado (aún no implementado): {e}")
    except AssertionError as e:
        print(f"\nFallo en la aserción: {e}")
    except Exception as e:
        print(f"\nError inesperado: {e}")
