import logging 

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Log to the console
        logging.FileHandler(".log", mode="a")  # Log to a file
    ]
)

logger = logging.getLogger("fastapi-app")
