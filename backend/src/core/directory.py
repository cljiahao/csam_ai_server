from pathlib import Path


class Directory:
    """Handles directory paths and folder creation for the application."""

    def __init__(self) -> None:
        """Initialize directory paths."""
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

    def create_folders(self, folders: list[Path]) -> None:
        """Create necessary folders for logging, configuration, and data."""
        for folder in folders:
            try:
                folder.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Failed to create directory {folder}: {e}")


# Instantiate Directory and create folders
directory = Directory()
folders = [
    directory.log_dir,
    directory.json_dir,
    directory.model_dir,
    directory.images_dir,
    directory.data_send_dir,
]
directory.create_folders(folders)
