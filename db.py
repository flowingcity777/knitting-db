import json
import os
import shutil
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class KnittingDB:
    def __init__(self, storage_file="knitting_db.json", auto_save=True):
        self.storage_file = storage_file
        self.auto_save = auto_save
        self.data = {}
        self._load_data()

    def _load_data(self):
        """Load data from disk, handle corruption gracefully."""
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, "r") as f:
                    self.data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️ Error loading data: {e}. Starting fresh.")
            self.data = {}

    def _save_data(self):
        """Save data to disk atomically."""
        try:
            with open(self.storage_file, "w") as f:
                json.dump(self.data, f)
        except IOError as e:
            print(f"⚠️ Failed to save data: {e}")

    def set(self, key, value, auto_save=None):
        """Store a knitting pattern (optionally skip immediate save)."""
        self.data[key] = value
        if (auto_save if auto_save is not None else self.auto_save):
            self._save_data()

    def get(self, key):
        """Retrieve a knitting pattern."""
        return self.data.get(key)

    def delete(self, key):
        """Delete a pattern."""
        if key in self.data:
            del self.data[key]
            self._save_data()

    # === Backup System ===
    def backup(self, backup_dir="backups"):
        """Create a timestamped local backup."""
        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"{backup_dir}/knitting_db_{timestamp}.json"
        try:
            shutil.copy2(self.storage_file, backup_file)
            print(f"✅ Local backup saved: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"⚠️ Local backup failed: {e}")
            return None

    def restore(self, backup_file=None):
        """Restore from the latest backup (or specific file)."""
        if backup_file is None:
            backup_file = self._find_latest_backup()
        if backup_file and os.path.exists(backup_file):
            try:
                shutil.copy2(backup_file, self.storage_file)
                self._load_data()
                print(f"✅ Restored from: {backup_file}")
            except Exception as e:
                print(f"⚠️ Restore failed: {e}")
        else:
            print("⚠️ No backups found. Starting fresh.")

    def _find_latest_backup(self, backup_dir="backups"):
        """Find the most recent backup file."""
        if not os.path.exists(backup_dir):
            return None
        backups = [f for f in os.listdir(backup_dir) if f.startswith("knitting_db_")]
        if not backups:
            return None
        latest = max(backups, key=lambda f: os.path.getctime(f"{backup_dir}/{f}"))
        return f"{backup_dir}/{latest}"

    # === Cloud Backup (Google Drive) ===
    def backup_to_drive(self, backup_dir="backups"):
        """Upload the latest backup to Google Drive."""
        try:
            backup_file = self.backup(backup_dir)  # Create local backup first
            if not backup_file:
                raise Exception("Local backup failed.")
            
            creds = service_account.Credentials.from_service_account_file("credentials.json")
            service = build("drive", "v3", credentials=creds)
            
            file_metadata = {
                "name": os.path.basename(backup_file),
                "parents": ["YOUR_DRIVE_FOLDER_ID"]  # Optional: Replace with your folder ID
            }
            media = MediaFileUpload(backup_file, mimetype="application/json")
            
            service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id"
            ).execute()
            print(f"☁️ Backup uploaded to Google Drive: {os.path.basename(backup_file)}")
        except Exception as e:
            print(f"⚠️ Drive upload failed: {e}")