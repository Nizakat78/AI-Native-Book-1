# Chapter 2: Voice-to-Action with OpenAI Whisper

## Introduction

This chapter explores how to convert spoken language into robotic actions using OpenAI's Whisper model for speech recognition. By integrating Whisper, we can create a natural and intuitive way for humans to interact with and command robots.

## Setting Up Whisper for Voice Command Recognition

OpenAI's Whisper is a versatile speech-to-text model that can be used for a wide range of applications, including voice command recognition. To set up Whisper, you can use the following steps:

1.  **Install the Whisper Library**:
    ```bash
    pip install openai-whisper
    ```
2.  **Record or Provide an Audio File**: For this example, we assume you have an audio file (e.g., in `.wav` format) that contains a voice command.
3.  **Transcribe the Audio**: Use the following Python script to transcribe the audio file into text:
    ```python
    import whisper

    model = whisper.load_model("base")
    result = model.transcribe("path/to/your/audio.wav")
    print(result["text"])
    ```

## Mapping Voice to Actionable ROS 2 Commands

Once you have the transcribed text, you can map it to a specific robotic action. A simple approach is to use a dictionary or a set of `if/elif/else` statements to map keywords in the text to ROS 2 commands.

```python
def map_command_to_action(text):
    if "move forward" in text:
        return "ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0.2}, angular: {z: 0.0}}'"
    elif "stop" in text:
        return "ros2 topic pub /cmd_vel geometry_msgs/Twist '{linear: {x: 0.0}, angular: {z: 0.0}}'"
    # ... more mappings
    else:
        return None
```

## Providing Audio Examples, Code, and Diagrams

*(Placeholder: This section would include actual audio files, complete runnable code, and diagrams illustrating the voice-to-action pipeline.)*

**Audio Example**:
-   `move-forward.wav`: A recording of the phrase "robot, move forward."

**Code**:
-   A Python script that:
    1.  Listens for an audio input or takes a file path.
    2.  Uses Whisper to transcribe the audio.
    3.  Maps the transcribed text to a ROS 2 command.
    4.  Executes the ROS 2 command using `subprocess.run()`.

**Diagram**:
-   A flowchart showing the data flow from audio input to robotic action.

## Validating Recognition

To validate the voice command recognition system, you should test it with a variety of audio inputs, including:

-   **Different voices**: Male, female, different accents.
-   **Different phrasing**: "move forward," "go straight," "can you move forward?"
-   **Noisy environments**: Test the system's performance with background noise.

By analyzing the transcription accuracy and the robot's response, you can evaluate the effectiveness of the voice-to-action system and identify areas for improvement.
