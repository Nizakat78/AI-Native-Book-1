# Data Model: Module 2 – The Digital Twin

This document defines the data entities for the Digital Twin module content.

## Entities

### Module

Represents the top-level container for this section of the textbook.

-   **title**: "Module 2 – The Digital Twin"
-   **focus**: "Physics simulation, environment building, and sensor emulation"

### Chapter

Represents one of the five chapters within the module.

-   **title** (string): The title of the chapter (e.g., "Introduction to Digital Twins").
-   **content** (Markdown): The body of the chapter, including text, code snippets, and image/diagram placeholders.

### Simulation Asset

Represents a downloadable asset used in the examples.

-   **name** (string): A descriptive name for the asset (e.g., "High-Fidelity Unity Scene").
-   **description** (string): A brief explanation of the asset.
-   **path** (string): The path to the asset in the project's Git repository.

## Relationships

-   The **Module** contains five **Chapter** entities.
-   **Chapters** may reference one or more **Simulation Assets**.
