# Research: Module 2 – The Digital Twin

This document outlines the research and decisions for the Digital Twin module.

## Key Decisions

### Simulation Parameters (Gazebo)

- **Decision**: Start with default Gazebo physics parameters for initial examples to ensure simplicity and accessibility. Introduce a dedicated section in "Best Practices & Reproducibility" to discuss the impact of custom parameters (e.g., friction, collision models) on simulation fidelity and provide an example of tuning them.
- **Rationale**: This approach allows beginners to get started quickly while still providing the necessary depth for more advanced users who need higher fidelity. It balances ease of learning with technical completeness.
- **Alternatives considered**:
    - **Always use custom values**: This would increase the initial learning curve and might be unnecessary for many introductory examples.
    - **Only use default values**: This would limit the educational value by not explaining how to achieve higher-fidelity simulations.

### Unity Environment Complexity

- **Decision**: Use simplified, prototype-level Unity environments for the core teaching examples. A single, more complex, high-fidelity scene will be created and provided as a downloadable asset to demonstrate advanced rendering and interaction without requiring the reader to build it from scratch.
- **Rationale**: This focuses the reader's effort on understanding the concepts rather than on complex 3D modeling. Providing a pre-built high-fidelity scene offers a clear, aspirational example of what's possible.
- **Alternatives considered**:
    - **Build high-fidelity scenes step-by-step**: Too time-consuming and outside the core scope of robotics simulation.
    - **Use only simple prototypes**: Fails to demonstrate the "high-fidelity rendering" aspect mentioned in the success criteria.

### Sensor Simulation Method

- **Decision**: Primarily use the built-in sensor models provided by Gazebo (e.g., `<camera>`, `<ray>`) for LiDAR, Depth Camera, and IMU simulation. Include one example of using a third-party sensor plugin to illustrate how to extend Gazebo's capabilities.
- **Rationale**: Built-in sensors are well-documented and sufficient for most introductory purposes. Showing a plugin example provides a path for more advanced users who need more realistic sensor noise or specific sensor behaviors.
- **Alternatives considered**:
    - **Exclusively use plugins**: This would add unnecessary complexity and dependency management for basic examples.
    - **Exclusively use built-in sensors**: This wouldn't fully prepare students for real-world scenarios where custom or more advanced sensor models are often required.
