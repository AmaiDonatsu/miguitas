# Miguitas 🧪

Investigación teórica de partículas subatómicas y herramientas científicas.

## Requisitos

Este proyecto utiliza [uv](https://docs.astral.sh/uv/) para la gestión de dependencias y el entorno virtual. Asegúrate de tenerlo instalado.

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/AmaiDonatsu/miguitas.git
   cd miguitas
   ```

2. **Configura el entorno:**
   Copia el archivo de ejemplo de variables de entorno y configúralo (si aplica):
   ```bash
   cp .env.example .env
   ```

3. **Sincroniza las dependencias:**
   ```bash
   uv sync
   ```

## Ejecución

Para iniciar el servidor MCP (Model Context Protocol):

```bash
uv run miguitas
```

O si prefieres activar el entorno virtual manualmente:

```bash
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

miguitas
```

## Herramientas Incluidas

- **calculate_kinetic_energy**: Calcula la energía cinética (Joules).
- **create_atom**: Genera un modelo atómico y su configuración electrónica.
- **get_flash_stats**: Recurso con información sobre Flash.
