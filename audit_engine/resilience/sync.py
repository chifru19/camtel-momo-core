import time
import logging
from typing import Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SyncCoordinator:
    def __init__(self, persistence_layer: Any, network_provider: Any, retry_limit: int = 5):
        self.persistence = persistence_layer
        self.network = network_provider
        self.retry_limit = retry_limit

    def process_queue(self):
        if not self.network.is_online():
            logger.info("Network offline. Sync deferred.")
            return
        pending = self.persistence.get_pending_logs()
        for log in pending:
            logger.info(f"Attempting sync for log ID: {log.id}")
            success = self._attempt_sync(log)
            if success:
                self.persistence.mark_as_synced(log.id)
            else:
                logger.error(f"Failed to sync log {log.id}.")
                break

    def _attempt_sync(self, log: Any, attempt: int = 1) -> bool:
        try:
            return self.network.upload(log)
        except Exception as e:
            if attempt > self.retry_limit:
                return False
            wait_time = 2 ** attempt
            logger.warning(f"Sync attempt {attempt} failed. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            return self._attempt_sync(log, attempt + 1)

if __name__ == "__main__":
    class MockPersistence:
        def get_pending_logs(self): return [type("Log", (object,), {"id": 1})]
        def mark_as_synced(self, log_id): print(f"Log {log_id} successfully marked as synced.")
    
    class MockNetwork:
        def is_online(self): return True
        def upload(self, log): return True

    coordinator = SyncCoordinator(MockPersistence(), MockNetwork())
    coordinator.process_queue()
