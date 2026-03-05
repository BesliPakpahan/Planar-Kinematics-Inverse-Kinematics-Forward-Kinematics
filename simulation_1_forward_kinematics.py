"""
Simulation 1: Forward Kinematics Demonstration
Shows how changing joint angles affects end-effector position

Author: BESLI SAUT MARITO PAKPAHAN
Course: SEMS6 - Legged Robot
Date: March 2026
"""

import numpy as np
import os
from kinematics import PlanarRobot4Link
from visualizer import RobotVisualizer


def main():
    print("=" * 60)
    print("SIMULATION 1: Forward Kinematics Demonstration")
    print("=" * 60)
    
    # Create output directory
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize robot with link lengths [L1, L2, L3, L4]
    link_lengths = [1.0, 1.0, 0.8, 0.6]
    robot = PlanarRobot4Link(link_lengths)
    viz = RobotVisualizer(robot, figsize=(12, 12))
    
    print(f"\nRobot Configuration:")
    print(f"  Link lengths: {link_lengths}")
    min_reach, max_reach = robot.get_workspace_limits()
    print(f"  Workspace: Min reach = {min_reach:.2f}m, Max reach = {max_reach:.2f}m")
    
    # ========================================
    # Part 1: Different static configurations
    # ========================================
    print("\n" + "-" * 60)
    print("Part 1: Static Configurations")
    print("-" * 60)
    
    configurations = [
        (np.array([0, 0, 0, 0]), "All joints at 0°"),
        (np.array([np.pi/2, 0, 0, 0]), "θ1=90°, others 0°"),
        (np.array([np.pi/4, np.pi/4, np.pi/4, np.pi/4]), "All joints at 45°"),
        (np.array([np.pi/3, -np.pi/6, np.pi/4, -np.pi/8]), "Mixed configuration"),
        (np.array([0, np.pi/2, -np.pi/2, np.pi/4]), "Folded configuration"),
        (np.array([np.pi, 0, 0, 0]), "θ1=180°, extended"),
    ]
    
    configs_with_positions = []
    
    for i, (angles, description) in enumerate(configurations):
        positions, end_pos = robot.forward_kinematics(angles)
        
        print(f"\nConfiguration {i+1}: {description}")
        print(f"  Joint angles (deg): [{', '.join([f'{np.rad2deg(a):.1f}' for a in angles])}]")
        print(f"  End-effector position: ({end_pos[0]:.3f}, {end_pos[1]:.3f})")
        
        # Save snapshot
        filename = f"{output_dir}/fk_config_{i+1}.png"
        viz.save_snapshot(angles, filename=filename, show_workspace=True)
        
        configs_with_positions.append((angles, f"Config {i+1}: {description}"))
    
    # Create comparison plot
    print(f"\nCreating comparison plot...")
    viz.create_comparison_plot(
        configs_with_positions,
        filename=f"{output_dir}/fk_comparison.png"
    )
    
    # ========================================
    # Part 2: Animated joint motions
    # ========================================
    print("\n" + "-" * 60)
    print("Part 2: Animated Joint Motions")
    print("-" * 60)
    
    # Animation 1: Rotating joint 1
    print("\nAnimation 1: Rotating Joint 1 (0° to 360°)")
    n_frames = 120
    angles_sequence_1 = []
    for i in range(n_frames):
        theta1 = (2 * np.pi * i) / n_frames
        angles = np.array([theta1, np.pi/6, -np.pi/12, np.pi/8])
        angles_sequence_1.append(angles)
    
    viz.animate_trajectory(
        angles_sequence_1,
        filename=f"{output_dir}/fk_animation_joint1.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # Animation 2: Rotating all joints together
    print("\nAnimation 2: Rotating All Joints Simultaneously")
    angles_sequence_2 = []
    for i in range(n_frames):
        t = (2 * np.pi * i) / n_frames
        angles = np.array([
            t,
            0.8 * np.sin(t),
            0.6 * np.cos(2*t),
            0.4 * np.sin(3*t)
        ])
        angles_sequence_2.append(angles)
    
    viz.animate_trajectory(
        angles_sequence_2,
        filename=f"{output_dir}/fk_animation_all_joints.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # Animation 3: Wave motion
    print("\nAnimation 3: Wave Motion Pattern")
    angles_sequence_3 = []
    for i in range(n_frames):
        t = (4 * np.pi * i) / n_frames
        angles = np.array([
            0.3 * np.sin(t),
            0.5 * np.sin(t - np.pi/4),
            0.4 * np.sin(t - np.pi/2),
            0.3 * np.sin(t - 3*np.pi/4)
        ])
        angles_sequence_3.append(angles)
    
    viz.animate_trajectory(
        angles_sequence_3,
        filename=f"{output_dir}/fk_animation_wave.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # ========================================
    # Part 3: Joint space exploration
    # ========================================
    print("\n" + "-" * 60)
    print("Part 3: Joint Space Exploration")
    print("-" * 60)
    
    # Create a smooth path through joint space
    print("\nCreating smooth joint space trajectory...")
    n_waypoints = 8
    waypoints = [
        np.array([0, 0, 0, 0]),
        np.array([np.pi/2, 0, 0, 0]),
        np.array([np.pi/2, np.pi/3, 0, 0]),
        np.array([np.pi/2, np.pi/3, np.pi/4, 0]),
        np.array([np.pi/2, np.pi/3, np.pi/4, np.pi/6]),
        np.array([np.pi/4, np.pi/6, np.pi/8, np.pi/12]),
        np.array([0, np.pi/2, -np.pi/4, np.pi/8]),
        np.array([0, 0, 0, 0]),
    ]
    
    # Interpolate between waypoints
    n_interpolation = 20
    angles_sequence_4 = []
    
    for i in range(len(waypoints) - 1):
        start = waypoints[i]
        end = waypoints[i + 1]
        
        for j in range(n_interpolation):
            alpha = j / n_interpolation
            angles = (1 - alpha) * start + alpha * end
            angles_sequence_4.append(angles)
    
    viz.animate_trajectory(
        angles_sequence_4,
        filename=f"{output_dir}/fk_animation_joint_space.mp4",
        fps=30,
        show_trajectory=True
    )
    
    print("\n" + "=" * 60)
    print("SIMULATION 1 COMPLETE!")
    print("=" * 60)
    print(f"\nOutputs saved to '{output_dir}/' directory:")
    print(f"  - 6 static configuration snapshots (fk_config_*.png)")
    print(f"  - 1 comparison plot (fk_comparison.png)")
    print(f"  - 4 animations (fk_animation_*.mp4)")
    print("\nTotal files: 11")


if __name__ == "__main__":
    main()
