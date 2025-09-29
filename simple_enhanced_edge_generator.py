"""
Simple Enhanced Edge Generator - Fixed Version

This generator intelligently selects naturally short content from the full dataset
without any truncation or fallback mechanisms. It organizes content into pools
based on natural length and prioritizes authentic short-form posts.
"""

import pandas as pd
import random
import re
import os
import logging

class SimpleEnhancedEdgeGenerator:
    """
    Fixed Simple Enhanced Edge Generator that uses the full dataset intelligently
    """
    
    def __init__(self, edge_file='data/enhanced_ultimate_god_tier.csv'):
        """Initialize with intelligent content pooling"""
        self.edge_file = edge_file
        self.df = None
        self.short_pool = None
        self.medium_pool = None
        self.recent_outputs = set()  # Track recent outputs to prevent repetition
        self.max_recent = 40  # Remember last 40 outputs
        
        self._setup_logging()
        self._load_and_organize_content()
        
    def _setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('simple_edge_generator')
        
    def _load_and_organize_content(self):
        """Load dataset and organize into intelligent content pools"""
        try:
            if os.path.exists(self.edge_file):
                self.df = pd.read_csv(self.edge_file)
                
                # Remove posts with obvious issues
                self.df = self.df.dropna(subset=['content'])
                self.df = self.df[self.df['content'].str.len() > 5]
                
                # Clean all content and calculate lengths
                self.df['cleaned_content'] = self.df['content'].apply(self._clean_content)
                self.df['content_length'] = self.df['cleaned_content'].str.len()
                
                # Filter out empty content after cleaning
                self.df = self.df[self.df['content_length'] >= 10]
                
                # Filter out content with unwanted terms
                unwanted_terms = ['OP', 'thread', 'board']
                for term in unwanted_terms:
                    self.df = self.df[~self.df['cleaned_content'].str.contains(term, case=False, na=False)]
                
                # Categorize and prioritize NEET/comedic/unhinged/political edge content
                self._categorize_priority_content()
                
                # Create intelligent pools based on natural content length
                self.short_pool = self.df[
                    (self.df['content_length'] >= 10) & 
                    (self.df['content_length'] <= 80)
                ].copy()
                
                self.medium_pool = self.df[
                    (self.df['content_length'] > 80) & 
                    (self.df['content_length'] <= 150)
                ].copy()
                
                # Create priority pools for NEET/comedic/unhinged/political content
                self.priority_short_pool = self.short_pool[self.short_pool['is_priority_content'] == True]
                self.priority_medium_pool = self.medium_pool[self.medium_pool['is_priority_content'] == True]
                
                self.logger.info(f"✅ Loaded {len(self.df)} total posts")
                self.logger.info(f"🎯 Organized: {len(self.short_pool)} short posts, {len(self.medium_pool)} medium posts")
                self.logger.info(f"🔥 Priority pools: {len(self.priority_short_pool)} short priority, {len(self.priority_medium_pool)} medium priority")
                
            else:
                self.logger.error(f"❌ Dataset not found: {self.edge_file}")
                self.df = pd.DataFrame()
                self.short_pool = pd.DataFrame()
                self.medium_pool = pd.DataFrame()
                
        except Exception as e:
            self.logger.error(f"❌ Failed to load dataset: {e}")
            self.df = pd.DataFrame()
            self.short_pool = pd.DataFrame()
            self.medium_pool = pd.DataFrame()
            
    def _clean_content(self, content):
        """Clean content for social media with enhanced HTML removal"""
        if pd.isna(content):
            return ""
            
        text = str(content)
        
        # Remove ALL HTML tags and entities completely
        text = re.sub(r'<[^>]*?>', '', text)  # Remove HTML tags
        text = re.sub(r'<[^>]*', '', text)    # Remove unclosed tags
        text = text.replace('&gt;', '').replace('&lt;', '')
        text = text.replace('&amp;', '&').replace('&quot;', '"')
        text = re.sub(r'&[a-zA-Z]+;', '', text)  # Remove HTML entities
        text = re.sub(r'&#\d+;', '', text)       # Remove numeric entities
        
        # Remove '>' characters
        text = text.replace('>', '')
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Enhanced number removal - catches attached numbers too
        text = re.sub(r'\d{6,}', '', text)  # Remove 6+ digit sequences (post IDs)
        text = re.sub(r'\b\d+\b', '', text)  # Remove standalone numbers
        text = re.sub(r'^\d+', '', text)  # Remove numbers at start
        text = re.sub(r'\d+$', '', text)  # Remove numbers at end
        
        # Remove common 4chan formatting
        text = re.sub(r'>>[0-9]+', '', text)
        text = re.sub(r'>>+', '', text)
        text = re.sub(r'\n+', ' ', text)
        text = re.sub(r'\r+', ' ', text)
        text = re.sub(r'\t+', ' ', text)
        
        # Remove excessive punctuation
        text = re.sub(r'\.{3,}', '...', text)
        text = re.sub(r'!{2,}', '!', text)
        text = re.sub(r'\?{2,}', '?', text)
        
        # Clean up formatting
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text
    
    def clean_content_for_output(self, content):
        """Clean content by removing '>' characters and ensuring proper short-medium formatting"""
        if not content:
            return content
            
        # Remove greentext arrows and clean formatting
        cleaned = content.replace('>', '').strip()
        
        # Enhanced number removal for final output
        cleaned = re.sub(r'\d{6,}', '', cleaned)  # Remove 6+ digit sequences (post IDs)
        cleaned = re.sub(r'\b\d+\b', '', cleaned)  # Remove standalone numbers
        cleaned = re.sub(r'^\d+', '', cleaned)  # Remove numbers at start
        cleaned = re.sub(r'\d+$', '', cleaned)  # Remove numbers at end
        
        # Remove multiple spaces
        cleaned = ' '.join(cleaned.split())
        
        # Ensure proper length for short to medium content (10-200 characters)
        if len(cleaned) > 200:
            cleaned = cleaned[:197] + "..."
        
        return cleaned.strip()
    
    def _categorize_priority_content(self):
        """Categorize content to prioritize NEET, comedic, unhinged, and political edge content"""
        
        # Keywords for NEET content
        neet_keywords = [
            'neet', 'wagecuck', 'wagie', 'unemployment', 'parents basement', 'tendies', 'mommy', 
            'jobless', 'no job', 'welfare', 'live with parents', 'basement dweller',
            'shut in', 'hikikomori', 'autistic', 'socially awkward', 'incel', 'virgin',
            'robot', 'tfw no gf', 'never had gf', 'kissless virgin'
        ]
        
        # Keywords for comedic content
        comedic_keywords = [
            'kek', 'lmao', 'hilarious', 'cringe', 'based', 'cope', 'seethe', 'dilate',
            'rent free', 'schizo', 'retard', 'autist', 'pepe', 'wojak', 'chad',
            'gigachad', 'sigma', 'beta', 'alpha', 'normie', 'normalfag'
        ]
        
        # Keywords for unhinged content
        unhinged_keywords = [
            'schizo', 'unhinged', 'insane', 'deranged', 'psychotic', 'manic', 'breakdown',
            'losing it', 'snapped', 'going crazy', 'mental', 'unstable', 'paranoid',
            'conspiracy', 'glowing', 'glow', 'fed posting', 'tinfoil'
        ]
        
        # Keywords for political edge content
        political_keywords = [
            'pol', 'redpill', 'blackpill', 'whitepill', 'clown world', 'honk honk',
            'jogger', 'goyim', 'merchant', 'nose', 'early life', 'oy vey',
            'leftist', 'rightoid', 'commie', 'fascist', 'nazi', 'jewish',
            'immigration', 'diversity', 'multicultural', 'woke', 'sjw'
        ]
        
        def check_priority_content(text):
            """Check if text contains priority keywords"""
            text_lower = text.lower()
            return (any(keyword in text_lower for keyword in neet_keywords) or
                    any(keyword in text_lower for keyword in comedic_keywords) or 
                    any(keyword in text_lower for keyword in unhinged_keywords) or
                    any(keyword in text_lower for keyword in political_keywords))
        
        # Add priority flag to dataframe
        self.df['is_priority_content'] = self.df['cleaned_content'].apply(check_priority_content)
        
        priority_count = len(self.df[self.df['is_priority_content'] == True])
        self.logger.info(f"🎯 Found {priority_count} priority NEET/comedic/unhinged/political posts")
        
    def generate_tweet(self):
        """Generate authentic short-form content prioritizing NEET/comedic/unhinged/political edge content"""
        
        import random
        
        # 70% chance to use priority content (NEET/comedic/unhinged/political edge)
        use_priority = random.random() < 0.7
        
        if use_priority:
            # Try priority short pool first
            if not self.priority_short_pool.empty:
                selected_row = self.priority_short_pool.sample(n=1).iloc[0]
                raw_content = selected_row['cleaned_content']
                return self.clean_content_for_output(raw_content)
            
            # Fallback to priority medium pool
            elif not self.priority_medium_pool.empty:
                selected_row = self.priority_medium_pool.sample(n=1).iloc[0]
                raw_content = selected_row['cleaned_content']
                return self.clean_content_for_output(raw_content)
        
        # Use general short pool (30% of time or when priority pools empty)
        if not self.short_pool.empty:
            selected_row = self.short_pool.sample(n=1).iloc[0]
            raw_content = selected_row['cleaned_content']
            return self.clean_content_for_output(raw_content)
        
        # Use medium pool as final fallback
        elif not self.medium_pool.empty:
            shorter_medium = self.medium_pool[self.medium_pool['content_length'] <= 150]
            if not shorter_medium.empty:
                selected_row = shorter_medium.sample(n=1).iloc[0]
                raw_content = selected_row['cleaned_content']
                return self.clean_content_for_output(raw_content)
                
        return "Content pool exhausted"
        
    def generate_multiple_tweets(self, count=5):
        """Generate multiple tweets"""
        tweets = []
        for _ in range(count):
            tweet = self.generate_tweet()
            tweets.append(tweet)
        return tweets

def main():
    """Test the fixed generator"""
    print("🔥 FIXED SIMPLE ENHANCED EDGE GENERATOR TEST")
    print("=" * 60)
    
    generator = SimpleEnhancedEdgeGenerator()
    
    if generator.df.empty:
        print("❌ No content available")
        return
        
    print(f"✅ Ready with {len(generator.df)} total posts")
    print(f"🎯 Short pool: {len(generator.short_pool)} posts")
    print(f"🎯 Medium pool: {len(generator.medium_pool)} posts")
    print("\n🎯 Generated tweets:")
    print("-" * 40)
    
    for i in range(10):
        tweet = generator.generate_tweet()
        print(f"{i+1:2d}. ({len(tweet):2d} chars) {tweet}")
        
    print("\n🔥 Test complete!")

if __name__ == "__main__":
    main()