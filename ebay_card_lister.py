#!/usr/bin/env python3
"""
eBay Sports Card Listing Assistant with Cassini Optimization
============================================================

This script helps you create optimized eBay listings for sports cards with:
- SEO-friendly titles optimized for Cassini algorithm
- Competitive pricing analysis via web scraping
- Batch processing for multiple cards
- Professional HTML descriptions
- Category optimization
- Analytics tracking SKUs

Author: AI Assistant
Version: 2.0
"""

import requests
from bs4 import BeautifulSoup
import re
import statistics
from datetime import datetime
import csv
import json
import time
import random
from typing import Dict, List, Optional, Tuple
import argparse
import sys

# --- Configuration ---
EBAY_CATEGORIES = {
    "baseball": "213",
    "basketball": "214", 
    "football": "215",
    "hockey": "216",
    "soccer": "261328",
    "wrestling": "261328",  # WWE cards use same category as trading cards
    "multi-sport": "217",
    "default": "261328"
}

# eBay Features field options (all 34 options)
EBAY_FEATURES = {
    "10th Anniversary Issue": ["10th", "anniversary"],
    "1st Edition": ["1st edition", "first edition"],
    "60th Anniversary Issue": ["60th", "anniversary"],
    "65th Anniversary Issue": ["65th", "anniversary"],
    "Base Set": ["base", "base set"],
    "Box Topper": ["box topper", "topper"],
    "Chase": ["chase"],
    "Checklist": ["checklist"],
    "Collectors Edition": ["collectors edition", "collector"],
    "Digital": ["digital"],
    "Embossed": ["embossed"],
    "Exchange/Redemption": ["exchange", "redemption", "redeem"],
    "Exclusive": ["exclusive"],
    "Framed": ["framed"],
    "Hologram": ["hologram", "holo"],
    "Insert": ["insert"],
    "Lenticular": ["lenticular"],
    "Limited Edition": ["limited edition", "limited", "le"],
    "Memorabilia": ["memorabilia", "mem", "patch", "jersey", "relic"],
    "Miscut": ["miscut"],
    "Misprint": ["misprint"],
    "One of One": ["1/1", "one of one", "1of1"],
    "Parallel/Variety": ["parallel", "variety", "prizm", "refractor", "gold", "silver", "rainbow"],
    "Printing Plate": ["printing plate", "plate"],
    "Promo": ["promo", "promotional"],
    "Puzzle": ["puzzle"],
    "Rookie": ["rookie", "rc"],
    "Sell Sheet": ["sell sheet"],
    "Serial Numbered": ["serial", "numbered", "/", "of"],
    "Short Print": ["short print", "sp"],
    "Sketch": ["sketch"],
    "Stamped": ["stamped"],
    "Sticker": ["sticker"],
    "AU": ["auto", "autograph", "au", "signed", "signature"]
}

# eBay Card Thickness options (all 14 options)
EBAY_CARD_THICKNESS = {
    "20 Pt.": ["20pt", "20 pt", "thin", "paper"],
    "35 Pt.": ["35pt", "35 pt", "regular"],
    "55 Pt.": ["55pt", "55 pt", "standard", "normal"],
    "59 Pt.": ["59pt", "59 pt"],
    "75 Pt.": ["75pt", "75 pt", "thick"],
    "79 Pt.": ["79pt", "79 pt"],
    "100 Pt.": ["100pt", "100 pt", "very thick"],
    "108 Pt.": ["108pt", "108 pt"],
    "130 Pt.": ["130pt", "130 pt", "extra thick"],
    "138 Pt.": ["138pt", "138 pt"],
    "180 Pt.": ["180pt", "180 pt", "super thick"],
    "197 Pt.": ["197pt", "197 pt"],
    "240 Pt.": ["240pt", "240 pt", "ultra thick"],
    "360 Pt.": ["360pt", "360 pt", "maximum thick"]
}

