# Propuesta de Arquitectura: Registro Global de Átomos (MCP v2)

## Objetivo
Refactorizar el MCP "Miguitas" para pasar de un modelo de **Instanciación Local** a uno de **Persistencia Global**. Esto permite crear átomos independientemente de las moléculas y gestionarlos mediante IDs únicos.

## 1. Diagrama de Clases (Estructura)

```mermaid
classDiagram
    class GlobalStore {
        - Dict~ID, Atom~ atoms
        - Dict~Name, Molecule~ molecules
        + create_atom(Z, symbol) -> AtomID
        + get_atom(AtomID) -> Atom
    }

    class Atom {
        + String id
        + int atomic_number
        + String state (FREE | BOUND)
        + String bound_molecule_id
    }

    class Molecule {
        + String name
        + List~String~ atom_ids
        + add_atom(AtomID)
    }

    GlobalStore "1" *-- "*" Atom : Contiene
    GlobalStore "1" *-- "*" Molecule : Contiene
    Molecule ..> Atom : Referencia (por ID)
```

## 2. Flujo de Operaciones (Sequence Diagram)

```mermaid
sequenceDiagram
    participant User
    participant System
    participant Store

    User->>System: create_atom(Z=6)
    System->>Store: Generar ID único (ej: "C_1")
    Store->>System: Guardar Atom(id="C_1", state="FREE")
    System->>User: Retorna ID: "C_1"

    User->>System: create_molecule("Metano")
    System->>Store: Crear nueva Molécula

    User->>System: add_atom("Metano", "C_1")
    System->>Store: check_status("C_1")
    
    alt Átomo Libre
        Store-->>System: OK
        System->>Store: Update "C_1" state -> BOUND("Metano")
        System->>Store: Link "C_1" to "Metano"
        System->>User: Éxito
    else Átomo Ocupado
        Store-->>System: Error (Ya en uso)
        System->>User: Error: Violación de conservación de materia
    end
```

## 3. Beneficios Técnicos
1.  **Reutilización:** Permite preparar un "banco de átomos" antes de empezar experimentos.
2.  **Trazabilidad:** Cada átomo tiene identidad única. Si un experimento falla, sabes exactamente qué átomo (ID) causó el problema.
3.  **Realismo:** Impide que el mismo átomo exista en dos moléculas simultáneamente.
