"""
Куйвалайнен Д.А.
kuyvalaynen@gmail.com
ЗЕБЗ-01-16
"""

from job_monitor import JobMonitor

if __name__ == "__main__":
    monitor = JobMonitor()
    monitor.run(timeout=30)
