from pathlib import Path


class Directory:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent

        # Log folder
        self.log_dir = self.base_dir / "log"

        # Config folder
        self.config_dir = self.base_dir / "config"
        self.json_dir = self.config_dir / "json"
        self.model_dir = self.config_dir / "model"

        # Data folder
        self.data_dir = self.base_dir / "data"
        self.images_dir = self.data_dir / "images"
        self.data_send_dir = self.data_dir / "datasend"

    def create_folders(self) -> None:
        folders = [
            self.log_dir,
            self.json_dir,
            self.model_dir,
            self.images_dir,
            self.data_send_dir,
        ]
        for fol in folders:
            try:
                fol.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Failed to create directory {fol}: {e}")


directory = Directory()
directory.create_folders()
