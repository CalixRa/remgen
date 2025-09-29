#!/usr/bin/env python3
"""
Automated Dynamic Content Generator

This script:
1. Processes content from dynamic content streams
2. Generates chaotic "Remilio" style posts using the processed content
3. Logs the generated posts locally without posting to social media
"""

import os
import time
import random
import logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Local modules
from enhanced_ultimate_edge_generator import EnhancedUltimateEdgeGenerator
# Twitter posting functionality removed

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("auto_content_bot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('auto_content_bot')

class AutoContentBot:
    """
    Automated bot that processes dynamic content streams and generates Remilio-style posts
    """
    
    def __init__(self):
        """Initialize the bot components"""
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Use the enhanced ultimate edge generator
        self.generator = EnhancedUltimateEdgeGenerator()
        
        # Twitter functionality removed
        self.twitter_enabled = False
        logger.info("Running in content generation mode - no posting to social media")
        
        # Bot settings from environment variables
        self.min_scrape_interval = int(os.getenv('MIN_SCRAPE_INTERVAL_HOURS', '3'))
        self.max_scrape_interval = int(os.getenv('MAX_SCRAPE_INTERVAL_HOURS', '6'))
        self.min_tweet_interval = int(os.getenv('MIN_TWEET_INTERVAL_HOURS', '2'))
        self.max_tweet_interval = int(os.getenv('MAX_TWEET_INTERVAL_HOURS', '5'))
        self.threads_per_scrape = int(os.getenv('THREADS_PER_SCRAPE', '10'))
    
    def scrape_content(self):
        """Process new content from dynamic streams using the SimpleMemeDatasetBuilder"""
        try:
            logger.info("Starting content scraping...")
            
            # Step 1: Process dynamic content
            chan_count = self.scraper.scrape_4chan()
            logger.info(f"Processed {chan_count} items from dynamic streams")
            
            # Step 2: Add prefabricated content
            prefab_count = self.scraper.add_prefabricated_content()
            logger.info(f"Added {prefab_count} prefabricated content items")
            
            # Step 3: Merge with existing datasets
            merged_count = self.scraper.merge_existing_datasets()
            logger.info(f"Merged {merged_count} items from existing datasets")
            
            # Step 4: Build final dataset
            dataset_path = self.scraper.build_dataset()
            
            # Get total count
            import pandas as pd
            df = pd.read_csv('data/god_tier_meme_dataset.csv')
            total_count = len(df)
            
            logger.info(f"Scraping complete. Dataset now contains {total_count} items.")
            # If we scraped anything new, consider this successful
            total_new = chan_count + prefab_count + merged_count
            return total_new > 0
        except Exception as e:
            logger.error(f"Error during scraping: {e}", exc_info=True)
            return False
    
    def generate_and_log_post(self):
        """Generate a Remilio-style post and log it locally"""
        try:
            # Generate a post
            logger.info("Generating post...")
            tweet_text = self.generator.generate_enhanced_edge_tweet()
            
            if not tweet_text:
                logger.warning("Failed to generate valid content.")
                return False
            
            logger.info(f"Generated post: {tweet_text}")
            
            # Log the post locally
            logger.info("Saving post to local storage.")
            # Log the generated tweet locally
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"generated_tweets/auto_content_tweet_{timestamp}.txt"
            os.makedirs('generated_tweets', exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Generated at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Tweet: {tweet_text}\n")
            logger.info(f"Tweet saved to {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Error during tweet generation: {e}", exc_info=True)
            return False
    
    def verify_dataset(self):
        """Verify the dataset exists and has content, force scrape if not"""
        dataset_path = 'data/god_tier_meme_dataset.csv'
        
        if not os.path.exists(dataset_path) or os.path.getsize(dataset_path) == 0:
            logger.warning(f"Dataset file {dataset_path} does not exist or is empty. Forcing scrape.")
            return self.scrape_content()
        
        try:
            import pandas as pd
            df = pd.read_csv(dataset_path)
            count = len(df)
            
            if count < 50:  # If we have too few items, force a scrape
                logger.warning(f"Dataset only contains {count} items. Forcing scrape to get more content.")
                return self.scrape_content()
            
            logger.info(f"Dataset verification passed. {count} items available.")
            return True
        except Exception as e:
            logger.error(f"Error verifying dataset: {e}", exc_info=True)
            return self.scrape_content()
    
    def run(self):
        """Run the bot in a continuous loop"""
        logger.info("Starting Dynamic Content Generator...")
        
        # Do an initial dataset verification to ensure we have content
        self.verify_dataset()
        
        last_scrape_time = time.time()
        consecutive_failures = 0
        max_consecutive_failures = 5
        
        while True:
            try:
                current_time = time.time()
                
                # Determine if it's time to scrape new content
                scrape_interval = random.randint(
                    self.min_scrape_interval * 3600,
                    self.max_scrape_interval * 3600
                )
                
                if current_time - last_scrape_time > scrape_interval:
                    scrape_success = self.scrape_content()
                    if scrape_success:
                        last_scrape_time = current_time
                        consecutive_failures = 0  # Reset failure counter on successful scrape
                    else:
                        consecutive_failures += 1
                        logger.warning(f"Scrape failed. Consecutive failures: {consecutive_failures}")
                
                # Generate and save a post locally
                post_success = self.generate_and_log_post()
                if post_success:
                    consecutive_failures = 0  # Reset failure counter on successful post generation
                else:
                    consecutive_failures += 1
                    logger.warning(f"Post generation failed. Consecutive failures: {consecutive_failures}")
                
                # If too many consecutive failures, try to reinitialize components
                if consecutive_failures >= max_consecutive_failures:
                    logger.warning(f"Too many consecutive failures ({consecutive_failures}). Reinitializing components...")
                    try:
                        # Reinitialize components
                        self.scraper = SimpleMemeDatasetBuilder(output_file='data/god_tier_meme_dataset.csv')
                        self.generator = SimpleTweetGenerator(input_file='data/god_tier_meme_dataset.csv')
                        
                        # Twitter functionality removed
                        
                        # Force a scrape after reinitialization
                        self.scrape_content()
                        last_scrape_time = time.time()
                        consecutive_failures = 0
                    except Exception as e:
                        logger.error(f"Error reinitializing components: {e}", exc_info=True)
                
                # Random sleep to avoid predictable patterns
                sleep_minutes = random.randint(30, 90)
                next_check = datetime.now() + timedelta(minutes=sleep_minutes)
                logger.info(f"Sleeping for {sleep_minutes} minutes (until {next_check.strftime('%H:%M:%S')})...")
                time.sleep(sleep_minutes * 60)
            
            except KeyboardInterrupt:
                logger.info("Bot stopped by user.")
                break
            
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}", exc_info=True)
                consecutive_failures += 1
                
                # Adjust sleep time based on consecutive failures (up to 60 minutes)
                sleep_minutes = min(15 * consecutive_failures, 60)
                next_check = datetime.now() + timedelta(minutes=sleep_minutes)
                logger.info(f"Sleeping for {sleep_minutes} minutes after error (until {next_check.strftime('%H:%M:%S')})...")
                time.sleep(sleep_minutes * 60)

def test_mode():
    """Run the bot in test mode - scrape once and generate some tweets"""
    print("=" * 80)
    print("4CHAN TWEET GENERATOR - TEST MODE")
    print("=" * 80)
    
    bot = AutoContentBot()
    
    print("\nScraping 4chan for new content...")
    bot.scrape_content()
    
    print("\nGenerating 5 sample tweets:")
    for i in range(5):
        tweet = bot.generator.generate_tweet()
        print(f"\nTweet {i+1}: {tweet}")
    
    print("\nTest complete! To run the bot continuously, run with --run")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--run":
        # Run the bot continuously
        bot = AutoContentBot()
        bot.run()
    else:
        # Run in test mode by default
        test_mode()