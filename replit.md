# Remilio - Dynamic Content Generation and Meme Platform

## Overview
Remilio is a content generation platform designed to process and transform dynamic content streams into social media-ready posts and memes. It utilizes specialized generators to create diverse content, ranging from edgy humor to transcendent quotes, while maintaining authentic online culture aesthetics. The project aims to provide high-quality, unique content for various social media platforms.

## User Preferences
Preferred communication style: Simple, everyday language.

## System Architecture
The application employs a multi-generator, two-server architecture. The frontend, a Flask web application, provides the user interface and calls a private backend API that hosts the core generation algorithms.

**Frontend:**
- **Flask Web Application:** Serves as the main user interface with content generation endpoints.
- **Template System:** Utilizes Bootstrap for responsive design with custom CSS.
- **Security:** Implements rate limiting, input validation, and suspicious pattern detection.

**Backend:**
- **Multiple Specialized Generators:** Each targets specific content types, including "Enhanced Ultimate Edge," "Simple Enhanced Edge," "Transcendent Quote," "Simple Transcendental," and "Ultra Enhanced."
- **Private API Server:** Hosts the core generation algorithms and data processing.
- **Anti-Repetition System:** Prevents duplicate content across generators using hash-based tracking.

**Content Sources & Processing:**
- **Dynamic Content Stream System:** Automated processing of various dynamic content streams.
- **Curated Datasets:** Quality-filtered content organized by type and source.
- **Content Filtering:** HTML tag removal and detection of suspicious patterns.
- **Quality Scoring:** A 5.0-10.0 scoring system for content curation.

**Key Features:**
- **Content Generation:** Produces unique content based on user requests, with a distribution system balancing different generator outputs.
- **Meme Generator:** Includes features like chaotic visual effects, text customization, and random content generation for memes.
- **Video Downloader:** Supports downloading videos from over 100 platforms with quality selection and batch processing.

## External Dependencies
- **Python 3.11:** Primary programming language.
- **Flask 3.1.1:** Web framework.
- **Pandas 2.1.4:** Data processing and CSV handling.
- **Requests 2.31.0:** HTTP client for API calls and scraping.
- **CSV Files:** Used for primary storage of scraped and curated content.
- **Local File System:** Stores content tracking and anti-repetition data.
- **In-Memory Caching:** For performance optimization of recent content tracking.
- **Optional Integrations:** Twitter API (for posting), Railway/DigitalOcean (for private server hosting), Selenium WebDriver (for dynamic scraping).