"""
Visualization module for planar 4-link robot
Handles rendering, animation, and saving to video/images
IMPROVED VERSION - Higher quality visuals

Author: BESLI SAUT MARITO PAKPAHAN
Course: SEMS6 - Legged Robot
Date: March 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle
from typing import List, Optional, Tuple
import os


class RobotVisualizer:
    """Visualizer for planar 4-link robot with enhanced visual quality"""
    
    def __init__(self, robot, figsize=(12, 12)):
        """
        Initialize visualizer
        
        Parameters:
        -----------
        robot : PlanarRobot4Link
            Robot instance
        figsize : tuple
            Figure size
        """
        self.robot = robot
        self.figsize = figsize
        
        # Enhanced color scheme with better contrast
        self.colors = {
            'link1': '#FF3838',      # Brighter red
            'link2': '#00D9FF',      # Brighter cyan
            'link3': '#4169E1',      # Royal blue
            'link4': '#32CD32',      # Lime green
            'joint': '#1a1a1a',      # Darker gray for joints
            'end_effector': '#FF1744', # Bright red
            'trajectory': '#9C27B0',  # Purple
            'workspace': '#757575',   # Medium gray
            'target': '#FFA726'       # Orange
        }
        
    def plot_robot(self, joint_angles: np.ndarray, 
                   ax: Optional[plt.Axes] = None,
                   show_workspace: bool = False,
                   target: Optional[np.ndarray] = None,
                   trajectory: Optional[np.ndarray] = None) -> plt.Axes:
        """
        Plot robot configuration with enhanced visuals
        
        Parameters:
        -----------
        joint_angles : np.ndarray
            Joint angles [θ1, θ2, θ3, θ4]
        ax : plt.Axes, optional
            Axes to plot on
        show_workspace : bool
            Whether to show workspace boundaries
        target : np.ndarray, optional
            Target position to show
        trajectory : np.ndarray, optional
            Trajectory points to show
            
        Returns:
        --------
        ax : plt.Axes
        """
        if ax is None:
            fig, ax = plt.subplots(figsize=self.figsize)
        else:
            ax.clear()
        
        # Get positions
        positions, end_effector = self.robot.forward_kinematics(joint_angles)
        
        # Plot workspace boundaries
        if show_workspace:
            min_reach, max_reach = self.robot.get_workspace_limits()
            workspace_outer = Circle((0, 0), max_reach, 
                                   fill=False, 
                                   linestyle='--', 
                                   color=self.colors['workspace'], 
                                   linewidth=3,
                                   alpha=0.6,
                                   label='Max Reach')
            ax.add_patch(workspace_outer)
            
            if min_reach > 0:
                workspace_inner = Circle((0, 0), min_reach, 
                                       fill=False, 
                                       linestyle='--', 
                                       color=self.colors['workspace'], 
                                       linewidth=3,
                                       alpha=0.6,
                                       label='Min Reach')
                ax.add_patch(workspace_inner)
        
        # Plot links with THICKER lines and better styling
        link_colors = [self.colors['link1'], self.colors['link2'], 
                      self.colors['link3'], self.colors['link4']]
        
        for i in range(4):
            ax.plot([positions[i, 0], positions[i+1, 0]], 
                   [positions[i, 1], positions[i+1, 1]], 
                   'o-', 
                   color=link_colors[i], 
                   linewidth=12,          # Much thicker
                   markersize=18,         # Larger markers
                   label=f'Link {i+1}',
                   solid_capstyle='round',
                   markeredgewidth=4,     # Thick white edge
                   markeredgecolor='white',
                   zorder=5)
        
        # Plot joints with LARGER markers
        for i in range(5):
            if i == 0:
                # Base - largest
                ax.plot(positions[i, 0], positions[i, 1], 
                       'o', 
                       color=self.colors['joint'], 
                       markersize=28,
                       markeredgewidth=5,
                       markeredgecolor='white',
                       label='Base',
                       zorder=15)
            elif i == 4:
                # End effector - square shape, bright
                ax.plot(positions[i, 0], positions[i, 1], 
                       's', 
                       color=self.colors['end_effector'], 
                       markersize=26,
                       markeredgewidth=5,
                       markeredgecolor='white',
                       label='End Effector',
                       zorder=15)
            else:
                # Regular joints
                ax.plot(positions[i, 0], positions[i, 1], 
                       'o', 
                       color=self.colors['joint'], 
                       markersize=22,
                       markeredgewidth=4,
                       markeredgecolor='white',
                       zorder=15)
        
        # Plot target if provided - very visible!
        if target is not None:
            ax.plot(target[0], target[1], 
                   '*', 
                   color=self.colors['target'], 
                   markersize=40,
                   markeredgewidth=4,
                   markeredgecolor='white',
                   label='Target',
                   zorder=20)
        
        # Plot trajectory if provided
        if trajectory is not None and len(trajectory) > 0:
            ax.plot(trajectory[:, 0], trajectory[:, 1], 
                   '-', 
                   color=self.colors['trajectory'], 
                   linewidth=4, 
                   alpha=0.7,
                   label='Trajectory')
            ax.scatter(trajectory[:, 0], trajectory[:, 1], 
                      color=self.colors['trajectory'], 
                      s=60, 
                      alpha=0.6,
                      zorder=10,
                      edgecolors='white',
                      linewidths=2)
        
        # Set equal aspect ratio and limits
        min_reach, max_reach = self.robot.get_workspace_limits()
        margin = 0.5
        ax.set_xlim(-max_reach - margin, max_reach + margin)
        ax.set_ylim(-max_reach - margin, max_reach + margin)
        ax.set_aspect('equal')
        
        # Grid with better visibility
        ax.grid(True, alpha=0.5, linestyle=':', linewidth=1.8, color='gray')
        ax.set_axisbelow(True)
        
        # Labels with LARGER fonts
        ax.set_xlabel('X Position (m)', fontsize=18, fontweight='bold')
        ax.set_ylabel('Y Position (m)', fontsize=18, fontweight='bold')
        ax.set_title('4-Link Planar Robot', fontsize=20, fontweight='bold', pad=20)
        
        # Legend with larger font and better styling
        ax.legend(loc='upper right', fontsize=12, framealpha=0.95, 
                 edgecolor='black', fancybox=True, shadow=True, 
                 bbox_to_anchor=(1.0, 1.0))
        
        # Add border to plot
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(2.5)
        
        return ax
    
    def animate_trajectory(self, 
                          angles_sequence: List[np.ndarray],
                          filename: str = 'animation.mp4',
                          fps: int = 30,
                          show_trajectory: bool = True,
                          show_workspace: bool = True) -> None:
        """
        Create animation from sequence of joint angles
        
        Parameters:
        -----------
        angles_sequence : list of np.ndarray
            Sequence of joint angle configurations
        filename : str
            Output filename
        fps : int
            Frames per second
        show_trajectory : bool
            Whether to show trajectory trail
        show_workspace : bool
            Whether to show workspace boundaries
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Compute all positions for trajectory
        trajectory_points = []
        for angles in angles_sequence:
            _, end_pos = self.robot.forward_kinematics(angles)
            trajectory_points.append(end_pos)
        trajectory_points = np.array(trajectory_points)
        
        def update(frame):
            """Update function for animation"""
            angles = angles_sequence[frame]
            
            if show_trajectory:
                traj = trajectory_points[:frame+1]
            else:
                traj = None
            
            self.plot_robot(angles, ax=ax, 
                          show_workspace=show_workspace,
                          trajectory=traj)
            
            # Add frame counter with larger font and better styling
            ax.text(0.02, 0.98, f'Frame: {frame+1}/{len(angles_sequence)}',
                   transform=ax.transAxes,
                   fontsize=16,
                   fontweight='bold',
                   verticalalignment='top',
                   bbox=dict(boxstyle='round,pad=0.8', 
                           facecolor='wheat', 
                           alpha=0.95, 
                           edgecolor='black', 
                           linewidth=2.5))
            
            return ax,
        
        # Create animation
        anim = animation.FuncAnimation(fig, update, 
                                      frames=len(angles_sequence),
                                      interval=1000/fps,
                                      blit=False,
                                      repeat=True)
        
        # Save animation with HIGH QUALITY
        print(f"Saving animation to {filename}...")
        
        if filename.endswith('.gif'):
            writer = animation.PillowWriter(fps=fps)
            dpi = 120
        else:
            writer = animation.FFMpegWriter(fps=fps, 
                                           metadata=dict(artist='Robot Simulator'),
                                           bitrate=4000,
                                           extra_args=['-vcodec', 'libx264'])
            dpi = 150
        
        anim.save(filename, writer=writer, dpi=dpi)
        print(f"Animation saved!")
        plt.close(fig)
    
    def save_snapshot(self, joint_angles: np.ndarray, 
                     filename: str = 'snapshot.png',
                     show_workspace: bool = True,
                     target: Optional[np.ndarray] = None,
                     trajectory: Optional[np.ndarray] = None,
                     dpi: int = 200) -> None:
        """
        Save a single snapshot of robot configuration
        
        Parameters:
        -----------
        joint_angles : np.ndarray
            Joint angles [θ1, θ2, θ3, θ4]
        filename : str
            Output filename
        show_workspace : bool
            Whether to show workspace boundaries
        target : np.ndarray, optional
            Target position to show
        trajectory : np.ndarray, optional
            Trajectory points to show
        dpi : int
            Image resolution (higher = better quality)
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        self.plot_robot(joint_angles, ax=ax,
                       show_workspace=show_workspace,
                       target=target,
                       trajectory=trajectory)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='black')
        print(f"Snapshot saved to {filename}")
        plt.close(fig)
    
    def create_comparison_plot(self, 
                              configs: List[Tuple[np.ndarray, str]],
                              filename: str = 'comparison.png',
                              dpi: int = 200) -> None:
        """
        Create comparison plot of multiple configurations
        
        Parameters:
        -----------
        configs : list of (angles, title)
            List of configurations to compare
        filename : str
            Output filename
        dpi : int
            Resolution
        """
        n_configs = len(configs)
        cols = min(3, n_configs)
        rows = (n_configs + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, 
                                figsize=(cols*7, rows*7))
        
        if n_configs == 1:
            axes = [axes]
        else:
            axes = axes.flatten()
        
        for i, (angles, title) in enumerate(configs):
            self.plot_robot(angles, ax=axes[i], show_workspace=True)
            axes[i].set_title(title, fontsize=16, fontweight='bold', pad=15)
            
            # Add border around each subplot
            for spine in axes[i].spines.values():
                spine.set_edgecolor('black')
                spine.set_linewidth(3)
        
        # Hide extra subplots
        for i in range(n_configs, len(axes)):
            axes[i].axis('off')
        
        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='black')
        print(f"Comparison plot saved to {filename}")
        plt.close(fig)
    
    def visualize_workspace(self, 
                           filename: str = 'workspace.png',
                           n_samples: int = 1000,
                           dpi: int = 200) -> None:
        """
        Visualize robot workspace by random sampling
        
        Parameters:
        -----------
        filename : str
            Output filename
        n_samples : int
            Number of random configurations to sample
        dpi : int
            Resolution
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Sample random configurations
        reachable_points = []
        
        for _ in range(n_samples):
            # Random joint angles
            angles = np.random.uniform(-np.pi, np.pi, 4)
            _, end_pos = self.robot.forward_kinematics(angles)
            reachable_points.append(end_pos)
        
        reachable_points = np.array(reachable_points)
        
        # Plot workspace boundary
        min_reach, max_reach = self.robot.get_workspace_limits()
        workspace_outer = Circle((0, 0), max_reach, 
                               fill=False, 
                               linestyle='--', 
                               color='red', 
                               linewidth=4,
                               label=f'Max Reach: {max_reach:.2f}m')
        ax.add_patch(workspace_outer)
        
        # Plot reachable points
        ax.scatter(reachable_points[:, 0], reachable_points[:, 1], 
                  c='blue', 
                  s=3, 
                  alpha=0.4,
                  label=f'Reachable Points ({n_samples} samples)')
        
        # Plot base
        ax.plot(0, 0, 'ko', markersize=25, label='Base', zorder=10,
               markeredgewidth=4, markeredgecolor='white')
        
        # Set limits and styling
        margin = 0.5
        ax.set_xlim(-max_reach - margin, max_reach + margin)
        ax.set_ylim(-max_reach - margin, max_reach + margin)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.5, linestyle=':', linewidth=1.8, color='gray')
        ax.set_xlabel('X Position (m)', fontsize=18, fontweight='bold')
        ax.set_ylabel('Y Position (m)', fontsize=18, fontweight='bold')
        ax.set_title('Robot Workspace Analysis', fontsize=20, fontweight='bold', pad=20)
        ax.legend(loc='upper right', fontsize=13, framealpha=0.95,
                 edgecolor='black', fancybox=True, shadow=True)
        
        # Add border
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(2.5)
        
        plt.tight_layout()
        plt.savefig(filename, dpi=dpi, bbox_inches='tight',
                   facecolor='white', edgecolor='black')
        print(f"Workspace visualization saved to {filename}")
        plt.close(fig)


if __name__ == "__main__":
    from kinematics import PlanarRobot4Link
    
    # Create robot and visualizer
    robot = PlanarRobot4Link([1.0, 1.0, 0.8, 0.6])
    viz = RobotVisualizer(robot)
    
    # Test snapshot
    print("Creating test snapshot...")
    test_angles = np.array([np.pi/4, np.pi/6, -np.pi/8, np.pi/12])
    viz.save_snapshot(test_angles, 
                     filename='test_snapshot.png',
                     show_workspace=True)
    
    print("Visualizer test complete!")
