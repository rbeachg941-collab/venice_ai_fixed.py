# eBay Sports Card Listing Assistant

A powerful Python script for creating Cassini-optimized eBay listings for sports cards with batch processing capabilities.

## Features

### 🎯 Cassini Optimization
- **SEO-Friendly Titles**: Constructs titles using proven keyword formulas
- **Category Optimization**: Suggests correct eBay category IDs for maximum visibility
- **Item Specifics**: Generates structured data that Cassini's algorithm loves

### 📊 Competitive Pricing Analysis
- **Web Scraping**: Analyzes recently sold eBay listings
- **Data-Driven Pricing**: Provides average, median, and price range analysis
- **Sales Volume**: Shows number of recent sales for market validation

### 🚀 Batch Processing
- **CSV Import/Export**: Process multiple cards at once
- **Template Generation**: Creates CSV templates for easy data entry
- **Bulk Operations**: Efficient processing with rate limiting

### 📝 Professional Listings
- **HTML Descriptions**: Mobile-friendly, professional templates
- **Analytics Tracking**: Unique SKUs for performance monitoring
- **Shipping Policies**: Pre-built shipping information

## Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Make Script Executable** (Linux/Mac):
   ```bash
   chmod +x ebay_card_lister.py
   ```

## Usage

### Interactive Mode (Single Card)

Run the script without arguments for interactive mode:

```bash
python ebay_card_lister.py
```

The script will prompt you for:
- Player Name
- Year
- Card Brand/Set
- Card Number
- Sport
- Special Attributes (Rookie, Auto, etc.)
- Grader (PSA, BGS, SGC)
- Grade

### Batch Processing Mode

1. **Create a CSV Template**:
   ```bash
   python ebay_card_lister.py --template
   ```
   This creates `card_template.csv` with example data.

2. **Edit the CSV** with your card details:
   ```csv
   player,year,card_set,card_number,sport,attributes,grader,grade
   Michael Jordan,1986,Fleer,57,basketball,Rookie RC,PSA,10
   Tom Brady,2000,Topps Chrome,236,football,Rookie RC Refractor,BGS,9.5
   ```

3. **Process the Batch**:
   ```bash
   python ebay_card_lister.py --batch card_template.csv --output results.csv
   ```

### Command Line Options

- `--batch, -b`: Process cards from CSV file
- `--output, -o`: Save results to CSV file
- `--template, -t`: Create CSV template file
- `--no-pricing`: Skip pricing analysis (faster processing)

## Output Format

The script generates:

### 1. SEO-Optimized Title
```
1986 Fleer Michael Jordan #57 Rookie RC PSA Grade 10
```

### 2. eBay Category
```
Basketball -> ID: 214
```

### 3. Pricing Analysis
```
- Listings Found: 15
- Average Price: $2,450.00
- Median Price: $2,200.00 (often the best indicator)
- Price Range: $1,800.00 to $3,100.00
```

### 4. Custom SKU
```
CARD-20231201-1430-JORDAN-ROOKIE
```

### 5. Item Specifics
```
- Player/Athlete: Michael Jordan
- Year Manufactured: 1986
- Set: Fleer
- Sport: Basketball
- Card Number: 57
- Type: Sports Trading Card
- Graded: Yes
- Grader: PSA
- Grade: 10
- Features: Rookie
```

### 6. HTML Description
Professional, mobile-friendly HTML template with:
- Card details
- Condition information
- Shipping policies
- Tracking SKU

## CSV Template Format

| Field | Description | Example |
|-------|-------------|---------|
| player | Player name | Michael Jordan |
| year | Card year | 1986 |
| card_set | Brand/set name | Fleer |
| card_number | Card number | 57 |
| sport | Sport type | basketball |
| attributes | Special features | Rookie RC |
| grader | Grading company | PSA |
| grade | Grade number | 10 |

## Supported Sports & Categories

- **Baseball**: Category 213
- **Basketball**: Category 214
- **Football**: Category 215
- **Hockey**: Category 216
- **Soccer**: Category 261328
- **Multi-sport**: Category 217

## Best Practices

### For Cassini Optimization:
1. **Use Complete Titles**: Include year, brand, player, card number, attributes
2. **Choose Correct Categories**: Use suggested category IDs
3. **Fill Item Specifics**: Complete all available fields
4. **Use Keywords**: Include relevant search terms in attributes

### For Pricing:
1. **Check Recent Sales**: Use median price as baseline
2. **Consider Condition**: Adjust for card condition vs. sold listings
3. **Market Timing**: Consider seasonal trends
4. **Competition**: Price competitively for faster sales

### For Batch Processing:
1. **Prepare Data**: Use the template to ensure consistent formatting
2. **Test Small Batches**: Start with 5-10 cards to verify results
3. **Monitor Rate Limits**: Script includes delays to avoid eBay blocking
4. **Save Results**: Always use `--output` to save processed data

## Troubleshooting

### Common Issues:

1. **"No recent sales found"**:
   - Try broader search terms
   - Check spelling of player/set names
   - Consider similar cards for pricing reference

2. **Web scraping errors**:
   - Check internet connection
   - eBay may be blocking requests (script includes delays)
   - Try again later or use `--no-pricing` flag

3. **CSV import errors**:
   - Check CSV format matches template
   - Ensure no empty required fields
   - Verify file encoding is UTF-8

### Performance Tips:

- Use `--no-pricing` for faster processing when pricing data isn't needed
- Process cards in smaller batches (50-100 at a time)
- Run during off-peak hours to avoid rate limiting

## Legal Notice

This script is for educational and personal use only. Users are responsible for:
- Complying with eBay's terms of service
- Respecting rate limits and website policies
- Ensuring accuracy of listing information
- Following applicable laws and regulations

## Support

For issues or questions:
1. Check the troubleshooting section
2. Verify your CSV format matches the template
3. Ensure all dependencies are installed correctly
4. Test with a single card first before batch processing

---

**Happy Listing!** 🏆