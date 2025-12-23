# Research: Module 3 – The AI-Robot Brain

This document outlines the research and decisions for the AI-Robot Brain module.

## Key Decisions

### Synthetic Data Generation Settings

-   **Decision**: Prioritize high-fidelity photorealistic scenes for synthetic data generation within NVIDIA Isaac Sim to maximize realism for AI training. Provide guidance on how to adjust settings for faster, simpler scenes, explaining the realism vs. performance trade-off for different use cases.
-   **Rationale**: The primary goal is to demonstrate advanced AI perception, which often benefits from realistic training data. Offering flexibility allows readers to optimize for their specific hardware or iteration speed.
-   **Alternatives considered**:
    -   **Exclusively use simple scenes**: This would limit the educational value by not showcasing the full capabilities of photorealistic simulation for AI.
    -   **Only high-fidelity scenes**: This could be computationally intensive and deter readers with less powerful hardware.

### VSLAM Algorithm Choice

-   **Decision**: Focus on the default Isaac ROS VSLAM implementation for ease of use and broad applicability. Discuss how to use built-in tools for tuning parameters and integrating with specific sensor configurations (e.g., different camera models), exploring the trade-off between ease of use and precision in various environments.
-   **Rationale**: Leveraging the optimized Isaac ROS stack provides a strong foundation. Demonstrating parameter tuning prepares readers for real-world scenarios where customization is often necessary.
-   **Alternatives considered**:
    -   **Implementing VSLAM from scratch**: Too complex and outside the scope of a textbook module on advanced perception.
    -   **Covering multiple VSLAM algorithms in depth**: Could lead to information overload without significant added value for the target audience.

### Nav2 Path-Planning Parameters

-   **Decision**: Present a range of Nav2 path-planning parameters, demonstrating their impact in both simple (e.g., clear, open space) and complex (e.g., cluttered, dynamic) humanoid navigation scenarios. Highlight the trade-off between plan complexity, computational load, and reproducibility for different bipedal robot movements.
-   **Rationale**: Nav2 is a widely used and highly configurable navigation stack in ROS 2. Showing a variety of scenarios helps readers understand its flexibility and limitations for humanoid robots.
-   **Alternatives considered**:
    -   **Only simple navigation scenarios**: Would not adequately cover the challenges of bipedal robot navigation.
    -   **Only complex navigation scenarios**: Could be overwhelming and difficult to reproduce for beginners.
