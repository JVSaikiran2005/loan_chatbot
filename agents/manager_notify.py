from typing import Dict
from .cloud_storage import CloudStorage


class ManagerNotifier:
    """Simulate sending the finalized loan package to a bank manager/head.

    This writes a record into the `manager_inbox.json` inside cloud storage
    so that an offline reviewer can pick it up.
    """

    def __init__(self, storage: CloudStorage = None):
        self.storage = storage or CloudStorage()

    def send_to_manager(self, session_id: str, package_path: str, metadata: Dict):
        payload = {
            'session_id': session_id,
            'package_path': package_path,
            'metadata': metadata,
            'notified_at': __import__('datetime').datetime.now().isoformat(),
            'status': 'pending_review'
        }
        self.storage.notify_manager(payload)
        return payload
