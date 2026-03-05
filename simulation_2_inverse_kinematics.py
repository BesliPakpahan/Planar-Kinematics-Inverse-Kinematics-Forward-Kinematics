"""
Simulation 2: Inverse Kinematics Demonstration
Shows how to reach target positions using IK
"""

import numpy as np
import os
from kinematics import PlanarRobot4Link
from visualizer import RobotVisualizer


def main():
    print("=" * 60)
    print("SIMULATION 2: Inverse Kinematics Demonstration")
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
    # Part 1: Reaching specific targets (Analytical IK)
    # ========================================
    print("\n" + "-" * 60)
    print("Part 1: Reaching Specific Targets (Analytical Method)")
    print("-" * 60)
    
    targets = [
        np.array([2.0, 1.5]),
        np.array([1.5, 2.0]),
        np.array([-1.5, 1.5]),
        np.array([0.5, 2.5]),
        np.array([2.5, 0.5]),
        np.array([-2.0, -1.0]),
    ]
    
    successful_configs = []
    
    for i, target in enumerate(targets):
        print(f"\nTarget {i+1}: ({target[0]:.2f}, {target[1]:.2f})")
        
        # Try analytical IK with different redundant joint values
        solution = robot.inverse_kinematics(target, θ3=0.0, θ4=0.0, elbow_up=True)
        
        if solution is not None:
            positions, achieved_pos = robot.forward_kinematics(solution)
            error = np.linalg.norm(achieved_pos - target)
            
            print(f"  Solution found!")
            print(f"  Joint angles (deg): [{', '.join([f'{np.rad2deg(a):.1f}' for a in solution])}]")
            print(f"  Achieved position: ({achieved_pos[0]:.3f}, {achieved_pos[1]:.3f})")
            print(f"  Error: {error:.6f}m")
            
            # Save snapshot
            filename = f"{output_dir}/ik_analytical_{i+1}.png"
            viz.save_snapshot(solution, filename=filename, 
                            show_workspace=True, target=target)
            
            successful_configs.append((solution, f"Target {i+1}"))
        else:
            print(f"  No solution found (target may be unreachable)")
    
    # Create comparison
    if successful_configs:
        viz.create_comparison_plot(
            successful_configs,
            filename=f"{output_dir}/ik_analytical_comparison.png"
        )
    
    # ========================================
    # Part 2: CCD-based IK
    # ========================================
    print("\n" + "-" * 60)
    print("Part 2: Cyclic Coordinate Descent (CCD) IK")
    print("-" * 60)
    
    ccd_targets = [
        np.array([2.5, 1.0]),
        np.array([1.0, 2.5]),
        np.array([-2.0, 1.5]),
        np.array([0.0, 3.0]),
    ]
    
    ccd_configs = []
    
    for i, target in enumerate(ccd_targets):
        print(f"\nCCD Target {i+1}: ({target[0]:.2f}, {target[1]:.2f})")
        
        # Use CCD IK
        solution = robot.inverse_kinematics_ccd(target, 
                                               max_iterations=1000,
                                               tolerance=0.01)
        
        positions, achieved_pos = robot.forward_kinematics(solution)
        error = np.linalg.norm(achieved_pos - target)
        
        print(f"  Joint angles (deg): [{', '.join([f'{np.rad2deg(a):.1f}' for a in solution])}]")
        print(f"  Achieved position: ({achieved_pos[0]:.3f}, {achieved_pos[1]:.3f})")
        print(f"  Error: {error:.6f}m")
        
        # Save snapshot
        filename = f"{output_dir}/ik_ccd_{i+1}.png"
        viz.save_snapshot(solution, filename=filename,
                        show_workspace=True, target=target)
        
        ccd_configs.append((solution, f"CCD Target {i+1}"))
    
    # Create comparison
    viz.create_comparison_plot(
        ccd_configs,
        filename=f"{output_dir}/ik_ccd_comparison.png"
    )
    
    # ========================================
    # Part 3: Animated target reaching
    # ========================================
    print("\n" + "-" * 60)
    print("Part 3: Animated Target Reaching")
    print("-" * 60)
    
    # Animation 1: Reaching moving target (circle)
    print("\nAnimation 1: Following Circular Path")
    n_frames = 150
    radius = 2.0
    center = np.array([0.5, 0.5])
    
    angles_sequence_1 = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    
    for i in range(n_frames):
        theta = (2 * np.pi * i) / n_frames
        target = center + radius * np.array([np.cos(theta), np.sin(theta)])
        
        # Use CCD IK with previous solution as initial guess
        solution = robot.inverse_kinematics_ccd(target, 
                                               initial_angles=current_angles,
                                               max_iterations=100,
                                               tolerance=0.05)
        angles_sequence_1.append(solution)
        current_angles = solution
    
    viz.animate_trajectory(
        angles_sequence_1,
        filename=f"{output_dir}/ik_animation_circle.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # Animation 2: Following figure-8 path
    print("\nAnimation 2: Following Figure-8 Path")
    angles_sequence_2 = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    
    for i in range(n_frames):
        t = (4 * np.pi * i) / n_frames
        target = np.array([
            1.5 * np.sin(t),
            1.0 * np.sin(2*t)
        ]) + np.array([0.0, 1.5])
        
        solution = robot.inverse_kinematics_ccd(target,
                                               initial_angles=current_angles,
                                               max_iterations=100,
                                               tolerance=0.05)
        angles_sequence_2.append(solution)
        current_angles = solution
    
    viz.animate_trajectory(
        angles_sequence_2,
        filename=f"{output_dir}/ik_animation_figure8.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # Animation 3: Square path
    print("\nAnimation 3: Following Square Path")
    square_corners = [
        np.array([1.5, 1.5]),
        np.array([1.5, -1.5]),
        np.array([-1.5, -1.5]),
        np.array([-1.5, 1.5]),
        np.array([1.5, 1.5]),
    ]
    
    angles_sequence_3 = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    n_steps_per_side = 30
    
    for i in range(len(square_corners) - 1):
        start = square_corners[i]
        end = square_corners[i + 1]
        
        for j in range(n_steps_per_side):
            alpha = j / n_steps_per_side
            target = (1 - alpha) * start + alpha * end
            
            solution = robot.inverse_kinematics_ccd(target,
                                                   initial_angles=current_angles,
                                                   max_iterations=100,
                                                   tolerance=0.05)
            angles_sequence_3.append(solution)
            current_angles = solution
    
    viz.animate_trajectory(
        angles_sequence_3,
        filename=f"{output_dir}/ik_animation_square.mp4",
        fps=30,
        show_trajectory=True
    )
    
    # Animation 4: Reaching multiple targets sequentially
    print("\nAnimation 4: Reaching Multiple Targets Sequentially")
    random_targets = [
        np.array([2.0, 1.0]),
        np.array([1.0, 2.5]),
        np.array([-1.5, 2.0]),
        np.array([-2.0, 0.5]),
        np.array([-1.0, -1.5]),
        np.array([1.0, -2.0]),
        np.array([2.5, -0.5]),
        np.array([1.5, 1.5]),
    ]
    
    angles_sequence_4 = []
    current_angles = np.array([0.0, 0.0, 0.0, 0.0])
    n_interpolation = 25
    pause_frames = 10
    
    for target in random_targets:
        # Interpolate to target
        start_angles = current_angles.copy()
        target_angles = robot.inverse_kinematics_ccd(target,
                                                     initial_angles=current_angles,
                                                     max_iterations=200,
                                                     tolerance=0.02)
        
        for j in range(n_interpolation):
            alpha = j / n_interpolation
            angles = (1 - alpha) * start_angles + alpha * target_angles
            angles_sequence_4.append(angles)
        
        # Pause at target
        for _ in range(pause_frames):
            angles_sequence_4.append(target_angles)
        
        current_angles = target_angles
    
    viz.animate_trajectory(
        angles_sequence_4,
        filename=f"{output_dir}/ik_animation_multi_target.mp4",
        fps=30,
        show_trajectory=True
    )
    
    print("\n" + "=" * 60)
    print("SIMULATION 2 COMPLETE!")
    print("=" * 60)
    print(f"\nOutputs saved to '{output_dir}/' directory:")
    print(f"  - Analytical IK snapshots and comparison")
    print(f"  - CCD IK snapshots and comparison")
    print(f"  - 4 IK animations (circle, figure-8, square, multi-target)")
    print("\nCheck the outputs folder for all results!")


if __name__ == "__main__":
    main()
