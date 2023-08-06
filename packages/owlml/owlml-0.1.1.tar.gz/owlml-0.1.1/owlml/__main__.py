"""Main entry point for OwlML CLI."""
import fire

from .upload_images import upload_images


def main() -> None:
    """Call CLI commands."""
    fire.Fire({"upload-images": upload_images})
