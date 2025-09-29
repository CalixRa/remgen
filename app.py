import os
import logging
import time
import random
import re
import hashlib
import json
from datetime import datetime, timedelta
from collections import defaultdict
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from enhanced_ultimate_edge_generator import EnhancedUltimateEdgeGenerator
from transcendent_quote_generator import TranscendentQuoteGenerator
from simple_enhanced_edge_generator import SimpleEnhancedEdgeGenerator
from simple_transcendental_generator import SimpleTranscendentalGenerator
from ultra_enhanced_generator import UltraEnhancedGenerator

from simple_csv_generator import SimpleCsvGenerator
from text_styling_system import TextStylingSystem
from long_form_generator import LongFormGenerator
from video_downloader import VideoDownloader
# Enhanced Ultimate Edge Generation System - Authentic Dynamic Content

# Configure enhanced logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_security.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('remilio_app')
security_logger = logging.getLogger('security')

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload size

# Security Configuration
RATE_LIMIT_STORAGE = defaultdict(lambda: defaultdict(list))
MAX_REQUESTS_PER_HOUR = {
    'generation': 300,  # Content generation requests
    'upload': 50,       # File uploads
    'api': 1000,        # API calls (increased for video downloads)
    'video_download': 2000,  # Video download progress checks
    'page': 500         # Page views
}

# Input validation patterns
SUSPICIOUS_PATTERNS = [
    r'<script[^>]*>.*?</script>',  # Script tags
    r'javascript:',                # JavaScript protocol
    r'on\w+\s*=',                 # Event handlers
    r'<iframe[^>]*>.*?</iframe>',  # Iframes
    r'DROP\s+TABLE',              # SQL injection
    r'SELECT\s+\*\s+FROM',        # SQL injection
    r'UNION\s+SELECT',            # SQL injection
    r'\.\./',                     # Path traversal
    r'eval\s*\(',                 # Code evaluation
    r'exec\s*\(',                 # Code execution
]

# Upload configuration
UPLOAD_FOLDER = 'static/uploaded_templates'
SAVED_MEMES_FOLDER = 'static/saved_memes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SAVED_MEMES_FOLDER'] = SAVED_MEMES_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create upload directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(SAVED_MEMES_FOLDER, exist_ok=True)

# Security Functions
def get_client_ip():
    """Get the real client IP address"""
    forwarded_for = request.headers.get('X-Forwarded-For')
    if forwarded_for:
        return forwarded_for.split(',')[0].strip()
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr or '127.0.0.1'

def is_rate_limited(ip_address, endpoint_type):
    """Check if IP is rate limited for specific endpoint type"""
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    
    # Clean old entries
    RATE_LIMIT_STORAGE[ip_address][endpoint_type] = [
        timestamp for timestamp in RATE_LIMIT_STORAGE[ip_address][endpoint_type]
        if timestamp > hour_ago
    ]
    
    # Check current count
    current_count = len(RATE_LIMIT_STORAGE[ip_address][endpoint_type])
    max_allowed = MAX_REQUESTS_PER_HOUR.get(endpoint_type, 100)
    
    if current_count >= max_allowed:
        security_logger.warning(f"Rate limit exceeded for {ip_address} on {endpoint_type}: {current_count}/{max_allowed}")
        return True
    
    # Add current request
    RATE_LIMIT_STORAGE[ip_address][endpoint_type].append(now)
    return False

def validate_input(text_input):
    """Validate text input for suspicious patterns"""
    if not text_input or not isinstance(text_input, str):
        return True  # Allow empty or non-string inputs
    
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, text_input, re.IGNORECASE):
            security_logger.warning(f"Suspicious input detected from {get_client_ip()}: {pattern}")
            return False
    
    # Check for excessive length
    if len(text_input) > 10000:
        security_logger.warning(f"Excessive input length from {get_client_ip()}: {len(text_input)} chars")
        return False
    
    return True

def log_security_event(event_type, details, severity="INFO"):
    """Log security events with details"""
    client_ip = get_client_ip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    security_event = {
        'timestamp': datetime.now().isoformat(),
        'client_ip': client_ip,
        'user_agent': user_agent,
        'event_type': event_type,
        'details': details,
        'endpoint': request.endpoint,
        'method': request.method,
        'url': request.url
    }
    
    if severity == "WARNING":
        security_logger.warning(f"Security Event: {json.dumps(security_event)}")
    elif severity == "ERROR":
        security_logger.error(f"Security Event: {json.dumps(security_event)}")
    else:
        security_logger.info(f"Security Event: {json.dumps(security_event)}")

# Security Decorators
def rate_limit(endpoint_type):
    """Rate limiting decorator"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            client_ip = get_client_ip()
            
            if is_rate_limited(client_ip, endpoint_type):
                log_security_event('rate_limit_exceeded', 
                                 {'endpoint_type': endpoint_type, 'ip': client_ip}, 
                                 'WARNING')
                return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def input_validation(f):
    """Input validation decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = get_client_ip()
        
        # Validate form data
        if request.method in ['POST', 'PUT']:
            for key, value in request.form.items():
                if isinstance(value, str) and not validate_input(value):
                    log_security_event('malicious_input_blocked', 
                                     {'field': key, 'ip': client_ip}, 
                                     'WARNING')
                    return jsonify({'error': 'Invalid input detected'}), 400
            
            # Validate JSON data
            if request.is_json:
                try:
                    json_data = request.get_json()
                    if json_data:
                        for key, value in json_data.items():
                            if isinstance(value, str) and not validate_input(value):
                                log_security_event('malicious_json_blocked', 
                                                 {'field': key, 'ip': client_ip}, 
                                                 'WARNING')
                                return jsonify({'error': 'Invalid input detected'}), 400
                except Exception as e:
                    log_security_event('invalid_json', 
                                     {'error': str(e), 'ip': client_ip}, 
                                     'WARNING')
                    return jsonify({'error': 'Invalid JSON data'}), 400
        
        return f(*args, **kwargs)
    return decorated_function

