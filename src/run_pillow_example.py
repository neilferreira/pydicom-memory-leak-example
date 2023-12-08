import logging
import queue
import tempfile
import threading
import time

from PIL import Image

import utils.logging_config  # noqa
from utils.mem import watch_memory

logger = logging.getLogger()


flip_queue = queue.Queue()


def worker():
    while True:
        try:
            original_image = flip_queue.get()

            print(f"Flip around {original_image}")
            horizontal_image = original_image.transpose(Image.FLIP_TOP_BOTTOM)
            with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
                horizontal_image.save(tmp.name)
        except Exception:
            logger.exception("An error occurred.")
        finally:
            flip_queue.task_done()


def run_workers():
    for x in range(5):
        t = threading.Thread(target=worker, daemon=True)
        t.start()


def on_image_receive(image):
    try:
        logger.info("received image")
        flip_queue.put(image)
    finally:
        return 0x0000


run_workers()
watch_memory()


for x in range(50):
    image = Image.open("src/image.jpg")
    on_image_receive(image=image)


print("Sleeping...")
time.sleep(15)
print(
    "At this point, the memory usage should be no more than ~2mb which is what it took to run this script."
    "Any more, and we have a memory leak"
)
