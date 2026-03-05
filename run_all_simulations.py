"""
Run All Simulations
Executes all 4 simulation scripts sequentially
"""

import subprocess
import sys
import time


def run_simulation(script_name, description):
    """Run a simulation script"""
    print("\n" + "=" * 70)
    print(f"RUNNING: {description}")
    print("=" * 70)
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              check=True, 
                              capture_output=False,
                              text=True)
        
        elapsed_time = time.time() - start_time
        print(f"\n✓ {description} completed successfully in {elapsed_time:.1f} seconds")
        return True
        
    except subprocess.CalledProcessError as e:
        elapsed_time = time.time() - start_time
        print(f"\n✗ {description} failed after {elapsed_time:.1f} seconds")
        print(f"Error: {e}")
        return False


def main():
    print("=" * 70)
    print("4-LINK PLANAR ROBOT KINEMATICS - SIMULATION SUITE")
    print("=" * 70)
    print("\nThis will run all simulations sequentially.")
    print("Each simulation will generate videos and images in the 'outputs' folder.")
    print("\nSimulations to run:")
    print("  1. Forward Kinematics Demonstration")
    print("  2. Inverse Kinematics Demonstration")
    print("  3. Advanced Trajectory Following")
    print("  4. Workspace Analysis")
    print("\nNote: This may take several minutes depending on your machine.")
    
    # Ask for confirmation
    response = input("\nProceed? (y/n): ")
    if response.lower() != 'y':
        print("Cancelled.")
        return
    
    start_total = time.time()
    
    simulations = [
        ("simulation_1_forward_kinematics.py", "Simulation 1: Forward Kinematics"),
        ("simulation_2_inverse_kinematics.py", "Simulation 2: Inverse Kinematics"),
        ("simulation_3_trajectory.py", "Simulation 3: Trajectory Following"),
        ("simulation_4_workspace.py", "Simulation 4: Workspace Analysis"),
    ]
    
    results = []
    
    for script, description in simulations:
        success = run_simulation(script, description)
        results.append((description, success))
    
    total_time = time.time() - start_total
    
    # Print summary
    print("\n" + "=" * 70)
    print("SIMULATION SUITE SUMMARY")
    print("=" * 70)
    
    for description, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {description}")
    
    print(f"\nTotal execution time: {total_time:.1f} seconds ({total_time/60:.1f} minutes)")
    
    successes = sum(1 for _, success in results if success)
    print(f"\nResults: {successes}/{len(results)} simulations completed successfully")
    
    if successes == len(results):
        print("\n🎉 All simulations completed successfully!")
        print("Check the 'outputs' folder for all generated files.")
    else:
        print("\n⚠ Some simulations failed. Check the error messages above.")


if __name__ == "__main__":
    main()
