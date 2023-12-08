import logging
import queue
import sys
import tempfile
import threading
import time

from pydicom import dcmread

import utils.logging_config  # noqa
from utils.mem import watch_memory

logger = logging.getLogger()


flip_queue = queue.Queue()


def worker():
    while True:
        try:
            original_image = flip_queue.get()

            SUPPORTED_TRANSFER_SYNTAXES = {
                "1.2.840.10008.1.2": "numpy_handler",  # Implicit VR Endian
                "1.2.840.10008.1.2.1": "numpy_handler",  # Explicit VR Little Endian
                "1.2.840.10008.1.2.1.99": "numpy_handler",  # Deflated Explicit VR Little Endian
                "1.2.840.10008.1.2.2": "numpy_handler",  # Explicit VR Big Endian
                "1.2.840.10008.1.2.5": "rle_handler",  # RLE Lossless
                "1.2.840.10008.1.2.4.50": "pillow_handler",  # JPEG Baseline (Process 1)
                "1.2.840.10008.1.2.4.70": "pylibjpeg_handler",  # JPEG Lossles (Process 14 SV 1)
            }

            print(
                f"Flip around {original_image} using {SUPPORTED_TRANSFER_SYNTAXES[original_image.file_meta.TransferSyntaxUID]}"  # noqa
            )
            original_image.decompress(SUPPORTED_TRANSFER_SYNTAXES[original_image.file_meta.TransferSyntaxUID])
            with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
                original_image.save_as(tmp.name)

            del original_image
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


sample_filename = f"src/{sys.argv[1]}.dcm"
# assert this file exists
dcmread(sample_filename)


run_workers()
watch_memory()


for x in range(75):
    image = dcmread(sample_filename)
    on_image_receive(image=image)


while flip_queue.qsize():
    print(f"{flip_queue.qsize()} remaining tasks..")
    time.sleep(1)

print("Script has completed.")
time.sleep(300)
