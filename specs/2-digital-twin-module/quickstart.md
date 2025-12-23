# Quickstart: Validating Module 2 Examples

This guide provides instructions on how to run and validate the simulation examples from Module 2.

## Prerequisites

-   ROS 2 (Foxy or later)
-   Gazebo 11
-   Unity Hub with a compatible Unity version (e.g., 2021.3 LTS)
-   Git and a configured Git client

## Validation Checks

### 1. Gazebo Simulations

1.  **Clone the Repository**: Ensure you have the latest version of the `AI-Book` repository.
2.  **Navigate to Example**: Go to the specific Gazebo example directory within the repository.
3.  **Launch Simulation**: Run the provided launch file.
    ```bash
    ros2 launch <package_name> <launch_file_name>.py
    ```
4.  **Verify**:
    -   The Gazebo world loads without errors.
    -   Objects (e.g., the humanoid robot) appear correctly.
    -   Physics interactions (e.g., gravity, collisions) behave as described in the chapter.

### 2. Unity Scenes

1.  **Open in Unity**: Add the cloned repository's Unity project to your Unity Hub and open it.
2.  **Navigate to Scene**: In the Project window, find and open the scene file corresponding to the chapter example.
3.  **Enter Play Mode**: Press the "Play" button in the Unity editor.
4.  **Verify**:
    -   The scene renders correctly without visual artifacts.
    -   Humanoid robot interactions, if any, function as described.

### 3. Sensor Data Validation

1.  **Run Simulation**: Launch the Gazebo simulation that includes the sensor example.
2.  **Echo Topic**: Use `ros2 topic echo` to inspect the output of the simulated sensor's topic. For example, for a LiDAR sensor publishing on `/scan`:
    ```bash
    ros2 topic echo /scan
    ```
3.  **Verify**:
    -   The topic is publishing data.
    -   The data format is consistent with the sensor type (e.g., `sensor_msgs/LaserScan` for LiDAR).
    -   The data values are realistic for the simulated environment (e.g., range values change as the robot moves).

### 4. Cross-Checking with References

-   For each example, compare the setup and behavior to the official documentation from Gazebo, Unity, or ROS 2 that is cited in the chapter.
-   Ensure that the simulation's behavior aligns with the principles described in the reference material.