def security_headers(f):
    """Add security headers decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        response = f(*args, **kwargs)
        
        # Add security headers
        if hasattr(response, 'headers'):
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'
            response.headers['X-XSS-Protection'] = '1; mode=block'
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            response.headers['Access-Control-Allow-Origin'] = '*'  # Basic CORS
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        
        return response
    return decorated_function

# Apply security headers to all routes
@app.after_request
def after_request(response):
    """Apply security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

def allowed_file(filename):
    """Check if uploaded file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_uploaded_templates():
    """Get list of uploaded template images"""
    templates = []
    if os.path.exists(UPLOAD_FOLDER):
        for filename in os.listdir(UPLOAD_FOLDER):
            if allowed_file(filename):
                templates.append({
                    'filename': filename,
                    'url': f'/static/uploaded_templates/{filename}',
                    'upload_time': datetime.fromtimestamp(
                        os.path.getctime(os.path.join(UPLOAD_FOLDER, filename))
                    ).strftime('%Y-%m-%d %H:%M')
                })
    # Sort by upload time, newest first
    templates.sort(key=lambda x: x['upload_time'], reverse=True)
    return templates

def get_saved_memes():
    """Get list of saved collaborative memes with text metadata"""
    import json
    memes = []
    if os.path.exists(SAVED_MEMES_FOLDER):
        for filename in os.listdir(SAVED_MEMES_FOLDER):
            if allowed_file(filename):
                filepath = os.path.join(SAVED_MEMES_FOLDER, filename)
                
                # Look for corresponding metadata file (handle both .png and .jpg extensions)
                if filename.endswith('.png'):
                    metadata_filename = filename.replace('.png', '_metadata.json')
                elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
                    metadata_filename = filename.replace('.jpg', '_metadata.json').replace('.jpeg', '_metadata.json')
                else:
                    continue  # Skip non-image files
                metadata_filepath = os.path.join(SAVED_MEMES_FOLDER, metadata_filename)
                
                meme_data = {
                    'filename': filename,
                    'url': f'/static/saved_memes/{filename}',
                    'created_at': datetime.fromtimestamp(
                        os.path.getctime(filepath)
                    ).strftime('%Y-%m-%d %H:%M'),
                    'top_text': '',
                    'bottom_text': ''
                }
                
                # Load text metadata if available
                if os.path.exists(metadata_filepath):
                    try:
                        with open(metadata_filepath, 'r', encoding='utf-8') as f:
                            metadata = json.load(f)
                            meme_data['top_text'] = metadata.get('top_text', '')
                            meme_data['bottom_text'] = metadata.get('bottom_text', '')
                    except Exception as e:
                        logger.warning(f"Could not load metadata for {filename}: {e}")
                
                memes.append(meme_data)
    
    # Sort by creation time, newest first
    memes.sort(key=lambda x: x['created_at'], reverse=True)
    return memes

# Initialize Enhanced Ultimate Edge Generation System
try:
    enhanced_edge_generator = EnhancedUltimateEdgeGenerator()
    logger.info("✅ Enhanced Ultimate Edge Generator initialized")
except Exception as e:
    enhanced_edge_generator = None
    logger.error(f"❌ Enhanced Ultimate Edge Generator failed: {e}")

try:
    simple_edge_generator = SimpleEnhancedEdgeGenerator()
    logger.info("✅ Simple Enhanced Edge Generator initialized")
except Exception as e:
    simple_edge_generator = None
    logger.error(f"❌ Simple Enhanced Edge Generator failed: {e}")

try:
    transcendent_generator = TranscendentQuoteGenerator()
    logger.info("✅ Transcendent Quote Generator initialized")
except Exception as e:
    transcendent_generator = None
    logger.error(f"❌ Transcendent Quote Generator failed: {e}")

try:
    simple_transcendental_generator = SimpleTranscendentalGenerator()
    logger.info("✅ Simple Transcendental Generator initialized")
except Exception as e:
    simple_transcendental_generator = None
    logger.error(f"❌ Simple Transcendental Generator failed: {e}")

try:
    ultra_enhanced_generator = UltraEnhancedGenerator()
    logger.info("✅ Ultra Enhanced Generator initialized")
except Exception as e:
    ultra_enhanced_generator = None
    logger.error(f"❌ Ultra Enhanced Generator failed: {e}")

try:
    csv_generator = SimpleCsvGenerator()
    logger.info("✅ Simple CSV Generator initialized")
except Exception as e:
    csv_generator = None
    logger.error(f"❌ Simple CSV Generator failed: {e}")

# Initialize text styling system
text_styling_system = TextStylingSystem()
logger.info("✅ Text Styling System initialized")

# Initialize long form generator
try:
    long_form_gen = LongFormGenerator()
    logger.info("✅ Long Form Generator initialized")
except Exception as e:
    long_form_gen = None
    logger.error(f"❌ Long Form Generator failed: {e}")

# Initialize video downloader
try:
    video_downloader = VideoDownloader()
    logger.info("✅ Video Downloader initialized")
except Exception as e:
    video_downloader = None
    logger.error(f"❌ Video Downloader failed: {e}")

# Twitter functionality removed
twitter_enabled = False
logger.info("Twitter functionality disabled in web interface")

@app.route('/')
def home():
    """Home page with tweet generation controls"""
    # Load featured tweets (most recent saved ones)
    featured_tweets = []
    
    try:
        os.makedirs('data/selected_tweets', exist_ok=True)
        saved_files = os.listdir('data/selected_tweets')
        saved_files.sort(reverse=True)  # Most recent first
        
        # Get top 3 most recent saved tweets
        for filename in saved_files[:3]:
            if filename.endswith('.txt'):
                filepath = os.path.join('data/selected_tweets', filename)
                timestamp = filename.replace('tweet_', '').replace('.txt', '')
                
                try:
                    timestamp = datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
                    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    timestamp = 'Unknown'
                
                with open(filepath, 'r') as f:
                    tweet_text = f.read().strip()
                
                featured_tweets.append({
                    'text': tweet_text,
                    'timestamp': timestamp
                })
    except Exception as e:
        logger.error(f"Error loading featured tweets: {e}", exc_info=True)
    
    return render_template('index.html', 
                          featured_tweets=featured_tweets,
                          twitter_enabled=twitter_enabled,
                          active_tab='home',
                          now=int(time.time()))  # For cache busting

@app.route('/saved')
def saved_tweets():
    """Show saved tweets"""
    # Load saved tweets
    saved_tweets = []
    
    try:
        os.makedirs('data/selected_tweets', exist_ok=True)
        saved_files = os.listdir('data/selected_tweets')
        saved_files.sort(reverse=True)  # Most recent first
        
        for filename in saved_files:
            if filename.endswith('.txt'):
                filepath = os.path.join('data/selected_tweets', filename)
                timestamp = filename.replace('tweet_', '').replace('.txt', '')
                
                try:
                    timestamp = datetime.strptime(timestamp, '%Y%m%d_%H%M%S')
                    timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    timestamp = 'Unknown'
                
                with open(filepath, 'r') as f:
                    tweet_text = f.read().strip()
                
                saved_tweets.append({
                    'text': tweet_text,
                    'timestamp': timestamp,
                    'filename': filename
                })
    except Exception as e:
        logger.error(f"Error loading saved tweets: {e}", exc_info=True)
    
    # Check if developer mode is enabled
    developer_mode = os.getenv('DEVELOPER_MODE', 'false').lower() == 'true'
    
    return render_template('saved.html', 
                          saved_tweets=saved_tweets,
                          active_tab='saved',
                          twitter_enabled=twitter_enabled,
                          developer_mode=developer_mode,
                          now=int(time.time()))  # For cache busting





@app.route('/generate', methods=['GET', 'POST'])
@rate_limit('generation')
@input_validation
def generate_tweets():
    """Generate new tweets and display them directly on page"""
    # Get count from either form data (POST) or query params (GET)
    if request.method == 'POST':
        count = int(request.form.get('count', 10))
    else:
        count = int(request.args.get('count', 10))
    
    tweets = []
    
    logger.info("🎯 Updated Distribution System: 20% Enhanced Ultimate + 20% Simple Enhanced + 20% Ultra Enhanced + 10% Transcendent + 10% Simple Transcendental + 10% CSV")
    
    # Generate tweets using exact 20/20/20/10/10/10 distribution with no fallbacks
    for i in range(count):
        try:
            # Determine generator based on exact distribution
            rand_val = random.random()
            
            # 20% Enhanced Ultimate Edge Generator
            if rand_val < 0.2:
                if enhanced_edge_generator:
                    tweet = enhanced_edge_generator.generate_enhanced_edge_tweet()
                    generator_type = "enhanced_ultimate_edge"
                    mood = "authentic_chan_edge"
                    intensity = "ultimate_edge_sophistication"
                    board = "enhanced_4chan_content"
                    logger.info("🔥 Generated tweet using ENHANCED ULTIMATE EDGE generator")
                else:
                    tweet = "Enhanced edge generator not available"
                    generator_type = "fallback"
                    mood = "fallback"
                    intensity = "fallback"
                    board = "fallback"
            
            # 20% Simple Enhanced Edge Generator (20% + 20% = 40% total)
            elif rand_val < 0.4:
                if simple_edge_generator:
                    tweet = simple_edge_generator.generate_tweet()
                    generator_type = "simple_enhanced_edge"
                    mood = "authentic_chan_simple"
                    intensity = "short_form_edge"
                    board = "simple_4chan_content"
                    logger.info("🔥 Generated tweet using SIMPLE ENHANCED EDGE generator")
                else:
                    tweet = "Simple edge generator not available"
                    generator_type = "fallback"
                    mood = "fallback"
                    intensity = "fallback"
                    board = "fallback"
            
            # 20% Ultra Enhanced Generator (40% + 20% = 60% total)
            elif rand_val < 0.6:
                if ultra_enhanced_generator:
                    tweet = ultra_enhanced_generator.generate_enhanced_tweet()
                    generator_type = "ultra_enhanced"
                    mood = "political_conspiracy_pudgy_penguin"
                    intensity = "ultra_enhanced_edge"
                    board = "political_paranoid_content"
                    logger.info("🔥 Generated tweet using ULTRA ENHANCED generator")
                else:
                    tweet = "Ultra enhanced generator not available"
                    generator_type = "fallback"
                    mood = "fallback"
                    intensity = "fallback"
                    board = "fallback"
            
            # 10% Transcendent Quote Generator (60% + 10% = 70% total)
            elif rand_val < 0.7:
                if transcendent_generator:
                    transcendent_result = transcendent_generator.generate_enhanced_content('mixed')
                    
                    if transcendent_result and transcendent_result[0] and len(transcendent_result) >= 2:
                        transcendent_quote = transcendent_result[0]
                        tweet = f"{transcendent_quote} - Remilio"
                    else:
                        transcendent_content, transcendent_type = transcendent_generator.generate_enhanced_content()
                        tweet = transcendent_content
                    
                    generator_type = "authentic_transcendent_quotes"
                    mood = "authentic_spiritual_beauty"
                    intensity = "pure_transcendent_wisdom"
                    board = "authentic_transcendent_content"
                    logger.info("✨ Generated tweet using TRANSCENDENT QUOTE generator")
                else:
                    tweet = "Transcendent generator not available"
                    generator_type = "fallback"
                    mood = "fallback"
                    intensity = "fallback"
                    board = "fallback"
            
            # 10% Simple Transcendental Generator (70% + 10% = 80% total)
            elif rand_val < 0.8:
                if simple_transcendental_generator:
                    tweet = simple_transcendental_generator.generate_quote()
                    generator_type = "simple_transcendental"
                    mood = "transcendental_mystical"
                    intensity = "pure_transcendental"
                    board = "unified_mystical_content"
                    logger.info("✨ Generated tweet using SIMPLE TRANSCENDENTAL generator")
                else:
                    tweet = "Simple transcendental generator not available"
                    generator_type = "fallback"
                    mood = "fallback"
                    intensity = "fallback"
                    board = "fallback"
            
            # 10% Simple CSV Generator (80% + 10% = 90% total)
            elif rand_val < 0.9:
                if csv_generator:
                    tweet = csv_generator.generate_content()
                    generator_type = "simple_csv"
                    mood = "clean_curated_content"
                    intensity = "high_quality_memes"
                    board = "curated_csv_content"
                    logger.info("📋 Generated tweet using SIMPLE CSV generator")
                else:
                    tweet = "CSV generator not available"
                    generator_type = "fallback"
                    mood = "fallback"
                    intensity = "fallback"
                    board = "fallback"
            
            # 10% Reserve/Fallback (90% + 10% = 100% total) - Use CSV as fallback
            else:
                if csv_generator:
                    tweet = csv_generator.generate_content()
                    generator_type = "simple_csv_fallback"
                    mood = "clean_curated_content"
                    intensity = "high_quality_memes"
                    board = "curated_csv_content"
                    logger.info("📋 Generated tweet using SIMPLE CSV generator (fallback)")
                else:
                    tweet = "All generators unavailable"
                    generator_type = "system_fallback"
                    mood = "fallback"
                    intensity = "fallback"
                    board = "fallback"
            
            if not tweet or len(tweet) < 10:
                logger.warning("Generated empty or very short tweet, skipping")
                continue
                
            tweets.append({
                'text': tweet,
                'generator_type': generator_type,
                'mood': mood,
                'intensity': intensity,
                'board': board
            })
        except Exception as e:
            logger.error(f"Error generating tweet: {e}", exc_info=True)
            flash(f"Error generating content: {str(e)}", "error")
            # Don't break, try to generate more tweets even if one fails
            continue
    
    # For direct tweet generation, add a message about success
    if tweets:
        flash(f"Generated {len(tweets)} new posts", "success")
    
    redirect_to = request.form.get('redirect_to', None)
    if redirect_to == 'home':
        return redirect(url_for('home'))
    elif redirect_to == 'saved':
        return redirect(url_for('saved_tweets'))
    else:
        return render_template('index.html', 
                              tweets=tweets,
                              twitter_enabled=twitter_enabled,
                              active_tab='home',
                              now=int(time.time()))  # For cache busting

@app.route('/save-tweet', methods=['POST'])
@rate_limit('api')
@input_validation
def save_tweet():
    """Save a selected tweet for manual posting - AJAX version"""
    tweet_text = request.form.get('tweet_text', '')
    
    if not tweet_text:
        return jsonify({'success': False, 'error': 'No tweet text provided'})
    
    try:
        # Create directory if it doesn't exist
        os.makedirs('data/selected_tweets', exist_ok=True)
        
        # Save to file with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'tweet_{timestamp}.txt'
        filepath = os.path.join('data/selected_tweets', filename)
        
        with open(filepath, 'w') as f:
            f.write(tweet_text)
        
        logger.info(f"Saved tweet to {filepath}")
        return jsonify({'success': True})
    
    except Exception as e:
        logger.error(f"Error saving tweet: {e}", exc_info=True)
        return jsonify({'success': False, 'error': str(e)})

@app.route('/post-tweet', methods=['POST'])
@rate_limit('api')
@input_validation
def post_tweet():
    """Save a selected tweet and redirect"""
    tweet_text = request.form.get('tweet_text', '')
    redirect_to = request.form.get('redirect_to', 'home')
    
    if not tweet_text:
        flash("No tweet text provided", "error")
    else:
        try:
            # Create directory if it doesn't exist
            os.makedirs('data/selected_tweets', exist_ok=True)
            
            # Save to file with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'tweet_{timestamp}.txt'
            filepath = os.path.join('data/selected_tweets', filename)
            
            with open(filepath, 'w') as f:
                f.write(tweet_text)
            
            logger.info(f"Saved tweet to {filepath}")
            flash("Tweet saved successfully", "success")
            
            # Twitter posting functionality has been removed
            flash("Tweet saved successfully to local storage", "info")
                
        except Exception as e:
            logger.error(f"Error saving tweet: {e}", exc_info=True)
            flash(f"Error saving tweet: {str(e)}", "error")
    
    if redirect_to == 'saved':
        return redirect(url_for('saved_tweets'))
    else:
        return redirect(url_for('home'))

@app.route('/delete_tweet/<filename>', methods=['POST'])
def delete_tweet(filename):
    """Delete a saved tweet - developer only"""
    # Check if developer mode is enabled
    developer_mode = os.getenv('DEVELOPER_MODE', 'false').lower() == 'true'
    
    if not developer_mode:
        flash("Access denied", "error")
        return redirect(url_for('saved_tweets'))
    
    try:
        filepath = os.path.join('data/selected_tweets', filename)
        if os.path.exists(filepath) and filename.endswith('.txt'):
            os.remove(filepath)
            logger.info(f"Deleted tweet file: {filename}")
            flash(f"Tweet deleted successfully", "success")
        else:
            flash("Tweet not found", "error")
    except Exception as e:
        logger.error(f"Error deleting tweet {filename}: {e}", exc_info=True)
        flash(f"Error deleting tweet: {str(e)}", "error")
    
    return redirect(url_for('saved_tweets'))

# Meme functionality temporarily disabled - generator was removed
# @app.route('/meme', methods=['GET', 'POST'])
# def meme_templates():
#     """Show available meme templates and generate memes from tweets"""
#     flash("Meme functionality temporarily disabled", "info")
#     return redirect(url_for('home'))

@app.route('/generate-meme-for-tweet/<tweet_id>', methods=['GET', 'POST'])
def generate_meme_for_tweet(tweet_id):
    """Generate a meme for a saved tweet"""
    try:
        # Load tweet from saved tweets
        filepath = os.path.join('data/selected_tweets', f'tweet_{tweet_id}.txt')
        if not os.path.exists(filepath):
            flash(f"Tweet {tweet_id} not found", "error")
            return redirect(url_for('saved_tweets'))
            
        with open(filepath, 'r') as f:
            tweet_text = f.read().strip()
        
        # Get template from form data if POST, otherwise use random template
        template_file = None
        if request.method == 'POST':
            template_file = request.form.get('template')
        
        # Clean the tweet text for meme use
        meme_text = tweet_text.replace('- Remilio', '').strip()
        
        # Split text for top/bottom if it's long
        if len(meme_text) > 50:
            words = meme_text.split()
            mid_point = len(words) // 2
            top_text = ' '.join(words[:mid_point])
            bottom_text = ' '.join(words[mid_point:])
        else:
            top_text = meme_text
            bottom_text = ""
        
        # Redirect to meme generator with pre-filled text
        return render_template('meme_generator.html', 
                              active_tab='meme_generator',
                              prefilled_top=top_text.upper(),
                              prefilled_bottom=bottom_text.upper(),
                              twitter_enabled=twitter_enabled,
                              timestamp=inject_now())
            
    except Exception as e:
        logger.error(f"Error generating meme: {e}", exc_info=True)
        flash(f"Error generating meme: {str(e)}", "error")
    
    return redirect(url_for('saved_tweets'))

# Create template files if they don't exist
def create_template_files():
    """Create the necessary HTML templates"""
    pass  # All templates are now managed directly

# Helper function to inject current timestamp for cache busting
@app.route('/longform', methods=['GET', 'POST'])
def longform_content():
    """Generate and display long-form chaotic content"""
    content = ""
    selected_style = "random"
    paragraph_count = 3
    
    # Available styles for selection
    styles = [
        {'id': 'random', 'name': 'Random Mix (Multiple Styles)'},
        {'id': 'cursed_mashup', 'name': 'Cursed Mashup'},
        {'id': 'conspiracy_overload', 'name': 'Conspiracy Overload'},
        {'id': 'existential_horror', 'name': 'Existential Horror'},
        {'id': 'tone_shift', 'name': 'Tone Shift'},
        {'id': 'fourth_wall', 'name': 'Fourth Wall Breaking'},
        {'id': 'narrative_collapse', 'name': 'Narrative Collapse'},
        {'id': 'theory_rabbit_hole', 'name': 'Theory Rabbit Hole'},
        {'id': 'identity_crisis', 'name': 'Identity Crisis'},
        {'id': 'timeline_fracture', 'name': 'Timeline Fracture'}
    ]
    
    if request.method == 'POST':
        try:
            # Get requested parameters
            style_id = request.form.get('style', 'random')
            selected_style = style_id
            paragraph_count = 1  # Hardcoded to generate exactly 1 paragraph
            
            # Generate the long-form content
            style_param = None if style_id == 'random' else style_id
            
            longform_gen = LongFormGenerator(
                input_file='data/god_tier_meme_dataset.csv',
                paragraph_count=paragraph_count,
                style=style_param
            )
            content = longform_gen.generate_content()
            longform_gen.log_content(content)
            
            # Flash success message
            flash(f'Generated new long-form content successfully!', 'success')
        except Exception as e:
            logger.error(f"Error generating long-form content: {e}", exc_info=True)
            flash(f'Error generating long-form content: {str(e)}', 'danger')
    
    return render_template('longform.html', 
                          content=content, 
                          styles=styles, 
                          selected_style=selected_style, 
                          active_tab='longform',
                          twitter_enabled=twitter_enabled,
                          timestamp=inject_now())







@app.route('/upload_template', methods=['POST'])
@rate_limit('upload')
@input_validation
def upload_template():
    """Upload a new meme template image"""
    if 'template_image' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('meme_generator'))
    
    file = request.files['template_image']
    
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('meme_generator'))
    
    if file and file.filename and allowed_file(file.filename):
        # Create secure filename
        original_filename = file.filename
        filename = secure_filename(original_filename)
        
        # Add timestamp to avoid conflicts
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{name}_{timestamp}{ext}"
        
        # Save file
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        flash(f'Template "{filename}" uploaded successfully!', 'success')
    else:
        flash('Invalid file type. Please upload PNG, JPG, JPEG, GIF, or WEBP files.', 'error')
    
    return redirect(url_for('meme_generator'))

@app.route('/delete_template/<filename>')
@rate_limit('api')
def delete_template(filename):
    """Delete an uploaded template"""
    try:
        # Security check - only allow deletion of files in upload folder
        safe_filename = secure_filename(filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            flash(f'Template "{filename}" deleted successfully!', 'success')
        else:
            flash('Template not found', 'error')
    except Exception as e:
        flash(f'Error deleting template: {str(e)}', 'error')
    
    return redirect(url_for('meme_generator'))

@app.context_processor
def inject_now():
    return {'now': int(time.time())}

# Add strftime filter for templates
@app.template_filter('strftime')
def strftime_filter(timestamp, format='%Y-%m-%d %H:%M:%S'):
    """Format timestamp using strftime"""
    if isinstance(timestamp, (int, float)):
        return datetime.fromtimestamp(timestamp).strftime(format)
    return str(timestamp)

@app.route('/meme-generator')
@app.route('/meme_generator')
def meme_generator():
    """Meme generator dashboard"""
    prefilled_top = request.args.get('top', '')
    prefilled_bottom = request.args.get('bottom', '')
    uploaded_templates = get_uploaded_templates()
    
    # Get font styling options from text styling system
    font_styles = text_styling_system.get_all_font_styles_css()
    style_options = text_styling_system.generate_style_options_html()
    
    return render_template('meme_generator.html', 
                          prefilled_top=prefilled_top,
                          prefilled_bottom=prefilled_bottom,
                          active_tab='meme_generator',
                          twitter_enabled=twitter_enabled,
                          uploaded_templates=uploaded_templates,
                          font_styles=font_styles,
                          style_options=style_options,
                          timestamp=inject_now())

@app.route('/api/generate-ultra-enhanced-text')
@rate_limit('api')
def generate_ultra_enhanced_text():
    """API endpoint to generate ultra enhanced paranoid text"""
    try:
        tweet = ultra_enhanced_generator.generate_enhanced_tweet()
        clean_text = tweet.replace('- Remilio', '').strip()
        
        # Limit to 280 characters for meme text to fit properly
        if len(clean_text) > 280:
            clean_text = clean_text[:277] + "..."
        
        return jsonify({'text': clean_text})
    except Exception as e:
        logger.error(f"Error generating ultra enhanced text: {e}")
        return jsonify({'text': 'THE SYSTEM IS DOWN'}), 500

@app.route('/api/generate-terminally-online-text')
@rate_limit('api')
def generate_terminally_online_text():
    """API endpoint to generate diverse, non-repetitive text"""
    try:
        # Use simple edge generator for diverse content
        tweet = simple_edge_generator.generate_tweet()
        clean_text = tweet.replace('- Remilio', '').strip()
        # Limit to 280 characters for meme text to fit properly
        if len(clean_text) > 280:
            clean_text = clean_text[:277] + "..."
        return jsonify({'text': clean_text})
    except Exception as e:
        logger.error(f"Error generating diverse text: {e}")
        return jsonify({'text': 'anon is experiencing technical difficulties...'}), 500

@app.route('/api/generate-auto-text')
def generate_auto_text():
    """API endpoint to generate text using distributed generator system"""
    try:
        # Use the same distribution system as the main tweet generator
        rand_val = random.random()
        generator_type = "unknown"
        
        # 20% Enhanced Ultimate Edge Generator
        if rand_val < 0.2:
            if enhanced_edge_generator:
                tweet = enhanced_edge_generator.generate_enhanced_edge_tweet()
                generator_type = "enhanced_ultimate_edge"
                logger.info("🔥 Generated meme text using ENHANCED ULTIMATE EDGE generator")
            else:
                tweet = "Enhanced edge generator not available"
                generator_type = "fallback"
        
        # 20% Simple Enhanced Edge Generator (20% + 20% = 40% total)
        elif rand_val < 0.4:
            if simple_edge_generator:
                tweet = simple_edge_generator.generate_tweet()
                generator_type = "simple_enhanced_edge"
                logger.info("🔥 Generated meme text using SIMPLE ENHANCED EDGE generator")
            else:
                tweet = "Simple edge generator not available"
                generator_type = "fallback"
        
        # 20% Ultra Enhanced Generator (40% + 20% = 60% total)
        elif rand_val < 0.6:
            if ultra_enhanced_generator:
                tweet = ultra_enhanced_generator.generate_enhanced_tweet()
                generator_type = "ultra_enhanced"
                logger.info("🔥 Generated meme text using ULTRA ENHANCED generator")
            else:
                tweet = "Ultra enhanced generator not available"
                generator_type = "fallback"
        
        # 10% Transcendent Quote Generator (60% + 10% = 70% total)
        elif rand_val < 0.7:
            if transcendent_generator:
                transcendent_result = transcendent_generator.generate_enhanced_content('mixed')
                if transcendent_result and transcendent_result[0] and len(transcendent_result) >= 2:
                    tweet = transcendent_result[0]
                else:
                    transcendent_content, transcendent_type = transcendent_generator.generate_enhanced_content()
                    tweet = transcendent_content
                generator_type = "transcendent_quote"
                logger.info("✨ Generated meme text using TRANSCENDENT QUOTE generator")
            else:
                tweet = "Transcendent generator not available"
                generator_type = "fallback"
        
        # 10% Simple Transcendental Generator (70% + 10% = 80% total)
        elif rand_val < 0.8:
            if simple_transcendental_generator:
                tweet = simple_transcendental_generator.generate_quote()
                generator_type = "simple_transcendental"
                logger.info("✨ Generated meme text using SIMPLE TRANSCENDENTAL generator")
            else:
                tweet = "Simple transcendental generator not available"
                generator_type = "fallback"
        
        # 20% Simple CSV Generator (80% + 20% = 100% total)
        else:
            if csv_generator:
                tweet = csv_generator.generate_content()
                generator_type = "simple_csv"
                logger.info("📋 Generated meme text using SIMPLE CSV generator")
            else:
                tweet = "CSV generator not available"
                generator_type = "fallback"
        
        # Clean and format text for meme display
        clean_text = tweet.replace('- Remilio', '').strip()
        
        # Remove any remaining reference indicators
        clean_text = re.sub(r'^>\s*', '', clean_text)
        clean_text = re.sub(r'\s*>+\s*$', '', clean_text)
        
        # Limit to 280 characters for proper meme text display
        if len(clean_text) > 280:
            # Try to truncate at sentence boundary
            if '.' in clean_text[:277]:
                clean_text = clean_text[:clean_text.rfind('.', 0, 277) + 1]
            elif ',' in clean_text[:277]:
                clean_text = clean_text[:clean_text.rfind(',', 0, 277)]
            else:
                clean_text = clean_text[:277] + "..."
        
        return jsonify({
            'text': clean_text,
            'generator': generator_type
        })
        
    except Exception as e:
        logger.error(f"Error generating auto text: {e}")
        return jsonify({'text': 'Content generation temporarily unavailable'}), 500

@app.route('/api/generate-genZ-brainrot-text')
@rate_limit('api')
def generate_genZ_brainrot_text():
    """API endpoint to generate Gen Z brainrot content"""
    try:
        # Initialize GenZ brainrot generator if not already done
        try:
            genZ_brainrot_generator = GenZBrainrotGenerator()
        except Exception as e:
            logger.error(f"Failed to initialize GenZ brainrot generator: {e}")
            return jsonify({'text': 'brainrot generator not available'}), 500
            
        content_type = request.args.get('type', None)  # gaming, sigma, social, skibidi, authentic
        tweet = genZ_brainrot_generator.generate_brainrot_content(content_type)
        
        # Clean and format text for meme display
        clean_text = tweet.replace('- Remilio', '').strip()
        
        # Limit to 280 characters for proper meme text display
        if len(clean_text) > 280:
            clean_text = clean_text[:277] + "..."
        
        return jsonify({'text': clean_text, 'type': content_type or 'mixed'})
    except Exception as e:
        logger.error(f"Error generating Gen Z brainrot text: {e}")
        return jsonify({'text': 'brainrot.exe has stopped working periodt'}), 500

@app.route('/save_collaborative_meme', methods=['POST'])
def save_collaborative_meme():
    """Save a meme to the collaborative collection with text metadata"""
    try:
        import base64
        import json
        
        # Get the image data and text from the request
        image_data = request.form.get('image_data')
        top_text = request.form.get('top_text', '')
        bottom_text = request.form.get('bottom_text', '')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Detect image format and extract base64 data
        image_format = 'jpg'  # Default to jpg for compression
        if 'data:image/png' in image_data:
            image_format = 'png'
        elif 'data:image/jpeg' in image_data:
            image_format = 'jpg'
        
        if 'base64,' in image_data:
            image_data = image_data.split('base64,')[1]
        
        # Generate unique filename with correct extension
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'meme_{timestamp}_{random.randint(1000, 9999)}.{image_format}'
        filepath = os.path.join(SAVED_MEMES_FOLDER, filename)
        
        # Decode and save the image
        image_bytes = base64.b64decode(image_data)
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # Save text metadata as JSON file
        metadata_filename = filename.replace(f'.{image_format}', '_metadata.json')
        metadata_filepath = os.path.join(SAVED_MEMES_FOLDER, metadata_filename)
        metadata = {
            'top_text': top_text,
            'bottom_text': bottom_text,
            'created_at': timestamp,
            'image_filename': filename
        }
        
        with open(metadata_filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved collaborative meme with text: {filename} (top: '{top_text[:50]}...', bottom: '{bottom_text[:50]}...')")
        return jsonify({'success': True, 'filename': filename})
        
    except Exception as e:
        logger.error(f"Error saving collaborative meme: {e}")
        return jsonify({'error': 'Failed to save meme'}), 500

@app.route('/get_collaborative_memes')
def get_collaborative_memes():
    """Get list of collaborative memes"""
    try:
        memes = get_saved_memes()
        return jsonify(memes)
    except Exception as e:
        logger.error(f"Error getting collaborative memes: {e}")
        return jsonify([]), 500

@app.route('/delete_saved_meme/<filename>', methods=['DELETE'])
@rate_limit('delete')
@input_validation
@security_headers
def delete_saved_meme(filename):
    """Delete a saved collaborative meme"""
    try:
        # Validate filename for security
        if not allowed_file(filename) or '..' in filename or '/' in filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        # Build full paths for image and metadata files
        image_path = os.path.join(SAVED_MEMES_FOLDER, filename)
        
        # Handle both .png and .jpg extensions for metadata
        if filename.endswith('.png'):
            metadata_filename = filename.replace('.png', '_metadata.json')
        elif filename.endswith('.jpg') or filename.endswith('.jpeg'):
            metadata_filename = filename.replace('.jpg', '_metadata.json').replace('.jpeg', '_metadata.json')
        else:
            return jsonify({'error': 'Invalid file type'}), 400
            
        metadata_path = os.path.join(SAVED_MEMES_FOLDER, metadata_filename)
        
        # Check if files exist and delete them
        deleted_files = []
        
        if os.path.exists(image_path):
            os.remove(image_path)
            deleted_files.append(filename)
            
        if os.path.exists(metadata_path):
            os.remove(metadata_path)
            deleted_files.append(metadata_filename)
        
        if not deleted_files:
            return jsonify({'error': 'File not found'}), 404
        
        logger.info(f"Deleted saved meme: {filename} and its metadata")
        return jsonify({'success': True, 'deleted_files': deleted_files})
        
    except Exception as e:
        logger.error(f"Error deleting saved meme {filename}: {e}")
        return jsonify({'error': 'Failed to delete meme'}), 500

# Video Downloader Routes
@app.route('/video-downloader')
@rate_limit('page')
def video_downloader_dashboard():
    """Video downloader dashboard"""
    try:
        # Get supported platforms
        platforms = video_downloader.get_supported_platforms() if video_downloader else []
        
        # Get download history
        history = video_downloader.get_download_history(limit=20) if video_downloader else []
        
        return render_template('video_downloader.html',
                              platforms=platforms,
                              download_history=history,
                              active_tab='video_downloader',
                              now=int(time.time()))
    except Exception as e:
        logger.error(f"Error loading video downloader dashboard: {e}")
        return render_template('video_downloader.html',
                              platforms=[],
                              download_history=[],
                              active_tab='video_downloader',
                              error="Video downloader not available",
                              now=int(time.time()))

@app.route('/api/video/info', methods=['POST'])
@rate_limit('video_download')
@input_validation
def get_video_info():
    """Get video information from URL"""
    try:
        if not video_downloader:
            return jsonify({'error': 'Video downloader not available'}), 503
        
        data = request.get_json()
        url = data.get('url', '').strip()
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        info = video_downloader.get_video_info(url)
        
        if 'error' in info:
            return jsonify({'error': info['error']}), 400
        
        return jsonify({
            'success': True,
            'info': info
        })
        
    except Exception as e:
        logger.error(f"Error getting video info: {e}")
        return jsonify({'error': 'Failed to get video information'}), 500

@app.route('/api/video/download', methods=['POST'])
@rate_limit('video_download')
@input_validation
def download_video():
    """Download video synchronously and return file info"""
    try:
        if not video_downloader:
            return jsonify({'error': 'Video downloader not available'}), 503
        
        data = request.get_json()
        url = data.get('url', '').strip()
        format_option = data.get('format', 'best')
        quality = data.get('quality', '1080')
        audio_only = data.get('audio_only', False)
        
        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Basic URL validation
        if not url.startswith(('http://', 'https://')):
            return jsonify({'error': 'Invalid URL format'}), 400
        
        # Build download options for synchronous download
        options = {
            'outtmpl': 'downloads/%(title)s_[%(height)sp].%(ext)s',
            'restrictfilenames': True,
            'ignoreerrors': False,
        }
        
        if audio_only or format_option in ['mp3', 'm4a']:
            options.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
            })
        else:
            # Map specific quality selections to appropriate yt-dlp format strings
            # Using more precise format selection that prioritizes specific heights
            if quality == '2160':
                # 4K (2160p) - try to get 2160p first, fallback to best available
                options['format'] = 'best[height>=2160]/best[height>=1440]/best[height>=1080]/best/worst'
            elif quality == '1440':
                # 2K (1440p) - try to get 1440p first, fallback appropriately
                options['format'] = 'best[height>=1440][height<=1440]/best[height>=1080][height<=1440]/best[height<=1440]/best/worst'
            elif quality == '1080':
                # Full HD (1080p) - try to get 1080p first, avoid higher resolutions
                options['format'] = 'best[height>=1080][height<=1200]/best[height>=720][height<=1200]/best[height<=1200]/worst'
            elif quality == '720':
                # HD (720p) - try to get 720p first, avoid higher resolutions  
                options['format'] = 'best[height>=720][height<=800]/best[height>=480][height<=800]/best[height<=800]/worst'
            elif quality == '480':
                # SD (480p) - try to get 480p first, avoid higher resolutions
                options['format'] = 'best[height>=480][height<=520]/best[height>=360][height<=520]/best[height<=520]/worst'
            elif quality == '360':
                # Low (360p) - get lowest acceptable quality
                options['format'] = 'best[height>=360][height<=400]/best[height<=400]/worst'
            else:
                # Fallback to 1080p range if no specific quality selected
                options['format'] = 'best[height>=1080][height<=1200]/best[height>=720][height<=1200]/best[height<=1200]/worst'
        
        # Debug logging to track quality selection
        logger.info(f"Quality selected: {quality}, Format string: {options.get('format')}")
        
        # Download synchronously 
        result = video_downloader.download_video_sync(url, options)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'file_info': result.get('file_info'),
                'message': 'Video downloaded successfully!'
            })
        else:
            return jsonify({
                'error': result.get('error', 'Download failed')
            }), 400
        
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return jsonify({'error': 'Failed to download video'}), 500

@app.route('/api/video/progress/<download_id>')
@rate_limit('video_download')
def get_download_progress(download_id):
    """Get download progress"""
    try:
        if not video_downloader:
            return jsonify({'error': 'Video downloader not available'}), 503
        
        progress = video_downloader.get_download_progress(download_id)
        
        if 'error' in progress:
            return jsonify({'error': progress['error']}), 404
        
        return jsonify({
            'success': True,
            'progress': progress
        })
        
    except Exception as e:
        logger.error(f"Error getting download progress: {e}")
        return jsonify({'error': 'Failed to get progress'}), 500

@app.route('/api/video/downloads')
@rate_limit('video_download')
def get_all_downloads():
    """Get all active downloads"""
    try:
        if not video_downloader:
            return jsonify({'error': 'Video downloader not available'}), 503
        
        downloads = video_downloader.get_all_downloads()
        
        return jsonify({
            'success': True,
            'downloads': downloads
        })
        
    except Exception as e:
        logger.error(f"Error getting downloads: {e}")
        return jsonify({'error': 'Failed to get downloads'}), 500

@app.route('/api/video/download_file/<download_id>')
@rate_limit('video_download')
def download_file(download_id):
    """Serve downloaded file to user"""
    try:
        if not video_downloader:
            return jsonify({'error': 'Video downloader not available'}), 503
        
        download_info = video_downloader.get_download_progress(download_id)
        
        if 'error' in download_info:
            return jsonify({'error': 'Download not found'}), 404
        
        if download_info.get('status') != 'completed':
            return jsonify({'error': 'Download not completed yet'}), 400
        
        filepath = download_info.get('filepath')
        if not filepath or not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        filename = download_info.get('filename', 'download')
        
        # Serve file with proper headers for download
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f"Error serving download file: {e}")
        return jsonify({'error': 'Failed to serve file'}), 500

@app.route('/api/video/serve/<filename>')
@rate_limit('video_download')
def serve_video_file(filename):
    """Serve downloaded video file directly by filename"""
    try:
        if not video_downloader:
            return jsonify({'error': 'Video downloader not available'}), 503
        
        # Security: Clean filename to prevent directory traversal
        import os
        filename = os.path.basename(filename)
        
        # Check if file exists in downloads directory
        filepath = os.path.join(video_downloader.download_dir, filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        # Serve the file with mobile-optimized headers for download
        from flask import Response
        import mimetypes
        
        # Get proper MIME type for better mobile compatibility
        mimetype, _ = mimetypes.guess_type(filename)
        if not mimetype:
            mimetype = 'application/octet-stream'
        
        response = send_file(
            filepath,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
        
        # Aggressive mobile-compatible headers for all browsers
        response.headers['Content-Disposition'] = f'attachment; filename=\"{filename}\"'
        response.headers['Content-Type'] = mimetype
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = '*'
        
        return response
        
    except Exception as e:
        logger.error(f"Error serving video file: {e}")
        return jsonify({'error': 'Failed to serve file'}), 500


if __name__ == '__main__':
    import os
    import sys
    
    # Robust server configuration to prevent loading screen issues
    port = int(os.environ.get('PORT', 5000))
    
    # Ensure Flask binding is stable
    try:
        print(f"🚀 Starting Remilio Meme Generator on 0.0.0.0:{port}")
        print("✅ Server ready - navigate to your app URL")
        
        # Use threaded=True for better stability and performance
        app.run(
            host='0.0.0.0', 
            port=port, 
            debug=False,
            threaded=True,
            use_reloader=False  # Prevents double loading issues
        )
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        print("🔧 Attempting fallback configuration...")
        try:
            # Fallback configuration
            app.run(host='0.0.0.0', port=5000, debug=False)
        except Exception as fallback_error:
            print(f"❌ Fallback also failed: {fallback_error}")
            sys.exit(1)