# User agents for web scraping
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# HTML Description Template - Cassini Optimized
HTML_TEMPLATE = """
<div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; border: 1px solid #ccc; padding: 15px;">
    <div style="text-align: center; background-color: #0053a0; color: #fff; padding: 10px; font-size: 24px; font-weight: bold;">
        {title}
    </div>
    <div style="padding: 20px;">
        <h1 style="color: #333; font-size: 20px; margin-bottom: 15px;">{year} {card_set} {player} #{card_number} {attributes}</h1>
        
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Sports Trading Card Details</h2>
        <ul style="list-style-type: none; padding: 0;">
            <li style="padding: 5px 0;"><strong>Player/Athlete:</strong> {player}</li>
            <li style="padding: 5px 0;"><strong>Year:</strong> {year}</li>
            <li style="padding: 5px 0;"><strong>Brand/Set:</strong> {card_set}</li>
            <li style="padding: 5px 0;"><strong>Card Number:</strong> #{card_number}</li>
            <li style="padding: 5px 0;"><strong>Sport:</strong> {sport_capitalized}</li>
            <li style="padding: 5px 0;"><strong>Special Features:</strong> {attributes}</li>
            {grader_info}
        </ul>
        
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Card Condition & Authenticity</h2>
        <p>
            This {year} {card_set} {player} #{card_number} {attributes} sports trading card is in excellent condition. 
            {authenticity_text} Please examine the high-resolution photos carefully as they show the exact card you will receive.
        </p>
        
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Professional Shipping & Protection</h2>
        <p>
            <strong>Secure Packaging:</strong> Your {player} card will be shipped in a penny sleeve, top loader, and team bag for maximum protection.
            <br><strong>Shipping Method:</strong> eBay Standard Envelope for cards under $20 or USPS Ground Advantage for cards over $20.
            <br><strong>Combined Shipping:</strong> Available for multiple card purchases. Please message us before payment.
            <br><strong>Fast Processing:</strong> Cards ship within 1-2 business days of payment.
        </p>
        
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Why Choose This Listing?</h2>
        <ul style="padding-left: 20px;">
            <li>Authentic {year} {card_set} {player} #{card_number} {attributes}</li>
            <li>Professional packaging and fast shipping</li>
            <li>Detailed photos showing exact condition</li>
            <li>Combined shipping available for multiple purchases</li>
            <li>Trusted seller with excellent feedback</li>
        </ul>
        
        <p style="background-color: #f8f9fa; padding: 10px; border-left: 4px solid #0053a0; margin: 15px 0;">
            <strong>Search Keywords:</strong> {player}, {year} {card_set}, #{card_number}, {attributes}, {sport_capitalized} trading card{sport_keywords}
        </p>
    </div>
    <div style="text-align: center; font-size: 12px; color: #888; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px;">
        <p>Thank you for viewing our {player} {year} {card_set} listing!</p>
        <p><strong>Listing SKU:</strong> {tracking_sku}</p>
    </div>
</div>
"""

