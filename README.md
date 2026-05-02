> [!CAUTION]
> THIS IS A WORK-IN-PROGRESS AND CURRENTLY JUST IN A PROOF-OF-CONCEPT STATE

# ANVision
## Introduction
ANVision is a robot vision system intended for the First Robotics Competition (FRC). The primary goal is to provide high framerate robot localization on the field using commonly available processors and cameras. The hope is to allow the robot to almost entirely rely on vision for localization to eliminate the problems with wheel odometry.

## Target Hardware
The hardware this project is intentionally limited to keep the project focused. The project may work on other platforms and with other cameras, but there is no guarantee it will maintain the level of performance seen with the targeted hardware. 

### Processors Platform

- Raspberry Pi 5 and CM5
- Orange PI 5 and its variants

### Cameras
- Arducam OV9281 1.3MP Camera (USB & CSI versions)
- Arducam OV2311 2MP Camera (USB & CSI versions)

## Initial Project Feature Goals
These are the initial goals for the project, though some may need to be dropped based on the final capability of the system

- AprilTag detection at max framerate of supported cameras with multiple Cameras
  - 2 cameras on Raspberry Pi 5
  - 3 cameras on Orange Pi 5
- On processor extrinsic calculation
  - The pose returned will be the estimated position of the origin of your robot
- Estimated standard deviation for PoseEstimation calculated on co-processor
- Multi-Tag/Multi-Camera pose integration
  - Standard deviation of each tag will be used to weight the pose estimation for each tag used
- NetworkTables interface for robot communications
- Rely on PTP to synchronize time with SystemCore
  - PTP will need to be installed on SystemCore the time to by synchronized properly
- Basic web UI
  - Allow viewing camera feed with or without graphics overlay
  - View estimated robot pose and other results
  - Import and Export configurations
- Basic image logging 
  
## Planned Future Feature

- Advanced Web UI
  - Geometric and intensity Calibration interface
  - Graphics draw as overlay on client side instead of written to the image
  - Camera Configuration
    - Spare cameras will be able to be saved to the processor for quick swap-out of a damaged camera
- Visual Odometry
  - For when AprilTags are not visible for a given camera
  - Should be able to be run in parallel with the AprilTag search to improve accuracy of results, but may impact framerate
- Inter-processor multi-tag integration
- Onboard Kalman-Filter for integrating
  - Integrates Visual Odometry and AprilTag results into a single pose result
- Perform field calibration  with a single camera and transfer to other cameras
  - Will require all cameras to have an intensity calibration
  - Should be able to work with a battery-powered, offboard camera/processor setup, so the robot will not be needed
- Dynamic image intensity control based on current estimated pose for fields with inconsistent lighting
- Post match field calibration to account for lighting changes throughout the day
- Dynamic AprilTag and VisualOdometry switching when no AprilTag should be in view of a camera
  - This allows the robot pose to be updated when no AprilTag is in view
