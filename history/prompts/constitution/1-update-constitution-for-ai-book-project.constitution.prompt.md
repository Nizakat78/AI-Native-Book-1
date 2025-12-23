---
id: 1
title: Update Constitution for AI Book Project
stage: constitution
date: 2025-12-21
surface: agent
model: gemini
feature: none
branch: 1-ai-in-robotics-m1s4
user: TODO(USER)
command: /sp.constitution
labels: [constitution,documentation]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

/sp.constitution Project: AI/Spec-driven textbook and RAG chatbot on Physical AI & Humanoid Robotics

Core principles:
- Accuracy from official docs and peer-reviewed sources
- Clarity for CS/robotics students
- Reproducibility of code, simulations, and experiments
- Integration-first (book + RAG chatbot)

Key standards:
- All claims must be source-backed (APA citations)
- ≥50% sources from peer-reviewed or official SDK docs
- Zero plagiarism tolerance
- Code examples must be runnable

Constraints:
- Word count: 15k–20k
- Minimum 30 sources
- Format: Docusaurus book deployed on GitHub Pages
- Tech stack: Spec-Kit Plus, Claude Code, ROS 2, Gazebo, NVIDIA Isaac, OpenAI Agents, FastAPI, Neon, Qdrant

Success criteria:
- Book fully published and structured by modules
- Embedded RAG chatbot answers from book content and selected text
- All content fact-checked and reproducible

## Response snapshot

I have updated the constitution to version 1.2.1 to reflect today's date. The core principles and standards remain unchanged.

Here is a suggested commit message:

```
docs: amend constitution to v1.2.1 (date update)
```

## Outcome

- ✅ Impact: Updated the constitution file with the current date and version.
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: none
- 🧠 Reflection: The user's request was a re-run of a previous request. The constitution was already up-to-date, except for the date. I updated the date and version.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): null
