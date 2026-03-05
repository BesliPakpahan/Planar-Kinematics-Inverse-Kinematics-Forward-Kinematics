"""
Simulation 3: Advanced Trajectory Following
Demonstrates smooth trajectory following with different path types

Author: BESLI SAUT MARITO PAKPAHAN
Course: SEMS6 - Legged Robot
Date: March 2026
"""

import numpy as np
import os
from kinematics import PlanarRobot4Link
from visualizer import RobotVisualizer


def generate_spiral_path(n_points=200, revolutions=3, max_radius=2.5):
    """Generate spiral trajectory"""
    path = []
    for i in range(n_points):
        t = (2 * np.pi * revolutions * i) / n_points
        r = max_radius * (i / n_points)
        x = r * np.cos(t)
        y = r * np.sin(t) + 1.0
        path.append([x, y])
    return np.array(path)


def generate_heart_path(n_points=200, scale=1.5):
    """Generate heart-shaped trajectory"""
    path = []
    for i in range(n_points):
        t = (2 * np.pi * i) / n_points
        # Parametric heart equation
        x = 16 * np.sin(t)**3
        y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
        # Normalize and scale
        path.append([scale * x / 20, scale * y / 20 + 1.5])
    return np.array(path)


def generate_star_path(n_points=200, outer_radius=2.0, inner_radius=0.8, n_points_star=5):
    """Generate star trajectory"""
    path = []
    angle_step = 2 * np.pi / (2 * n_points_star)
    
    # Generate star vertices
    vertices = []
    for i in range(2 * n_points_star):
        angle = i * angle_step
        radius = outer_radius if i % 2 == 0 else inner_radius
        vertices.append([radius * np.cos(angle - np.pi/2), 
                        radius * np.sin(angle - np.pi/2) + 1.5])
    
    # Close the path
    vertices.append(vertices[0])
    
    # Interpolate between vertices
    points_per_segment = n_points // (2 * n_points_star)
    for i in range(len(vertices) - 1):
        start = np.array(vertices[i])
        end = np.array(vertices[i + 1])
        
        for j in range(points_per_segment):
            alpha = j / points_per_segment
            point = (1 - alpha) * start + alpha * end
            path.append(point)
    
    return np.array(path)


def generate_infinity_path(n_points=200, width=2.0, height=1.5):
    """Generate infinity symbol (lemniscate) trajectory"""
    path = []
    for i in range(n_points):
        t = (2 * np.pi * i) / n_points
        # Lemniscate of Bernoulli
        scale = 1 / (1 + np.sin(t)**2)
        x = width * scale * np.cos(t)
        y = height * scale * np.sin(t) * np.cos(t) + 1.5
        path.append([x, y])
    return np.array(path)


