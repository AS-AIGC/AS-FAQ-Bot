"""
Automated Data Update Script
This script automatically updates data from the GitHub repository and regenerates
the vector database on an hourly schedule.

It will:
1. Download data from GitHub
2. Process the data
3. Generate combined_context_en.csv
4. Generate new vector database
"""

import os
import time
import logging
import shutil
import schedule
from datetime import datetime
import sys
from pathlib import Path

# Add the project root to the Python path to import local modules
sys.path.append(str(Path(__file__).parent))

# Import local modules
from utils.update_data import download_github_repo, combine_csv_files, check_git_updates
from utils.respond import SearchQASystem

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auto_update.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Constants
DATA_FOLDER = "FAQ_data"
DATA_DIR = os.path.abspath("./" + DATA_FOLDER)
OUTPUT_FILE = os.path.abspath("./combined_context_en.csv")
VECTOR_DB_PATH = os.path.abspath("./vector_database.bin")
REPO_URL = os.getenv("REPO_URL")


def update_data():
    """Main function to update data and regenerate the vector database"""
    try:
        # Create data directory if it doesn't exist
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)
            logger.info(f"Created data directory: {DATA_DIR}")
        
        # First check if there are any updates
        if not check_git_updates():
            logger.info("No updates in the repository, skipping update process")
            return True
            
        start_time = datetime.now()
        logger.info(f"Starting data update at {start_time}")
        
        # Change to data directory for operations
        original_dir = os.getcwd()
        os.chdir(DATA_FOLDER)
        logger.info(f"Changed working directory to {os.getcwd()}")
        
        # Download GitHub repository
        logger.info("Downloading GitHub repository...")
        download_github_repo()
        
        # Process and combine CSV files
        logger.info("Processing and combining CSV files...")
        combine_csv_files()
        
        # Move the combined CSV file if it's not already in the right place
        if os.path.exists(OUTPUT_FILE) and os.path.abspath(OUTPUT_FILE) != OUTPUT_FILE:
            logger.info(f"Moving {OUTPUT_FILE} to its final location")
            shutil.move(OUTPUT_FILE, OUTPUT_FILE)
        
        # Change back to original directory
        os.chdir(original_dir)
        logger.info(f"Changed working directory back to {original_dir}")
        
        # Update vector database
        logger.info("Updating vector database...")
        qa_system = SearchQASystem()
        qa_system._update_vector_database()
        
        end_time = datetime.now()
        duration = end_time - start_time
        logger.info(f"Data update completed at {end_time}. Duration: {duration}")
        
        return True
    except Exception as e:
        logger.error(f"Error during data update: {str(e)}")
        return False


def run_scheduler():
    """Run the scheduler loop"""
    # Schedule hourly updates
    schedule.every(1).hour.do(update_data)
    logger.info("Scheduled hourly updates")
    
    # Keep the script running and execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute


if __name__ == "__main__":
    try:
        logger.info("Starting automated data update service")
        # Run update immediately on startup
        logger.info("Running initial update...")
        if REPO_URL is None or REPO_URL == "":
            logger.error("REPO_URL environment variable is not set. Exiting.")
            sys.exit(1)
        
        update_data()
        
        # Start the scheduler
        run_scheduler()
    except KeyboardInterrupt:
        logger.info("Service stopped by user")
    except Exception as e:
        logger.error(f"Service error: {str(e)}")
