"""
main.py - Servidor MCP para herramientas de química.

Este servidor expone herramientas que permiten a agentes AI
interactuar con modelos de átomos y moléculas usando un registro global.

Los átomos se crean con IDs únicos y persisten durante la sesión.
Las moléculas referencian átomos existentes, respetando la conservación de materia.
"""

from fastmcp import FastMCP
from miguitas.tools.chemistry import (
    # Herramientas de átomos
    create_atom,
    get_atom_info,
    list_atoms,
    # Herramientas de moléculas
    create_molecule,
    add_atom_to_molecule,
    connect_atoms,
    get_molecule_status,
    validate_molecule,
    list_molecules,
    # Herramientas de sesión
    get_session_stats,
    clear_session,
)

mcp = FastMCP("miguitasServer")

# =============================================================================
# HERRAMIENTAS DE ÁTOMOS
# =============================================================================

mcp.tool()(create_atom)
mcp.tool()(get_atom_info)
mcp.tool()(list_atoms)

# =============================================================================
# HERRAMIENTAS DE MOLÉCULAS
# =============================================================================

mcp.tool()(create_molecule)
mcp.tool()(add_atom_to_molecule)
mcp.tool()(connect_atoms)
mcp.tool()(get_molecule_status)
mcp.tool()(validate_molecule)
mcp.tool()(list_molecules)

# =============================================================================
# HERRAMIENTAS DE SESIÓN
# =============================================================================

mcp.tool()(get_session_stats)
mcp.tool()(clear_session)

# =============================================================================
# OTRAS HERRAMIENTAS
# =============================================================================

@mcp.tool()
def calculate_kinetic_energy(mass_kg: float, velocity_ms: float) -> str:
    """Calcula la energía cinética de un objeto. Útil para medir impactos de superhéroes."""
    energy = 0.5 * mass_kg * (velocity_ms ** 2)
    return f"La energía cinética resultante es de {energy} Joules. $$E_k = \\frac{{1}}{{2}}mv^2$$"


# =============================================================================
# RECURSOS
# =============================================================================

@mcp.resource("hero://stats/flash")
def get_flash_stats() -> str:
    return "Nombre: Barry Allen | Velocidad Máxima: Mach 10 | Resistencia: Alta"


@mcp.resource("chemistry://help/workflow")
def get_chemistry_workflow() -> str:
    """Flujo de trabajo para construir moléculas."""
    return """
# Flujo de Trabajo: Química en Miguitas

## Paso 1: Crear Átomos
Crea los átomos que necesitas. Cada átomo recibe un ID único.

```
create_atom("C", 6)  → C_1
create_atom("H", 1)  → H_1
create_atom("H", 1)  → H_2
create_atom("H", 1)  → H_3
create_atom("H", 1)  → H_4
```

## Paso 2: Verificar Átomos
Usa `list_atoms()` para ver todos los átomos y sus estados.
- 🟢 FREE = disponible para usar
- 🔴 BOUND = ya está en una molécula

## Paso 3: Crear Molécula
```
create_molecule("metano")
```

## Paso 4: Añadir Átomos a la Molécula
Usa los IDs de los átomos creados:
```
add_atom_to_molecule("metano", "C_1")
add_atom_to_molecule("metano", "H_1")
add_atom_to_molecule("metano", "H_2")
add_atom_to_molecule("metano", "H_3")
add_atom_to_molecule("metano", "H_4")
```

⚠️ IMPORTANTE: Un átomo solo puede estar en UNA molécula.
Si intentas añadir C_1 a otra molécula, recibirás un error.

## Paso 5: Conectar Átomos
```
connect_atoms("metano", "C_1", "H_1", "SINGLE")
connect_atoms("metano", "C_1", "H_2", "SINGLE")
connect_atoms("metano", "C_1", "H_3", "SINGLE")
connect_atoms("metano", "C_1", "H_4", "SINGLE")
```

## Paso 6: Validar
```
validate_molecule("metano")
```

## Números Atómicos Comunes
| Elemento | Símbolo | Z | Espacios |
|----------|---------|---|----------|
| Hidrógeno | H | 1 | 1 |
| Carbono | C | 6 | 4 |
| Nitrógeno | N | 7 | 3 |
| Oxígeno | O | 8 | 2 |
| Azufre | S | 16 | 2 |
| Cloro | Cl | 17 | 1 |
"""


@mcp.resource("chemistry://help/conservation")
def get_conservation_help() -> str:
    """Información sobre la conservación de materia."""
    return """
# Conservación de Materia

Este sistema implementa el principio de conservación de materia:

## Regla Principal
Un átomo solo puede existir en UN lugar a la vez.

## Estados de un Átomo
- **FREE (🟢)**: El átomo existe pero no pertenece a ninguna molécula.
- **BOUND (🔴)**: El átomo pertenece a una molécula específica.

## Comportamiento
1. Al crear un átomo con `create_atom()`, queda en estado FREE.
2. Al añadirlo a una molécula con `add_atom_to_molecule()`, cambia a BOUND.
3. Si intentas añadir un átomo BOUND a otra molécula, el sistema rechaza la operación.

## Ejemplo de Error
```
> create_atom("C", 6)           # C_1 creado (FREE)
> create_molecule("metano")
> add_atom_to_molecule("metano", "C_1")  # C_1 ahora BOUND
> create_molecule("etano")
> add_atom_to_molecule("etano", "C_1")   # ERROR: C_1 ya está en "metano"
```

## Solución
Crea un nuevo átomo para la segunda molécula:
```
> create_atom("C", 6)           # C_2 creado (FREE)
> add_atom_to_molecule("etano", "C_2")  # OK
```
"""


def main():
    mcp.run()


if __name__ == "__main__":
    main()