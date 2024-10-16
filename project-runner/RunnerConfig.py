from EventManager.Models.RunnerEvents import RunnerEvents
from EventManager.EventSubscriptionController import EventSubscriptionController
from ConfigValidator.Config.Models.RunTableModel import RunTableModel
from ConfigValidator.Config.Models.FactorModel import FactorModel
from ConfigValidator.Config.Models.RunnerContext import RunnerContext
from ConfigValidator.Config.Models.OperationType import OperationType
from ProgressManager.Output.OutputProcedure import OutputProcedure as output

from typing import Dict, Any, Optional
from pathlib import Path
from os.path import dirname, realpath

import pandas as pd
import time
import subprocess
import shlex

class RunnerConfig:
    ROOT_DIR = Path(dirname(realpath(__file__)))

    # ================================ USER SPECIFIC CONFIG ================================
    name: str = "loop_optimization_experiment"
    results_output_path: Path = ROOT_DIR / 'experiments'
    operation_type: OperationType = OperationType.AUTO
    time_between_runs_in_ms: int = 1000

    def __init__(self):
        EventSubscriptionController.subscribe_to_multiple_events([
            (RunnerEvents.BEFORE_EXPERIMENT, self.before_experiment),
            (RunnerEvents.BEFORE_RUN, self.before_run),
            (RunnerEvents.START_RUN, self.start_run),
            (RunnerEvents.START_MEASUREMENT, self.start_measurement),
            (RunnerEvents.INTERACT, self.interact),
            (RunnerEvents.STOP_MEASUREMENT, self.stop_measurement),
            (RunnerEvents.STOP_RUN, self.stop_run),
            (RunnerEvents.POPULATE_RUN_DATA, self.populate_run_data),
            (RunnerEvents.AFTER_EXPERIMENT, self.after_experiment)
        ])
        self.run_table_model = None
        output.console_log("Custom runner configuration loaded")

    def create_run_table_model(self) -> RunTableModel:
        """Create the run_table model with randomized runs and 16 repetitions."""
        # Factor for the subject (Sherlock and CogVideo)
        subject = FactorModel("subject", ["CogVideo", "Sherlock"])
        
        # Factor for treatment (Default Loop, Optimized Loop - which will be renamed dynamically)
        treatment = FactorModel("treatment", ["Default Loop", "Loop Unswitching", "Loop Unrolling"])
        
        # Factor for iterations (10 and 20)
        iterations = FactorModel("iterations", [10, 20])

        # Exclude unwanted variations: CogVideo should not use Loop Unrolling, Sherlock should not use Loop Unswitching
        exclude_variations = [
            {subject: ["CogVideo"], treatment: ["Loop Unrolling"]},
            {subject: ["Sherlock"], treatment: ["Loop Unswitching"]}
        ]

        # Create the RunTableModel, set repetitions to 16, and enable shuffle
        self.run_table_model = RunTableModel(
            factors=[subject, treatment, iterations],
            exclude_variations=exclude_variations,
            data_columns=['system_power', 'used_memory'],
            shuffle=True,
            repetitions=16
        )

        return self.run_table_model

    def before_experiment(self) -> None:
        """Activities to perform before the experiment starts."""
        output.console_log("Preparing for loop optimization experiment...")

    def before_run(self) -> None:
        """Activities to perform before each run."""
        output.console_log("Setting up before each run...")

    def start_run(self, context: RunnerContext) -> None:
        """Activities to start each run."""
        subject = context.run_variation['subject']
        treatment = context.run_variation['treatment']
        iterations = context.run_variation['iterations']
        
        output.console_log(f"Starting run with subject: {subject}, treatment: {treatment}, iterations: {iterations}")

    def start_measurement(self, context: RunnerContext) -> None:
        """Start energy measurement with EnergiBridge."""
        sampling_interval = 1000  # 1 sample per second
        subject = context.run_variation['subject']
        treatment = context.run_variation['treatment']
        iterations = context.run_variation['iterations']

        # Select the appropriate script based on the subject and treatment
        if subject == "Sherlock":
            script = "sherlock_snippet.py" if treatment == "Default Loop" else "sherlock_optimized.py"

        
            # Create a mock list of usernames (this should be provided in your real experiment)
            usernames = "user1\nuser2\nuser3\nuser4"

            profiler_cmd = f'sudo energibridge ' \
                       f'--interval {sampling_interval} ' \
                       f'--output {context.run_dir / "energibridge.csv"} ' \
                       f'--summary ' \
                       f'python3 examples/project-runner/{script} --usernames  {usernames}'

        elif subject == "CogVideo":
            script = "cogvideo_snippet.py" if treatment == "Default Loop" else "cogvideo_optimized.py"

            profiler_cmd = f'sudo energibridge ' \
                       f'--interval {sampling_interval} ' \
                       f'--output {context.run_dir / "energibridge.csv"} ' \
                       f'--summary ' \
                       f'python3 examples/project-runner/{script} --prompts "A girl is on the beach" ' \
                       f'--retry_times {iterations} --type t2v'

        # Command to run the experiment
        

        energibridge_log = open(f'{context.run_dir}/energibridge.log', 'w')
        self.profiler = subprocess.Popen(shlex.split(profiler_cmd), stdout=energibridge_log)
        output.console_log(f"Started energy measurement using EnergiBridge for subject: {subject}, treatment: {treatment}, iterations: {iterations}.")

    def interact(self, context: RunnerContext) -> None:
        """Allow the experiment to run for a specified duration."""
        output.console_log("Running the experiment for 60 seconds...")
        # output.console.log("Running EXPERIMENT ....")
        time.sleep(60)
        # self.profiler.wait()

    def stop_measurement(self, context: RunnerContext) -> None:
        """Stop the energy measurement."""
        self.profiler.terminate()
        self.profiler.wait()
        output.console_log("Stopped energy measurement.")

    def stop_run(self, context: RunnerContext) -> None:
        """Clean up after each run."""
        output.console_log("Run completed. Cleaning up...")

    def populate_run_data(self, context: RunnerContext) -> Optional[Dict[str, Any]]:
        """Parse measurement data and populate run results."""
        df = pd.read_csv(context.run_dir / "energibridge.csv")
        total_power = round(df['SYSTEM_POWER (Watts)'].sum(), 3)
        used_memory = round(df['USED_MEMORY'].sum(), 3)

        run_data = {
            'system_power': total_power,
            'used_memory': used_memory,
        }
        return run_data

    def after_experiment(self) -> None:
        """Actions to take after the experiment ends."""
        output.console_log("Loop optimization experiment completed.")

    # ================================ DO NOT ALTER BELOW THIS LINE ================================
    experiment_path: Path = None
