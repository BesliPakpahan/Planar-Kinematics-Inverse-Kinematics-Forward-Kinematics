"""
Planar 4-Link Robot Kinematics Module
Implements Forward Kinematics (FK) and Inverse Kinematics (IK)

Author: BESLI SAUT MARITO PAKPAHAN
Course: SEMS6 - Legged Robot
Date: March 2026
"""

import numpy as np
from typing import Tuple, List, Optional
import warnings


class PlanarRobot4Link:
    """
    4-Link Planar Robot Arm
    
    Parameters:
    -----------
    link_lengths : list of float
        Lengths of the 4 links [L1, L2, L3, L4]
    """
    
    def __init__(self, link_lengths: List[float] = [1.0, 1.0, 1.0, 1.0]):
        """Initialize the 4-link planar robot"""
        if len(link_lengths) != 4:
            raise ValueError("Must provide exactly 4 link lengths")
        
        self.link_lengths = np.array(link_lengths)
        self.L1, self.L2, self.L3, self.L4 = link_lengths
        
    def forward_kinematics(self, joint_angles: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Compute forward kinematics
        
        Parameters:
        -----------
        joint_angles : np.ndarray
            Array of 4 joint angles [θ1, θ2, θ3, θ4] in radians
            
        Returns:
        --------
        positions : np.ndarray
            Array of (x, y) positions for each joint and end-effector
            Shape: (5, 2) for base + 4 joints
        end_effector : np.ndarray
            Position of end-effector (x, y)
        """
        if len(joint_angles) != 4:
            raise ValueError("Must provide exactly 4 joint angles")
        
        θ1, θ2, θ3, θ4 = joint_angles
        
        # Cumulative angles (absolute angles from x-axis)
        α1 = θ1
        α2 = θ1 + θ2
        α3 = θ1 + θ2 + θ3
        α4 = θ1 + θ2 + θ3 + θ4
        
        # Position of each joint
        positions = np.zeros((5, 2))  # Base + 4 joints
        
        # Base (origin)
        positions[0] = [0, 0]
        
        # Joint 1
        positions[1] = [
            self.L1 * np.cos(α1),
            self.L1 * np.sin(α1)
        ]
        
        # Joint 2
        positions[2] = [
            positions[1, 0] + self.L2 * np.cos(α2),
            positions[1, 1] + self.L2 * np.sin(α2)
        ]
        
        # Joint 3
        positions[3] = [
            positions[2, 0] + self.L3 * np.cos(α3),
            positions[2, 1] + self.L3 * np.sin(α3)
        ]
        
        # End effector (Joint 4 / tip)
        positions[4] = [
            positions[3, 0] + self.L4 * np.cos(α4),
            positions[3, 1] + self.L4 * np.sin(α4)
        ]
        
        return positions, positions[4]
    
    def inverse_kinematics(self, target_pos: np.ndarray, 
                          θ3: Optional[float] = None,
                          θ4: Optional[float] = None,
                          elbow_up: bool = True) -> Optional[np.ndarray]:
        """
        Compute inverse kinematics using analytical method
        
        For a 4-DOF robot reaching a 2D point, we have 2 degrees of redundancy.
        We can fix θ3 and θ4 to get a unique solution.
        
        Parameters:
        -----------
        target_pos : np.ndarray
            Target end-effector position (x, y)
        θ3 : float, optional
            Fixed angle for joint 3 (if None, defaults to 0)
        θ4 : float, optional
            Fixed angle for joint 4 (if None, defaults to 0)
        elbow_up : bool
            Configuration preference for 2-link solution
            
        Returns:
        --------
        joint_angles : np.ndarray or None
            Array of 4 joint angles [θ1, θ2, θ3, θ4] or None if no solution
        """
        x_target, y_target = target_pos
        
        # Default values for redundant joints
        if θ3 is None:
            θ3 = 0.0
        if θ4 is None:
            θ4 = 0.0
        
        # Calculate the required position for joint 2 (end of second link)
        # Working backwards from the target
        α34 = θ3 + θ4  # Combined angle of links 3 and 4
        L34 = self.L3 + self.L4  # If we treat links 3&4 as one link
        
        # More sophisticated approach: use actual link 3 and 4 geometry
        # Position that joint 3 needs to reach
        x2_required = x_target - self.L4 * np.cos(θ3 + θ4) - self.L3 * np.cos(θ3)
        y2_required = y_target - self.L4 * np.sin(θ3 + θ4) - self.L3 * np.sin(θ3)
        
        # Now solve 2-link IK for links 1 and 2 to reach (x2_required, y2_required)
        solution = self._solve_2link_ik(x2_required, y2_required, 
                                       self.L1, self.L2, elbow_up)
        
        if solution is None:
            return None
        
        θ1, θ2 = solution
        
        # Adjust θ3 and θ4 to be relative angles (not absolute)
        # θ3 and θ4 are already relative in our formulation
        
        return np.array([θ1, θ2, θ3, θ4])
    
    def _solve_2link_ik(self, x: float, y: float, 
                       L1: float, L2: float, 
                       elbow_up: bool = True) -> Optional[Tuple[float, float]]:
        """
        Solve 2-link inverse kinematics
        
        Parameters:
        -----------
        x, y : float
            Target position
        L1, L2 : float
            Link lengths
        elbow_up : bool
            True for elbow-up configuration, False for elbow-down
            
        Returns:
        --------
        (θ1, θ2) : tuple or None
            Joint angles or None if unreachable
        """
        # Distance to target
        D = np.sqrt(x**2 + y**2)
        
        # Check if target is reachable
        if D > L1 + L2 or D < abs(L1 - L2):
            warnings.warn(f"Target ({x:.2f}, {y:.2f}) is unreachable. Distance: {D:.2f}, "
                        f"Max reach: {L1 + L2:.2f}, Min reach: {abs(L1 - L2):.2f}")
            return None
        
        # Angle to target
        φ = np.arctan2(y, x)
        
        # Cosine law to find θ2
        cos_θ2 = (D**2 - L1**2 - L2**2) / (2 * L1 * L2)
        
        # Clamp to valid range (numerical errors)
        cos_θ2 = np.clip(cos_θ2, -1.0, 1.0)
        
        # Two solutions for θ2
        if elbow_up:
            θ2 = np.arccos(cos_θ2)
        else:
            θ2 = -np.arccos(cos_θ2)
        
        # Solve for θ1
        k1 = L1 + L2 * np.cos(θ2)
        k2 = L2 * np.sin(θ2)
        θ1 = φ - np.arctan2(k2, k1)
        
        return (θ1, θ2)
    
    def inverse_kinematics_ccd(self, target_pos: np.ndarray, 
                              initial_angles: Optional[np.ndarray] = None,
                              max_iterations: int = 1000,
                              tolerance: float = 0.01) -> np.ndarray:
        """
        Inverse kinematics using Cyclic Coordinate Descent (CCD) algorithm
        This is more general and handles redundancy naturally.
        
        Parameters:
        -----------
        target_pos : np.ndarray
            Target end-effector position (x, y)
        initial_angles : np.ndarray, optional
            Initial guess for joint angles
        max_iterations : int
            Maximum number of iterations
        tolerance : float
            Convergence tolerance (distance to target)
            
        Returns:
        --------
        joint_angles : np.ndarray
            Array of 4 joint angles [θ1, θ2, θ3, θ4]
        """
        if initial_angles is None:
            # Start with random configuration
            angles = np.random.uniform(-np.pi, np.pi, 4)
        else:
            angles = initial_angles.copy()
        
        for iteration in range(max_iterations):
            # Get current end-effector position
            positions, current_pos = self.forward_kinematics(angles)
            
            # Check if we're close enough
            error = np.linalg.norm(current_pos - target_pos)
            if error < tolerance:
                return angles
            
            # CCD: Update each joint starting from the last one
            for joint_idx in range(3, -1, -1):
                # Current positions
                positions, current_pos = self.forward_kinematics(angles)
                
                # Position of current joint
                joint_pos = positions[joint_idx]
                
                # Vectors from joint to end-effector and to target
                to_end = current_pos - joint_pos
                to_target = target_pos - joint_pos
                
                # Skip if vectors are too small
                if np.linalg.norm(to_end) < 1e-6 or np.linalg.norm(to_target) < 1e-6:
                    continue
                
                # Angle between vectors
                cos_angle = np.dot(to_end, to_target) / (np.linalg.norm(to_end) * np.linalg.norm(to_target))
                cos_angle = np.clip(cos_angle, -1.0, 1.0)
                
                # Cross product to determine direction
                cross = to_end[0] * to_target[1] - to_end[1] * to_target[0]
                angle_diff = np.arccos(cos_angle) * np.sign(cross)
                
                # Update joint angle
                angles[joint_idx] += angle_diff
                
                # Normalize angle to [-π, π]
                angles[joint_idx] = np.arctan2(np.sin(angles[joint_idx]), 
                                              np.cos(angles[joint_idx]))
        
        # Return best solution found
        warnings.warn(f"CCD did not converge after {max_iterations} iterations. "
                     f"Final error: {error:.4f}")
        return angles
    
    def get_workspace_limits(self) -> Tuple[float, float]:
        """
        Get the workspace limits (min and max reach)
        
        Returns:
        --------
        min_reach, max_reach : float, float
        """
        max_reach = np.sum(self.link_lengths)
        min_reach = max(0, np.max(self.link_lengths) - np.sum(self.link_lengths[np.arange(4) != np.argmax(self.link_lengths)]))
        
        return min_reach, max_reach
    
    def jacobian(self, joint_angles: np.ndarray) -> np.ndarray:
        """
        Compute the Jacobian matrix
        
        Parameters:
        -----------
        joint_angles : np.ndarray
            Current joint angles
            
        Returns:
        --------
        J : np.ndarray
            Jacobian matrix (2x4)
        """
        θ1, θ2, θ3, θ4 = joint_angles
        
        # Cumulative angles
        α1 = θ1
        α2 = θ1 + θ2
        α3 = θ1 + θ2 + θ3
        α4 = θ1 + θ2 + θ3 + θ4
        
        # Jacobian for end-effector position
        J = np.zeros((2, 4))
        
        # ∂x/∂θ_i
        J[0, 0] = -self.L1*np.sin(α1) - self.L2*np.sin(α2) - self.L3*np.sin(α3) - self.L4*np.sin(α4)
        J[0, 1] = -self.L2*np.sin(α2) - self.L3*np.sin(α3) - self.L4*np.sin(α4)
        J[0, 2] = -self.L3*np.sin(α3) - self.L4*np.sin(α4)
        J[0, 3] = -self.L4*np.sin(α4)
        
        # ∂y/∂θ_i
        J[1, 0] = self.L1*np.cos(α1) + self.L2*np.cos(α2) + self.L3*np.cos(α3) + self.L4*np.cos(α4)
        J[1, 1] = self.L2*np.cos(α2) + self.L3*np.cos(α3) + self.L4*np.cos(α4)
        J[1, 2] = self.L3*np.cos(α3) + self.L4*np.cos(α4)
        J[1, 3] = self.L4*np.cos(α4)
        
        return J


if __name__ == "__main__":
    # Test the kinematics
    robot = PlanarRobot4Link([1.0, 1.0, 0.8, 0.6])
    
    # Test forward kinematics
    print("=" * 50)
    print("FORWARD KINEMATICS TEST")
    print("=" * 50)
    test_angles = np.array([np.pi/4, np.pi/6, np.pi/8, np.pi/12])
    positions, end_effector = robot.forward_kinematics(test_angles)
    print(f"Joint angles: {np.rad2deg(test_angles)}")
    print(f"End-effector position: {end_effector}")
    print(f"All positions:\n{positions}")
    
    # Test inverse kinematics
    print("\n" + "=" * 50)
    print("INVERSE KINEMATICS TEST (Analytical)")
    print("=" * 50)
    target = np.array([2.0, 1.5])
    solution = robot.inverse_kinematics(target, θ3=0.1, θ4=0.1)
    if solution is not None:
        print(f"Target: {target}")
        print(f"Solution angles: {np.rad2deg(solution)}")
        _, achieved_pos = robot.forward_kinematics(solution)
        print(f"Achieved position: {achieved_pos}")
        print(f"Error: {np.linalg.norm(achieved_pos - target):.6f}")
    
    # Test CCD
    print("\n" + "=" * 50)
    print("INVERSE KINEMATICS TEST (CCD)")
    print("=" * 50)
    target = np.array([1.5, 2.0])
    solution_ccd = robot.inverse_kinematics_ccd(target)
    print(f"Target: {target}")
    print(f"Solution angles: {np.rad2deg(solution_ccd)}")
    _, achieved_pos = robot.forward_kinematics(solution_ccd)
    print(f"Achieved position: {achieved_pos}")
    print(f"Error: {np.linalg.norm(achieved_pos - target):.6f}")
    
    # Test workspace
    print("\n" + "=" * 50)
    print("WORKSPACE INFO")
    print("=" * 50)
    min_reach, max_reach = robot.get_workspace_limits()
    print(f"Min reach: {min_reach:.2f}")
    print(f"Max reach: {max_reach:.2f}")
