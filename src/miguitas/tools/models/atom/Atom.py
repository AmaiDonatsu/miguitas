class Atom:
    def __init__(self, name: str, symbol: str, atomic_number: int):
        self.name = name
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.num_of_electrons = atomic_number # Asumiendo átomo neutro
        self.configuration = self._build_configuration()

    def _build_configuration(self):
        sublevels = []
        for n in range(1, 8):
            for l_val, symbol in enumerate(['s', 'p', 'd', 'f']):
                if l_val < n: # Regla cuántica: l < n
                    sublevels.append({
                        "name": f"{n}{symbol}",
                        "n": n,
                        "l": l_val,
                        "energy": n + l_val, 
                        "capacity": 2 * (2 * l_val + 1) 
                    })

        sublevels.sort(key=lambda x: (x["energy"], x["n"]))

        remaining = self.num_of_electrons
        result = []
        for sub in sublevels:
            if remaining <= 0: break
            
            take = min(remaining, sub["capacity"])
            result.append(f"{sub['name']}^{take}")
            remaining -= take
            
        return " ".join(result)

    def __str__(self):
        return f"Elemento: {self.name} ({self.symbol}) | Z: {self.atomic_number}\nConfiguración: {self.configuration}"

if __name__ == "__main__":
    element = Atom("Helio", "He", 2)
    print(element)