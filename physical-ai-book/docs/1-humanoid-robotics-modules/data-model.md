# Data Model: AI-native Textbook

This document defines the data model for the AI-native textbook.

## Entities

### Module

Represents a top-level section of the textbook.

**Attributes**:
- `title` (string): The title of the module.
- `focus` (string): A brief description of the module's focus.

### Chapter

Represents a subsection of a module.

**Attributes**:
- `title` (string): The title of the chapter.
- `content` (string, Markdown): The full content of the chapter in Markdown format.

## Relationships

- A `Module` can have one or more `Chapters`.
