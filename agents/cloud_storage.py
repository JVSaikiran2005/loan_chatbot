import os
import json
from datetime import datetime
from typing import Dict, Optional


class CloudStorage:
    """Simple local 'cloud' storage that saves files and stores metadata.

    This simulates a cloud DB by keeping files under `cloud_storage/`
    and a `metadata.json` file that holds records for each upload/package.
    """

    def __init__(self, base_dir: str = 'cloud_storage'):
        self.base_dir = base_dir
        self.files_dir = os.path.join(self.base_dir, 'files')
        self.packages_dir = os.path.join(self.base_dir, 'packages')
        self.meta_path = os.path.join(self.base_dir, 'metadata.json')
        self.manager_inbox = os.path.join(self.base_dir, 'manager_inbox.json')

        os.makedirs(self.files_dir, exist_ok=True)
        os.makedirs(self.packages_dir, exist_ok=True)

        # Initialize metadata files if missing
        if not os.path.exists(self.meta_path):
            with open(self.meta_path, 'w', encoding='utf-8') as fh:
                json.dump({'uploads': [], 'packages': []}, fh, indent=2)

        if not os.path.exists(self.manager_inbox):
            with open(self.manager_inbox, 'w', encoding='utf-8') as fh:
                json.dump([], fh, indent=2)

    def save_file(self, file_stream, filename: str, metadata: Optional[Dict] = None) -> str:
        """Save an incoming file stream into the storage and record metadata.

        Returns the saved filepath.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        safe_name = f"{timestamp}_{filename}"
        dest = os.path.join(self.files_dir, safe_name)

        # write bytes
        file_stream.seek(0)
        with open(dest, 'wb') as fh:
            fh.write(file_stream.read())

        # append metadata
        self._append_metadata('uploads', {
            'filename': safe_name,
            'original_name': filename,
            'saved_path': dest,
            'timestamp': timestamp,
            'meta': metadata or {}
        })

        return dest

    def create_package(self, session_id: str, files: Dict[str, str], package_meta: Optional[Dict] = None) -> str:
        """Create a package (loan folder) that groups files and metadata and store it.

        `files` is a mapping of logical name -> absolute path.
        Returns the package path.
        """
        pkg_name = f"package_{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        pkg_dir = os.path.join(self.packages_dir, pkg_name)
        os.makedirs(pkg_dir, exist_ok=True)

        # copy or move files into package dir (we'll copy to keep originals)
        pkg_files = {}
        for key, path in files.items():
            if not path:
                continue
            if os.path.exists(path):
                dest_path = os.path.join(pkg_dir, os.path.basename(path))
                with open(path, 'rb') as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())
                pkg_files[key] = dest_path

        record = {
            'session_id': session_id,
            'package_name': pkg_name,
            'package_path': pkg_dir,
            'files': pkg_files,
            'metadata': package_meta or {},
            'created_at': datetime.now().isoformat()
        }

        self._append_metadata('packages', record)
        return pkg_dir

    def notify_manager(self, manager_payload: Dict) -> None:
        """Add an entry to the manager inbox (simulated notification)."""
        with open(self.manager_inbox, 'r+', encoding='utf-8') as fh:
            try:
                data = json.load(fh)
            except Exception:
                data = []
            data.insert(0, manager_payload)
            fh.seek(0)
            json.dump(data, fh, indent=2)
            fh.truncate()

    def _append_metadata(self, key: str, entry: Dict) -> None:
        with open(self.meta_path, 'r+', encoding='utf-8') as fh:
            try:
                meta = json.load(fh)
            except Exception:
                meta = {'uploads': [], 'packages': []}

            if key not in meta:
                meta[key] = []
            meta[key].insert(0, entry)
            fh.seek(0)
            json.dump(meta, fh, indent=2)
            fh.truncate()
