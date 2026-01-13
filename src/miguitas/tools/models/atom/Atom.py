class Atom:
    def __init__(self, name: str, symbol: str, atomic_number: int):
        self.name = name
        self.symbol = symbol
        self.atomic_number = atomic_number
        self.num_of_electrons = atomic_number # Asumiendo átomo neutro
        self._config_data = self._calculate_configuration()
        self.configuration = self._config_data["string"]
        self.valence_electrons = self._config_data["valence_count"]
        self.available_spaces = self._config_data["available"]

    @property
    def inputs(self):
        """Representa el átomo como nodo: sus entradas son los espacios disponibles."""
        return self.available_spaces

    def _calculate_configuration(self):
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
        result_str = []
        valence_map = {} # n -> electron_count
        
        for sub in sublevels:
            if remaining <= 0: break
            
            take = min(remaining, sub["capacity"])
            result_str.append(f"{sub['name']}^{take}")
            
            n = sub["n"]
            valence_map[n] = valence_map.get(n, 0) + take
            
            remaining -= take
            
        # Determinar capa de valencia (el n más alto alcanzado)
        if not valence_map:
            return {"string": "", "valence_count": 0, "available": 0}
            
        max_n = max(valence_map.keys())
        valence_count = valence_map[max_n]
        
        # Capacidad de la capa de valencia (Regla del Octeto / Dueto)
        # Para n=1 (H, He), la capacidad es 2.
        # Para n>1, consideramos s y p para el octeto (8).
        capacity = 2 if max_n == 1 else 8
        available = max(0, capacity - valence_count)
            
        return {
            "string": " ".join(result_str),
            "valence_count": valence_count,
            "available": available
        }

    def __str__(self):
        node_info = f" | Entradas de nodo: {self.available_spaces}"
        return f"Elemento: {self.name} ({self.symbol}) | Z: {self.atomic_number}{node_info}\nConfiguración: {self.configuration}"

if __name__ == "__main__":
    element = Atom("Helio", "He", 2)
    print(element)