from pathlib import Path
from shutil import rmtree


class DirectoryManager:
    """Handles directory structure and ensures required folders exist."""

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

        self._initialize_base_folders()

    def _initialize_base_folders(self):
        """Initialize base required directory paths."""
        folders = [
            self.log_dir,
            self.json_dir,
            self.model_dir,
            self.images_dir,
        ]
        for folder in folders:
            self.create_directory(folder)

    def create_directory(self, folder_path: Path, to_remove: bool = False) -> None:
        """Helper method to ensure the destination directory exists, and remove it if necessary."""
        if to_remove and folder_path.exists():
            try:
                rmtree(folder_path)
            except Exception as e:
                raise OSError(
                    f"Failed to remove existing directory: {folder_path}"
                ) from e

        try:
            folder_path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            raise OSError(f"Failed to create directory: {folder_path}") from e

    def list_png_paths(self, folder_path: Path) -> list[Path]:
        """Returns a list of all .png files in the given directory."""
        if not folder_path.exists():
            raise FileNotFoundError(f"Directory not found: {folder_path}")

        if not folder_path.is_dir():
            raise ValueError(f"Path is not a directory: {folder_path}")

        return list(folder_path.glob("*.png"))


directory_manager = DirectoryManager()
