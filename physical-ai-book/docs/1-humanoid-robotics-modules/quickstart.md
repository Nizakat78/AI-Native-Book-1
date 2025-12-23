# Quickstart: Contributing to the AI-native Textbook

This guide explains how to contribute to the AI-native textbook project.

## Prerequisites

- Node.js and npm
- Git
- A text editor (e.g., VS Code)

## Setup

1.  Clone the repository.
2.  Install the dependencies:
    ```bash
    npm install
    ```

## Workflow

The project follows a spec-driven workflow:

1.  **Specify**: Create a feature specification for the content you want to generate using the `/sp.specify` command.
2.  **Plan**: Create a technical plan for the feature using the `/sp.plan` command.
3.  **Write**: Use the AI-assisted writing tools to generate the content based on the spec and plan.
4.  **Review**: Review the generated content against the quality validation checklist.
5.  **Publish**: Once the content is approved, it can be published by merging it into the main branch.

## Running the Docusaurus Site Locally

To preview the book locally, run the following command:

```bash
npm start
```

This will start a local development server and open up a browser window. Most changes are reflected live without having to restart the server.
