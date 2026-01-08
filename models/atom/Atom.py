class Atom:
    def __init__(self, name: str, atomic_number: int, num_of_electrons: int = None, electron_configuration: str = None):
        self.name = name
        self.atomic_number = atomic_number
        self.num_of_electrons = num_of_electrons
        self.electron_configuration = electron_configuration

    def _electron_configuration(self):
        if (self.num_of_electrons is None):
            self.num_of_electrons = self._calculate_number_of_electrons()
            num_of_electrons = self.num_of_electrons

            n=1
            while num_of_electrons > 0:
                ls = [for in ORBITALS.get(lambda x: x["l"] == n-1)]
                
            
        return self.electron_configuration

    def _calculate_number_of_electrons(self):
        number_of_electrons = self.atomic_number
        return number_of_electrons
    def __str__(self):
        return f"{self.name} ({self.atomic_number})"


def calculate_energy(n):
    return n + 1

ORBITALS = {
    "s": {
        "l": 0,
        "electrons": 2
    },
    "p": {
        "l": 1,
        "electrons": 6
    },
    "d": {
        "l": 2,
        "electrons": 10
    },
    "f": {
        "l": 3,
        "electrons": 14
    }
}
