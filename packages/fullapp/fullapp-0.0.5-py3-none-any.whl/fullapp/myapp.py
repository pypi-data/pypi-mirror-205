import logging
from fastapi import FastAPI

LOGGER = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class MyApp:
    def say(self, msg: str):
        full_msg = f"Saying: {msg}"
        LOGGER.info(full_msg)
        print(msg)

    def log_stuff(self):
        LOGGER.debug("debug message")
        LOGGER.info("info message")
        LOGGER.warning("warn message")
        LOGGER.error("error message")
        LOGGER.critical("critical message")


if __name__ == "__main__":  # pragma: no cover
    my_app = MyApp()
    my_app.log_stuff()
    my_app.say(
        (
            "Logging isn't configured here (but is in main.py), so just "
            "default logging, which doesn't include debug, or files."
        )
    )
