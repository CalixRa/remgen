#!/usr/bin/env python3
"""
Transcendent Quote Generator - AI-Powered Mystical Wisdom Creation

This advanced generator creates original transcendent quotes, mystical aphorisms,
sacred wisdom sayings, esoteric reflections, and spiritual beauty quotes.
It combines authentic 4chan esoteric content with AI-powered generation to create
beautiful, profound, and spiritually resonant content (20-280 characters).

Content Categories:
- Transcendent quotes: Universal truths and cosmic insights
- Mystical aphorisms: Brief, profound spiritual statements
- Sacred wisdom sayings: Ancient-style wisdom for modern times
- Esoteric reflections: Deep metaphysical observations
- Spiritual beauty quotes: Aesthetic and divine inspiration
"""

import pandas as pd
import random
import re
import logging
import csv
import os
from datetime import datetime
import hashlib

class TranscendentQuoteGenerator:
    """
    Elite generator for creating original transcendent and mystical content
    """
    
    def __init__(self, esoteric_file='data/god_tier_esoteria.csv'):
        """Initialize the transcendent quote generator"""
        self.esoteric_file = esoteric_file
        self.df = None
        self.content_pools = {}
        self.recent_content = set()
        self.max_recent = 20  # Much smaller tracking for maximum content diversity
        
        self._setup_logging()
        self._load_esoteric_dataset()
        self._organize_content_pools()
        self._initialize_wisdom_templates()
        
    def _setup_logging(self):
        """Setup logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('transcendent_generator')
        
    def _load_esoteric_dataset(self):
        """Load the esoteric content dataset"""
        try:
            if os.path.exists(self.esoteric_file):
                self.df = pd.read_csv(self.esoteric_file)
                self.logger.info(f"✨ Loaded {len(self.df)} transcendent posts from esoteric dataset")
            else:
                self.logger.warning(f"⚠️ Esoteric dataset not found at {self.esoteric_file}")
                self.df = pd.DataFrame()
        except Exception as e:
            self.logger.error(f"❌ Error loading esoteric dataset: {e}")
            self.df = pd.DataFrame()
            
    def _organize_content_pools(self):
        """Organize esoteric content into pools by category and quality"""
        if self.df.empty:
            self.logger.warning("⚠️ No esoteric content available for organization")
            return
            
        # Organize by category and quality
        categories = ['transcendental', 'esoteric_knowledge', 'spiritual_insight', 
                     'aesthetic_beauty', 'philosophical_wisdom', 'general_wisdom']
        
        for category in categories:
            category_posts = self.df[self.df['category'] == category]
            
            # High quality (9-10)
            high_quality = category_posts[category_posts['quality_score'] >= 9]
            if not high_quality.empty:
                self.content_pools[f"{category}_elite"] = high_quality
                
            # Medium quality (7-8)
            medium_quality = category_posts[
                (category_posts['quality_score'] >= 7) & 
                (category_posts['quality_score'] < 9)
            ]
            if not medium_quality.empty:
                self.content_pools[f"{category}_high"] = medium_quality
                
            # Good quality (6)
            good_quality = category_posts[category_posts['quality_score'] == 6]
            if not good_quality.empty:
                self.content_pools[f"{category}_good"] = good_quality
                
        self.logger.info(f"🔮 Organized esoteric content into {len(self.content_pools)} transcendent pools")
        
    def _initialize_wisdom_templates(self):
        """Initialize templates for generating original transcendent content"""
        
        # Transcendent quote templates
        self.transcendent_templates = [
            "The {essence} of {concept} lies not in {surface}, but in {depth}",
            "When {seeker} seeks {truth}, {truth} reveals itself through {medium}",
            "In the {state} of {being}, we discover the {revelation} of {reality}",
            "The {path} to {destination} begins with {first_step} and ends with {understanding}",
            "{wisdom} whispers that {insight}, while {illusion} shouts {deception}",
            "Beyond the {veil} of {appearance} lies the {eternal} {truth}",
            "The {soul} recognizes {beauty} not through {senses}, but through {recognition}"
        ]
        
        # Mystical aphorism templates
        self.mystical_templates = [
            "{element} teaches {lesson}",
            "In {silence}, {voice} speaks",
            "{paradox} reveals {truth}",
            "The {seeker} becomes the {sought}",
            "{question} contains its own {answer}",
            "Where {darkness} meets {light}, {wisdom} is born",
            "{emptiness} holds {fullness}"
        ]
        
        # Sacred wisdom templates
        self.sacred_templates = [
            "Ancient {teachers} knew: {wisdom}",
            "The {sacred_text} teaches that {lesson}",
            "In {tradition}, we learn {truth}",
            "Sacred {practice} reveals {insight}",
            "The {wise_ones} understood {mystery}",
            "{divine_quality} manifests through {expression}",
            "Holy {essence} dwells in {location}"
        ]
        
        # Esoteric reflection templates
        self.esoteric_templates = [
            "The {symbol} represents {meaning}, yet {deeper_meaning} lies beneath",
            "In {esoteric_system}, {principle} governs {manifestation}",
            "{hidden_knowledge} reveals itself to those who {requirement}",
            "The {mystery_school} taught that {secret_wisdom}",
            "{alchemical_process} transforms {base} into {noble}",
            "Sacred {geometry} demonstrates {cosmic_principle}",
            "{archetypal_force} moves through {expression}"
        ]
        
        # Spiritual beauty templates
        self.beauty_templates = [
            "Beauty {verb} when {condition}",
            "The {aesthetic} reflects the {divine}",
            "In {natural_phenomenon}, we glimpse {transcendence}",
            "{art_form} becomes sacred when {transformation}",
            "Divine {quality} shines through {manifestation}",
            "The {beautiful_thing} whispers of {eternal_truth}",
            "{sensory_experience} awakens {spiritual_recognition}"
        ]
        
        # Word pools for template filling
        self._initialize_word_pools()
        
    def _initialize_word_pools(self):
        """Initialize word pools for template generation"""
        
        self.word_pools = {
            'essence': ['truth', 'beauty', 'wisdom', 'love', 'spirit', 'soul', 'divine nature', 'cosmic force'],
            'concept': ['existence', 'consciousness', 'reality', 'enlightenment', 'awakening', 'transcendence'],
            'surface': ['appearance', 'illusion', 'form', 'material', 'temporal', 'visible'],
            'depth': ['essence', 'eternal truth', 'divine core', 'infinite mystery', 'sacred heart'],
            'seeker': ['the soul', 'consciousness', 'the heart', 'the awakening mind', 'divine spark'],
            'truth': ['wisdom', 'light', 'understanding', 'revelation', 'gnosis', 'illumination'],
            'medium': ['silence', 'contemplation', 'grace', 'surrender', 'presence', 'stillness'],
            'state': ['silence', 'meditation', 'prayer', 'contemplation', 'presence', 'awareness'],
            'being': ['pure consciousness', 'divine presence', 'eternal now', 'sacred stillness'],
            'revelation': ['mystery', 'truth', 'beauty', 'love', 'divine nature', 'cosmic order'],
            'reality': ['existence', 'the infinite', 'cosmic consciousness', 'divine being'],
            'path': ['journey', 'way', 'pilgrimage', 'quest', 'spiritual practice'],
            'destination': ['enlightenment', 'truth', 'peace', 'love', 'divine union', 'awakening'],
            'first_step': ['surrender', 'humility', 'awareness', 'questioning', 'opening'],
            'understanding': ['wisdom', 'insight', 'recognition', 'realization', 'awakening'],
            'wisdom': ['the heart', 'inner knowing', 'divine voice', 'sacred intuition'],
            'insight': ['all is one', 'love prevails', 'truth endures', 'beauty heals'],
            'illusion': ['the ego', 'fear', 'separation', 'material attachment'],
            'deception': ['division', 'scarcity', 'limitation', 'separation'],
            'veil': ['illusion', 'appearance', 'form', 'temporal', 'mundane'],
            'appearance': ['form', 'matter', 'surface', 'temporal reality'],
            'eternal': ['divine', 'infinite', 'sacred', 'timeless', 'unchanging'],
            'soul': ['heart', 'consciousness', 'divine spark', 'inner being'],
            'beauty': ['truth', 'divine harmony', 'cosmic order', 'sacred geometry'],
            'senses': ['perception', 'observation', 'analysis', 'judgment'],
            'recognition': ['remembrance', 'divine knowing', 'heart wisdom', 'soul recognition'],
            'element': ['silence', 'darkness', 'water', 'fire', 'earth', 'wind'],
            'lesson': ['patience', 'humility', 'surrender', 'acceptance', 'love'],
            'silence': ['stillness', 'emptiness', 'void', 'sacred space'],
            'voice': ['wisdom', 'truth', 'divine guidance', 'inner knowing'],
            'paradox': ['emptiness', 'darkness', 'silence', 'surrender'],
            'question': ['seeking', 'yearning', 'wondering', 'questioning'],
            'answer': ['peace', 'understanding', 'acceptance', 'love'],
            'darkness': ['unknowing', 'mystery', 'silence', 'emptiness'],
            'light': ['understanding', 'awareness', 'consciousness', 'illumination'],
            'emptiness': ['void', 'silence', 'surrender', 'letting go'],
            'fullness': ['completeness', 'wholeness', 'divine presence', 'infinite love']
        }
        
    def _get_template_content(self, template, word_pools):
        """Fill a template with appropriate words"""
        try:
            # Extract placeholder words from template
            placeholders = re.findall(r'\{(\w+)\}', template)
            
            # Fill placeholders with random words from pools
            filled_template = template
            for placeholder in placeholders:
                if placeholder in word_pools:
                    word = random.choice(word_pools[placeholder])
                    filled_template = filled_template.replace(f'{{{placeholder}}}', word, 1)
                else:
                    # If word not in pool, use placeholder as is (remove braces)
                    filled_template = filled_template.replace(f'{{{placeholder}}}', placeholder)
                    
            return filled_template
            
        except Exception as e:
            self.logger.error(f"Error filling template: {e}")
            return "In silence, wisdom speaks."
            
    def _get_content_hash(self, content):
        """Generate hash for content tracking"""
        return hashlib.md5(content.lower().encode()).hexdigest()[:8]
        
    def _is_content_recent(self, content):
        """Check if content was used recently"""
        content_hash = self._get_content_hash(content)
        return content_hash in self.recent_content
        
    def _track_content_usage(self, content):
        """Track content usage for anti-repetition"""
        content_hash = self._get_content_hash(content)
        self.recent_content.add(content_hash)
        
        # Keep only recent items
        if len(self.recent_content) > self.max_recent:
            # Remove oldest items (simplified approach)
            excess = len(self.recent_content) - self.max_recent
            for _ in range(excess):
                self.recent_content.pop()
                
    def _is_balanced_length(self, content_length):
        """Check if content length fits balanced distribution (short/medium/long)"""
        import random
        
        # Define length categories
        if content_length < 50:
            category = 'short'
        elif content_length < 120:
            category = 'medium'
        else:
            category = 'long'
        
        # Randomly accept different lengths to create balance
        # 40% short, 35% medium, 25% long for good variety
        if category == 'short':
            return random.random() < 0.4
        elif category == 'medium':
            return random.random() < 0.35
        else:  # long
            return random.random() < 0.25
    
    def _is_suitable_transcendent_content(self, content):
        """Filter content to prioritize transcendent themes while preserving authentic 4chan diversity"""
        content_lower = content.lower()
        
        # Basic quality filters only
        if len(content) < 8 or len(content) > 280:
            return False
            
        # Block HTML content and URLs only
        if any(html_tag in content_lower for html_tag in ['<html', '<div', '<span', '<p>', 'http://', 'https://']):
            return False
            
        # Block excessive numbers only (timestamps, IDs)
        import re
        if re.search(r'\d{6,}', content):
            return False
            
        # Block only obvious non-content
        if content_lower.strip() in ['no', 'yes', 'ok', 'lol', 'this', 'bump']:
            return False
            
        # Minimal blacklist - only clear spam/influencer content
        strict_blacklist = [
            'youtube.com', 'instagram.com', 'tiktok.com', 'subscribe to',
            'onlyfans.com', 'patreon.com', 'follow me'
        ]
        
        if any(term in content_lower for term in strict_blacklist):
            return False
        
        # Transcendent and spiritual keywords (expanded for variety)
        transcendent_keywords = [
            'god', 'divine', 'sacred', 'holy', 'spiritual', 'soul', 'consciousness', 
            'meditation', 'prayer', 'transcendent', 'enlightenment', 'wisdom', 
            'truth', 'beauty', 'love', 'peace', 'eternal', 'infinite', 'cosmos',
            'universe', 'creation', 'light', 'darkness', 'silence', 'mystery',
            'faith', 'grace', 'spirit', 'essence', 'being', 'existence', 'nature',
            'art', 'poetry', 'music', 'philosophy', 'metaphysics', 'mystical',
            'esoteric', 'occult', 'hermetic', 'gnosis', 'awakening', 'liberation',
            'meaning', 'purpose', 'destiny', 'journey', 'dream', 'hope', 'heart',
            'mind', 'thought', 'feeling', 'emotion', 'moment', 'time', 'space',
            'reality', 'world', 'life', 'death', 'birth', 'change', 'transform',
            'energy', 'vibration', 'frequency', 'resonance', 'harmony', 'balance'
        ]
        
        # Philosophical and profound indicators
        profound_keywords = [
            'imagine', 'envision', 'picture', 'dream', 'create', 'inspiration',
            'discover', 'explore', 'journey', 'path', 'way', 'become', 'transform',
            'awaken', 'realize', 'understand', 'learn', 'grow', 'evolve', 'think',
            'feel', 'remember', 'forget', 'believe', 'know', 'wonder', 'question',
            'experience', 'see', 'hear', 'touch', 'taste', 'smell', 'sense'
        ]
        
        # Count positive indicators
        transcendent_score = sum(1 for keyword in transcendent_keywords if keyword in content_lower)
        profound_score = sum(1 for keyword in profound_keywords if keyword in content_lower)
        
        # Much more permissive acceptance criteria:
        # 1. Has transcendent/spiritual content
        if transcendent_score >= 1:
            return True
            
        # 2. Has profound/philosophical content
        if profound_score >= 1:
            return True
            
        # 3. Is substantial and authentic 4chan content (preserve chan culture)
        if len(content.split()) >= 8:
            return True
            
        return False
                
    def generate_transcendent_quote(self):
        """Generate a transcendent quote using templates and wisdom"""
        template = random.choice(self.transcendent_templates)
        quote = self._get_template_content(template, self.word_pools)
        
        # Ensure proper length
        if len(quote) > 280:
            # Simplify for length
            simple_templates = [
                "The {essence} of {concept} is {truth}",
                "{wisdom} reveals {insight}",
                "In {state}, we discover {revelation}"
            ]
            template = random.choice(simple_templates)
            quote = self._get_template_content(template, self.word_pools)
            
        return quote.strip()
        
    def generate_mystical_aphorism(self):
        """Generate a mystical aphorism"""
        template = random.choice(self.mystical_templates)
        aphorism = self._get_template_content(template, self.word_pools)
        
        # Ensure brevity for aphorisms
        if len(aphorism) > 150:
            # Use shorter templates
            short_templates = [
                "{element} teaches {lesson}",
                "In {silence}, {voice} speaks",
                "{emptiness} holds {fullness}"
            ]
            template = random.choice(short_templates)
            aphorism = self._get_template_content(template, self.word_pools)
            
        return aphorism.strip()
        
    def generate_sacred_wisdom(self):
        """Generate sacred wisdom saying"""
        template = random.choice(self.sacred_templates)
        wisdom = self._get_template_content(template, self.word_pools)
        return wisdom.strip()
        
    def generate_esoteric_reflection(self):
        """Generate esoteric reflection"""
        template = random.choice(self.esoteric_templates)
        reflection = self._get_template_content(template, self.word_pools)
        return reflection.strip()
        
    def generate_spiritual_beauty_quote(self):
        """Generate spiritual beauty quote"""
        template = random.choice(self.beauty_templates)
        beauty_quote = self._get_template_content(template, self.word_pools)
        return beauty_quote.strip()
        
    def generate_enhanced_content(self, quote_type='mixed'):
        """Generate 100% authentic content from esoteric dataset"""
        
        # Always use authentic esoteric content only
        if self.df.empty:
            self.logger.warning("⚠️ No esoteric dataset available")
            return None, 'no_data'
        
        # Get authentic content from quality pools (prioritize elite and high quality)
        preferred_pools = [pool for pool in self.content_pools.keys() if 'elite' in pool or 'high' in pool]
        fallback_pools = [pool for pool in self.content_pools.keys() if 'good' in pool]
        
        available_pools = preferred_pools if preferred_pools else fallback_pools
        
        if not available_pools:
            self.logger.warning("⚠️ No content pools available")
            return None, 'no_pools'
        
        # Try to find suitable authentic content
        max_attempts = 20
        for attempt in range(max_attempts):
            pool_name = random.choice(available_pools)
            pool = self.content_pools[pool_name]
            
            if not pool.empty:
                authentic_post = pool.sample(1).iloc[0]
                authentic_content = authentic_post['content']
                
                # Filter out influencer names and prioritize spiritual content
                if self._is_suitable_transcendent_content(authentic_content):
                    # Check length with balanced approach
                    content_length = len(authentic_content)
                    if self._is_balanced_length(content_length):
                        # Use authentic content from the vast dataset (18,452 posts)
                        if not self._is_content_recent(authentic_content) or len(self.recent_content) > 10:
                            self._track_content_usage(authentic_content)
                            # Clean content by removing '>' characters
                            cleaned_content = authentic_content.replace('>', '').strip()
                            category = authentic_post.get('category', 'general_wisdom')
                            quality = authentic_post.get('quality_score', 6)
                            return cleaned_content, f'authentic_{category}_q{quality}'
        
        # No suitable content found
        return None, 'no_suitable_content'
        
    def generate_transcendent_content(self, count=1, quote_type='mixed'):
        """Generate multiple pieces of transcendent content"""
        results = []
        
        for i in range(count):
            content, generation_type = self.generate_enhanced_content(quote_type)
            
            results.append({
                'content': content,
                'type': quote_type if quote_type != 'mixed' else generation_type,
                'generation_method': generation_type,
                'length': len(content),
                'generated_at': datetime.now().isoformat()
            })
            
        return results
        
    def log_transcendent_content(self, content, content_type, generation_type="transcendent"):
        """Log generated transcendent content"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'content': content,
            'type': content_type,
            'generation_type': generation_type,
            'length': len(content)
        }
        
        log_file = 'data/transcendent_log.csv'
        
        # Create log file if it doesn't exist
        if not os.path.exists(log_file):
            with open(log_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=log_data.keys())
                writer.writeheader()
                
        # Append log entry
        with open(log_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=log_data.keys())
            writer.writerow(log_data)
            
        self.logger.info(f"✨ Generated {content_type} content: {content[:50]}...")

def main():
    """Test the transcendent quote generator"""
    generator = TranscendentQuoteGenerator()
    
    print("🌟 Transcendent Quote Generator Test")
    print("=" * 50)
    
    # Generate different types of content
    types = ['transcendent', 'mystical', 'sacred', 'esoteric', 'beauty']
    
    for quote_type in types:
        print(f"\n🔮 {quote_type.title()} Content:")
        results = generator.generate_transcendent_content(count=3, quote_type=quote_type)
        
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['content']}")
            print(f"   (Type: {result['type']}, Method: {result['generation_method']}, Length: {result['length']})")
            
            # Log the content
            generator.log_transcendent_content(
                result['content'], 
                result['type'], 
                result['generation_method']
            )

if __name__ == "__main__":
    main()