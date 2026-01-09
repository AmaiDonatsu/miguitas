from miguitas.tools.models.atom.Atom import Atom

def create_atom(name: str, symbol: str, atomic_number: int) -> str:
    """Crea un átomo y devuelve su configuración electrónica."""
    atom = Atom(name=name, symbol=symbol, atomic_number=atomic_number)
    return str(atom)