def generate_custom_text_path(n_points=300):
    """Generate path that spells 'IK' (Inverse Kinematics)"""
    path = []
    
    # Letter 'I' (vertical line)
    for i in range(n_points // 3):
        alpha = i / (n_points // 3)
        path.append([-1.5, 0.5 + 2.0 * alpha])
    
    # Move to 'K'
    for i in range(n_points // 6):
        alpha = i / (n_points // 6)
        path.append([-1.5 + 1.0 * alpha, 2.5])
    
    # Letter 'K' - vertical line
    for i in range(n_points // 4):
        alpha = i / (n_points // 4)
        path.append([-0.5, 2.5 - 2.0 * alpha])
    
    # K - upper diagonal
    for i in range(n_points // 6):
        alpha = i / (n_points // 6)
        path.append([-0.5 + 1.0 * alpha, 1.5 + 1.0 * alpha])
    
    # Back to middle
    for i in range(n_points // 6):
        alpha = i / (n_points // 6)
        path.append([0.5 - 1.0 * alpha, 2.5 - 1.0 * alpha])
    
    # K - lower diagonal
    for i in range(n_points // 6):
        alpha = i / (n_points // 6)
        path.append([-0.5 + 1.0 * alpha, 1.5 - 1.0 * alpha])
    
    return np.array(path)


def main():
    print("=" * 60)
    print("SIMULATION 3: Advanced Trajectory Following")
    print("=" * 60)
    
    # Create output directory
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize robot
    link_lengths = [1.0, 1.0, 0.8, 0.6]
    robot = PlanarRobot4Link(link_lengths)
    viz = RobotVisualizer(robot, figsize=(12, 12))
    
    print(f"\nRobot Configuration:")
    print(f"  Link lengths: {link_lengths}")
    min_reach, max_reach = robot.get_workspace_limits()
    print(f"  Workspace: Min reach = {min_reach:.2f}m, Max reach = {max_reach:.2f}m")
    
    # ========================================
    # Trajectory 1: Spiral
    # ========================================
    print("\n" + "-" * 60)
    print("Trajectory 1: Spiral Path")
    print("-" * 60)
    
    spiral_path = generate_spiral_path(n_points=200, revolutions=3, max_radius=2.3)
    print(f"Generated spiral path with {len(spiral_path)} points")
    
    angles_sequence_spiral = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    
    for i, target in enumerate(spiral_path):
        if i % 50 == 0:
            print(f"  Processing point {i}/{len(spiral_path)}...")
        
        solution = robot.inverse_kinematics_ccd(target,
                                               initial_angles=current_angles,
                                               max_iterations=50,
                                               tolerance=0.05)
        angles_sequence_spiral.append(solution)
        current_angles = solution
    
    print("  Saving animation...")
    viz.animate_trajectory(
        angles_sequence_spiral,
        filename=f"{output_dir}/trajectory_spiral.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # ========================================
    # Trajectory 2: Heart
    # ========================================
    print("\n" + "-" * 60)
    print("Trajectory 2: Heart-Shaped Path")
    print("-" * 60)
    
    heart_path = generate_heart_path(n_points=200, scale=1.2)
    print(f"Generated heart path with {len(heart_path)} points")
    
    angles_sequence_heart = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    
    for i, target in enumerate(heart_path):
        if i % 50 == 0:
            print(f"  Processing point {i}/{len(heart_path)}...")
        
        solution = robot.inverse_kinematics_ccd(target,
                                               initial_angles=current_angles,
                                               max_iterations=50,
                                               tolerance=0.05)
        angles_sequence_heart.append(solution)
        current_angles = solution
    
    print("  Saving animation...")
    viz.animate_trajectory(
        angles_sequence_heart,
        filename=f"{output_dir}/trajectory_heart.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # ========================================
    # Trajectory 3: Star
    # ========================================
    print("\n" + "-" * 60)
    print("Trajectory 3: Star Path")
    print("-" * 60)
    
    star_path = generate_star_path(n_points=200, outer_radius=2.0, inner_radius=0.8)
    print(f"Generated star path with {len(star_path)} points")
    
    angles_sequence_star = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    
    for i, target in enumerate(star_path):
        if i % 50 == 0:
            print(f"  Processing point {i}/{len(star_path)}...")
        
        solution = robot.inverse_kinematics_ccd(target,
                                               initial_angles=current_angles,
                                               max_iterations=50,
                                               tolerance=0.05)
        angles_sequence_star.append(solution)
        current_angles = solution
    
    print("  Saving animation...")
    viz.animate_trajectory(
        angles_sequence_star,
        filename=f"{output_dir}/trajectory_star.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # ========================================
    # Trajectory 4: Infinity Symbol
    # ========================================
    print("\n" + "-" * 60)
    print("Trajectory 4: Infinity Symbol (Lemniscate)")
    print("-" * 60)
    
    infinity_path = generate_infinity_path(n_points=200, width=2.0, height=1.2)
    print(f"Generated infinity path with {len(infinity_path)} points")
    
    angles_sequence_infinity = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    
    for i, target in enumerate(infinity_path):
        if i % 50 == 0:
            print(f"  Processing point {i}/{len(infinity_path)}...")
        
        solution = robot.inverse_kinematics_ccd(target,
                                               initial_angles=current_angles,
                                               max_iterations=50,
                                               tolerance=0.05)
        angles_sequence_infinity.append(solution)
        current_angles = solution
    
    print("  Saving animation...")
    viz.animate_trajectory(
        angles_sequence_infinity,
        filename=f"{output_dir}/trajectory_infinity.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # ========================================
    # Trajectory 5: Sine Wave
    # ========================================
    print("\n" + "-" * 60)
    print("Trajectory 5: Sine Wave")
    print("-" * 60)
    
    sine_path = []
    n_points = 200
    for i in range(n_points):
        x = -2.5 + 5.0 * (i / n_points)
        y = 1.5 + 1.0 * np.sin(3 * np.pi * i / n_points)
        sine_path.append([x, y])
    sine_path = np.array(sine_path)
    
    print(f"Generated sine wave path with {len(sine_path)} points")
    
    angles_sequence_sine = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    
    for i, target in enumerate(sine_path):
        if i % 50 == 0:
            print(f"  Processing point {i}/{len(sine_path)}...")
        
        solution = robot.inverse_kinematics_ccd(target,
                                               initial_angles=current_angles,
                                               max_iterations=50,
                                               tolerance=0.05)
        angles_sequence_sine.append(solution)
        current_angles = solution
    
    print("  Saving animation...")
    viz.animate_trajectory(
        angles_sequence_sine,
        filename=f"{output_dir}/trajectory_sine_wave.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # ========================================
    # Create comparison snapshots
    # ========================================
    print("\n" + "-" * 60)
    print("Creating Comparison Snapshots")
    print("-" * 60)
    
    # Sample points from each trajectory
    sample_configs = [
        (angles_sequence_spiral[len(angles_sequence_spiral)//2], "Spiral (mid)"),
        (angles_sequence_heart[len(angles_sequence_heart)//4], "Heart (25%)"),
        (angles_sequence_star[len(angles_sequence_star)//3], "Star (33%)"),
        (angles_sequence_infinity[len(angles_sequence_infinity)//2], "Infinity (mid)"),
        (angles_sequence_sine[len(angles_sequence_sine)//2], "Sine Wave (mid)"),
    ]
    
    viz.create_comparison_plot(
        sample_configs,
        filename=f"{output_dir}/trajectory_comparison.png"
    )
    
    print("\n" + "=" * 60)
    print("SIMULATION 3 COMPLETE!")
    print("=" * 60)
    print(f"\nOutputs saved to '{output_dir}/' directory:")
    print(f"  - 5 trajectory animations:")
    print(f"    * trajectory_spiral.mp4")
    print(f"    * trajectory_heart.mp4")
    print(f"    * trajectory_star.mp4")
    print(f"    * trajectory_infinity.mp4")
    print(f"    * trajectory_sine_wave.mp4")
    print(f"  - 1 comparison plot")
    print("\nCheck the outputs folder for all results!")


if __name__ == "__main__":
    main()
