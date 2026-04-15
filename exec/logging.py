import logging
import os

def setup():
    os.makedirs("bot", exist_ok=True)
    log_path = os.path.join("exec", "exec.log")

    logging.basicConfig(
        filename=log_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s -%(message)s",
    )

    return logging.getLogger()