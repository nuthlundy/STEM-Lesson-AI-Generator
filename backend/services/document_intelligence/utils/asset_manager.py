import os
import shutil

class AssetManager:
    def __init__(self, job_id: str, base_dir: str = "uploads/jobs"):
        self.job_id = job_id
        self.base_dir = base_dir

    def get_job_dir(self) -> str:
        """Returns the absolute path for the job directory."""
        return os.path.abspath(os.path.join(self.base_dir, self.job_id))

    def get_assets_dir(self) -> str:
        """Returns the absolute path for the job assets directory."""
        return os.path.join(self.get_job_dir(), "assets")

    def create_job_workspace(self) -> None:
        """Creates the job and assets directories if they do not exist."""
        os.makedirs(self.get_job_dir(), exist_ok=True)
        os.makedirs(self.get_assets_dir(), exist_ok=True)

    def get_asset_filename(self, page_number: int, asset_type: str, index: int, extension: str) -> str:
        """Generates a standardized filename for an asset."""
        # Ensure extension doesn't have a leading dot
        ext = extension.lstrip('.')
        return f"{self.job_id}_page{page_number}_{asset_type}_{index}.{ext}"

    def save_asset(self, page_number: int, asset_type: str, index: int, extension: str, data: bytes) -> str:
        """Saves asset bytes to the job's asset folder and returns the relative path inside the workspace."""
        self.create_job_workspace()
        filename = self.get_asset_filename(page_number, asset_type, index, extension)
        filepath = os.path.join(self.get_assets_dir(), filename)
        with open(filepath, "wb") as f:
            f.write(data)
        # Return relative path directly, e.g., "assets/job_page1_image_0.png"
        return os.path.relpath(filepath, self.get_job_dir()).replace('\\', '/')

    def clean_job_workspace(self) -> None:
        """Deletes the job directory and all its contents."""
        job_dir = self.get_job_dir()
        if os.path.exists(job_dir):
            shutil.rmtree(job_dir)
