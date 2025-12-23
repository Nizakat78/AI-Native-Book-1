# Quickstart: Validating Module 3 Experiments

This guide provides instructions on how to run and validate the experiments from Module 3.

## Prerequisites

-   NVIDIA Graphics Card (RTX series or equivalent)
-   NVIDIA Isaac Sim (installed and configured)
-   ROS 2 (Foxy or later)
-   Isaac ROS (installed and configured)
-   Nav2 (installed and configured for ROS 2)
-   Git and a configured Git client

## Validation Checks

### 1. NVIDIA Isaac Sim Photorealistic Simulation

1.  **Clone the Repository**: Ensure you have the latest version of the `AI-Book` repository.
2.  **Navigate to Project**: Go to the specific Isaac Sim project directory within the repository.
3.  **Launch Simulation**: Open the project in Isaac Sim and launch the desired simulation scene.
4.  **Verify Synthetic Data Generation**:
    -   Ensure the simulation runs without errors.
    -   Verify that synthetic data (e.g., RGB, depth, segmentation masks) is being generated correctly as described in the chapter.
    -   Check for photorealistic rendering quality.

### 2. Isaac ROS & Hardware-Accelerated VSLAM

1.  **Launch Isaac Sim (if using simulated robot)**: Start the Isaac Sim environment with the humanoid robot and sensors.
2.  **Launch Isaac ROS VSLAM Pipeline**: Run the provided ROS 2 launch file for the VSLAM pipeline.
    ```bash
    ros2 launch <isaac_ros_package> <vslam_launch_file_name>.py
    ```
3.  **Verify VSLAM Performance**:
    -   Monitor the estimated robot pose in RViz or a similar visualization tool.
    -   Compare the estimated trajectory with the ground truth (if available in simulation).
    -   Check for real-time performance and accuracy as the robot moves.

### 3. Nav2 Path Planning for Bipedal Robots

1.  **Launch Simulation (e.g., Isaac Sim or Gazebo)**: Start the simulation with the humanoid robot and navigation stack.
2.  **Launch Nav2 Stack**: Run the provided ROS 2 launch file for the Nav2 stack, configured for bipedal robots.
    ```bash
    ros2 launch <nav2_package> <nav2_launch_file_name>.py
    ```
3.  **Set Navigation Goal**: Use RViz to set a navigation goal for the humanoid robot.
4.  **Verify Path Planning**:
    -   Observe the robot's movement; it should generate a feasible and collision-free path.
    -   Evaluate the efficiency and smoothness of the generated path.
    -   Check if the robot successfully reaches the target destination.

### 4. Cross-Checking with References

-   For each experiment, compare the setup and results to the official NVIDIA Isaac documentation, ROS 2 tutorials, or peer-reviewed papers that are cited in the chapter.
-   Ensure that the experiment's behavior aligns with expected outcomes and established benchmarks.
