import os
import time
import random
import logging
import traceback
from dotenv import load_dotenv

# Local modules
from scraper import FourChanScraper
from generator import TweetGenerator
from twitter_bot import TwitterBot
from logger import setup_logger

# Load environment variables
load_dotenv()

# Set up logger
logger = setup_logger('4chan_twitter_bot')

class Bot4ChanTwitter:
    """
    Main bot class that orchestrates the scraping, generation, and tweeting process
    """
    
    def __init__(self):
        """Initialize the bot components"""
        # Define consistent file paths
        self.data_dir = 'data'
        self.dataset_file = os.path.join(self.data_dir, 'chan_shitpost_dataset.csv')
        self.tweet_log_file = os.path.join(self.data_dir, 'tweet_log.csv')
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize components with consistent file paths
        self.scraper = FourChanScraper(boards=['b', 'r9k'], output_file=self.dataset_file)
        self.generator = TweetGenerator(input_file=self.dataset_file)
        self.twitter_bot = TwitterBot(log_file=self.tweet_log_file)
        
        # Bot settings
        self.min_scrape_interval = int(os.getenv('MIN_SCRAPE_INTERVAL_HOURS', '3'))
        self.max_scrape_interval = int(os.getenv('MAX_SCRAPE_INTERVAL_HOURS', '6'))
        self.min_tweet_interval = int(os.getenv('MIN_TWEET_INTERVAL_HOURS', '2'))
        self.max_tweet_interval = int(os.getenv('MAX_TWEET_INTERVAL_HOURS', '5'))
        self.threads_per_scrape = int(os.getenv('THREADS_PER_SCRAPE', '10'))
    
    def scrape_content(self):
        """Scrape new content from 4chan"""
        try:
            logger.info("Starting content scraping...")
            num_scraped = self.scraper.scrape(max_threads_per_board=self.threads_per_scrape)
            logger.info(f"Scraping complete. Collected {num_scraped} new items.")
            return num_scraped > 0
        except Exception as e:
            logger.error(f"Error during scraping: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def generate_and_tweet(self):
        """Generate a tweet and post it to Twitter"""
        try:
            # Check if it's time to tweet
            if not self.twitter_bot.should_tweet_now(
                min_hours=self.min_tweet_interval,
                max_hours=self.max_tweet_interval
            ):
                logger.info("Not time to tweet yet.")
                return False
            
            # Generate a tweet
            logger.info("Generating tweet...")
            tweet_text = self.generator.generate_multiple_tweets(count=3)
            
            if not tweet_text or tweet_text == "Failed to generate a valid tweet.":
                logger.warning("Failed to generate valid tweet content.")
                return False
            
            logger.info(f"Generated tweet: {tweet_text}")
            
            # Post the tweet
            logger.info("Posting to Twitter...")
            success, result = self.twitter_bot.post_tweet(tweet_text)
            
            if success:
                logger.info(f"Successfully posted tweet with ID: {result}")
            else:
                logger.error(f"Failed to post tweet: {result}")
            
            return success
        
        except Exception as e:
            logger.error(f"Error during tweet generation/posting: {e}")
            logger.error(traceback.format_exc())
            return False
    
    def run(self):
        """Run the bot in a continuous loop"""
        logger.info("Starting 4chan Twitter Bot...")
        
        last_scrape_time = 0
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        while True:
            try:
                current_time = time.time()
                
                # Verify dataset file exists
                if not os.path.exists(self.dataset_file) or os.path.getsize(self.dataset_file) == 0:
                    logger.warning(f"Dataset file {self.dataset_file} does not exist or is empty. Forcing scrape.")
                    scrape_success = self.scrape_content()
                    if scrape_success:
                        last_scrape_time = current_time
                        logger.info("Initial scraping completed successfully.")
                    else:
                        logger.error("Initial scraping failed. Will retry after delay.")
                        time.sleep(15 * 60)  # 15 minutes
                        continue
                
                # Determine if it's time to scrape new content
                scrape_interval = random.randint(
                    self.min_scrape_interval * 3600,
                    self.max_scrape_interval * 3600
                )
                
                # Scrape content if it's time or if we have few items
                should_scrape = False
                
                if current_time - last_scrape_time > scrape_interval:
                    logger.info("Scheduled scraping time reached.")
                    should_scrape = True
                else:
                    # Check if we have enough content for generation
                    try:
                        if os.path.exists(self.dataset_file):
                            df = pd.read_csv(self.dataset_file)
                            if len(df) < 100:  # If we have less than 100 items
                                logger.info(f"Dataset has only {len(df)} items. Forcing scrape to get more content.")
                                should_scrape = True
                    except Exception as e:
                        logger.error(f"Error checking dataset size: {e}")
                        should_scrape = True  # Scrape anyway if we can't check
                
                if should_scrape:
                    scrape_success = self.scrape_content()
                    if scrape_success:
                        last_scrape_time = current_time
                        logger.info("Scraping completed successfully.")
                
                # Try to generate and post a tweet
                tweet_result = self.generate_and_tweet()
                if tweet_result:
                    # Reset failure counter on success
                    consecutive_failures = 0
                    logger.info("Tweet generation and posting successful.")
                else:
                    consecutive_failures += 1
                    logger.warning(f"Tweet generation or posting failed. Consecutive failures: {consecutive_failures}")
                
                # If we've had too many consecutive failures, try to reinitialize components
                if consecutive_failures >= max_consecutive_failures:
                    logger.warning(f"Too many consecutive failures ({consecutive_failures}). Reinitializing components...")
                    try:
                        # Reinitialize components
                        self.generator = TweetGenerator(input_file=self.dataset_file)
                        self.twitter_bot = TwitterBot(log_file=self.tweet_log_file)
                        consecutive_failures = 0
                    except Exception as e:
                        logger.error(f"Error reinitializing components: {e}")
                
                # Random sleep to avoid predictable patterns
                sleep_minutes = random.randint(30, 90)
                logger.info(f"Sleeping for {sleep_minutes} minutes (until {time.strftime('%H:%M:%S', time.localtime(time.time() + sleep_minutes*60))})...")
                time.sleep(sleep_minutes * 60)
            
            except KeyboardInterrupt:
                logger.info("Bot stopped by user.")
                break
            
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                logger.error(traceback.format_exc())
                consecutive_failures += 1
                
                # Determine sleep time based on consecutive failures
                sleep_minutes = min(15 * consecutive_failures, 60)  # Max 60 minutes
                logger.info(f"Sleeping for {sleep_minutes} minutes after error...")
                time.sleep(sleep_minutes * 60)

if __name__ == "__main__":
    # Create and run the bot
    bot = Bot4ChanTwitter()
    bot.run()
