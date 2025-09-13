# Quick Start Guide - eBay Sports Card Lister

## 🚀 Get Started in 3 Steps

### 1. Install Dependencies
```bash
pip3 install --break-system-packages -r requirements.txt
```

### 2. Create Your Card Template
```bash
python3 ebay_card_lister.py --template
```
This creates `card_template.csv` with example data.

### 3. Process Your Cards
```bash
python3 ebay_card_lister.py --batch card_template.csv --output my_results.csv
```

## 📋 What You Get

For each card, the script generates:

✅ **SEO-Optimized Title** (Cassini-friendly)  
✅ **eBay Category ID** (for maximum visibility)  
✅ **Competitive Pricing Analysis** (from recent sales)  
✅ **Custom Tracking SKU** (for analytics)  
✅ **Item Specifics** (structured data)  
✅ **Professional HTML Description** (mobile-friendly)

## 📊 Example Output

**Title**: `1986 Fleer Michael Jordan #57 Rookie RC PSA Grade 10`  
**Category**: Basketball → ID: 214  
**SKU**: `CARD-20250913-0633-JORDAN-ROOKIE`  
**Pricing**: Median price from recent sales (when available)

## 🎯 Key Features

- **Batch Processing**: Handle multiple cards at once
- **Cassini Optimization**: SEO-friendly titles and categories
- **Web Scraping**: Real-time pricing from eBay sold listings
- **CSV Import/Export**: Easy data management
- **Professional Templates**: Ready-to-use HTML descriptions

## 📝 CSV Format

Edit `card_template.csv` with your cards:

| Field | Example |
|-------|---------|
| player | Michael Jordan |
| year | 1986 |
| card_set | Fleer |
| card_number | 57 |
| sport | basketball |
| attributes | Rookie RC |
| grader | PSA |
| grade | 10 |

## 🔧 Command Options

- `--template`: Create CSV template
- `--batch file.csv`: Process cards from CSV
- `--output file.csv`: Save results to CSV
- `--no-pricing`: Skip pricing analysis (faster)

## ⚡ Pro Tips

1. **Start Small**: Test with 2-3 cards first
2. **Check Results**: Review generated titles and pricing
3. **Use Median Price**: Often the best indicator for quick sales
4. **Complete Data**: Fill all fields for best results

## 🛠️ Troubleshooting

**No pricing data?** Try broader search terms or check spelling.  
**Script errors?** Ensure all dependencies are installed.  
**Rate limiting?** Script includes delays, but eBay may still block requests.

---

**Ready to list? Run the commands above and start optimizing your eBay listings!** 🏆