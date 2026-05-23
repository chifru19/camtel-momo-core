from rich.live import Live
from rich.table import Table
import time
import random

def generate_table():
    table = Table(title="Camtel Audit Platform - Live Status")
    table.add_column("Module", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Resilience", style="magenta")
    
    # Simulate dynamic status
    status = "Operational" if random.random() > 0.2 else "Syncing"
    table.add_row("Core Ledger", "Operational", "Ready")
    table.add_row("Transfer Engine", "Active", "Ready")
    table.add_row("Reconciliation", status, "Pending")
    table.add_row("Connectivity", "Degraded" if status == "Syncing" else "Stable", "Active")
    return table

if __name__ == "__main__":
    with Live(generate_table(), refresh_per_second=1) as live:
        while True:
            time.sleep(1)
            live.update(generate_table())
