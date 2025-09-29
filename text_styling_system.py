#!/usr/bin/env python3
"""
Text Styling System - Inspired by Remilia Generator

Implements text styling options including:
- Font selection (Impact, Glow, Angelic, Chinese)
- Text formatting (no caps lock option)
- Multiple text effects and styling
"""

import re
import random

class TextStylingSystem:
    """
    Advanced text styling system for meme generation
    """
    
    def __init__(self):
        """Initialize styling system"""
        self.font_styles = {
            'impact': {
                'name': 'Impact',
                'css_class': 'font-impact',
                'weight': 'bold',
                'transform': 'uppercase',
                'shadow': '2px 2px 0px #000000'
            },
            'glow': {
                'name': 'Glow',
                'css_class': 'font-glow',
                'weight': 'bold',
                'transform': 'uppercase',
                'shadow': '0px 0px 10px #ffffff, 0px 0px 20px #ffffff'
            },
            'angelic': {
                'name': 'Angelic',
                'css_class': 'font-angelic',
                'weight': 'normal',
                'transform': 'capitalize',
                'shadow': '0px 0px 15px #ffff00, 0px 0px 30px #ffff00'
            },
            'chinese': {
                'name': 'Chinese',
                'css_class': 'font-chinese',
                'weight': 'normal',
                'transform': 'none',
                'shadow': '1px 1px 2px #000000'
            }
        }
        
        self.text_effects = {
            'outline': 'text-stroke: 2px black;',
            'shadow': 'text-shadow: 2px 2px 4px rgba(0,0,0,0.8);',
            'glow_white': 'text-shadow: 0 0 10px white, 0 0 20px white;',
            'glow_yellow': 'text-shadow: 0 0 15px yellow, 0 0 30px yellow;',
            'emboss': 'text-shadow: 1px 1px 0px white, -1px -1px 0px black;'
        }
    
    def apply_no_caps_option(self, text, no_caps=False):
        """Apply no caps lock option to text"""
        if not text:
            return text
            
        if no_caps:
            # Convert from all caps to title case or mixed case
            if text.isupper():
                # Convert to title case with some randomness
                words = text.split()
                styled_words = []
                
                for word in words:
                    if len(word) > 3 and random.random() > 0.3:
                        # Title case for longer words
                        styled_words.append(word.title())
                    else:
                        # Keep some words lowercase for variety
                        styled_words.append(word.lower())
                
                return ' '.join(styled_words)
            else:
                return text
        else:
            # Default behavior - uppercase for impact
            return text.upper()
    
    def get_font_style_css(self, font_type='impact', custom_color='white'):
        """Get CSS styling for specified font type"""
        if font_type not in self.font_styles:
            font_type = 'impact'  # Default fallback
        
        style = self.font_styles[font_type]
        
        css = f"""
        .{style['css_class']} {{
            font-family: '{style['name']}', 'Arial Black', sans-serif;
            font-weight: {style['weight']};
            text-transform: {style['transform']};
            color: {custom_color};
            text-shadow: {style['shadow']};
            -webkit-text-stroke: 1px black;
        }}
        """
        
        return css
    
    def apply_text_styling(self, text, style_config):
        """Apply comprehensive text styling"""
        if not text:
            return text, 'impact'
        
        # Extract styling options
        font_type = style_config.get('font', 'impact')
        no_caps = style_config.get('no_caps', False)
        effect = style_config.get('effect', 'outline')
        
        # Apply no caps option
        styled_text = self.apply_no_caps_option(text, no_caps)
        
        # Apply special character transformations for Chinese style
        if font_type == 'chinese':
            styled_text = self.add_chinese_aesthetic(styled_text)
        
        # Apply angelic transformations
        elif font_type == 'angelic':
            styled_text = self.add_angelic_aesthetic(styled_text)
        
        return styled_text, font_type
    
    def add_chinese_aesthetic(self, text):
        """Add Chinese-inspired aesthetic elements"""
        # Add occasional unicode characters for aesthetic
        aesthetic_chars = ['✧', '◆', '◇', '※', '⟡']
        
        words = text.split()
        if len(words) > 1 and random.random() > 0.7:
            # Occasionally add aesthetic character
            insert_pos = random.randint(1, len(words))
            char = random.choice(aesthetic_chars)
            words.insert(insert_pos, char)
        
        return ' '.join(words)
    
    def add_angelic_aesthetic(self, text):
        """Add angelic-inspired aesthetic elements"""
        # Add angel-themed elements
        angelic_chars = ['✨', '☆', '✧', '◇', '⟡']
        
        if random.random() > 0.6:
            char = random.choice(angelic_chars)
            return f"{char} {text} {char}"
        
        return text
    
    def generate_style_options_html(self):
        """Generate HTML for style selection interface"""
        html = """
        <div class="text-styling-panel">
            <h3>Text Styling Options</h3>
            
            <div class="font-selection">
                <label>Font Style:</label>
                <select id="fontSelect" onchange="updateFontStyle()">
                    <option value="impact">Impact (Classic)</option>
                    <option value="glow">Glow (Glowing)</option>
                    <option value="angelic">Angelic (Divine)</option>
                    <option value="chinese">Chinese (Aesthetic)</option>
                </select>
            </div>
            
            <div class="text-options">
                <label>
                    <input type="checkbox" id="noCapsLock" onchange="updateTextStyle()">
                    No Caps Lock (Mixed Case)
                </label>
            </div>
            
            <div class="effect-selection">
                <label>Text Effect:</label>
                <select id="effectSelect" onchange="updateTextEffect()">
                    <option value="outline">Outline</option>
                    <option value="shadow">Drop Shadow</option>
                    <option value="glow_white">White Glow</option>
                    <option value="glow_yellow">Golden Glow</option>
                    <option value="emboss">Embossed</option>
                </select>
            </div>
        </div>
        """
        
        return html
    
    def get_all_font_styles_css(self):
        """Get CSS for all font styles"""
        css = ""
        for font_type in self.font_styles:
            css += self.get_font_style_css(font_type)
        
        # Add effect classes
        css += """
        .text-outline { -webkit-text-stroke: 2px black; }
        .text-shadow { text-shadow: 2px 2px 4px rgba(0,0,0,0.8); }
        .text-glow-white { text-shadow: 0 0 10px white, 0 0 20px white; }
        .text-glow-yellow { text-shadow: 0 0 15px yellow, 0 0 30px yellow; }
        .text-emboss { text-shadow: 1px 1px 0px white, -1px -1px 0px black; }
        """
        
        return css

def main():
    """Test the text styling system"""
    styling = TextStylingSystem()
    
    test_texts = [
        "WHEN YOU REALIZE",
        "BOTTOM TEXT ENERGY",
        "TRANSCENDENT WISDOM",
        "ANGELIC VIBES ONLY"
    ]
    
    style_configs = [
        {'font': 'impact', 'no_caps': False, 'effect': 'outline'},
        {'font': 'glow', 'no_caps': True, 'effect': 'glow_white'},
        {'font': 'angelic', 'no_caps': True, 'effect': 'glow_yellow'},
        {'font': 'chinese', 'no_caps': True, 'effect': 'shadow'}
    ]
    
    print("=== TEXT STYLING SYSTEM TEST ===")
    
    for i, text in enumerate(test_texts):
        config = style_configs[i % len(style_configs)]
        styled_text, font_type = styling.apply_text_styling(text, config)
        
        print(f"Original: {text}")
        print(f"Styled ({font_type}): {styled_text}")
        print(f"Config: {config}")
        print("-" * 40)
    
    print("\nCSS Classes:")
    print(styling.get_all_font_styles_css())

if __name__ == "__main__":
    main()