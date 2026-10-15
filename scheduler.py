"""
Automated Daily Scheduler for MexConsumerPulse.
Runs the autonomous agent pipeline and generates daily intelligence reports
on a regular schedule (e.g., daily at 06:00 AM local time or configurable intervals).
"""

import sys
import time
import subprocess
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def run_daily_pipeline():
    """
    Triggers the complete agent swarm run and daily report synthesis.
    """
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{now_str}] >>> Starting scheduled daily pipeline execution...")
    try:
        proc = subprocess.run(
            [sys.executable, str(BASE_DIR / "run.py"), "--all"],
            capture_output=True,
            text=True,
            check=True
        )
        print(proc.stdout)
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] >>> Scheduled pipeline run finished successfully.")
    except subprocess.CalledProcessError as e:
        print(f"[Error] Scheduled run failed with exit code {e.returncode}:")
        print(e.stderr)

def start_scheduler(interval_hours: int = 24, run_immediately: bool = True):
    """
    Continuous scheduler loop.
    """
    print("=" * 65)
    print(" MexConsumerPulse Scheduler Initialized")
    print(f" Interval: Every {interval_hours} hours")
    print(f" Run immediately: {run_immediately}")
    print(" Press Ctrl+C to stop.")
    print("=" * 65)

    if run_immediately:
        run_daily_pipeline()

    interval_seconds = interval_hours * 3600

    while True:
        try:
            print(f"\n[Scheduler] Sleeping for {interval_hours} hours until next daily update...")
            time.sleep(interval_seconds)
            run_daily_pipeline()
        except KeyboardInterrupt:
            print("\n[Scheduler] Scheduler stopped by user.")
            break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MexConsumerPulse Daily Scheduler")
    parser.add_argument("--interval-hours", type=int, default=24, help="Hours between runs (default: 24)")
    parser.add_argument("--skip-initial", action="store_true", help="Skip immediate run on launch")
    args = parser.parse_args()

    start_scheduler(interval_hours=args.interval_hours, run_immediately=not args.skip_initial)