class CardLister:
    """Main class for eBay card listing operations."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def get_card_details_interactive(self) -> Dict[str, str]:
        """Gathers card information from the user via prompts."""
        print("\n--- Enter Card Details ---")
        details = {
            'player': input("Player/Athlete Name: ").strip(),
            'year': input("Year/Season: ").strip(),
            'card_set': input("Card Brand/Set (e.g., Topps Chrome, Panini Chronicles): ").strip(),
            'card_number': input("Card Number (e.g., FX-JWD): ").strip(),
            'sport': input("Sport (baseball, basketball, football, hockey, wrestling, etc.): ").strip().lower(),
            'attributes': input("Special Attributes (e.g., Rookie, RC, Auto, Refractor, /99): ").strip(),
            'grader': input("Grader (e.g., PSA, BGS, SGC) [leave blank if raw]: ").strip().upper(),
            'grade': input("Grade (e.g., 10, 9.5) [leave blank if raw]: ").strip(),
            'parallel_variety': input("Parallel/Variety (e.g., Red Prizm, Gold, /99) [optional]: ").strip(),
            'insert_set': input("Insert Set (e.g., Flux Auto Red) [optional]: ").strip(),
            'autographed': input("Autographed (Yes/No) [optional]: ").strip().lower(),
            'autograph_auth': input("Autograph Authentication (e.g., Panini Authentic) [optional]: ").strip(),
            'team': input("Team/League (e.g., WWE, Lakers, Yankees) [optional]: ").strip(),
            'manufacturer': input("Manufacturer (e.g., Panini, Topps, Upper Deck) [optional]: ").strip(),
            'card_condition': input("Card Condition (Near Mint, Excellent, etc.) [optional]: ").strip(),
            'card_type': input("Card Type (Standard, Jumbo, etc.) [optional]: ").strip(),
        }
        return details
    
    def generate_seo_title(self, details: Dict[str, str]) -> str:
        """Constructs a Cassini-optimized title with strategic keyword placement."""
        # Cassini optimization: Put most important keywords first
        # Priority: Year, Brand, Player, Card#, Attributes, Grader, Grade
        
        # Build title components with strategic placement
        title_parts = []
        
        # 1. Year (high search volume)
        if details['year']:
            title_parts.append(details['year'])
        
        # 2. Brand/Set (critical for categorization)
        if details['card_set']:
            title_parts.append(details['card_set'])
        
        # 3. Player name (primary search term)
        if details['player']:
            title_parts.append(details['player'])
        
        # 4. Card number (specificity)
        if details['card_number']:
            title_parts.append(f"#{details['card_number']}")
        
        # 5. Attributes (rookie, auto, etc. - high value keywords)
        if details['attributes']:
            title_parts.append(details['attributes'])
        
        # 6. Grader (trust signals)
        if details['grader']:
            title_parts.append(details['grader'])
        
        # 7. Grade (specificity and value)
        if details['grade'] and details['grader']:
            title_parts.append(f"Grade {details['grade']}")
        elif details['grade']:
            title_parts.append(details['grade'])
        
        # Join and ensure under 80 characters
        title = " ".join(title_parts)
        
        # Ensure title is under 80 characters
        if len(title) > 80:
            # Try removing less critical elements
            if len(title) > 80 and details['grade'] and details['grader']:
                # Try without "Grade" prefix
                title_parts_alt = title_parts[:-1] + [details['grade']]
                title_alt = " ".join(title_parts_alt)
                if len(title_alt) <= 80:
                    title = title_alt
                else:
                    # Remove grade entirely if still too long
                    title = " ".join(title_parts[:-1])
            
            # If still too long, truncate intelligently
            if len(title) > 80:
                # Keep the most important parts
                essential_parts = [
                    details['year'],
                    details['card_set'],
                    details['player']
                ]
                essential_title = " ".join(filter(None, essential_parts))
                
                if len(essential_title) <= 80:
                    title = essential_title
                else:
                    # Last resort: truncate player name
                    title = title[:77] + "..."
        
        return title
    
    def validate_title_optimization(self, title: str, details: Dict[str, str]) -> Dict[str, any]:
        """Validate and analyze title for Cassini optimization."""
        analysis = {
            'title': title,
            'length': len(title),
            'under_80_chars': len(title) <= 80,
            'keyword_density': {},
            'optimization_score': 0,
            'recommendations': []
        }
        
        # Check keyword density
        keywords = [details['year'], details['card_set'], details['player'], details['attributes']]
        for keyword in keywords:
            if keyword:
                count = title.lower().count(keyword.lower())
                analysis['keyword_density'][keyword] = count
        
        # Calculate optimization score
        score = 0
        
        # Length score (optimal is 60-80 characters)
        if 60 <= len(title) <= 80:
            score += 30
        elif len(title) < 60:
            score += 20
            analysis['recommendations'].append("Title could be longer for better SEO")
        else:
            score += 10
            analysis['recommendations'].append("Title is too long - consider shortening")
        
        # Keyword presence score
        if details['year'] in title:
            score += 20
        if details['card_set'] in title:
            score += 20
        if details['player'] in title:
            score += 20
        if details['attributes'] in title:
            score += 10
        
        analysis['optimization_score'] = score
        
        # Add recommendations based on score
        if score < 70:
            analysis['recommendations'].append("Consider adding more keywords for better visibility")
        if score >= 80:
            analysis['recommendations'].append("Excellent title optimization!")
        
        return analysis
    
    def detect_features(self, details: Dict[str, str]) -> List[str]:
        """Detect eBay features from card attributes and details."""
        detected_features = []
        attributes_text = details.get('attributes', '').lower()
        parallel_variety = details.get('parallel_variety', '').lower()
        insert_set = details.get('insert_set', '').lower()
        
        # Combine all text for feature detection
        search_text = f"{attributes_text} {parallel_variety} {insert_set}".lower()
        
        # Check each eBay feature
        for feature_name, keywords in EBAY_FEATURES.items():
            for keyword in keywords:
                if keyword in search_text:
                    if feature_name not in detected_features:
                        detected_features.append(feature_name)
                    break
        
        # Special handling for serial numbered cards
        if any(char in search_text for char in ['/', 'of']) and 'serial' not in search_text:
            # Check if it looks like a serial number (e.g., "25/99", "1/1")
            import re
            serial_pattern = r'\d+/\d+'
            if re.search(serial_pattern, search_text):
                if "Serial Numbered" not in detected_features:
                    detected_features.append("Serial Numbered")
        
        # Special handling for memorabilia
        mem_keywords = ['patch', 'jersey', 'relic', 'memorabilia', 'mem']
        if any(keyword in search_text for keyword in mem_keywords):
            if "Memorabilia" not in detected_features:
                detected_features.append("Memorabilia")
        
        # Special handling for autographs
        auto_keywords = ['auto', 'autograph', 'au', 'signed', 'signature']
        if any(keyword in search_text for keyword in auto_keywords):
            if "AU" not in detected_features:
                detected_features.append("AU")
        
        return detected_features
    
    def suggest_category(self, sport: str) -> Tuple[str, str]:
        """Suggests an eBay category ID based on the sport."""
        category_id = EBAY_CATEGORIES.get(sport, EBAY_CATEGORIES["default"])
        return category_id, sport.capitalize()
    
    def analyze_pricing(self, details: Dict[str, str]) -> Optional[Dict]:
        """Scrapes eBay for sold listings to provide pricing analysis."""
        print("\n--- Analyzing Competitor Pricing (Sold Listings) ---")
        
        # Build search query
        search_terms = [
            details['year'],
            details['card_set'],
            details['player'],
            details['card_number'],
            details['attributes'],
            details['grader'],
            details['grade'],
        ]
        query = "+".join(filter(None, search_terms))
        url = f"https://www.ebay.com/sch/i.html?_nkw={query}&_sacat=0&LH_Complete=1&LH_Sold=1"
        
        try:
            # Add random delay to avoid rate limiting
            time.sleep(random.uniform(1, 3))
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching eBay page: {e}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        price_elements = soup.select('span.s-item__price')
        
        prices = []
        for el in price_elements:
            # Clean price text: remove currency symbols, commas, and handle price ranges
            price_text = el.get_text(strip=True).split(' to ')[0]  # Handle ranges like "$10 to $15"
            cleaned_price = re.sub(r'[^\d.]', '', price_text)
            if cleaned_price and float(cleaned_price) > 0:
                prices.append(float(cleaned_price))
        
        if not prices:
            print("No recent sales found for this exact card. Try broadening your search terms.")
            return None
        
        analysis = {
            'count': len(prices),
            'avg': round(statistics.mean(prices), 2),
            'median': round(statistics.median(prices), 2),
            'min': round(min(prices), 2),
            'max': round(max(prices), 2)
        }
        return analysis
    
    def generate_item_specifics(self, details: Dict[str, str]) -> Dict[str, str]:
        """Creates a comprehensive dictionary of item specifics for eBay."""
        specifics = {
            # Required fields
            "Player/Athlete": details['player'],
            "Year Manufactured": details['year'],
            "Set": details['card_set'],
            "Sport": details['sport'].capitalize(),
            "Card Number": details['card_number'],
            "Type": "Sports Trading Card",
            "Graded": "Yes" if details['grader'] else "No",
        }
        
        # Optional fields with high search volume
        if details.get('manufacturer'):
            specifics["Manufacturer"] = details['manufacturer']
        
        if details.get('parallel_variety'):
            specifics["Parallel/Variety"] = details['parallel_variety']
        
        if details.get('team'):
            specifics["Team"] = details['team']
        
        if details.get('insert_set'):
            specifics["Insert Set"] = details['insert_set']
        
        # Grading information
        if details['grader']:
            specifics["Grader"] = details['grader']
            if details['grade']:
                specifics["Grade"] = details['grade']
        
        # Autograph information
        autographed = details.get('autographed', '').lower()
        if autographed in ['yes', 'y', 'true'] or 'auto' in details['attributes'].lower():
            specifics["Autographed"] = "Yes"
            if details.get('autograph_auth'):
                specifics["Autograph Authentication"] = details['autograph_auth']
            if details['player']:
                specifics["Signed By"] = details['player']
        else:
            specifics["Autographed"] = "No"
        
        # Features - Use comprehensive detection
        detected_features = self.detect_features(details)
        
        # Set individual feature fields
        specifics["Rookie"] = "Yes" if "Rookie" in detected_features else "No"
        specifics["Memorabilia"] = "Yes" if "Memorabilia" in detected_features else "No"
        
        # Set the main Features field with all detected features
        if detected_features:
            specifics["Features"] = ", ".join(detected_features)
        else:
            specifics["Features"] = "Base Set"  # Default if no features detected
        
        # Condition information
        if details.get('card_condition'):
            specifics["Card Condition"] = details['card_condition']
        
        if details.get('card_type'):
            specifics["Card Size"] = details['card_type']
        
        # Additional common fields
        specifics["Country/Region of Manufacture"] = "United States"
        specifics["Language"] = "English"
        specifics["Card Thickness"] = "55 Pt."
        specifics["Original/Licensed Reprint"] = "Original"
        
        # Sport-specific fields
        if details['sport'] == 'wrestling':
            specifics["League"] = "WWE"
        
        return specifics
    
    def generate_tracking_sku(self, details: Dict[str, str]) -> str:
        """Generates a unique SKU for internal tracking."""
        now = datetime.now().strftime("%Y%m%d-%H%M")
        player_slug = details['player'].split()[-1].upper()  # Use player's last name
        attr_slug = details.get('attributes', 'BASE').split()[0].upper()
        return f"CARD-{now}-{player_slug}-{attr_slug}"
    
    def generate_enhanced_html_description(self, details: Dict[str, str], title: str, tracking_sku: str) -> str:
        """Generate Cassini-optimized HTML description with enhanced content."""
        # Prepare additional variables for the template
        sport_capitalized = details['sport'].capitalize()
        
        # Generate grader info
        if details['grader'] and details['grade']:
            grader_info = f'<li style="padding: 5px 0;"><strong>Grading:</strong> {details["grader"]} Grade {details["grade"]}</li>'
            authenticity_text = f"This card has been professionally graded by {details['grader']} with a grade of {details['grade']}, ensuring authenticity and condition."
        elif details['grader']:
            grader_info = f'<li style="padding: 5px 0;"><strong>Grading:</strong> {details["grader"]}</li>'
            authenticity_text = f"This card has been authenticated by {details['grader']}, ensuring authenticity."
        else:
            grader_info = '<li style="padding: 5px 0;"><strong>Grading:</strong> Raw/Ungraded</li>'
            authenticity_text = "This card is raw/ungraded. Please examine photos carefully for condition assessment."
        
        # Generate sport-specific keywords
        sport_keywords = {
            'baseball': ', baseball card, MLB',
            'basketball': ', basketball card, NBA',
            'football': ', football card, NFL',
            'hockey': ', hockey card, NHL',
            'soccer': ', soccer card, football card',
            'wrestling': ', wrestling card, WWE card, WWE'
        }
        sport_keyword_suffix = sport_keywords.get(details['sport'], f', {sport_capitalized} card')
        
        # Format the HTML template
        html_description = HTML_TEMPLATE.format(
            title=title,
            player=details['player'],
            year=details['year'],
            card_set=details['card_set'],
            card_number=details['card_number'],
            attributes=details['attributes'],
            sport_capitalized=sport_capitalized,
            grader_info=grader_info,
            authenticity_text=authenticity_text,
            sport_keywords=sport_keyword_suffix,
            tracking_sku=tracking_sku
        )
        
        return html_description

    def process_single_card(self, details: Dict[str, str]) -> Dict:
        """Process a single card and return all generated data."""
        title = self.generate_seo_title(details)
        title_analysis = self.validate_title_optimization(title, details)
        category_id, category_name = self.suggest_category(details['sport'])
        pricing_analysis = self.analyze_pricing(details)
        item_specifics = self.generate_item_specifics(details)
        tracking_sku = self.generate_tracking_sku(details)
        html_description = self.generate_enhanced_html_description(details, title, tracking_sku)
        
        return {
            'title': title,
            'title_analysis': title_analysis,
            'category_id': category_id,
            'category_name': category_name,
            'pricing_analysis': pricing_analysis,
            'item_specifics': item_specifics,
            'tracking_sku': tracking_sku,
            'html_description': html_description,
            'original_details': details
        }
    
    def print_results(self, results: Dict):
        """Prints formatted results for a single card."""
        print("\n" + "="*50)
        print("      >>> COPY-PASTE YOUR OPTIMIZED LISTING <<<")
        print("="*50 + "\n")
        
        print("1. CASSINI-OPTIMIZED TITLE:")
        print("------------------------------------------")
        print(results['title'])
        
        # Show title analysis
        analysis = results['title_analysis']
        print(f"Length: {analysis['length']}/80 characters")
        print(f"Optimization Score: {analysis['optimization_score']}/100")
        
        if analysis['recommendations']:
            print("Recommendations:")
            for rec in analysis['recommendations']:
                print(f"  • {rec}")
        
        print(f"Keyword Density: {analysis['keyword_density']}")
        print()
        
        print(f"2. SUGGESTED EBAY CATEGORY:")
        print("------------------------------------------")
        print(f"{results['category_name']} -> ID: {results['category_id']}\n")
        
        print("3. PRICING ANALYSIS (from recent sales):")
        print("------------------------------------------")
        if results['pricing_analysis']:
            analysis = results['pricing_analysis']
            print(f"   - Listings Found: {analysis['count']}")
            print(f"   - Average Price:  ${analysis['avg']}")
            print(f"   - Median Price:   ${analysis['median']} (often the best indicator)")
            print(f"   - Price Range:    ${analysis['min']} to ${analysis['max']}")
            print("RECOMMENDATION: Price your card around the median price for a quick sale.")
        else:
            print("Could not retrieve pricing data. Please research manually.")
        print("\n")
        
        print("4. CUSTOM SKU (for Analytics Tracking):")
        print("------------------------------------------")
        print(results['tracking_sku'])
        print("\n")
        
        print("5. ITEM SPECIFICS:")
        print("------------------------------------------")
        for key, value in results['item_specifics'].items():
            if value:
                print(f"- {key}: {value}")
        print("\n")
        
        print("6. HTML DESCRIPTION (copy and paste into the HTML tab of the description box):")
        print("------------------------------------------")
        print(results['html_description'])
    
    def load_cards_from_csv(self, filename: str) -> List[Dict[str, str]]:
        """Load card details from a CSV file."""
        cards = []
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    # Clean up the data
                    card = {key.strip(): value.strip() for key, value in row.items()}
                    cards.append(card)
            print(f"Loaded {len(cards)} cards from {filename}")
            return cards
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            return []
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []
    
    def save_results_to_csv(self, results: List[Dict], filename: str):
        """Save processed results to a CSV file."""
        if not results:
            print("No results to save.")
            return
        
        fieldnames = [
            'player', 'year', 'card_set', 'card_number', 'sport', 'attributes',
            'grader', 'grade', 'parallel_variety', 'insert_set', 'autographed',
            'autograph_auth', 'team', 'manufacturer', 'card_condition', 'card_type',
            'title', 'title_length', 'optimization_score', 'category_id', 'category_name', 
            'tracking_sku', 'avg_price', 'median_price', 'price_range', 'sales_count'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in results:
                    row = result['original_details'].copy()
                    row.update({
                        'title': result['title'],
                        'title_length': result['title_analysis']['length'],
                        'optimization_score': result['title_analysis']['optimization_score'],
                        'category_id': result['category_id'],
                        'category_name': result['category_name'],
                        'tracking_sku': result['tracking_sku'],
                        'avg_price': result['pricing_analysis']['avg'] if result['pricing_analysis'] else 'N/A',
                        'median_price': result['pricing_analysis']['median'] if result['pricing_analysis'] else 'N/A',
                        'price_range': f"${result['pricing_analysis']['min']}-${result['pricing_analysis']['max']}" if result['pricing_analysis'] else 'N/A',
                        'sales_count': result['pricing_analysis']['count'] if result['pricing_analysis'] else 'N/A'
                    })
                    writer.writerow(row)
            
            print(f"Results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def batch_process(self, cards: List[Dict[str, str]]) -> List[Dict]:
        """Process multiple cards in batch."""
        results = []
        total_cards = len(cards)
        
        print(f"\n--- Processing {total_cards} cards ---")
        
        for i, card_details in enumerate(cards, 1):
            print(f"\nProcessing card {i}/{total_cards}: {card_details.get('player', 'Unknown')}")
            
            try:
                result = self.process_single_card(card_details)
                results.append(result)
                
                # Add delay between requests to be respectful
                if i < total_cards:
                    time.sleep(random.uniform(2, 4))
                    
            except Exception as e:
                print(f"Error processing card {i}: {e}")
                continue
        
        return results
    
    def create_csv_template(self, filename: str):
        """Create a CSV template file for batch input."""
        template_data = [
            {
                'player': 'Michael Jordan',
                'year': '1986',
                'card_set': 'Fleer',
                'card_number': '57',
                'sport': 'basketball',
                'attributes': 'Rookie RC',
                'grader': 'PSA',
                'grade': '10',
                'parallel_variety': '',
                'insert_set': '',
                'autographed': '',
                'autograph_auth': '',
                'team': 'Chicago Bulls',
                'manufacturer': 'Fleer',
                'card_condition': 'Near Mint',
                'card_type': 'Standard'
            },
            {
                'player': 'Joaquin Wilde',
                'year': '2022',
                'card_set': 'Panini Chronicles WWE',
                'card_number': 'FX-JWD',
                'sport': 'wrestling',
                'attributes': 'Auto',
                'grader': '',
                'grade': '',
                'parallel_variety': 'Red Prizm',
                'insert_set': 'Flux Auto Red',
                'autographed': 'Yes',
                'autograph_auth': 'Panini Authentic',
                'team': 'WWE',
                'manufacturer': 'Panini',
                'card_condition': 'Near Mint',
                'card_type': 'Standard'
            },
            {
                'player': 'LeBron James',
                'year': '2023',
                'card_set': 'Panini Prizm',
                'card_number': '1',
                'sport': 'basketball',
                'attributes': 'Rookie RC Patch Auto /25',
                'grader': 'PSA',
                'grade': '9',
                'parallel_variety': 'Gold Refractor',
                'insert_set': 'Rookie Patch Auto',
                'autographed': 'Yes',
                'autograph_auth': 'Panini Authentic',
                'team': 'Lakers',
                'manufacturer': 'Panini',
                'card_condition': 'Near Mint',
                'card_type': 'Standard'
            }
        ]
        
        fieldnames = [
            'player', 'year', 'card_set', 'card_number', 'sport', 'attributes', 
            'grader', 'grade', 'parallel_variety', 'insert_set', 'autographed',
            'autograph_auth', 'team', 'manufacturer', 'card_condition', 'card_type'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(template_data)
            
            print(f"CSV template created: {filename}")
            print("Edit this file with your card details and use --batch mode to process them.")
        except Exception as e:
            print(f"Error creating template: {e}")

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='eBay Sports Card Listing Assistant')
    parser.add_argument('--batch', '-b', help='Process cards from CSV file')
    parser.add_argument('--output', '-o', help='Output CSV file for batch results')
    parser.add_argument('--template', '-t', action='store_true', help='Create CSV template file')
    parser.add_argument('--no-pricing', action='store_true', help='Skip pricing analysis (faster)')
    
    args = parser.parse_args()
    
    lister = CardLister()
    
    if args.template:
        lister.create_csv_template('card_template.csv')
        return
    
    if args.batch:
        # Batch processing mode
        cards = lister.load_cards_from_csv(args.batch)
        if not cards:
            return
        
        results = lister.batch_process(cards)
        
        if args.output:
            lister.save_results_to_csv(results, args.output)
        
        # Print summary
        print(f"\n--- BATCH PROCESSING COMPLETE ---")
        print(f"Processed: {len(results)} cards")
        print(f"Successful: {len([r for r in results if r['pricing_analysis']])} with pricing data")
        
        # Show first result as example
        if results:
            print(f"\n--- EXAMPLE OUTPUT (First Card) ---")
            lister.print_results(results[0])
    
    else:
        # Interactive mode
        try:
            card_details = lister.get_card_details_interactive()
            results = lister.process_single_card(card_details)
            lister.print_results(results)
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()