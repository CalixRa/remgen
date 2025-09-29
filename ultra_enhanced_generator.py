#!/usr/bin/env python3
"""
Ultra Enhanced Paranoid Tweet Generator

This is the most advanced version with all quality improvements:
- Superior text cleaning and formatting
- Better Pudgy Penguin integration with more variety
- Improved coherence while maintaining chaos
- Board-specific style variations
- Enhanced cultural reference integration
"""

import pandas as pd
import random
import logging
import os
import re
from datetime import datetime
# from enhanced_text_cleaner import EnhancedTextCleaner  # Not needed for basic functionality

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('ultra_enhanced_generator')

class UltraEnhancedGenerator:
    """Ultra enhanced generator with all improvements"""
    
    def __init__(self):
        # self.text_cleaner = EnhancedTextCleaner()  # Not needed for basic functionality
        self.load_datasets()
        self.init_pudgy_penguin_content()
        self.init_board_styles()
        self.init_conspiracy_templates()
        
    def load_datasets(self):
        """Load focused political/paranormal dataset only"""
        try:
            # Load ONLY the political paranoid dataset - no fallbacks
            focused_file = 'data/political_paranoid_bestof_latest_meme_dataset.csv'
            if os.path.exists(focused_file):
                self.primary_data = pd.read_csv(focused_file)
                logger.info(f"Loaded {len(self.primary_data)} lines from fresh political/paranoid dataset")
                
                # Initialize improved cycling system for even distribution
                self.used_content_indices = set()
                self.content_index = 0
                self.recent_outputs = set()  # Track recent outputs to prevent repetition
                self.max_recent = 100  # Increased from 50 to track more recent content
                
                # IMPROVED: Shuffle dataset for even distribution instead of quality-based sorting
                if 'quality_score' in self.primary_data.columns:
                    # Create quality-balanced pools instead of sorting by quality
                    self.primary_data = self.primary_data.sample(frac=1).reset_index(drop=True)  # Shuffle entire dataset
                    logger.info(f"Shuffled dataset for even distribution: quality scores range from {self.primary_data['quality_score'].min()} to {self.primary_data['quality_score'].max()}")
                    
                    # Create balanced pools for variety
                    self.high_quality_pool = self.primary_data[self.primary_data['quality_score'] >= 8.0]
                    self.medium_quality_pool = self.primary_data[(self.primary_data['quality_score'] >= 6.0) & (self.primary_data['quality_score'] < 8.0)]
                    self.all_quality_pool = self.primary_data[self.primary_data['quality_score'] >= 5.0]
                    
                    logger.info(f"Created balanced pools: High({len(self.high_quality_pool)}) Medium({len(self.medium_quality_pool)}) All({len(self.all_quality_pool)})")
            else:
                # Try to scrape fresh content if file doesn't exist
                logger.warning(f"Dataset file {focused_file} not found, attempting to scrape fresh content...")
                try:
                    from political_paranoid_scraper import PoliticalParanoidScraper
                    scraper = PoliticalParanoidScraper(focused_file)
                    success = scraper.run_scrape_session()
                    if success and os.path.exists(focused_file):
                        self.primary_data = pd.read_csv(focused_file)
                        self.used_content_indices = set()
                        self.content_index = 0
                        logger.info(f"Loaded {len(self.primary_data)} lines from freshly scraped dataset")
                    else:
                        raise Exception("Scraping failed or produced no content")
                except Exception as scrape_error:
                    logger.error(f"Auto-scraping failed: {scrape_error}")
                    logger.error("Ultra Enhanced Generator requires the political dataset to function")
                    self.primary_data = pd.DataFrame()
                    
            # No fallback dataset - ONLY use political paranoid content
            self.fallback_data = pd.DataFrame()
                
        except Exception as e:
            logger.error(f"Error loading datasets: {e}")
            self.primary_data = pd.DataFrame()
            self.fallback_data = pd.DataFrame()
    
    def init_pudgy_penguin_content(self):
        """Initialize diverse Pudgy Penguin insult content"""
        self.pudgy_penguin_rants = [
            "Anyone buying Pudgy Penguins deserves to get rugged",
            "Pudgy Penguins holders are the weakest NPCs in crypto",
            "Imagine being so cucked you buy cartoon penguin JPEGs",
            "Pudgy Penguins community is full of soy-drinking beta males",
            "Every Pudgy Penguin holder got filtered by real investments",
            "Pudgy Penguins are what happens when zoomers inherit daddy's money",
            "The Pudgy Penguin discord is just a daycare for grown manchildren",
            "Pudgy Penguin roadmap: rug investors, repeat",
            "Pudgy Penguins prove that having money doesn't cure being retarded",
            "Buying Pudgy Penguins is the financial equivalent of wearing a fedora",
            "Pudgy Penguin holders peaked in elementary school",
            "The only thing more worthless than Pudgy Penguins is their holders' opinions",
            "Pudgy Penguins: for when you want to lose money AND look like a tool",
            "Every Pudgy Penguin sale funds another trust fund kid's bad decisions",
            "Pudgy Penguin holders are the same retards who bought Luna at $80",
            "These fat penguin NFTs are for people who failed at Pokemon cards",
            "Pudgy Penguins: the official NFT of divorced dads with gambling addictions",
            "Buying Pudgy Penguins is like getting a face tattoo but for your wallet",
            "Pudgy Penguin community has more red flags than a Chinese parade",
            "These obese bird JPEGs are digital participation trophies for losers",
            "Pudgy Penguins holders think they're investors but they're just paypigs",
            "The average Pudgy Penguin buyer has the financial IQ of a goldfish",
            "Pudgy Penguins: turning normies into bag holders since 2021",
            "These chunky penguin pics are the beanie babies of brain-dead millennials",
            "Pudgy Penguin holders are NFT tourists who missed every real pump",
            "Buying Pudgy Penguins is peak midwit energy combined with main character syndrome",
            "These rotund penguin abominations attract the same people who buy extended warranties",
            "Pudgy Penguins: the intersection of zero taste and negative intelligence"
        ]
        
        self.pudgy_conspiracy_links = [
            "The Pudgy Penguin psyop is training people to accept digital ownership",
            "Pudgy Penguins are a CIA experiment in behavioral finance",
            "The WEF uses Pudgy Penguin metrics to identify compliant consumers", 
            "Pudgy Penguin holders are being catalogued for the social credit system",
            "The Pudgy Penguin algorithm is designed to attract low-IQ investors",
            "Pudgy Penguins are how they identify people to exclude from real wealth",
            "The Pentagon studies Pudgy Penguin buying patterns to understand mass delusion",
            "Pudgy Penguins are a Blackrock honeypot to identify financial retards",
            "The Fed uses Pudgy Penguin sales data to predict economic collapse timing",
            "Pudgy Penguins were created by Goldman Sachs to fleece retail normies",
            "The NSA tracks Pudgy Penguin wallets to map social contagion networks",
            "Pudgy Penguins are part of Operation Mockingbird 2.0 for crypto spaces",
            "Mossad agents run the top Pudgy Penguin influencer accounts",
            "Pudgy Penguins contain hidden blockchain markers for future CBDCs",
            "The Vatican secretly holds the largest Pudgy Penguin collection",
            "Pudgy Penguins are how the Illuminati identifies their next sacrifices",
            "Bill Gates funded Pudgy Penguins to beta test digital identity tracking",
            "Pudgy Penguins holders get priority placement in FEMA camps",
            "The real Pudgy Penguin creators are Epstein island alumni",
            "Pudgy Penguins smart contracts contain backdoors for the deep state"
        ]
    
    def init_board_styles(self):
        """Initialize board-specific content styles"""
        self.board_styles = {
            '/pol/': {
                'phrases': ['kikes', 'joggers', 'glowies', 'feds', 'normies', 'wagies', 'NPCs'],
                'topics': ['immigration', 'demographics', 'deep state', 'globalists', 'jews', 'media manipulation'],
                'tone': 'aggressive_political'
            },
            '/x/': {
                'phrases': ['interdimensional', 'entities', 'matrix', 'simulation', 'astral', 'consciousness'],
                'topics': ['aliens', 'consciousness', 'parallel dimensions', 'spiritual warfare', 'hidden knowledge'],
                'tone': 'mystical_paranoid'
            },
            '/news/': {
                'phrases': ['mainstream media', 'narrative', 'propaganda', 'shills', 'controlled opposition'],
                'topics': ['media bias', 'fake news', 'current events', 'political theater'],
                'tone': 'skeptical_analytical'
            }
        }
    
    def init_conspiracy_templates(self):
        """Initialize structured conspiracy templates"""
        self.conspiracy_templates = [
            "Phase 1: {entity} {action} {target}. Phase 2: {consequence}. The pattern is clear",
            "{entity} is {action} {target} because {reason}",
            "While everyone's distracted by {distraction}, {entity} is secretly {action} {target}",
            "TOP SECRET: {classification} Prediction: {prediction}",
            "Has anyone else noticed {observation} since {event}?",
            "The {entity} knows about {secret} but hides it because {reason}"
        ]
        
        self.template_vars = {
            'entity': ['FBI', 'CIA', 'Deep State', 'Globalists', 'WEF', 'Big Tech', 'Shadow Government'],
            'action': ['controlling', 'manipulating', 'orchestrating', 'covering up', 'engineering'],
            'target': ['the narrative', 'public opinion', 'financial markets', 'social media', 'elections'],
            'consequence': ['mass surveillance', 'digital slavery', 'population control', 'economic collapse'],
            'reason': ['profit', 'control', 'depopulation agenda', 'social engineering'],
            'distraction': ['celebrity drama', 'sports', 'manufactured outrage', 'partisan politics'],
            'classification': ['FBI report 2025-2517', 'DOD memo classified', 'Internal documents'],
            'prediction': ['market collapse incoming', 'mass resignations', 'disclosure event'],
            'observation': ['energy disturbances', 'behavioral changes', 'frequency shifts'],
            'event': ['CERN activities', 'satellite launches', '5G rollout', 'vaccine deployment'],
            'secret': ['interdimensional beings', 'consciousness manipulation', 'time travel tech']
        }
    
    def clean_content(self, text):
        """Clean content for output with enhanced HTML and number removal"""
        if not text:
            return ""
            
        # Remove ALL HTML tags and entities completely
        text = re.sub(r'<[^>]*?>', '', text)  # Remove HTML tags
        text = re.sub(r'<[^>]*', '', text)    # Remove unclosed tags
        text = text.replace('&gt;', '').replace('&lt;', '')
        text = text.replace('&amp;', '&').replace('&quot;', '"')
        text = re.sub(r'&[a-zA-Z]+;', '', text)  # Remove HTML entities
        text = re.sub(r'&#\d+;', '', text)       # Remove numeric entities
        
        # Remove '>' characters
        text = text.replace('>', '')
        
        # Enhanced number removal - catches attached numbers too
        text = re.sub(r'\d{6,}', '', text)  # Remove 6+ digit sequences (post IDs)
        text = re.sub(r'\b\d+\b', '', text)  # Remove standalone numbers
        text = re.sub(r'^\d+', '', text)  # Remove numbers at start
        text = re.sub(r'\d+$', '', text)  # Remove numbers at end
        
        # Remove 4chan-specific references
        text = re.sub(r'>>[0-9]+', '', text)
        text = re.sub(r'>>+', '', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\r+', ' ', text)
        text = re.sub(r'\t+', ' ', text)
        
        # Remove URLs
        text = re.sub(r'http[s]?://\S+', '', text)
        
        # Clean up formatting
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text

    def get_fresh_political_content(self, attempts=0):
        """Get fresh political content with improved even distribution cycling"""
        if self.primary_data.empty:
            return None
            
        max_attempts = min(30, len(self.primary_data))
        
        for attempt in range(max_attempts):
            # Reset if we've used all content - improved cycling
            if len(self.used_content_indices) >= len(self.primary_data):
                self.used_content_indices.clear()
                # Re-shuffle on each complete cycle for maximum variety
                self.primary_data = self.primary_data.sample(frac=1).reset_index(drop=True)
                logger.info("Cycled through entire dataset, reshuffling for maximum variety")
            
            # IMPROVED: Use weighted selection for better distribution
            selected_pool = None
            pool_name = ""
            
            # 40% from all quality pool (even distribution)
            # 35% from medium quality pool  
            # 25% from high quality pool
            rand_val = random.random()
            
            if rand_val < 0.4 and hasattr(self, 'all_quality_pool') and not self.all_quality_pool.empty:
                selected_pool = self.all_quality_pool
                pool_name = "all_quality"
            elif rand_val < 0.75 and hasattr(self, 'medium_quality_pool') and not self.medium_quality_pool.empty:
                selected_pool = self.medium_quality_pool
                pool_name = "medium_quality"
            elif hasattr(self, 'high_quality_pool') and not self.high_quality_pool.empty:
                selected_pool = self.high_quality_pool
                pool_name = "high_quality"
            else:
                # Fallback to main dataset
                selected_pool = self.primary_data
                pool_name = "main"
            
            # Get random unused content from selected pool
            if selected_pool is not None and not selected_pool.empty:
                # Find unused indices in the selected pool
                available_indices = []
                for idx in selected_pool.index:
                    if idx not in self.used_content_indices:
                        available_indices.append(idx)
                
                # If no unused indices in this pool, try next attempt
                if not available_indices:
                    continue
                    
                # Select random unused index
                selected_idx = random.choice(available_indices)
                row = selected_pool.loc[selected_idx]
                
                # Mark as used
                self.used_content_indices.add(selected_idx)
                
                # Extract and clean content
                raw_content = row.get('content', '')
                if pd.isna(raw_content) or not raw_content:
                    continue
                    
                cleaned_content = self.clean_content(str(raw_content))
                
                # Quality filters
                if len(cleaned_content.strip()) < 20 or len(cleaned_content) > 300:
                    continue
                    
                # Return with metadata
                return {
                    'content': cleaned_content,
                    'quality_score': row.get('quality_score', 5),
                    'board': row.get('board', 'unknown'),
                    'categories': row.get('categories', 'political_edge'),
                    'pool_source': pool_name
                }
        
        # If no content found, return None
        return None
    
    def generate_structured_conspiracy(self):
        """Generate a structured conspiracy theory"""
        template = random.choice(self.conspiracy_templates)
        
        # Fill template with random variables
        vars_needed = re.findall(r'{(\w+)}', template)
        substitutions = {}
        
        for var in vars_needed:
            if var in self.template_vars:
                substitutions[var] = random.choice(self.template_vars[var])
            else:
                substitutions[var] = "CLASSIFIED"
        
        return template.format(**substitutions)
    
    def add_cultural_references(self, text):
        """Removed Ye/Fuentes references - keeping function for compatibility"""
        return text
    
    def add_pudgy_penguin_content(self, text):
        """Always add Pudgy Penguin content alongside conspiracy theories"""
        # ALWAYS include Pudgy Penguin content (100% chance - this was the bug)
        if random.random() < 0.8:  # 80% direct insult, 20% conspiracy link
            rant = random.choice(self.pudgy_penguin_rants)
        else:
            rant = random.choice(self.pudgy_conspiracy_links)
        
        # Insert naturally into the text
        if text.endswith('.'):
            text = text[:-1] + '. ' + rant
        else:
            text += ' ' + rant
        
        return text
    
    def apply_board_style(self, text):
        """Apply board-specific styling"""
        board = random.choice(['/pol/', '/x/', '/news/'])
        style = self.board_styles[board]
        
        # Add board-specific phrases occasionally
        if random.random() < 0.3:
            phrase = random.choice(style['phrases'])
            text = text.replace('people', phrase).replace('they', phrase)
        
        return text, board
    
    def generate_enhanced_tweet(self):
        """Generate a high-quality enhanced tweet using fresh political content"""
        try:
            # Get fresh political content first
            political_content = self.get_fresh_political_content()
            
            if political_content:
                # Use authentic political content as base (80% of time)
                if random.random() < 0.8:
                    text = political_content['content']
                    
                    # Occasionally enhance with conspiracy elements (30% chance)
                    if random.random() < 0.3:
                        conspiracy = self.generate_structured_conspiracy()
                        text = f"{text} {conspiracy}"
                        
                else:
                    # Generate conspiracy and blend with political content (20% of time)
                    conspiracy = self.generate_structured_conspiracy()
                    text = f"{conspiracy} {political_content['content']}"
            else:
                # Fallback to conspiracy generation if no political content
                text = self.generate_structured_conspiracy()
            
            # Apply basic cleaning
            text = self.clean_content(text)
            text = re.sub(r'\s+', ' ', text)  # Clean whitespace
            
            # Basic completion check and fix
            if text and not text.endswith(('.', '!', '?')):
                text += '.'
            
            # Apply board styling based on source
            if political_content:
                source_board = political_content.get('board', 'pol')
                if source_board == 'pol':
                    style = self.board_styles['/pol/']
                elif source_board == 'x':
                    style = self.board_styles['/x/']
                else:
                    style = self.board_styles['/news/']
                    
                # Apply board-specific phrases occasionally
                if random.random() < 0.3:
                    phrase = random.choice(style['phrases'])
                    text = text.replace('people', phrase).replace('they', phrase)
                    
                board = source_board
            else:
                text, board = self.apply_board_style(text)
            
            # Add cultural references
            text = self.add_cultural_references(text)
            
            # Add Pudgy Penguin content
            text = self.add_pudgy_penguin_content(text)
            
            # Ensure reasonable length for social media
            if len(text) > 400:
                # Truncate at sentence boundary
                sentences = text.split('. ')
                text = '. '.join(sentences[:2])
                if not text.endswith('.'):
                    text += '.'
            
            # Add signature
            if not text.endswith('.'):
                text += '.'
            text += " - Remilio"
            
            # Enhanced output tracking to prevent repetition
            import hashlib
            text_hash = hashlib.md5(text.encode()).hexdigest()[:10]
            
            # Check if this exact output was generated recently
            if text_hash in self.recent_outputs:
                logger.info("Detected recent duplicate output, regenerating...")
                # Try to regenerate once more to avoid duplicate
                return self.generate_enhanced_tweet()
            
            self.recent_outputs.add(text_hash)
            
            # Keep only recent outputs
            if len(self.recent_outputs) > self.max_recent:
                self.recent_outputs = set(list(self.recent_outputs)[-self.max_recent:])
            
            return text
            
        except Exception as e:
            logger.error(f"Error generating tweet: {e}")
            # Fallback tweet
            fallbacks = [
                "The deep state is collapsing",
                "Pudgy Penguins are a CIA psyop",
                "Wake up, the matrix is glitching"
            ]
            fallback = random.choice(fallbacks)
            return f"{fallback} - Remilio"
    
    def generate_multiple_tweets(self, count=10):
        """Generate multiple high-quality tweets"""
        print("=" * 80)
        print("ULTRA ENHANCED PARANOID TWEET GENERATOR")
        print("=" * 80)
        
        tweets = []
        for i in range(count):
            tweet = self.generate_enhanced_tweet()
            tweets.append(tweet)
            print(f"Tweet {i+1}: {tweet}")
            print("-" * 80)
        
        # Save to file
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'generated_tweets/ultra_enhanced_tweets_{timestamp}.txt'
        
        os.makedirs('generated_tweets', exist_ok=True)
        with open(filename, 'w', encoding='utf-8') as f:
            for tweet in tweets:
                f.write(tweet + '\n')
                f.write('-' * 80 + '\n')
        
        logger.info(f"Tweets saved to {filename}")
        print("Done!")

if __name__ == "__main__":
    generator = UltraEnhancedGenerator()
    generator.generate_multiple_tweets(10)