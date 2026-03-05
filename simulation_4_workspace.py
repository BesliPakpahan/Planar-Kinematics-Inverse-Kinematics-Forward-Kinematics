"""
Simulation 4: Workspace Analysis and Visualization
Analyzes and visualizes the robot's reachable workspace

Author: BESLI SAUT MARITO PAKPAHAN
Course: SEMS6 - Legged Robot
Date: March 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import os
from kinematics import PlanarRobot4Link
from visualizer import RobotVisualizer


def main():
    print("=" * 60)
    print("SIMULATION 4: Workspace Analysis")
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
    print(f"  Theoretical workspace: Min reach = {min_reach:.2f}m, Max reach = {max_reach:.2f}m")
    
    # ========================================
    # Part 1: Random Sampling Workspace
    # ========================================
    print("\n" + "-" * 60)
    print("Part 1: Workspace via Random Sampling")
    print("-" * 60)
    
    print("Generating workspace by random sampling...")
    viz.visualize_workspace(
        filename=f"{output_dir}/workspace_random_sampling.png",
        n_samples=5000
    )
    
    # ========================================
    # Part 2: Systematic Grid Sampling
    # ========================================
    print("\n" + "-" * 60)
    print("Part 2: Workspace via Systematic Sampling")
    print("-" * 60)
    
    print("Generating workspace by systematic joint space sampling...")
    
    # Sample joint space systematically
    n_samples_per_joint = 15
    reachable_points = []
    
    theta_ranges = [
        np.linspace(-np.pi, np.pi, n_samples_per_joint),
        np.linspace(-np.pi, np.pi, n_samples_per_joint),
        np.linspace(-np.pi, np.pi, n_samples_per_joint),
        np.linspace(-np.pi, np.pi, n_samples_per_joint)
    ]
    
    total_configs = n_samples_per_joint ** 4
    print(f"  Total configurations to sample: {total_configs}")
    print(f"  This may take a moment...")
    
    count = 0
    for θ1 in theta_ranges[0][::2]:  # Sample every 2nd to reduce computation
        for θ2 in theta_ranges[1][::2]:
            for θ3 in theta_ranges[2][::2]:
                for θ4 in theta_ranges[3][::2]:
                    angles = np.array([θ1, θ2, θ3, θ4])
                    _, end_pos = robot.forward_kinematics(angles)
                    reachable_points.append(end_pos)
                    count += 1
    
    print(f"  Sampled {count} configurations")
    reachable_points = np.array(reachable_points)
    
    # Plot workspace
    fig, ax = plt.subplots(figsize=(12, 12))
    
    # Plot theoretical boundaries
    workspace_outer = Circle((0, 0), max_reach, 
                           fill=False, 
                           linestyle='--', 
                           color='red', 
                           linewidth=3,
                           label=f'Max Reach: {max_reach:.2f}m')
    ax.add_patch(workspace_outer)
    
    # Plot actual reachable points (with alpha for density visualization)
    ax.scatter(reachable_points[:, 0], reachable_points[:, 1], 
              c='blue', 
              s=2, 
              alpha=0.3,
              label=f'Reachable Points ({len(reachable_points)} samples)')
    
    # Plot base
    ax.plot(0, 0, 'ko', markersize=20, label='Base', zorder=10,
           markeredgewidth=3, markeredgecolor='white')
    
    # Styling
    margin = 0.5
    ax.set_xlim(-max_reach - margin, max_reach + margin)
    ax.set_ylim(-max_reach - margin, max_reach + margin)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
    ax.set_xlabel('X Position (m)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Y Position (m)', fontsize=14, fontweight='bold')
    ax.set_title('Workspace - Systematic Sampling', fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/workspace_systematic_sampling.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved workspace_systematic_sampling.png")
    
    # ========================================
    # Part 3: Workspace Density Heatmap
    # ========================================
    print("\n" + "-" * 60)
    print("Part 3: Workspace Density Heatmap")
    print("-" * 60)
    
    print("Creating density heatmap...")
    
    # Create 2D histogram
    bins = 100
    H, xedges, yedges = np.histogram2d(reachable_points[:, 0], 
                                       reachable_points[:, 1], 
                                       bins=bins,
                                       range=[[-max_reach-0.5, max_reach+0.5],
                                             [-max_reach-0.5, max_reach+0.5]])
    
    # Plot heatmap
    fig, ax = plt.subplots(figsize=(12, 12))
    
    im = ax.imshow(H.T, origin='lower', 
                   extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]],
                   cmap='hot', 
                   aspect='auto',
                   interpolation='bilinear')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Reachability Density', fontsize=12, fontweight='bold')
    
    # Plot theoretical boundary
    workspace_outer = Circle((0, 0), max_reach, 
                           fill=False, 
                           linestyle='--', 
                           color='cyan', 
                           linewidth=3,
                           label=f'Max Reach: {max_reach:.2f}m')
    ax.add_patch(workspace_outer)
    
    # Plot base
    ax.plot(0, 0, 'c*', markersize=25, label='Base', zorder=10,
           markeredgewidth=2, markeredgecolor='white')
    
    ax.set_xlim(-max_reach - 0.5, max_reach + 0.5)
    ax.set_ylim(-max_reach - 0.5, max_reach + 0.5)
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3, color='white', linestyle=':', linewidth=0.5)
    ax.set_xlabel('X Position (m)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Y Position (m)', fontsize=14, fontweight='bold')
    ax.set_title('Workspace Density Heatmap', fontsize=16, fontweight='bold', pad=20)
    ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
    
    plt.tight_layout()
    plt.savefig(f"{output_dir}/workspace_heatmap.png", dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  Saved workspace_heatmap.png")
    
    # ========================================
    # Part 4: Workspace Boundary Detection
    # ========================================
    print("\n" + "-" * 60)
    print("Part 4: Workspace Boundary Analysis")
    print("-" * 60)
    
    print("Detecting workspace boundary...")
    
    # Find convex hull or boundary
    from scipy.spatial import ConvexHull
    
    try:
        hull = ConvexHull(reachable_points)
        boundary_points = reachable_points[hull.vertices]
        
        fig, ax = plt.subplots(figsize=(12, 12))
        
        # Plot all points
        ax.scatter(reachable_points[:, 0], reachable_points[:, 1], 
                  c='lightblue', s=1, alpha=0.3, label='Reachable Points')
        
        # Plot boundary
        # Close the boundary by adding first point at end
        boundary_closed = np.vstack([boundary_points, boundary_points[0]])
        ax.plot(boundary_closed[:, 0], boundary_closed[:, 1], 
               'r-', linewidth=3, label='Convex Hull Boundary')
        ax.scatter(boundary_points[:, 0], boundary_points[:, 1], 
                  c='red', s=50, zorder=10, label='Boundary Vertices',
                  edgecolors='white', linewidths=2)
        
        # Plot theoretical boundary
        workspace_outer = Circle((0, 0), max_reach, 
                               fill=False, 
                               linestyle='--', 
                               color='green', 
                               linewidth=2,
                               label=f'Theoretical Max: {max_reach:.2f}m')
        ax.add_patch(workspace_outer)
        
        # Plot base
        ax.plot(0, 0, 'ko', markersize=20, label='Base', zorder=10,
               markeredgewidth=3, markeredgecolor='white')
        
        ax.set_xlim(-max_reach - 0.5, max_reach + 0.5)
        ax.set_ylim(-max_reach - 0.5, max_reach + 0.5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3, linestyle=':', linewidth=0.5)
        ax.set_xlabel('X Position (m)', fontsize=14, fontweight='bold')
        ax.set_ylabel('Y Position (m)', fontsize=14, fontweight='bold')
        ax.set_title('Workspace Boundary (Convex Hull)', fontsize=16, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=11, framealpha=0.9)
        
        plt.tight_layout()
        plt.savefig(f"{output_dir}/workspace_boundary.png", dpi=150, bbox_inches='tight')
        plt.close(fig)
        print(f"  Saved workspace_boundary.png")
        print(f"  Boundary vertices: {len(boundary_points)}")
        
    except Exception as e:
        print(f"  Could not compute convex hull: {e}")
    
    # ========================================
    # Part 5: Animation of Workspace Exploration
    # ========================================
    print("\n" + "-" * 60)
    print("Part 5: Workspace Exploration Animation")
    print("-" * 60)
    
    print("Creating workspace exploration animation...")
    
    # Generate random configurations
    n_frames = 200
    angles_sequence = []
    
    for i in range(n_frames):
        if i % 50 == 0:
            print(f"  Generating frame {i}/{n_frames}...")
        
        # Random configuration
        angles = np.random.uniform(-np.pi, np.pi, 4)
        angles_sequence.append(angles)
    
    print("  Saving animation...")
    viz.animate_trajectory(
        angles_sequence,
        filename=f"{output_dir}/workspace_exploration.mp4",
        fps=30,
        show_trajectory=True,
        show_workspace=True
    )
    
    # ========================================
    # Part 6: Workspace Statistics
    # ========================================
    print("\n" + "-" * 60)
    print("Part 6: Workspace Statistics")
    print("-" * 60)
    
    # Compute statistics
    distances = np.linalg.norm(reachable_points, axis=1)
    
    stats = {
        'Total Samples': len(reachable_points),
        'Mean Distance from Base': np.mean(distances),
        'Std Distance from Base': np.std(distances),
        'Min Distance': np.min(distances),
        'Max Distance': np.max(distances),
        'X Range': [np.min(reachable_points[:, 0]), np.max(reachable_points[:, 0])],
        'Y Range': [np.min(reachable_points[:, 1]), np.max(reachable_points[:, 1])],
    }
    
    print(f"\nWorkspace Statistics:")
    print(f"  Total Samples: {stats['Total Samples']}")
    print(f"  Mean Distance from Base: {stats['Mean Distance from Base']:.3f} m")
    print(f"  Std Distance from Base: {stats['Std Distance from Base']:.3f} m")
    print(f"  Min Distance: {stats['Min Distance']:.3f} m")
    print(f"  Max Distance: {stats['Max Distance']:.3f} m")
    print(f"  X Range: [{stats['X Range'][0]:.3f}, {stats['X Range'][1]:.3f}] m")
    print(f"  Y Range: [{stats['Y Range'][0]:.3f}, {stats['Y Range'][1]:.3f}] m")
    
    # Save statistics to file
    with open(f"{output_dir}/workspace_statistics.txt", 'w') as f:
        f.write("WORKSPACE ANALYSIS STATISTICS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Robot Configuration:\n")
        f.write(f"  Link lengths: {link_lengths}\n\n")
        f.write(f"Workspace Statistics:\n")
        for key, value in stats.items():
            if isinstance(value, list):
                f.write(f"  {key}: [{value[0]:.3f}, {value[1]:.3f}]\n")
            elif isinstance(value, int):
                f.write(f"  {key}: {value}\n")
            else:
                f.write(f"  {key}: {value:.3f}\n")
    
    print(f"\nStatistics saved to workspace_statistics.txt")
    
    print("\n" + "=" * 60)
    print("SIMULATION 4 COMPLETE!")
    print("=" * 60)
    print(f"\nOutputs saved to '{output_dir}/' directory:")
    print(f"  - workspace_random_sampling.png")
    print(f"  - workspace_systematic_sampling.png")
    print(f"  - workspace_heatmap.png")
    print(f"  - workspace_boundary.png")
    print(f"  - workspace_exploration.mp4")
    print(f"  - workspace_statistics.txt")
    print("\nCheck the outputs folder for all results!")


if __name__ == "__main__":
    main()
