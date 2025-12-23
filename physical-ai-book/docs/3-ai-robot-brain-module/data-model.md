# Data Model: Module 3 – The AI-Robot Brain

This document defines the data entities for the AI-Robot Brain module content.

## Entities

### Module

Represents the top-level container for this section of the textbook.

-   **title**: "Module 3 – The AI-Robot Brain"
-   **focus**: "Advanced perception, simulation, and bipedal robot navigation"

### Chapter

Represents one of the five chapters within the module.

-   **title** (string): The title of the chapter (e.g., "Introduction to the AI-Robot Brain").
-   **content** (Markdown): The body of the chapter, including text, code snippets, and image/diagram placeholders.

### Simulation Experiment

Represents a self-contained simulation or experiment project for the module.

-   **name** (string): A descriptive name for the experiment (e.g., "Isaac Sim Photorealistic Scene").
-   **description** (string): A brief explanation of the experiment's goal.
-   **path** (string): The path to the experiment's files in the project's Git repository.

## Relationships

-   The **Module** contains five **Chapter** entities.
-   **Chapters** may reference one or more **Simulation Experiment** entities.
