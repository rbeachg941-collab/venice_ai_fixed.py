#!/usr/bin/env python3
"""
Example usage of the eBay Card Lister script
===========================================

This script demonstrates how to use the CardLister class programmatically
for custom applications or integrations.
"""

from ebay_card_lister import CardLister

def example_single_card():
    """Example of processing a single card."""
    print("=== Single Card Example ===")
    
    lister = CardLister()
    
    # Example card data
    card_data = {
        'player': 'Michael Jordan',
        'year': '1986',
        'card_set': 'Fleer',
        'card_number': '57',
        'sport': 'basketball',
        'attributes': 'Rookie RC',
        'grader': 'PSA',
        'grade': '10'
    }
    
    # Process the card
    result = lister.process_single_card(card_data)
    
    # Print results
    lister.print_results(result)
    
    return result

def example_batch_cards():
    """Example of processing multiple cards."""
    print("\n=== Batch Processing Example ===")
    
    lister = CardLister()
    
    # Example batch data
    cards_data = [
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
        },
        {
            'player': 'LeBron James',
            'year': '2003',
            'card_set': 'Topps Chrome',
            'card_number': '111',
            'sport': 'basketball',
            'attributes': 'Rookie RC',
            'grader': 'PSA',
            'grade': '9'
        }
    ]
    
    # Process batch
    results = lister.batch_process(cards_data)
    
    # Save results
    lister.save_results_to_csv(results, 'example_results.csv')
    
    # Print summary
    print(f"\nProcessed {len(results)} cards:")
    for i, result in enumerate(results, 1):
        pricing = result['pricing_analysis']
        if pricing:
            print(f"{i}. {result['original_details']['player']} - Median: ${pricing['median']}")
        else:
            print(f"{i}. {result['original_details']['player']} - No pricing data")
    
    return results

def example_custom_analysis():
    """Example of custom analysis on results."""
    print("\n=== Custom Analysis Example ===")
    
    lister = CardLister()
    
    # Load example data
    cards_data = [
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
    
    results = lister.batch_process(cards_data)
    
    # Custom analysis
    total_value = 0
    cards_with_pricing = 0
    
    print("\nCustom Analysis:")
    print("-" * 30)
    
    for result in results:
        player = result['original_details']['player']
        pricing = result['pricing_analysis']
        
        if pricing:
            median_price = pricing['median']
            total_value += median_price
            cards_with_pricing += 1
            print(f"{player}: ${median_price} (based on {pricing['count']} sales)")
        else:
            print(f"{player}: No pricing data available")
    
    if cards_with_pricing > 0:
        avg_value = total_value / cards_with_pricing
        print(f"\nAverage portfolio value: ${avg_value:.2f}")
        print(f"Total estimated value: ${total_value:.2f}")

if __name__ == "__main__":
    print("eBay Card Lister - Example Usage")
    print("=" * 40)
    
    try:
        # Run examples
        example_single_card()
        example_batch_cards()
        example_custom_analysis()
        
        print("\n" + "=" * 40)
        print("Examples completed successfully!")
        print("Check 'example_results.csv' for batch processing output.")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("Make sure you have installed the required dependencies:")
        print("pip install -r requirements.txt")