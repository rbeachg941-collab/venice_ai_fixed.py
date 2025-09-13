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
    "multi-sport": "217",
    "default": "261328"
}

# User agents for web scraping
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# HTML Description Template
HTML_TEMPLATE = """
<div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; border: 1px solid #ccc; padding: 15px;">
    <div style="text-align: center; background-color: #0053a0; color: #fff; padding: 10px; font-size: 24px; font-weight: bold;">
        {title}
    </div>
    <div style="padding: 20px;">
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Card Details</h2>
        <ul style="list-style-type: none; padding: 0;">
            <li style="padding: 5px 0;"><strong>Player:</strong> {player}</li>
            <li style="padding: 5px 0;"><strong>Year:</strong> {year}</li>
            <li style="padding: 5px 0;"><strong>Set:</strong> {card_set}</li>
            <li style="padding: 5px 0;"><strong>Card #:</strong> {card_number}</li>
            <li style="padding: 5px 0;"><strong>Grader:</strong> {grader}</li>
            <li style="padding: 5px 0;"><strong>Grade:</strong> {grade}</li>
            <li style="padding: 5px 0;"><strong>Attributes:</strong> {attributes}</li>
        </ul>
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Condition</h2>
        <p>
            Please see the high-resolution photos for the exact condition of the card. The card pictured is the exact card you will receive.
        </p>
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Shipping & Handling</h2>
        <p>
            - Card will be shipped securely in a penny sleeve, top loader, and team bag.
            <br>- Shipped via eBay Standard Envelope for cards under $20 or USPS Ground Advantage for cards over $20.
            <br>- Combined shipping is available. Please message us before paying.
        </p>
    </div>
    <div style="text-align: center; font-size: 12px; color: #888; margin-top: 20px;">
        <p>Thank you for viewing our listing!</p>
        <p>SKU: {tracking_sku}</p>
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
            'player': input("Player Name: ").strip(),
            'year': input("Year: ").strip(),
            'card_set': input("Card Brand/Set (e.g., Topps Chrome): ").strip(),
            'card_number': input("Card Number: ").strip(),
            'sport': input("Sport (baseball, basketball, etc.): ").strip().lower(),
            'attributes': input("Special Attributes (e.g., Rookie, RC, Auto, Refractor, /99): ").strip(),
            'grader': input("Grader (e.g., PSA, BGS, SGC) [leave blank if raw]: ").strip().upper(),
            'grade': input("Grade (e.g., 10, 9.5) [leave blank if raw]: ").strip(),
        }
        return details
    
    def generate_seo_title(self, details: Dict[str, str]) -> str:
        """Constructs a Cassini-optimized title."""
        parts = [
            details['year'],
            details['card_set'],
            details['player'],
            f"#{details['card_number']}" if details['card_number'] else "",
            details['attributes'],
            details['grader'],
            f"Grade {details['grade']}" if details['grade'] and details['grader'] else details['grade'],
        ]
        # Filter out empty parts and join them
        title = " ".join(filter(None, parts))
        return title[:80]  # eBay titles are max 80 characters
    
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
        """Creates a dictionary of item specifics."""
        specifics = {
            "Player/Athlete": details['player'],
            "Year Manufactured": details['year'],
            "Set": details['card_set'],
            "Sport": details['sport'].capitalize(),
            "Card Number": details['card_number'],
            "Type": "Sports Trading Card",
            "Graded": "Yes" if details['grader'] else "No",
        }
        
        if details['grader']:
            specifics["Grader"] = details['grader']
            specifics["Grade"] = details['grade']
        
        features = []
        if 'rookie' in details['attributes'].lower() or 'rc' in details['attributes'].lower():
            features.append("Rookie")
        if 'auto' in details['attributes'].lower() or 'autograph' in details['attributes'].lower():
            features.append("Autograph")
            specifics["Autographed"] = "Yes"
        
        if features:
            specifics["Features"] = ", ".join(features)
        
        return specifics
    
    def generate_tracking_sku(self, details: Dict[str, str]) -> str:
        """Generates a unique SKU for internal tracking."""
        now = datetime.now().strftime("%Y%m%d-%H%M")
        player_slug = details['player'].split()[-1].upper()  # Use player's last name
        attr_slug = details.get('attributes', 'BASE').split()[0].upper()
        return f"CARD-{now}-{player_slug}-{attr_slug}"
    
    def process_single_card(self, details: Dict[str, str]) -> Dict:
        """Process a single card and return all generated data."""
        title = self.generate_seo_title(details)
        category_id, category_name = self.suggest_category(details['sport'])
        pricing_analysis = self.analyze_pricing(details)
        item_specifics = self.generate_item_specifics(details)
        tracking_sku = self.generate_tracking_sku(details)
        html_description = HTML_TEMPLATE.format(title=title, **details, tracking_sku=tracking_sku)
        
        return {
            'title': title,
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
        
        print("1. SEO-FRIENDLY TITLE (80 characters max):")
        print("------------------------------------------")
        print(results['title'])
        print(f"Length: {len(results['title'])} characters\n")
        
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
            'grader', 'grade', 'title', 'category_id', 'category_name',
            'tracking_sku', 'avg_price', 'median_price', 'price_range',
            'sales_count'
        ]
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                
                for result in results:
                    row = result['original_details'].copy()
                    row.update({
                        'title': result['title'],
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
                'grade': '10'
            },
            {
                'player': 'Tom Brady',
                'year': '2000',
                'card_set': 'Topps Chrome',
                'card_number': '236',
                'sport': 'football',
                'attributes': 'Rookie RC Refractor',
                'grader': 'BGS',
                'grade': '9.5'
            }
        ]
        
        fieldnames = ['player', 'year', 'card_set', 'card_number', 'sport', 'attributes', 'grader', 'grade']
        
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