#!/usr/bin/env python3
"""
Enhanced Ultimate Edge Generator - Authentic 4chan Edge Content

This generator creates the most controversial and edgy content using authentic
posts from the Enhanced Ultimate Edge Scraper. It transforms raw 4chan content
into polished social media posts while preserving the authentic edge and
controversial nature.

Core Philosophy: "Maximum Edge with Authentic Voice"
- Preserve genuine controversial takes and hot opinions
- Transform chan culture into social media compatible format
- Maintain authentic edginess while removing platform-specific references
- Create content that pushes boundaries with real user sentiment

Generation Styles:
- Sexual Edge Mode: Relationship hot takes and dating commentary
- Political Edge Mode: Controversial political opinions and takes
- Dark Humor Edge Mode: Edgy jokes and provocative humor
- General Edge Mode: Broad controversial statements and opinions
"""

import pandas as pd
import random
import logging
import os
from datetime import datetime
import hashlib
import time
import re
import html

class EnhancedUltimateEdgeGenerator:
    """
    Elite generator for maximum edge content using authentic 4chan material
    """
    
    def __init__(self, edge_file='data/enhanced_ultimate_god_tier.csv'):
        """Initialize the enhanced ultimate edge generator"""
        self.edge_file = edge_file
        self.df = None
        self.content_pools = {}
        self.recent_content = set()
        self.max_recent = 100
        self.setup_logging()
        self.load_edge_dataset()
        self.organize_content_pools()
        
    def setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('enhanced_edge_generator')
        
    def load_edge_dataset(self):
        """Load the enhanced edge dataset"""
        try:
            if os.path.exists(self.edge_file):
                self.df = pd.read_csv(self.edge_file)
                self.logger.info(f"✅ Loaded {len(self.df)} authentic edge posts")
            else:
                self.logger.error(f"❌ Edge dataset not found: {self.edge_file}")
                self.df = pd.DataFrame()
        except Exception as e:
            self.logger.error(f"❌ Failed to load edge dataset: {e}")
            self.df = pd.DataFrame()
            
    def organize_content_pools(self):
        """Organize edge content into quality and category pools"""
        if self.df.empty:
            self.logger.warning("⚠️ No edge content available")
            return
            
        # Organize by category (the actual column name)
        categories = ['sexual_edge', 'political_edge', 'dark_humor_edge', 'general_edge']
        
        for category in categories:
            if 'category' in self.df.columns:
                type_content = self.df[self.df['category'] == category]
            else:
                # Fallback to all content if no category column
                type_content = self.df
                
            if not type_content.empty:
                # Further organize by quality_score (the actual column name)
                quality_col = 'quality_score' if 'quality_score' in self.df.columns else 'edge_quality'
                self.content_pools[f'{category}_high'] = type_content[type_content[quality_col] >= 8]
                self.content_pools[f'{category}_medium'] = type_content[
                    (type_content[quality_col] >= 6) & (type_content[quality_col] < 8)
                ]
                self.content_pools[f'{category}_good'] = type_content[type_content[quality_col] >= 5]
                
        self.logger.info(f"🔥 Organized edge content into {len(self.content_pools)} quality pools")
        
    def get_content_hash(self, content):
        """Generate hash for content tracking"""
        return hashlib.md5(content.encode()).hexdigest()[:12]
        
    def is_content_recent(self, content):
        """Check if content was used recently"""
        content_hash = self.get_content_hash(content)
        return content_hash in self.recent_content
        
    def track_content_usage(self, content):
        """Track content usage for anti-repetition"""
        content_hash = self.get_content_hash(content)
        self.recent_content.add(content_hash)
        
        # Keep only recent content to prevent infinite growth
        if len(self.recent_content) > self.max_recent:
            # Remove oldest entries (approximate)
            self.recent_content = set(list(self.recent_content)[-self.max_recent:])
            
    def select_generation_style(self):
        """Select a generation style based on content availability"""
        available_styles = []
        
        # Check what content is available
        if any('sexual_edge' in pool for pool in self.content_pools.keys()):
            available_styles.extend(['sexual_edge'] * 3)  # Weighted higher
        if any('political_edge' in pool for pool in self.content_pools.keys()):
            available_styles.extend(['political_edge'] * 2)
        if any('dark_humor_edge' in pool for pool in self.content_pools.keys()):
            available_styles.extend(['dark_humor_edge'] * 3)  # Weighted higher
        if any('general_edge' in pool for pool in self.content_pools.keys()):
            available_styles.extend(['general_edge'] * 4)  # Most common
            
        return random.choice(available_styles) if available_styles else 'general_edge'
        
    def get_fresh_edge_content(self, style=None, quality_tier=None, max_attempts=20):
        """Get fresh edge content that hasn't been used recently"""
        if style is None:
            style = self.select_generation_style()
            
        # Define quality preference order
        if quality_tier is None:
            quality_tiers = ['high', 'medium', 'good']
        else:
            quality_tiers = [quality_tier]
            
        for quality in quality_tiers:
            pool_key = f'{style}_{quality}'
            if pool_key in self.content_pools and not self.content_pools[pool_key].empty:
                pool = self.content_pools[pool_key]
                
                for attempt in range(max_attempts):
                    content_row = pool.sample(n=1).iloc[0]
                    content = content_row['content']
                    
                    if not self.is_content_recent(content):
                        return content_row
                        
        # Fallback: return any available content
        if not self.df.empty:
            self.logger.warning(f"⚠️ Using fallback content for {style}")
            return self.df.sample(n=1).iloc[0]
            
        return None
        
    def clean_edge_for_output(self, content):
        """Clean edge content for social media while preserving controversial nature"""
        if not content:
            return ""
            
        # Remove HTML entities and tags
        text = html.unescape(content)
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove standalone numbers
        text = re.sub(r'\b\d+\b', '', text)
        
        # Remove 4chan-specific references and '>' characters
        board_patterns = [
            r'>>?\d+',  # Post references
            r'/pol/', r'/r9k/', r'/b/', r'/x/', r'/fit/', r'/v/', r'/tv/', 
            r'/a/', r'/adv/', r'/o/', r'/ck/', r'/g/', r'/mu/', r'/lit/', 
            r'/his/', r'/sci/',
            r'\bOP\b', r'\b4chan\b', r'\bthread\b', r'\bboard\b',
            r'>+',  # Remove all '>' characters (greentext indicators)
        ]
        
        for pattern in board_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
            
        # Clean up formatting
        text = re.sub(r'\s+', ' ', text)  # Normalize whitespace
        text = text.strip()
        
        # Remove common chan artifacts
        text = re.sub(r'^(kek|based|cringe|cope|seethe)\s*', '', text, flags=re.IGNORECASE)
        text = re.sub(r'\s*(kek|based|cringe|cope|seethe)$', '', text, flags=re.IGNORECASE)
        
        return text
        
    def apply_length_constraints(self, content):
        """Apply proper length constraints for social media"""
        if len(content) < 10:
            return ""
        if len(content) > 280:
            # Smart truncation at sentence or clause boundaries
            truncated = content[:277]
            if '.' in truncated:
                truncated = truncated.rsplit('.', 1)[0] + '.'
            elif ',' in truncated:
                truncated = truncated.rsplit(',', 1)[0]
            else:
                truncated = truncated + "..."
            return truncated
        return content
        
    def enhance_sexual_edge_content(self, content):
        """Return sexual edge content without any enhancement prefixes"""
        return content
        
    def enhance_political_edge_content(self, content):
        """Return political edge content without any enhancement prefixes"""
        return content
        
    def enhance_dark_humor_content(self, content):
        """Return dark humor content without any enhancement prefixes"""
        return content
        
    def generate_enhanced_edge_tweet(self, style=None):
        """Generate an enhanced edge tweet"""
        if self.df.empty:
            self.logger.error("❌ No edge content available")
            return "No authentic edge content available"
            
        # Get fresh content
        content_row = self.get_fresh_edge_content(style)
        if content_row is None:
            return "Unable to generate fresh edge content"
            
        # Extract content and metadata
        raw_content = content_row['content']
        edge_type = content_row.get('category', 'general_edge')
        edge_quality = content_row.get('quality_score', 5)
        board = content_row.get('board', 'unknown')
        
        # Clean the content
        cleaned_content = self.clean_edge_for_output(raw_content)
        if not cleaned_content:
            return self.generate_enhanced_edge_tweet(style)  # Try again
            
        # Apply style-specific enhancements
        if edge_type == 'sexual_edge':
            enhanced_content = self.enhance_sexual_edge_content(cleaned_content)
        elif edge_type == 'political_edge':
            enhanced_content = self.enhance_political_edge_content(cleaned_content)
        elif edge_type == 'dark_humor_edge':
            enhanced_content = self.enhance_dark_humor_content(cleaned_content)
        else:
            enhanced_content = cleaned_content
            
        # Apply length constraints
        final_content = self.apply_length_constraints(enhanced_content)
        
        if not final_content:
            return self.generate_enhanced_edge_tweet(style)  # Try again
            
        # Track usage
        self.track_content_usage(raw_content)
        
        # Log generation
        self.log_edge_tweet(final_content, edge_type, edge_quality, board)
        
        return final_content
        
    def generate_category_specific_tweet(self, category):
        """Generate edge tweet for a specific category"""
        return self.generate_enhanced_edge_tweet(style=category)
        
    def log_edge_tweet(self, tweet, edge_type, quality, board, generation_type="enhanced_edge"):
        """Log generated edge tweet"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            'timestamp': timestamp,
            'tweet': tweet,
            'edge_type': edge_type,
            'quality': quality,
            'source_board': board,
            'generation_type': generation_type,
            'length': len(tweet)
        }
        
        log_file = 'data/enhanced_edge_log.csv'
        log_df = pd.DataFrame([log_entry])
        
        if os.path.exists(log_file):
            log_df.to_csv(log_file, mode='a', header=False, index=False)
        else:
            log_df.to_csv(log_file, index=False)
            
        self.logger.info(f"🔥 Generated {edge_type} tweet (quality: {quality}, source: {board})")
        
    def generate_multiple_edge_tweets(self, count=5, variety=True):
        """Generate multiple diverse edge tweets"""
        tweets = []
        
        if variety:
            # Generate variety across different edge types
            styles = ['sexual_edge', 'political_edge', 'dark_humor_edge', 'general_edge']
            for i in range(count):
                style = styles[i % len(styles)] if i < len(styles) else None
                tweet = self.generate_enhanced_edge_tweet(style)
                tweets.append(tweet)
        else:
            # Generate without style constraints
            for _ in range(count):
                tweet = self.generate_enhanced_edge_tweet()
                tweets.append(tweet)
                
        return tweets

def main():
    """Test the enhanced ultimate edge generator"""
    print("🔥 ENHANCED ULTIMATE EDGE GENERATOR TEST")
    print("=" * 80)
    
    generator = EnhancedUltimateEdgeGenerator()
    
    if generator.df.empty:
        print("❌ No edge content loaded - run the Enhanced Ultimate Edge Scraper first")
        return
        
    print(f"✅ Loaded {len(generator.df)} authentic edge posts")
    print(f"🔥 Organized into {len(generator.content_pools)} content pools")
    print()
    
    # Test different edge types
    edge_types = ['sexual_edge', 'political_edge', 'dark_humor_edge', 'general_edge']
    
    for edge_type in edge_types:
        print(f"🎯 Testing {edge_type.upper()} generation:")
        print("-" * 50)
        
        for i in range(3):
            tweet = generator.generate_enhanced_edge_tweet(edge_type)
            print(f"  {i+1}. {tweet}")
            time.sleep(0.5)  # Brief pause between generations
            
        print()
        
    print("🔥 VARIETY TEST - Mixed edge content:")
    print("-" * 50)
    variety_tweets = generator.generate_multiple_edge_tweets(count=5, variety=True)
    for i, tweet in enumerate(variety_tweets, 1):
        print(f"  {i}. {tweet}")
        
    print("\n🔥 ENHANCED ULTIMATE EDGE GENERATOR TEST COMPLETE!")

if __name__ == "__main__":
    main()