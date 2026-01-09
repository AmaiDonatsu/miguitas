from fastmcp import FastMCP
from miguitas.tools.chemistry import create_atom

mcp = FastMCP("miguitasServer")

mcp.tool()(create_atom)

@mcp.tool()
def calculate_kinetic_energy(mass_kg: float, velocity_ms: float) -> str:
    """Calcula la energía cinética de un objeto. Útil para medir impactos de superhéroes."""
    # Usamos LaTeX para la explicación científica
    # E_k = 1/2 * m * v^2
    energy = 0.5 * mass_kg * (velocity_ms ** 2)
    return f"La energía cinética resultante es de {energy} Joules. $$E_k = \\frac{1}{2}mv^2$$"


@mcp.resource("hero://stats/flash")
def get_flash_stats() -> str:
    return "Nombre: Barry Allen | Velocidad Máxima: Mach 10 | Resistencia: Alta"

def main():
    mcp.run()

if __name__ == "__main__":
    main()