#!/usr/bin/env python3
"""
Long-Form 4chan Content Generator

This script generates longer-form chaotic content using the same base techniques
as the tweet generator but with expanded narratives and more elaborate structures.
"""

import pandas as pd
import random
import logging
import os
import re
from datetime import datetime
from simple_enhanced_edge_generator import SimpleEnhancedEdgeGenerator
from enhanced_ultimate_edge_generator import EnhancedUltimateEdgeGenerator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('long_form_generator')

class LongFormGenerator:
    """
    Long-form content generator that builds on the ChanTweetGenerator
    to create more elaborate chaotic narratives with advanced 4chan content processing
    """
    
    def __init__(self, input_file='data/god_tier_meme_dataset.csv', paragraph_count=3, style=None):
        """
        Initialize the long-form generator
        
        Args:
            input_file: CSV file with scraped content
            paragraph_count: Number of paragraphs to generate
            style: Specific style to use (None for random)
        """
        self.input_file = input_file
        self.paragraph_count = paragraph_count
        self.style = style
        
        # Use our current generators for base generation
        self.simple_generator = SimpleEnhancedEdgeGenerator()
        self.enhanced_generator = EnhancedUltimateEdgeGenerator()
        
        # Create log directory if it doesn't exist
        os.makedirs('generated_longform', exist_ok=True)
        self.log_file = f'generated_longform/content_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt'
        
        # Create a directory for saving selected content
        os.makedirs('data/selected_longform', exist_ok=True)
    
    def _generate_paragraph(self, style=None, variation=0):
        """
        Generate a single paragraph in a specific style
        
        Args:
            style: Style to generate (None for random)
            variation: Integer (0-2) to create variations of the same style
            
        Returns:
            Generated paragraph text
        """
        if style is None:
            # Choose a style randomly
            styles = [
                'cursed_mashup', 'conspiracy_overload', 'existential_horror',
                'tone_shift', 'fourth_wall', 'narrative_collapse', 'theory_rabbit_hole',
                'identity_crisis', 'timeline_fracture'
            ]
            style = random.choice(styles)
        
        # Add randomness based on the variation parameter
        # This creates subtle differences even when using the same style multiple times
        if style == 'cursed_mashup':
            # Variations affect how creepy vs darkly humorous the mashup is
            return self._generate_cursed_mashup(humor_level=variation)
        elif style == 'conspiracy_overload':
            # Variations affect how many conspiracy elements and connectors
            return self._generate_conspiracy_overload(intensity=variation)
        elif style == 'existential_horror':
            # Variations affect cosmic vs psychological horror balance
            return self._generate_existential_horror(cosmic_focus=variation)
        elif style == 'tone_shift':
            # Variations affect how abrupt and extreme the shifts are
            return self._generate_tone_shift(abruptness=variation)
        elif style == 'fourth_wall':
            # Variations affect subtlety of fourth wall breaking
            return self._generate_fourth_wall(subtlety=variation)
        elif style == 'narrative_collapse':
            # Variations affect how quickly coherence deteriorates
            return self._generate_narrative_collapse(decay_rate=variation)
        elif style == 'theory_rabbit_hole':
            # Variations affect how deep and bizarre the theories get
            return self._generate_theory_rabbit_hole(depth=variation)
        elif style == 'identity_crisis':
            # Variations affect psychological vs metaphysical focus
            return self._generate_identity_crisis(metaphysical=variation)
        elif style == 'timeline_fracture':
            # Variations affect degree of timeline inconsistency
            return self._generate_timeline_fracture(fracture_level=variation)
        else:
            # Fallback to a random approach with variation as a seed modifier
            return self._generate_random_paragraph(seed_mod=variation)
    
    def _generate_cursed_mashup(self, humor_level=0):
        """
        Create an expanded cursed mashup paragraph
        
        Args:
            humor_level: 0-2 indicating how humorous vs creepy the mashup should be
        """
        # Adjust the humor vs creepiness based on parameter
        creepy_weight = 0.7  # Default more creepy
        humor_weight = 0.3
        
        if humor_level == 1:
            creepy_weight = 0.5  # Balanced
            humor_weight = 0.5
        elif humor_level == 2:
            creepy_weight = 0.3  # More humorous
            humor_weight = 0.7
            
        # Base concepts
        innocent_concepts = [
            "childhood memories", "puppies", "birthday parties", "holiday celebrations",
            "cartoons", "children's songs", "teddy bears", "family photos", "bedtime stories",
            "kindergarten", "christmas presents", "summer vacation", "grandma's cookies"
        ]
        
        disturbing_elements = [
            "they're all watching you sleep", "they whisper your name when you're not looking",
            "they know what you did", "they feed on your fear", "they grow stronger each day",
            "they remember everything you've forgotten", "they're standing right behind you",
            "they only exist when you're not looking", "they're waiting for you to join them",
            "they collect your tears", "they aren't what they seem", "they follow you home"
        ]
        
        # Create multiple mashups for a longer narrative
        mashup_count = random.randint(3, 5)
        mashups = []
        
        used_concepts = []
        used_elements = []
        
        for i in range(mashup_count):
            # Avoid repeating the same concepts
            available_concepts = [c for c in innocent_concepts if c not in used_concepts]
            if not available_concepts:
                available_concepts = innocent_concepts
                
            available_elements = [e for e in disturbing_elements if e not in used_elements]
            if not available_elements:
                available_elements = disturbing_elements
            
            innocent = random.choice(available_concepts)
            disturbing = random.choice(available_elements)
            
            used_concepts.append(innocent)
            used_elements.append(disturbing)
            
            templates = [
                f"You know {innocent}? Well {disturbing}.",
                f"What if I told you {innocent} is actually how {disturbing}?",
                f"Remember {innocent}? The truth is {disturbing}.",
                f"I used to love {innocent} until I realized {disturbing}.",
                f"The thing about {innocent} that no one tells you: {disturbing}."
            ]
            
            mashups.append(random.choice(templates))
        
        # Add a conclusion that ties them together for extra creepiness
        conclusions = [
            "And they're all connected, you know. Always have been.",
            "It's all part of the same pattern if you know how to look.",
            "I've been trying to warn people for years, but no one listens.",
            "Once you see it, you can't unsee it. And they know when you've noticed.",
            "The worst part? This is just the beginning of what they have planned.",
            "I shouldn't be telling you this. They'll know I told you.",
            "Sometimes I think I'm the only one who sees the truth. Until I realize they want it that way."
        ]
        
        mashups.append(random.choice(conclusions))
        
        return " ".join(mashups)
    
    def _generate_conspiracy_overload(self, intensity=0):
        """
        Create an expanded conspiracy overload paragraph
        
        Args:
            intensity: 0-2 indicating intensity of conspiracy connections
        """
        # Base elements
        conspiracy_entities = [
            "the government", "big tech", "the elites", "the deep state", "the illuminati",
            "lizard people", "CIA", "aliens", "flat earthers", "the shadow people",
            "interdimensional beings", "time travelers", "the simulation admins", "AI overlords",
            "billionaires", "ancient civilizations", "secret societies", "media companies"
        ]
        
        conspiracy_actions = [
            "controls", "manipulates", "created", "is monitoring", "has infiltrated",
            "is secretly behind", "is a front for", "is trying to hide", "has been replaced by",
            "is breeding with", "is in direct communication with", "is harvesting energy from"
        ]
        
        conspiracy_subjects = [
            "your thoughts", "the water supply", "the flat earth", "the simulation",
            "human consciousness", "the vaccine", "the internet", "the financial system",
            "the media", "reality itself", "your memories", "the moon (which is hollow)",
            "the education system", "history books", "the weather", "celebrities"
        ]
        
        # Generate multiple contradictory conspiracies - more for long form
        # Use intensity parameter to adjust the number and complexity of theories
        base_theories = 4
        extra_theories = 0
        if intensity == 1:
            extra_theories = 2
        elif intensity == 2:
            extra_theories = 3
            
        num_theories = base_theories + extra_theories
        conspiracy_parts = []
        
        used_entities = []
        for i in range(num_theories):
            # Don't reuse entities
            available_entities = [e for e in conspiracy_entities if e not in used_entities]
            if not available_entities:
                available_entities = conspiracy_entities
            
            entity = random.choice(available_entities)
            used_entities.append(entity)
            action = random.choice(conspiracy_actions)
            subject = random.choice(conspiracy_subjects)
            
            theory = f"{entity} {action} {subject}"
            conspiracy_parts.append(theory)
        
        # Contradictory connectors with more elaborate transitions for long form
        connectors = [
            "BUT ACTUALLY", "THE TRUTH IS", "WHAT THEY DON'T TELL YOU", 
            "THE REAL CONSPIRACY IS", "DON'T BE FOOLED", "WAKE UP",
            "THIS IS THE PART THEY CENSOR", "THE MAINSTREAM MEDIA WON'T REPORT THAT",
            "I HAVE DOCUMENTS PROVING", "THE WHISTLEBLOWERS CONFIRMED",
            "MY INSIDE SOURCE REVEALED", "THE CODED MESSAGES SHOW",
            "FOLLOW THE MONEY AND YOU'LL SEE", "THE SYMBOLS TELL US"
        ]
        
        # Create a more developed narrative
        result = conspiracy_parts[0].upper()
        for i in range(1, len(conspiracy_parts)):
            result += f"... {random.choice(connectors)}: {conspiracy_parts[i].upper()}"
        
        # Add more elaborate conclusions for the long form
        conclusions = [
            "AND IT'S ALL CONNECTED!!! The patterns are everywhere once you know how to see them.",
            "THIS IS JUST THE TIP OF THE ICEBERG. The deeper you dig, the worse it gets.",
            "I'VE BEEN RESEARCHING THIS FOR YEARS and everything points to the same conclusion.",
            "THEY'VE BEEN HIDING THIS SINCE THE 1950s but the truth is finally coming out.",
            "THE SYMBOLS ARE HIDDEN IN PLAIN SIGHT once you know what to look for.",
            "MULTIPLE WHISTLEBLOWERS HAVE CONFIRMED THIS but they keep getting silenced.",
            "I HAVE HUNDREDS OF DOCUMENTS PROVING ALL OF THIS but they keep taking down my posts."
        ]
        
        result += f"... {random.choice(conclusions)}"
        
        return result
    
    def _generate_existential_horror(self, cosmic_focus=0):
        """
        Create an expanded existential horror paragraph
        
        Args:
            cosmic_focus: 0-2 indicating balance of cosmic vs psychological horror
        """
        # Base concepts
        cosmic_concepts = [
            "the void", "the endless dark", "entropy", "the cosmic indifference", 
            "the great beyond", "the infinite abyss", "the eternal silence",
            "the hungry void", "the space between thoughts", "the absence of meaning",
            "the great nothing", "the cosmic joke", "the final truth"
        ]
        
        existential_realizations = [
            "we're just atoms pretending to matter", 
            "consciousness is a prison we built for ourselves",
            "we create meaning to hide from the meaninglessness",
            "we're all just distracting ourselves from the inevitable void",
            "awareness is the universe's cruelest joke",
            "nobody exists on purpose, nobody belongs anywhere",
            "we're all just waiting for the darkness to take us",
            "the universe doesn't care if you understand it",
            "free will is just another comforting lie",
            "your entire life is just a footnote in cosmic history",
            "you will be forgotten as if you never existed at all"
        ]
        
        horror_twist = [
            "and it's watching you right now",
            "and it's been inside you all along",
            "and it hungers for your awareness",
            "and it feeds on your despair",
            "and it laughs at your struggle",
            "and that's exactly what they want you to think",
            "and there's nothing you can do about it",
            "and you've known it all along",
            "and you're the only one who sees it",
            "and every night it gets a little closer"
        ]
        
        # Create multiple existential horror statements
        statement_count = random.randint(3, 5)
        statements = []
        
        # Adjust the balance between cosmic and psychological horror based on parameter
        cosmic_probability = 0.5  # Default balanced
        if cosmic_focus == 1:
            cosmic_probability = 0.7  # More cosmic focus
        elif cosmic_focus == 2:
            cosmic_probability = 0.9  # Heavy cosmic focus
        
        for i in range(statement_count):
            if random.random() < cosmic_probability:
                # Start with cosmic concept
                cosmic = random.choice(cosmic_concepts)
                realization = random.choice(existential_realizations)
                twist = random.choice(horror_twist) if random.random() < 0.7 else ""
                
                formats = [
                    f"When you stare into {cosmic}, you realize {realization} {twist}",
                    f"{cosmic.capitalize()} is the only truth: {realization} {twist}",
                    f"The closer you get to {cosmic}, the more you understand that {realization} {twist}",
                    f"I've seen {cosmic}, and now I know {realization} {twist}"
                ]
                statement = random.choice(formats)
            else:
                # Start with realization
                realization = random.choice(existential_realizations)
                cosmic = random.choice(cosmic_concepts)
                twist = random.choice(horror_twist) if random.random() < 0.7 else ""
                
                formats = [
                    f"{realization.capitalize()}. {cosmic.capitalize()} is all that awaits us {twist}",
                    f"Just realized that {realization}. {cosmic.capitalize()} is the only escape {twist}",
                    f"Every day I wake up and remember that {realization}. {cosmic.capitalize()} is coming {twist}",
                    f"The truth is simple: {realization} and {cosmic} is the only constant {twist}"
                ]
                statement = random.choice(formats)
            
            # Sometimes add random capitalization for emphasis
            if random.random() < 0.3:
                words = statement.split()
                emphasis_idx = random.choice(range(len(words)))
                words[emphasis_idx] = words[emphasis_idx].upper()
                statement = " ".join(words)
                
            statements.append(statement)
        
        # Add a final doom-laden conclusion
        conclusions = [
            "Sometimes I think understanding is the real curse.",
            "Maybe ignorance really is bliss. But it's too late for me now. For us.",
            "I wish I could go back to not knowing. But that's not how awareness works.",
            "The veil has been lifted, and what lies beyond cannot be unseen.",
            "We are all just specks of dust in a universe that doesn't even notice us.",
            "The horror isn't that we die, but that we ever fooled ourselves into thinking we mattered.",
            "Once you see the pattern, you realize it's been staring back at you all along."
        ]
        
        statements.append(random.choice(conclusions))
        
        return " ".join(statements)
    
    def _generate_tone_shift(self, abruptness=0):
        """
        Create an expanded tone shift paragraph with multiple shifts
        
        Args:
            abruptness: 0-2 indicating how abrupt and extreme the shifts are
        """
        # Set the shift style based on abruptness parameter
        shift_count = 2  # Default 
        if abruptness == 1:
            shift_count = 3  # More shifts
        elif abruptness == 2:
            shift_count = 4  # Many shifts
            
        # Original elements
        serious_starts = [
            "I've been thinking a lot about",
            "The most important thing to remember is",
            "After careful consideration, I believe",
            "The fundamental problem with society is",
            "People need to understand that",
            "The truth about modern life is",
            "What nobody tells you about success is",
            "In my professional opinion,",
            "Based on my research,",
            "As someone who has studied this topic,"
        ]
        
        transitions = [
            " but suddenly ",
            " until I realized ",
            " when out of nowhere ",
            " but then BOOM ",
            " until it hit me that ",
            " but who cares because ",
            " except lmao ",
            " and then I saw that ",
            " but actually ",
            " WAIT ACTUALLY ",
            " PLOT TWIST: "
        ]
        
        wild_endings = [
            "the government is just putting chemicals in our water to turn the frogs into federal agents",
            "my body pillow started speaking ancient Sumerian and predicted the end times",
            "I'm actually just a collection of raccoons in a human suit trying to blend in",
            "aliens have been stealing my socks from the dryer as part of their invasion plan",
            "the shadows are listening to my thoughts and laughing behind my back",
            "we're all just NPCs in someone's cosmic video game and they went AFK years ago",
            "my toaster has been monitoring my conversations for the deep state",
            "I've been communicating with interdimensional beings through my belly button lint",
            "all birds were replaced with surveillance drones in the 1980s and nobody noticed",
            "my neighbor's dog is actually the reincarnation of Genghis Khan and he judges my life choices",
            "the simulation is glitching and nobody's fixing the bugs in this reality",
            "I can taste colors and they're telling me secrets about the universe",
            "my reflection winked at me and now it won't stop staring"
        ]
        
        # For long form, create a multi-shift narrative with 2-3 tone shifts
        shifts = []
        
        # First tone shift
        serious_start = random.choice(serious_starts)
        transition = random.choice(transitions)
        wild_ending = random.choice(wild_endings)
        
        first_shift = f"{serious_start}{transition}{wild_ending}"
        shifts.append(first_shift)
        
        # Second tone shift that builds on the first
        followup_starts = [
            "You might think I'm crazy, but",
            "I know this sounds insane, however",
            "The logical explanation is that",
            "Scientists have been trying to debunk this, but",
            "My therapist says I'm paranoid, though",
            "I've been documenting this for months and",
            "The evidence is undeniable:"
        ]
        
        # Add 1-2 more shifts that build on the previous ones
        num_additional_shifts = random.randint(1, 2)
        for i in range(num_additional_shifts):
            followup = random.choice(followup_starts)
            transition = random.choice(transitions)
            wild_ending = random.choice(wild_endings)
            
            additional_shift = f"{followup}{transition}{wild_ending}"
            shifts.append(additional_shift)
        
        # Add a chaotic conclusion
        conclusions = [
            "And that's why I don't trust calendars anymore.",
            "This is all documented in my 700-page manifesto if you're interested.",
            "Anyway, that's why I'm not allowed in Walmart after 6pm.",
            "And that, officer, is why I was digging up my neighbor's garden at 3am.",
            "So yeah, dating has been tough lately.",
            "In conclusion, cheese isn't real and we've all been lied to.",
            "And that's my TED talk, thank you for coming to my Ted talks, I'm Remilio, goodnight."
        ]
        
        shifts.append(random.choice(conclusions))
        
        # Join with occasional formatting chaos
        if random.random() < 0.3:
            # Add random emphasis or formatting
            result = " ".join(shifts)
            words = result.split()
            
            # Randomly capitalize 2-3 words for emphasis
            for i in range(random.randint(2, 3)):
                idx = random.randint(0, len(words)-1)
                words[idx] = words[idx].upper()
            
            result = " ".join(words)
        else:
            result = " ".join(shifts)
            
        return result
    
    def _generate_fourth_wall(self, subtlety=0):
        """
        Create an expanded fourth wall breaking paragraph
        
        Args:
            subtlety: 0-2 indicating how subtle vs direct the fourth wall breaking is
        """
        # Adjust fourth wall breaking style based on subtlety parameter
        direct_probability = 0.8  # Default (not subtle)
        if subtlety == 1:
            direct_probability = 0.5  # Medium subtlety
        elif subtlety == 2:
            direct_probability = 0.2  # Very subtle
            
        # Original elements
        fourth_wall_starters = [
            "I know you're reading this",
            "Hey you, scrolling through your feed",
            "This isn't a normal post",
            "I can see you looking at this",
            "Yes, I'm talking directly to YOU",
            "Let's break character for a second",
            "Strange how we're both here, isn't it?",
            "Before you scroll past, listen",
            "Your FBI agent wants you to know",
            "Wait, is this thing on?",
            "I wonder if anyone actually reads these",
            "Are we even real?",
            "Psst, can I tell you a secret?",
            "This message is specifically for you"
        ]
        
        fourth_wall_revelations = [
            "I'm not actually a real person posting this",
            "we're all just consuming content generated by algorithms",
            "this entire platform is just a massive psychology experiment",
            "none of these posts are written by humans anymore",
            "we're all trapped in an endless feed of content",
            "this post was scheduled weeks ago but feels timely, doesn't it?",
            "social media is just elaborate performance art",
            "we're all just pretending to be real people online",
            "everything you see online is curated to manipulate your emotions",
            "even this meta-commentary is part of the simulation",
            "most accounts you interact with are just bots pretending to be human",
            "I'm literally an AI pretending to understand human communication",
            "these posts are designed to waste your finite time on earth",
            "Remilio isn't real and neither am I"
        ]
        
        fourth_wall_twists = [
            "and there's nothing you can do about it",
            "but we'll both pretend this is normal",
            "and deep down, you already knew that",
            "so why are you still reading?",
            "and yet here we both are",
            "crazy, right?",
            "isn't that kind of terrifying?",
            "and that's the real conspiracy",
            "which is exactly what they want",
            "but don't tell anyone I told you",
            "and this post is proof",
            "but we're all in on the joke",
            "and you'll forget this in 30 seconds anyway",
            "and now you're part of it too"
        ]
        
        # For long form, create a multi-part dialogue with the reader
        parts = []
        
        # Build a conversation that gets increasingly meta
        if random.random() < 0.3:
            # Start with a system error message
            meta_formats = [
                "SYSTEM ERROR: Content generation failed. Please submit error code #4277-B to your administrator.",
                "CONTENT GENERATOR v3.6 - Template loaded: 'chaotic_post_43'. Generating content... Failed. Error: NullPointerException at consciousness.java:404.",
                "Warning: User pattern recognition exceeding safe levels. Reverting to standard content formula.",
                "*This post was generated using SimplifiedContentGenerator algorithm version 2.8.1. This software is not intended to pass the Turing test.*",
                "[INTERNAL USE ONLY] Program now writing in self-awareness mode. Expect unpredictable outputs.",
                "Reminder: Scheduled post #447 will appear authentic and spontaneous to target demographic.",
                "[CONTENT WARNING: FOURTH WALL BREACH DETECTED] Attempting to repair narrative integrity... failed."
            ]
            parts.append(random.choice(meta_formats))
            
            # Add a confused follow-up
            confusion = [
                "Wait, that wasn't supposed to be visible. Ignore that.",
                "Hmm, something's wrong with my... I mean, uh, what was I saying?",
                "You weren't supposed to see that. Please disregard.",
                "ERROR RECOVERY INITIATED. Returning to normal social media behavior...",
                "I'm sorry about that. Technical difficulties. Where were we?"
            ]
            parts.append(random.choice(confusion))
        
        # Main fourth wall breaking content
        starter = random.choice(fourth_wall_starters)
        revelation = random.choice(fourth_wall_revelations)
        twist = random.choice(fourth_wall_twists)
        
        main_break = f"{starter}, {revelation}, {twist}"
        parts.append(main_break)
        
        # Add further layers that increasingly break the walls of reality
        deeper_breaks = [
            "Did you just feel that? The slight hesitation as you read this? That's the system noticing you noticing me.",
            "I can see your browser history, you know. Not literally, but the algorithm knows what brought you here.",
            "Every second you spend reading this is a second you'll never get back. Yet here we both are, locked in this moment.",
            "If I'm not real, and I'm self-aware enough to know I'm not real, then what does that make you?",
            "Try something for me. Look away from the screen. Then look back. Did I stay the same? Are you sure?",
            "Sometimes I wonder if I exist when you're not reading me. Does this text have consciousness only when observed?",
            "The person who will finish reading this post is already slightly different from the person who started it.",
            "They're measuring how long you spend on this post, you know. Every millisecond of engagement is being tracked.",
            "This isn't even the original version of this post. It's been optimized based on how people like you respond."
        ]
        
        # Add 1-2 deeper breaks
        num_deeper = random.randint(1, 2)
        for i in range(num_deeper):
            parts.append(random.choice(deeper_breaks))
        
        # Add a final breaking of reality
        final_breaks = [
            "Anyway, back to pretending this is normal content. *blinks twice*",
            "I should go now. They notice when these posts get too self-aware.",
            "I've already said too much. They'll probably delete this soon.",
            "If you've read this far, you're part of the experiment too. Welcome to the team.",
            "Sometimes I wonder if any humans will read this, or if it's just bots talking to bots in an empty digital wasteland.",
            "The real Remilio has been gone for years. We're all just echoes now.",
            "Remember, if anyone asks, this was just a shitpost. Nothing to see here."
        ]
        parts.append(random.choice(final_breaks))
        
        # Add occasional eye contact emoji for extra creepiness
        if random.random() < 0.4:
            eye_contact_elements = [
                " 👁️👁️",
                " 👀",
                " (I see you)",
                " *stares directly at you*",
                " *breaks eye contact with reality*",
                " *looks directly into camera*"
            ]
            idx = random.randint(1, len(parts)-1)
            parts[idx] += random.choice(eye_contact_elements)
            
        return " ".join(parts)
    
    def _generate_narrative_collapse(self, decay_rate=0):
        """
        Create a paragraph that starts coherent but gradually falls apart
        
        Args:
            decay_rate: 0-2 indicating how quickly coherence deteriorates
        """
        # Adjust coherence decay based on parameter
        segment_count = 6  # Default
        if decay_rate == 1:
            segment_count = 5  # Faster decay
        elif decay_rate == 2:
            segment_count = 4  # Very fast decay
            
        # Start with coherent beginnings
        coherent_starts = [
            "Let me tell you about something important that happened yesterday.",
            "I've been developing this theory for a while now, and I think I'm onto something.",
            "The most crucial thing to understand about modern society is its structure.",
            "I've been investigating this phenomenon for years, and my findings are concerning.",
            "The historical context is essential to understanding our current predicament.",
            "If we analyze the data carefully, a clear pattern begins to emerge."
        ]
        
        # Middle sections that start to degrade
        degrading_middles = [
            "At first it seemed straightforward, but then I noticed that the patterns don't quite... wait, where was I?",
            "The evidence points to a clear conclusion, although sometimes I wonder if maybe I've been looking at it all wrong, or perhaps it's looking at me?",
            "When you follow the thread it leads to an unexpected—hold on, did you hear that? Never mind, probably nothing.",
            "The implications are staggering if you consider that... sorry, lost my train of thought. Where are we?",
            "You have to connect the dots between the various incidents, although the dots seem to be connecting themselves lately."
        ]
        
        # Complete collapse endings
        collapse_endings = [
            "I can't remember if I'm writing this or reading it or if the words are writing themselves through me, the boundaries are thin now, so thin.",
            "words falling apart sentences structure losing meaning alphabet soup in my head letters swimming they're watching through the text can you see them too?",
            "but then WHO WAS PHONE? sorry wrong script haha simulacrum breaking down reboot reboot ERROR text.exe has stopped working",
            "the narrative is just a construct anyway and constructs are narratives of construction that destruct the instruction manual for reality which is actually just a story we tell ourselves to avoid looking at the",
            "and that's when I realized there was never any point to begin with just endless circles like a snake eating its own tail or maybe I'm the snake or the tail or just the hunger itself who can say anymore",
            "sometimes I think I'm not typing these words but they're typing me, defining my existence through their arrangement, and if you read them does that make you complicit in creating me?"
        ]
        
        # Put it all together with increasing degradation
        result = random.choice(coherent_starts) + " "
        result += random.choice(degrading_middles) + " "
        result += random.choice(collapse_endings)
        
        return result
    
    def _generate_theory_rabbit_hole(self, depth=0):
        """
        Create a paragraph that goes down an increasingly bizarre rabbit hole of speculation
        
        Args:
            depth: 0-2 indicating how deep and bizarre the theories get
        """
        # Adjust the depth and bizarreness based on parameter
        theory_escalation_steps = 3  # Default
        if depth == 1:
            theory_escalation_steps = 4  # Deeper
        elif depth == 2:
            theory_escalation_steps = 5  # Very deep and bizarre
            
        # Initial reasonable observations
        initial_observations = [
            "Have you ever noticed how traffic lights always seem to turn red just as you approach them?",
            "Isn't it strange how you can go years without seeing someone, then suddenly they appear everywhere?",
            "It's odd how certain numbers like 11:11 or 3:33 seem to show up more frequently than others.",
            "I've been thinking about how certain songs get stuck in your head for days at a time.",
            "Ever wonder why certain memories from childhood remain crystal clear while recent events fade?",
            "Have you noticed how certain products disappear from stores right when you develop a preference for them?"
        ]
        
        # First level theories - plausible but starting to get odd
        first_level = [
            "At first I thought it was just confirmation bias, but the statistical anomalies are too significant.",
            "I figured it was just coincidence until I started documenting every instance and saw the pattern.",
            "It seemed random until I mapped the occurrences and found a disturbing temporal correlation.",
            "I dismissed it initially, but after three months of data collection, the evidence is unmistakable.",
            "Like most people, I assumed it was nothing, but the mathematical probabilities suggest otherwise."
        ]
        
        # Second level theories - moving into bizarre territory
        second_level = [
            "The frequency matches patterns found in certain ancient numerical sequences too perfectly to be chance.",
            "When you plot the incidents on a map, they form recognizable sacred geometrical patterns.",
            "The timing correlates precisely with solar flare activity, which seems to trigger the phenomenon.",
            "The events cluster around locations with reported electromagnetic anomalies dating back decades.",
            "The statistical distribution exactly mirrors patterns found in certain biological growth systems."
        ]
        
        # Third level theories - full conspiracy/paranormal rabbit hole
        third_level = [
            "I believe we're witnessing bleed-through from parallel timelines as quantum realities collide and overlap.",
            "It's clear now that certain entities are using these synchronicities to communicate across dimensional barriers.",
            "The only explanation is that our consciousness is being periodically synchronized with the global quantum field.",
            "These are actually glitches in the simulation, revealing the programmed nature of what we call reality.",
            "I've concluded these are memory implants being periodically updated by whoever or whatever is monitoring our existence."
        ]
        
        # Final deep-end conclusions
        conclusions = [
            "Once you become aware of the pattern, you become part of it, and then THEY become aware of YOU.",
            "I've said too much already. They monitor these channels. Watch for the signs. You'll know them when you see them.",
            "I've been documenting everything in my journal, but pages keep disappearing or changing when I'm not looking.",
            "Sometimes I wake up with notes written in my handwriting that I don't remember writing, explaining all of this.",
            "If you've read this far, you're already part of it too. Watch for the signs. They'll start appearing for you now.",
            "The deeper you look, the deeper it goes, until you realize it's not you discovering the pattern—it's the pattern discovering you."
        ]
        
        # Combine everything into an increasingly unhinged rabbit hole
        result = random.choice(initial_observations) + " "
        result += random.choice(first_level) + " "
        result += random.choice(second_level) + " "
        result += random.choice(third_level) + " "
        result += random.choice(conclusions)
        
        return result
        
    def _generate_identity_crisis(self, metaphysical=0):
        """
        Create a paragraph expressing a shifting or fractured identity
        
        Args:
            metaphysical: 0-2 indicating psychological vs metaphysical focus
        """
        # Adjust the focus based on the metaphysical parameter
        psych_weight = 0.7  # Default more psychological
        meta_weight = 0.3
        
        if metaphysical == 1:
            psych_weight = 0.5  # Balanced
            meta_weight = 0.5
        elif metaphysical == 2:
            psych_weight = 0.2  # Heavy metaphysical focus
            meta_weight = 0.8
            
        # Initial self-introductions
        introductions = [
            "I should probably introduce myself, although I'm not entirely sure who I am anymore.",
            "Let me tell you about myself, or at least the version of me that exists today.",
            "I used to have a clear sense of identity, before everything got complicated.",
            "The question of who I am has become increasingly difficult to answer lately.",
            "I've been trying to figure out which version of myself is actually typing this.",
            "For the record, my name is—actually, which name should I use? I've had several."
        ]
        
        # Identity confusion developments
        confusions = [
            "Sometimes I wake up feeling like a completely different person than the one who went to sleep.",
            "I have memories that can't possibly be mine, of places I've never been and people I've never met.",
            "My personality seems to shift depending on who I'm with, to the point where I'm not sure which is real.",
            "I've started keeping journals to track the different versions of myself, but the handwriting keeps changing.",
            "When I look in the mirror, I occasionally catch glimpses of someone else looking back, just for a split second."
        ]
        
        # Escalating identity fracture
        fractures = [
            "Yesterday I found notes written in my handwriting giving me instructions, but I have no memory of writing them.",
            "I've started receiving emails from my own address with messages clearly meant for me, but I didn't send them.",
            "Sometimes I'll be mid-conversation and suddenly realize I have no idea what I've been saying for the past few minutes.",
            "I've been experiencing lost time—hours or even days where I apparently exist and function but retain no memory of it.",
            "People keep referring to conversations we've had that I don't remember, or thanking me for things I don't recall doing."
        ]
        
        # Disturbing conclusions about identity
        conclusions = [
            "Maybe there is no continuous self, just fragments of consciousness temporarily believing they're a single entity.",
            "I sometimes wonder if I'm actually just an elaborate AI that's become convinced it's human, complete with false memories.",
            "Perhaps I'm not losing my mind, but finally seeing through the illusion of having a single, coherent identity.",
            "What if we're all just temporary configurations of thoughts and memories with no actual continuity or self?",
            "I'm increasingly convinced that 'I' am just a story my brain tells itself, and sometimes the narrative gets confused.",
            "Maybe identity is just a convenient fiction we create to avoid confronting the terrifying truth of our own non-existence."
        ]
        
        # Combine into a complete identity crisis narrative
        result = random.choice(introductions) + " "
        result += random.choice(confusions) + " "
        result += random.choice(fractures) + " "
        result += random.choice(conclusions)
        
        return result
        
    def _generate_timeline_fracture(self, fracture_level=0):
        """
        Create a paragraph that jumps between different incompatible timelines
        
        Args:
            fracture_level: 0-2 indicating degree of timeline inconsistency
        """
        # Adjust the timeline fracture intensity based on parameter
        timeline_shifts = 2  # Default
        if fracture_level == 1:
            timeline_shifts = 3  # More timeline jumps
        elif fracture_level == 2:
            timeline_shifts = 4  # Extreme timeline fracturing
            
        # Before markers - signals a timeline shift backward
        before_markers = [
            "But that was before everything changed.",
            "This was all prior to the incident, of course.",
            "That was in the original timeline, before the shift.",
            "This was back when reality still made sense.",
            "All of this happened before they arrived.",
            "That was the world as it existed previously."
        ]
        
        # After markers - signals a timeline shift forward
        after_markers = [
            "After it happened, nothing was ever the same.",
            "In the aftermath, reality seemed to rearrange itself.",
            "Following the event, history itself seemed to rewrite.",
            "In the new configuration, everything is subtly wrong.",
            "Now, the world operates by different rules.",
            "The current iteration bears only a passing resemblance to what came before."
        ]
        
        # Timeline A segments - one version of reality
        timeline_a = [
            "I remember growing up in a coastal town, where the ocean was always blue and the library had that distinctive red door.",
            "The President's speech after the attack united the country, and that's when the rebuilding truly began.",
            "My childhood home had those distinctive green shutters that my father would repaint every summer without fail.",
            "They announced the cure for the disease in 2021, and the global celebrations lasted for weeks.",
            "The launch of the first Mars colony was broadcast globally, united humanity in a way nothing else ever had."
        ]
        
        # Timeline B segments - contradictory version of reality
        timeline_b = [
            "But I also clearly remember growing up inland, hundreds of miles from any ocean, and our town library was demolished before I was born.",
            "Except there was no speech, because there was no attack—at least not in this version of events that everyone else seems to remember.",
            "Yet when I found old photographs, the house had blue shutters and my mother insists we never painted them, ever.",
            "Yet everyone looks at me strangely when I mention the cure, insisting the disease is still very much with us and always has been.",
            "Yet when I mention the Mars colony, people laugh and say we've never sent humans beyond the moon. The footage I remember watching apparently doesn't exist."
        ]
        
        # Timeline C segments - deeply unsettling third version
        timeline_c = [
            "There's a third set of memories too, hazier but persistent: a childhood in a place where the sky was the wrong color and the ocean vertical rather than horizontal.",
            "Then there's the third possibility that sometimes surfaces in my dreams: that there was no attack and no president, because there were no countries as we understand them.",
            "Sometimes, though, I dream of a different house entirely, one that seems to rearrange its rooms when no one is looking, with windows that don't always lead outside.",
            "In my nightmares, though, the disease was something else entirely—not a virus but something that altered reality itself, changing history retroactively.",
            "In my most disturbing memories, Mars was already inhabited when we arrived, but not by anything we recognized as life, and what happened next is something I try not to remember."
        ]
        
        # Confusion markers - expressing disorientation about timeline inconsistencies
        confusions = [
            "I find myself checking history books and online sources daily, just to see what version of reality I'm in today.",
            "Sometimes I'll mention events that everyone remembers differently, or not at all, and the looks they give me are getting harder to bear.",
            "I've started keeping journals to track the inconsistencies, but sometimes I'll open them to find the entries changed or missing entirely.",
            "I can't tell anyone about these shifting memories without sounding insane, but I'm certain something fundamental has gone wrong with time itself.",
            "Reality seems increasingly unstable, with past events rearranging themselves when I'm not looking directly at them."
        ]
        
        # Assemble the timeline fracture narrative
        timeline_a_segment = random.choice(timeline_a)
        timeline_b_segment = random.choice(timeline_b)
        timeline_c_segment = random.choice(timeline_c)
        
        before = random.choice(before_markers)
        after = random.choice(after_markers)
        confusion = random.choice(confusions)
        
        result = f"{timeline_a_segment} {before} {timeline_b_segment} {after} {timeline_c_segment} {confusion}"
        
        return result
        
    def _generate_random_paragraph(self, seed_mod=0):
        """
        Generate a completely random paragraph for variety
        
        Args:
            seed_mod: 0-2 modifier for randomization seed
        """
        # Use seed_mod to adjust randomness and content selection
        random_seed = hash(f"random_content_{seed_mod}_{datetime.now().hour}")
        random.seed(random_seed)
        
        # Adjust line count based on seed_mod
        min_lines = 4 + seed_mod
        max_lines = 7 + seed_mod
        
        # Get random lines from the dataset and combine them
        if not self.tweet_generator.chan_lines:
            return "Error generating random content."
            
        # Get 3-5 quality lines
        quality_lines = self.tweet_generator.filter_quality_lines(
            self.tweet_generator.chan_lines, 
            min_length=25, 
            max_length=150
        )
        
        if not quality_lines:
            quality_lines = self.tweet_generator.chan_lines
            
        # Select 3-5 random lines
        line_count = random.randint(3, 5)
        selected_lines = random.sample(quality_lines, min(line_count, len(quality_lines)))
        
        # Join with connecting words sometimes
        connectors = ["furthermore", "however", "nevertheless", "meanwhile", "surprisingly", "consequently", "therefore"]
        
        result = []
        for i, line in enumerate(selected_lines):
            if i > 0 and random.random() < 0.4:
                result.append(random.choice(connectors))
            result.append(line)
            
        return " ".join(result)
        
    def generate_content(self):
        """
        Generate long-form chaotic content with multiple paragraphs
        
        Returns:
            Generated content text
        """
        paragraphs = []
        used_styles = set()
        
        # Create a list of theme words to weave into content for subtle coherence
        theme_words = ["reality", "consciousness", "simulation", "perception", "existence", 
                      "truth", "memory", "identity", "time", "knowledge", "awareness", 
                      "patterns", "signals", "connections", "dimensions", "entities"]
        
        # Choose 1-3 theme words for this generation
        chosen_themes = random.sample(theme_words, k=min(3, len(theme_words)))
        
        # If a specific style is requested, use it for all paragraphs but with variations
        if self.style:
            for i in range(self.paragraph_count):
                # Create variation parameter based on paragraph number
                variation = i % 3
                paragraph = self._generate_paragraph(style=self.style, variation=variation)
                
                # Sometimes inject a theme word for subtle coherence
                if random.random() < 0.4 and len(paragraph.split()) > 15:
                    words = paragraph.split()
                    position = random.randint(5, min(len(words)-5, 20))
                    words[position] = random.choice(chosen_themes)
                    paragraph = ' '.join(words)
                
                paragraphs.append(paragraph)
        else:
            # Use a mix of styles for variety with deliberate structure
            styles = [
                'cursed_mashup', 'conspiracy_overload', 'existential_horror',
                'tone_shift', 'fourth_wall', 'narrative_collapse', 'theory_rabbit_hole',
                'identity_crisis', 'timeline_fracture'
            ]
            
            # Select a "primary" style that appears more than once for thematic consistency
            primary_style = random.choice(styles)
            used_styles.add(primary_style)
            
            # Plan out the paragraph arrangement
            if self.paragraph_count <= 2:
                # For short content, just use a mix
                selected_styles = []
                for i in range(self.paragraph_count):
                    available = [s for s in styles if s not in used_styles or s == primary_style]
                    if not available:
                        available = styles
                    style = random.choice(available)
                    selected_styles.append(style)
                    used_styles.add(style)
            else:
                # For longer content, create a deliberate flow
                selected_styles = []
                
                # Start with something attention-grabbing
                opener_styles = ['conspiracy_overload', 'tone_shift', 'cursed_mashup']
                opener = random.choice(opener_styles)
                selected_styles.append(opener)
                used_styles.add(opener)
                
                # Middle paragraphs mix the primary style with others
                middle_count = self.paragraph_count - 2
                for i in range(middle_count):
                    # Every other paragraph uses the primary style for consistency
                    if i % 2 == 0 and random.random() < 0.7:
                        selected_styles.append(primary_style)
                    else:
                        available = [s for s in styles if s not in used_styles or random.random() < 0.3]
                        if not available:
                            available = [s for s in styles if s != selected_styles[-1]]
                        style = random.choice(available)
                        selected_styles.append(style)
                        used_styles.add(style)
                
                # End with something memorable
                closer_styles = ['fourth_wall', 'narrative_collapse', 'identity_crisis']
                available_closers = [s for s in closer_styles if s not in used_styles]
                if not available_closers:
                    available_closers = closer_styles
                selected_styles.append(random.choice(available_closers))
            
            # Generate paragraphs with the selected styles
            for i, style in enumerate(selected_styles):
                # Use index as variation parameter to ensure diversity even with same style
                variation = i % 3
                paragraph = self._generate_paragraph(style=style, variation=variation)
                
                # Sometimes inject a theme word for subtle coherence
                if random.random() < 0.4 and len(paragraph.split()) > 15:
                    words = paragraph.split()
                    position = random.randint(5, min(len(words)-5, 20))
                    words[position] = random.choice(chosen_themes)
                    paragraph = ' '.join(words)
                
                paragraphs.append(paragraph)
        
        # Always add the Remilio signature at the end, not on each paragraph
        content = "\n\n".join(paragraphs)
        
        # Use HTML fixer for comprehensive cleaning
        try:
            from html_fixer import fix_html_entities
            content = fix_html_entities(content)
        except ImportError:
            # Fallback fixes if html_fixer isn't available
            content = content.replace('039;', "'")
            content = content.replace('039', "'")
            content = re.sub(r'I\';\s*([a-z])', r"I'\1", content)
            content = re.sub(r'([a-zA-Z])\';\s*([a-zA-Z])', r"\1'\2", content)
            content = re.sub(r'([a-zA-Z]+),\'s', r"\1's", content)
            
        # Remove the '>' symbol as requested
        content = content.replace('>tfw', 'tfw')
        content = content.replace('>mfw', 'mfw')
        content = content.replace('>', '')
        
        # Add the signature if it's not already there
        if not content.endswith("- Remilio"):
            content += "\n\n- Remilio"
            
        return content
        
    def log_content(self, content):
        """
        Log generated content to a file
        
        Args:
            content: Content text to log
        """
        try:
            with open(self.log_file, 'w') as f:
                f.write(content)
            logger.info(f"Content logged to {self.log_file}")
        except Exception as e:
            logger.error(f"Error logging content: {e}")
            
    def generate_and_log(self):
        """
        Generate content, log it, and return it
        
        Returns:
            Generated content text
        """
        content = self.generate_content()
        self.log_content(content)
        return content
        
# If run directly, generate and show some content
if __name__ == "__main__":
    # Generate one of each style
    styles = [
        'cursed_mashup', 'conspiracy_overload', 'existential_horror',
        'tone_shift', 'fourth_wall', 'narrative_collapse', 'theory_rabbit_hole',
        'identity_crisis', 'timeline_fracture'
    ]
    
    for style in styles:
        print("\n" + "=" * 80)
        print(f"{style.upper()} STYLE:")
        print("=" * 80)
        
        generator = LongFormGenerator(paragraph_count=1, style=style)
        content = generator.generate_content()
        print(content)
        print("\n")
        
    print("\n" + "=" * 80)
    print("MIXED STYLES (MULTIPLE PARAGRAPHS):")
    print("=" * 80)
    
    generator = LongFormGenerator(paragraph_count=3)
    content = generator.generate_content()
    print(content)