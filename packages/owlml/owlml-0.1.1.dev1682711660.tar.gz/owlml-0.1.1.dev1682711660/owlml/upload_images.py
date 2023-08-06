"""Upload images to a CVAT task."""
from pathlib import Path
from typing import Any, Optional, Union

import randomname
from cvat_sdk.core.helpers import TqdmProgressReporter
from cvat_sdk.core.proxies.tasks import ResourceType
from tqdm import tqdm

from .auth import get_cvat_client

VALID_IMAGE_FORMATS = [".jpg", ".jpeg", ".png"]


def create_task(name: str, project_id: int, segment_size: int = 25) -> dict[str, Any]:
    """Create a new task (without attached images/videos)."""
    data = {"name": name, "project_id": project_id, "segment_size": segment_size}
    with get_cvat_client() as client:
        task, _ = client.tasks.api.create(data)
    return task.to_dict()


def upload_image_list(task_id: int, image_list: list[Union[str, Path]]) -> None:
    """Upload a list of images to a task."""
    with get_cvat_client() as client:
        task = client.tasks.retrieve(task_id)
        task.upload_data(
            ResourceType.LOCAL,
            [str(i) for i in image_list],
            pbar=TqdmProgressReporter(tqdm()),
        )


def upload_images(
    image_directory: Union[str, Path],
    project_id: Optional[int] = None,
    task_name: Optional[str] = None,
    segment_size: int = 25,
) -> None:
    """Upload images from a directory to a task."""
    if project_id is None:
        raise ValueError("project_id must be specified")
    if task_name is None:
        task_name = randomname.get_name()
    task = create_task(task_name, project_id, segment_size)
    task_id = task["id"]
    image_directory = Path(image_directory)
    images = []
    for extension in VALID_IMAGE_FORMATS:
        images.extend(image_directory.glob(f"*{extension}"))
    upload_image_list(task_id, sorted(images))
    print(f"Uploaded {len(images)} images to task {task_name}")
