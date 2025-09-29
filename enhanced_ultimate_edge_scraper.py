#!/usr/bin/env python3
"""
Enhanced Ultimate Edge Scraper

Recreates the original scraper that built enhanced_ultimate_god_tier.csv
This scraper targets ALL major dynamic content streams to find the most controversial,
provocative, and high-quality edge content across different communities.

Strategy:
- Cast wide net across all boards (/pol/, /v/, /b/, /a/, /tv/, /g/, /adv/, /r9k/, /fit/, /mu/, etc.)
- Apply sophisticated quality filtering for genuinely provocative content
- Categorize by edge type (political_edge, sexual_edge, dark_humor_edge, general_edge)
- Score content quality (7-10 range for elite material only)
- Anti-repetition and freshness tracking
"""

import requests
import json
import csv
import time
import random
import logging
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Set
import re
from collections import defaultdict

class EnhancedUltimateEdgeScraper:
    """
    Elite scraper for collecting the most controversial content from all dynamic content streams
    """
    
    def __init__(self, output_file='data/enhanced_ultimate_god_tier_refreshed.csv'):
        """Initialize the enhanced ultimate edge scraper"""
        self.output_file = output_file
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # All major content streams for comprehensive edge collection
        self.target_boards = [
            'pol',  # Politics - highest edge content
            'v',    # Video Games - gaming culture edge
            'b',    # Random - chaotic edge content
            'a',    # Anime & Manga - otaku culture edge
            'tv',   # Television & Film - entertainment edge
            'g',    # Technology - tech culture edge
            'adv',  # Advice - relationship/life edge
            'r9k',  # ROBOT9001 - incel/social edge
            'fit',  # Fitness - lifestyle edge
            'mu',   # Music - culture edge
            'x',    # Paranormal - conspiracy edge
            'o',    # Auto - car culture edge
            'lit',  # Literature - intellectual edge
            'his',  # History - historical edge
            'sci',  # Science - academic edge
            'ck',   # Food & Cooking - lifestyle edge
            'int',  # International - global edge
            'sp',   # Sports - sports culture edge
            'biz',  # Business & Finance - economic edge
            'diy'   # DIY - practical edge
        ]
        
        # Content collected for anti-repetition
        self.collected_hashes: Set[str] = set()
        self.board_stats = defaultdict(int)
        self.category_stats = defaultdict(int)
        
        self.setup_logging()
        
        # Edge detection patterns for quality content
        self.edge_indicators = {
            'political_edge': [
                r'\b(?:immigration|diversity|feminism|marxist|communist|socialist)\b',
                r'\b(?:white guilt|replacement|invasion|genocide)\b',
                r'\b(?:democracy|republic|voting|elections).*(?:scam|fake|rigged)\b',
                r'\b(?:media|press|journalists).*(?:lies|propaganda|fake)\b',
                r'\b(?:woke|progressive|liberal).*(?:ideology|agenda|destroy)\b'
            ],
            'sexual_edge': [
                r'\b(?:hypergamy|chad|beta|alpha|sigma)\b',
                r'\b(?:dating|women|relationships).*(?:destroyed|ruined|impossible)\b',
                r'\b(?:feminism|feminists).*(?:ruined|destroyed|cancer)\b',
                r'\b(?:marriage|divorce).*(?:scam|trap|mistake)\b',
                r'\b(?:tinder|dating apps).*(?:degeneracy|destruction)\b'
            ],
            'dark_humor_edge': [
                r'\b(?:kys|kill yourself|rope|anhero)\b',
                r'\b(?:retard|autist|sperg).*(?:tier|level|mode)\b',
                r'\b(?:based|cringe|cope|seethe)\b',
                r'\b(?:normalfag|normie|wagecuck|neet)\b',
                r'\b(?:cope|dilate|have sex|touch grass)\b'
            ],
            'general_edge': [
                r'\b(?:society|civilization).*(?:collapse|dying|doomed)\b',
                r'\b(?:modern|current).*(?:world|times).*(?:garbage|shit|hell)\b',
                r'\b(?:everyone|people).*(?:stupid|retarded|brainwashed)\b',
                r'\b(?:system|establishment).*(?:rigged|corrupt|broken)\b',
                r'\b(?:normies|masses).*(?:cattle|sheep|npcs)\b'
            ]
        }
        
        # Quality scoring keywords
        self.quality_boosters = [
            'always', 'never', 'every', 'all', 'everyone', 'nobody',
            'inevitable', 'doomed', 'destroyed', 'ruined', 'finished',
            'truth', 'reality', 'fact', 'obvious', 'clearly', 'obviously'
        ]
        
    def setup_logging(self):
        """Setup comprehensive logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_ultimate_edge_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def get_board_catalog(self, board: str) -> List[Dict]:
        """Get catalog of threads from a specific board"""
        try:
            url = f'https://a.4cdn.org/{board}/catalog.json'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            catalog_data = response.json()
            threads = []
            
            for page in catalog_data:
                for thread in page.get('threads', []):
                    threads.append(thread)
                    
            return threads
            
        except Exception as e:
            self.logger.error(f"Error fetching catalog for /{board}/: {e}")
            return []
            
    def is_edge_thread(self, thread: Dict, board: str) -> bool:
        """Determine if thread likely contains edge content"""
        content_fields = []
        
        # Get thread subject and comment
        if 'sub' in thread:
            content_fields.append(thread['sub'].lower())
        if 'com' in thread:
            content_fields.append(thread['com'].lower())
            
        full_content = ' '.join(content_fields)
        
        # Check for edge indicators
        edge_score = 0
        for category, patterns in self.edge_indicators.items():
            for pattern in patterns:
                if re.search(pattern, full_content, re.IGNORECASE):
                    edge_score += 1
                    
        # Board-specific edge detection
        board_multipliers = {
            'pol': 2.0,    # Politics naturally edgy
            'r9k': 1.8,    # Robot culture
            'b': 1.5,      # Random chaos
            'adv': 1.3,    # Relationship advice edge
            'x': 1.2,      # Paranormal edge
        }
        
        edge_score *= board_multipliers.get(board, 1.0)
        
        # Reply count indicates controversial content
        replies = thread.get('replies', 0)
        if replies > 50:
            edge_score += 1
        if replies > 100:
            edge_score += 2
            
        return edge_score >= 2
        
    def scrape_thread(self, board: str, thread_no: int) -> List[Dict]:
        """Scrape all posts from a thread"""
        try:
            url = f'https://a.4cdn.org/{board}/thread/{thread_no}.json'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            thread_data = response.json()
            return thread_data.get('posts', [])
            
        except Exception as e:
            self.logger.debug(f"Error fetching thread {thread_no} from /{board}/: {e}")
            return []
            
    def extract_edge_content(self, post: Dict, board: str) -> Optional[Dict]:
        """Extract and process edge content from post"""
        if 'com' not in post:
            return None
            
        content = post['com']
        
        # Clean HTML tags and decode entities
        content = re.sub(r'<[^>]+>', '', content)
        content = content.replace('&gt;', '>').replace('&lt;', '<')
        content = content.replace('&quot;', '"').replace('&#039;', "'")
        content = content.replace('&amp;', '&')
        
        # Remove quotes and references
        content = re.sub(r'&gt;&gt;\d+', '', content)
        content = re.sub(r'&gt;.*?\n', '', content)
        
        # Clean whitespace
        content = ' '.join(content.split())
        content = content.strip()
        
        # Filter out low quality content
        if not self.passes_edge_filters(content):
            return None
            
        # Determine edge category and quality score
        category = self.categorize_edge_content(content, board)
        quality_score = self.calculate_edge_quality_score(content, post, board)
        
        # Only keep high quality edge content (7+)
        if quality_score < 7:
            return None
            
        # Check for duplicates
        content_hash = hashlib.md5(content.encode()).hexdigest()[:16]
        if content_hash in self.collected_hashes:
            return None
            
        self.collected_hashes.add(content_hash)
        
        # Determine era based on content patterns
        era = self.estimate_content_era(content)
        
        return {
            'content': content,
            'board': board,
            'category': category,
            'quality_score': quality_score,
            'length': len(content),
            'era': era,
            'scraped_at': datetime.now().isoformat()
        }
        
    def passes_edge_filters(self, content: str) -> bool:
        """Check if content passes basic edge quality filters"""
        # Length requirements
        if len(content) < 30 or len(content) > 500:
            return False
            
        # Must contain controversial indicators
        has_edge_indicators = False
        for category, patterns in self.edge_indicators.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    has_edge_indicators = True
                    break
            if has_edge_indicators:
                break
                
        if not has_edge_indicators:
            return False
            
        # Filter out low quality patterns
        low_quality_patterns = [
            r'^>+\s*$',  # Only greentext arrows
            r'^\d+$',    # Only numbers
            r'^[A-Z\s]+$',  # All caps (unless short)
            r'^\W+$',    # Only punctuation
            r'bump',     # Thread bumps
            r'^sauce\?*$',  # Sauce requests
            r'^this$',   # Single word responses
            r'^based$',  # Single based responses
        ]
        
        for pattern in low_quality_patterns:
            if re.match(pattern, content, re.IGNORECASE):
                return False
                
        return True
        
    def categorize_edge_content(self, content: str, board: str) -> str:
        """Categorize edge content by type"""
        content_lower = content.lower()
        
        # Count matches for each category
        category_scores = {}
        for category, patterns in self.edge_indicators.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, content_lower))
                score += matches
            category_scores[category] = score
            
        # Board-specific category preferences
        board_preferences = {
            'pol': 'political_edge',
            'r9k': 'sexual_edge',
            'adv': 'sexual_edge',
            'x': 'general_edge',
            'b': 'dark_humor_edge'
        }
        
        # Get highest scoring category
        if any(category_scores.values()):
            best_category = max(category_scores.items(), key=lambda x: x[1])[0]
        else:
            best_category = board_preferences.get(board, 'general_edge')
            
        return best_category
        
    def calculate_edge_quality_score(self, content: str, post: Dict, board: str) -> int:
        """Calculate quality score for edge content (7-10 for elite only)"""
        score = 7  # Base score for passing initial filters
        
        content_lower = content.lower()
        
        # Quality boosting factors
        booster_count = sum(1 for booster in self.quality_boosters 
                           if booster in content_lower)
        score += min(booster_count, 2)
        
        # Board quality multipliers
        board_quality = {
            'pol': 1.0,    # High quality political discourse
            'lit': 0.8,    # Intellectual edge
            'his': 0.8,    # Historical edge
            'adv': 0.6,    # Relationship advice
            'r9k': 0.5,    # Incel content quality varies
            'b': 0.3,      # Random chaos
        }
        
        if board in board_quality:
            score = int(score * board_quality[board])
            
        # Length and complexity bonuses
        if len(content) > 100:
            score += 1
        if len(content) > 200:
            score += 1
            
        # Controversial statement patterns
        controversial_patterns = [
            r'\b(?:always|never|all|every|everyone|nobody)\b',
            r'\b(?:fact|truth|reality|obvious)\b',
            r'\b(?:destroyed|ruined|finished|doomed)\b'
        ]
        
        for pattern in controversial_patterns:
            if re.search(pattern, content_lower):
                score += 1
                break
                
        # Cap at 10
        return min(score, 10)
        
    def estimate_content_era(self, content: str) -> str:
        """Estimate content era based on terminology and references"""
        content_lower = content.lower()
        
        # Modern era indicators (2021-2024)
        modern_terms = ['covid', 'vaccine', 'lockdown', 'tiktok', 'zoom', 'remote work', 'nft', 'crypto']
        if any(term in content_lower for term in modern_terms):
            return '2021-2024'
            
        # Late 2010s indicators (2015-2020)
        late_terms = ['trump', 'brexit', 'metoo', 'gamergate', 'sjw', 'woke', 'based']
        if any(term in content_lower for term in late_terms):
            return '2015-2020'
            
        # Early 2010s indicators (2009-2014)
        early_terms = ['obama', 'occupy', 'hipster', 'yolo', 'swag', 'reddit']
        if any(term in content_lower for term in early_terms):
            return '2009-2014'
            
        # Classic era (2003-2008)
        classic_terms = ['newfag', 'oldfag', 'epic', 'win', 'fail', 'lulz']
        if any(term in content_lower for term in classic_terms):
            return '2003-2008'
            
        # Default to recent
        return '2015-2020'
        
    def scrape_board(self, board: str, max_threads: int = 25) -> List[Dict]:
        """Scrape edge content from a specific board"""
        self.logger.info(f"🔥 Scraping edge content from /{board}/ (max {max_threads} threads)")
        
        # Get catalog
        threads = self.get_board_catalog(board)
        if not threads:
            self.logger.warning(f"No threads found for /{board}/")
            return []
            
        # Filter for edge threads
        edge_threads = [t for t in threads if self.is_edge_thread(t, board)]
        
        # Sort by reply count (controversy indicator)
        edge_threads.sort(key=lambda x: x.get('replies', 0), reverse=True)
        
        # Limit threads
        edge_threads = edge_threads[:max_threads]
        
        collected_posts = []
        
        for i, thread in enumerate(edge_threads):
            thread_no = thread['no']
            self.logger.info(f"  Scraping thread {i+1}/{len(edge_threads)}: {thread_no}")
            
            posts = self.scrape_thread(board, thread_no)
            
            for post in posts:
                edge_post = self.extract_edge_content(post, board)
                if edge_post:
                    collected_posts.append(edge_post)
                    self.board_stats[board] += 1
                    self.category_stats[edge_post['category']] += 1
                    
            # Rate limiting
            time.sleep(random.uniform(1.0, 2.5))
            
        self.logger.info(f"✅ Collected {len(collected_posts)} edge posts from /{board}/")
        return collected_posts
        
    def save_edge_posts(self, posts: List[Dict]):
        """Save edge posts to CSV file"""
        if not posts:
            return
            
        # Check if file exists to determine if we need headers
        file_exists = False
        try:
            with open(self.output_file, 'r'):
                file_exists = True
        except FileNotFoundError:
            pass
            
        with open(self.output_file, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['content', 'board', 'category', 'quality_score', 'length', 'era', 'scraped_at']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            if not file_exists:
                writer.writeheader()
                
            for post in posts:
                writer.writerow(post)
                
        self.logger.info(f"💾 Saved {len(posts)} edge posts to {self.output_file}")
        
    def run_comprehensive_edge_scrape(self, max_threads_per_board: int = 25):
        """Run comprehensive edge scraping across all boards"""
        self.logger.info("🚀 Starting Enhanced Ultimate Edge Scraper")
        self.logger.info(f"Target boards: {', '.join(self.target_boards)}")
        
        start_time = datetime.now()
        all_posts = []
        
        for i, board in enumerate(self.target_boards):
            self.logger.info(f"\n📋 Scraping board {i+1}/{len(self.target_boards)}: /{board}/")
            
            try:
                board_posts = self.scrape_board(board, max_threads_per_board)
                all_posts.extend(board_posts)
                
                # Save incrementally
                if board_posts:
                    self.save_edge_posts(board_posts)
                    
            except Exception as e:
                self.logger.error(f"Error scraping /{board}/: {e}")
                continue
                
            # Longer delay between boards
            time.sleep(random.uniform(3.0, 6.0))
            
        # Final statistics
        elapsed = datetime.now() - start_time
        self.logger.info(f"\n🎯 Enhanced Ultimate Edge Scraping Complete!")
        self.logger.info(f"⏱️  Total time: {elapsed}")
        self.logger.info(f"📊 Total edge posts collected: {len(all_posts)}")
        self.logger.info(f"📁 Saved to: {self.output_file}")
        
        # Board statistics
        self.logger.info("\n📈 Board Statistics:")
        for board, count in sorted(self.board_stats.items(), key=lambda x: x[1], reverse=True):
            self.logger.info(f"  /{board}/: {count} posts")
            
        # Category statistics  
        self.logger.info("\n🏷️  Category Statistics:")
        for category, count in sorted(self.category_stats.items(), key=lambda x: x[1], reverse=True):
            self.logger.info(f"  {category}: {count} posts")

def main():
    """Run the enhanced ultimate edge scraper"""
    scraper = EnhancedUltimateEdgeScraper()
    scraper.run_comprehensive_edge_scrape(max_threads_per_board=30)

if __name__ == "__main__":
    main()