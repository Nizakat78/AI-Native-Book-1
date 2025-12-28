<!--



Version change: 1.1.0 -> 1.2.0
Modified principles:
- Accuracy: Specified explicit sources (official docs, peer-reviewed papers).
- Clarity: Defined target audience (CS/robotics students).
- Reproducibility: Explicitly mentioned code, simulations, and experiments.
- Integration-first: Clarified as book + RAG chatbot.
Added sections:
- None
Removed sections:
- None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md
- ✅ .specify/templates/spec-template.md
- ✅ .specify/templates/tasks-template.md
- ✅ .specify/templates/commands/sp.constitution.md
- ⚠ pending README.md
- ⚠ pending docs/quickstart.md
Follow-up TODOs:
- TODO(README.md): Update project description to reflect new principles and chatbot integration.
- TODO(docs/quickstart.md): Add specific instructions for RAG chatbot setup and usage.
-->
# AI/Spec-driven textbook and RAG chatbot on Physical AI & Humanoid Robotics Constitution

## Core Principles

### Accuracy
All technical content must be derived from official documentation and peer-reviewed sources. Every claim must be source-backed with APA citations.

### Clarity
Content must be understandable for advanced computer science and robotics students. Technical jargon should be explained or used in a context where its meaning is clear.

### Reproducibility
All code examples, simulation setups, and experiments must be accompanied by step-by-step instructions and references, ensuring they are testable and can be recreated by the reader.

### Integration-first
The book content and the embedded RAG chatbot must function as a cohesive unit. The chatbot should primarily draw answers from the book's content.

## Key Standards

- All factual claims and technical implementations must be traceable to specified sources.
- Minimum 50% of sources must be peer-reviewed articles; the remainder from authoritative SDK/documentation.
- Zero plagiarism tolerance before deployment.
- Code examples must be runnable in their specified environments (ROS 2, Gazebo, NVIDIA Isaac, etc.).
- Writing clarity: Target Flesch-Kincaid grade 10-12.

## Constraints

- Word count: 15,000–20,000 words (entire book).
- Minimum 30 sources (peer-reviewed + SDK docs).
- Format: Docusaurus website deployed on GitHub Pages.
- Tech stack: Spec-Kit Plus, Claude Code, ROS 2, Gazebo, NVIDIA Isaac, OpenAI Agents, FastAPI, Neon, Qdrant.

## Success Criteria

- The book is fully published and structured by modules.
- The embedded RAG chatbot accurately answers questions based solely on the book's content and selected text.
- All content is fact-checked and reproducible.

## Governance

- This Constitution supersedes all other practices and documentation.
- Amendments require detailed documentation of rationale, user/stakeholder approval, and a migration plan for affected artifacts.
- All pull requests and reviews must verify compliance with this Constitution.
- Any deviation from stated principles or constraints must be explicitly justified and approved.

**Version**: 1.2.0 | **Ratified**: TODO(RATIFICATION_DATE): Please provide the original ratification date. | **Last Amended**: 2025-12-20

