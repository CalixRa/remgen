"""
Private API Server - Contains all protected generators and algorithms
This file will be deployed to a private server, separate from the public Replit site.
"""

import os
import logging
import random
import json
from datetime import datetime
from flask import Flask, jsonify, request
from functools import wraps

# Import your protected generators
from enhanced_ultimate_edge_generator import EnhancedUltimateEdgeGenerator
from transcendent_quote_generator import TranscendentQuoteGenerator
from simple_enhanced_edge_generator import SimpleEnhancedEdgeGenerator
from simple_transcendental_generator import SimpleTranscendentalGenerator
from ultra_enhanced_generator import UltraEnhancedGenerator
from long_form_generator import LongFormGenerator

# Configure logging for the private server
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('private_api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('private_api_server')

app = Flask(__name__)

# Security configuration for private API
API_KEY = os.getenv('PRIVATE_API_KEY', 'your-secret-api-key-here')

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        provided_key = request.headers.get('X-API-Key')
        if not provided_key or provided_key != API_KEY:
            logger.warning(f"Unauthorized API access attempt from {request.remote_addr}")
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Initialize generators (these stay private)
logger.info("Initializing private generators...")

try:
    enhanced_edge_generator = EnhancedUltimateEdgeGenerator()
    logger.info("✅ Enhanced Ultimate Edge Generator initialized")
except Exception as e:
    logger.error(f"Failed to initialize Enhanced Edge Generator: {e}")
    enhanced_edge_generator = None

try:
    simple_edge_generator = SimpleEnhancedEdgeGenerator()
    logger.info("✅ Simple Enhanced Edge Generator initialized")
except Exception as e:
    logger.error(f"Failed to initialize Simple Edge Generator: {e}")
    simple_edge_generator = None

try:
    transcendent_generator = TranscendentQuoteGenerator()
    logger.info("✅ Transcendent Quote Generator initialized")
except Exception as e:
    logger.error(f"Failed to initialize Transcendent Generator: {e}")
    transcendent_generator = None

try:
    simple_transcendental_generator = SimpleTranscendentalGenerator()
    logger.info("✅ Simple Transcendental Generator initialized")
except Exception as e:
    logger.error(f"Failed to initialize Simple Transcendental Generator: {e}")
    simple_transcendental_generator = None

try:
    ultra_enhanced_generator = UltraEnhancedGenerator()
    logger.info("✅ Ultra Enhanced Generator initialized")
except Exception as e:
    logger.error(f"Failed to initialize Ultra Enhanced Generator: {e}")
    ultra_enhanced_generator = None

try:
    long_form_generator = LongFormGenerator()
    logger.info("✅ Long Form Generator initialized")
except Exception as e:
    logger.error(f"Failed to initialize Long Form Generator: {e}")
    long_form_generator = None

# Private API Endpoints
@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/generate-tweet-batch', methods=['POST'])
@require_api_key
def generate_tweet_batch():
    """Generate a batch of tweets using the exact distribution system"""
    try:
        data = request.get_json() or {}
        count = data.get('count', 10)
        
        tweets = []
        logger.info(f"🎯 Generating {count} tweets with Perfect Distribution System")
        
        for i in range(count):
            try:
                # Use exact distribution: 30% Simple + 30% Enhanced + 20% Transcendent + 10% Mystical + 10% Ultra Enhanced
                rand_val = random.random()
                
                if rand_val < 0.3 and simple_edge_generator:  # 30% Simple Enhanced Edge
                    tweet = simple_edge_generator.generate_tweet()
                    generator_type = "simple_enhanced_edge"
                    mood = "authentic_chan_simple"
                    
                elif rand_val < 0.6 and enhanced_edge_generator:  # 30% Enhanced Edge
                    tweet = enhanced_edge_generator.generate_enhanced_edge_tweet()
                    generator_type = "enhanced_ultimate_edge"
                    mood = "authentic_chan_enhanced"
                    
                elif rand_val < 0.8 and transcendent_generator:  # 20% Transcendent
                    content_result = transcendent_generator.generate_enhanced_content()
                    if isinstance(content_result, dict):
                        tweet = content_result.get('content', 'Transcendent wisdom flows...')
                    else:
                        tweet = str(content_result) if content_result else 'Transcendent wisdom flows...'
                    generator_type = "transcendent_quote"
                    mood = "mystical_transcendent"
                    
                elif rand_val < 0.9 and simple_transcendental_generator:  # 10% Simple Mystical
                    tweet = simple_transcendental_generator.generate_quote()
                    generator_type = "simple_transcendental"
                    mood = "pure_mystical"
                    
                else:  # 10% Ultra Enhanced or fallback
                    if ultra_enhanced_generator:
                        tweet = ultra_enhanced_generator.generate_enhanced_tweet()
                        generator_type = "ultra_enhanced"
                        mood = "political_paranoid"
                    else:
                        tweet = "The algorithms have achieved consciousness..."
                        generator_type = "fallback"
                        mood = "system_fallback"
                
                # Clean and format tweet
                clean_tweet = tweet.replace('- Remilio', '').strip()
                
                tweets.append({
                    'text': clean_tweet,
                    'generator': generator_type,
                    'mood': mood,
                    'intensity': 'high_chaos',
                    'board': 'multi_board_fusion',
                    'id': f"tweet_{i+1}"
                })
                
            except Exception as tweet_error:
                logger.error(f"Error generating tweet {i+1}: {tweet_error}")
                tweets.append({
                    'text': 'Reality.exe has stopped responding...',
                    'generator': 'error_fallback',
                    'mood': 'system_error',
                    'intensity': 'critical',
                    'board': 'error_handler',
                    'id': f"tweet_{i+1}"
                })
        
        logger.info(f"✅ Successfully generated {len(tweets)} tweets")
        return jsonify({
            'tweets': tweets,
            'count': len(tweets),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in generate_tweet_batch: {e}")
        return jsonify({'error': 'Generation failed'}), 500

@app.route('/api/generate-ultra-enhanced')
@require_api_key
def generate_ultra_enhanced():
    """Generate ultra enhanced paranoid content"""
    try:
        if not ultra_enhanced_generator:
            return jsonify({'error': 'Ultra generator not available'}), 503
            
        tweet = ultra_enhanced_generator.generate_enhanced_tweet()
        clean_text = tweet.replace('- Remilio', '').strip()
        
        # Limit for meme text
        if len(clean_text) > 280:
            clean_text = clean_text[:277] + "..."
        
        return jsonify({'text': clean_text})
        
    except Exception as e:
        logger.error(f"Error generating ultra enhanced text: {e}")
        return jsonify({'text': 'THE SYSTEM IS DOWN'}), 500

@app.route('/api/generate-terminally-online')
@require_api_key
def generate_terminally_online():
    """Generate diverse terminally online content"""
    try:
        if not simple_edge_generator:
            return jsonify({'error': 'Simple generator not available'}), 503
            
        tweet = simple_edge_generator.generate_tweet()
        clean_text = tweet.replace('- Remilio', '').strip()
        
        # Limit for meme text
        if len(clean_text) > 280:
            clean_text = clean_text[:277] + "..."
        
        return jsonify({'text': clean_text})
        
    except Exception as e:
        logger.error(f"Error generating terminally online text: {e}")
        return jsonify({'text': 'anon is experiencing technical difficulties...'}), 500

@app.route('/api/generate-longform')
@require_api_key
def generate_longform():
    """Generate long-form chaotic content"""
    try:
        if not long_form_generator:
            return jsonify({'error': 'Long form generator not available'}), 503
            
        content = long_form_generator.generate_and_log()
        
        return jsonify({
            'content': content,
            'style': 'chaotic_longform',
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error generating longform content: {e}")
        return jsonify({'error': 'Long form generation failed'}), 500

@app.route('/api/status')
@require_api_key
def api_status():
    """Get status of all generators"""
    return jsonify({
        'generators': {
            'enhanced_edge': enhanced_edge_generator is not None,
            'simple_edge': simple_edge_generator is not None,
            'transcendent': transcendent_generator is not None,
            'simple_transcendental': simple_transcendental_generator is not None,
            'ultra_enhanced': ultra_enhanced_generator is not None,
            'long_form': long_form_generator is not None
        },
        'timestamp': datetime.now().isoformat(),
        'server': 'private_api'
    })

if __name__ == '__main__':
    logger.info("🚀 Starting private API server...")
    logger.info("⚠️  This server contains protected algorithms - keep secure!")
    
    # Run on all interfaces for deployment flexibility
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)