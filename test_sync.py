import logging
from audit_engine.resilience.sync import SyncCoordinator

# Mock classes to simulate environment behavior
class MockPersistence:
    def get_pending_logs(self):
        return [type('Log', (object,), {'id': 1})]
    def mark_as_synced(self, log_id):
        print(f"Log {log_id} successfully marked as synced.")

class MockNetwork:
    def __init__(self):
        self.attempts = 0
    def is_online(self):
        return True
    def upload(self, log):
        self.attempts += 1
        if self.attempts < 3: # Fail twice, then succeed
            raise Exception("Connection unstable")
        return True

# Run the test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    coordinator = SyncCoordinator(MockPersistence(), MockNetwork())
    coordinator.process_queue()