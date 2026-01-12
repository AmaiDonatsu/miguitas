class Molecule:
    def __init__(self, name: str, formula: str, atoms: list) -> None:
        self.name = name
        self.formula = formula
        self.atoms = atoms

    def _build_molecule(self):
        structure = []
        for group in self.atoms:
            for atom in group:
                pass
        
     
        pass

"""
difernetes listas de listas de átomos 

metano example
{
    C: {
        lastLevel: "2"
        num_electrons: "4",

        1:  
    }
    
}

""" 