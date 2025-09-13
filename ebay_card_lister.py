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
# eBay Sport options (all 104 options) with category mapping
EBAY_SPORTS = {
    # Major Sports with specific categories
    "Baseball": "213",
    "Basketball": "214", 
    "Football": "215",
    "Ice Hockey": "216",
    "Soccer": "261328",
    "Wrestling": "261328",
    
    # Other sports (use trading card category)
    "Aikido": "261328",
    "Alpine/Downhill": "261328",
    "Archery": "261328",
    "Athletics": "261328",
    "Australian Football": "261328",
    "Auto Racing": "261328",
    "Backcountry Skiing": "261328",
    "Badminton": "261328",
    "Beach Soccer": "261328",
    "Beach Volleyball": "261328",
    "Biathlon": "261328",
    "Billiards": "261328",
    "Bobsleigh": "261328",
    "Bodyboarding": "261328",
    "Bodybuilding": "261328",
    "Bowling": "261328",
    "Bowls": "261328",
    "Boxing": "261328",
    "Breaking": "261328",
    "Canoeing": "261328",
    "Climbing": "261328",
    "Cricket": "261328",
    "Curling": "261328",
    "Cycling": "261328",
    "Dance": "261328",
    "Darts": "261328",
    "Diving": "261328",
    "Dodgeball": "261328",
    "Downhill Skiing": "261328",
    "Equestrian": "261328",
    "eSports": "261328",
    "Fencing": "261328",
    "Field Hockey": "261328",
    "Figure Skating": "261328",
    "Fistball": "261328",
    "Gaelic Football": "261328",
    "Gliding": "261328",
    "Golf": "261328",
    "Gymnastics": "261328",
    "Handball": "261328",
    "Horse Racing": "261328",
    "Ice Skating": "261328",
    "Jiu-Jitsu": "261328",
    "Judo": "261328",
    "Kabaddi": "261328",
    "Karate": "261328",
    "Kayaking": "261328",
    "Kendo": "261328",
    "Kitesurfing": "261328",
    "Korfball": "261328",
    "Krav Maga": "261328",
    "Kung Fu": "261328",
    "Lacrosse": "261328",
    "Luge": "261328",
    "Mixed Martial Arts (MMA)": "261328",
    "Modern Pentathlon": "261328",
    "Motorboat Racing": "261328",
    "Motorcycle Racing": "261328",
    "Muay Thai": "261328",
    "Netball": "261328",
    "Ninjitsu": "261328",
    "Nordic/Cross-Country": "261328",
    "Nordic Combined": "261328",
    "Paragliding": "261328",
    "Poker": "261328",
    "Polo": "261328",
    "Pool": "261328",
    "Rallycross": "261328",
    "Rodeo": "261328",
    "Roller Derby": "261328",
    "Roller Skating": "261328",
    "Rowing": "261328",
    "Rugby League": "261328",
    "Rugby Union": "261328",
    "Running": "261328",
    "Sailing": "261328",
    "Shooting": "261328",
    "Skateboarding": "261328",
    "Skeleton": "261328",
    "Ski Jumping": "261328",
    "Snowboarding": "261328",
    "Softball": "261328",
    "Squash": "261328",
    "Surfing": "261328",
    "Swimming": "261328",
    "Table Tennis": "261328",
    "Taekwondo": "261328",
    "Tai Chi": "261328",
    "Tchoukball": "261328",
    "Telemark": "261328",
    "Tennis": "261328",
    "Trampolining": "261328",
    "Triathlon": "261328",
    "Volleyball": "261328",
    "Wakeboarding": "261328",
    "Water Polo": "261328",
    "Weight Lifting": "261328",
    "Windsurfing": "261328"
}

# Sport keyword mapping for detection
SPORT_KEYWORDS = {
    "baseball": "Baseball",
    "basketball": "Basketball", 
    "football": "Football",
    "hockey": "Ice Hockey",
    "ice hockey": "Ice Hockey",
    "soccer": "Soccer",
    "wrestling": "Wrestling",
    "mma": "Mixed Martial Arts (MMA)",
    "mixed martial arts": "Mixed Martial Arts (MMA)",
    "tennis": "Tennis",
    "golf": "Golf",
    "boxing": "Boxing",
    "cricket": "Cricket",
    "rugby": "Rugby Union",
    "rugby league": "Rugby League",
    "rugby union": "Rugby Union",
    "volleyball": "Volleyball",
    "swimming": "Swimming",
    "cycling": "Cycling",
    "running": "Running",
    "athletics": "Athletics",
    "track and field": "Athletics",
    "auto racing": "Auto Racing",
    "motorcycle racing": "Motorcycle Racing",
    "horse racing": "Horse Racing",
    "poker": "Poker",
    "esports": "eSports",
    "e-sports": "eSports",
    "electronic sports": "eSports"
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

# eBay Original/Licensed Reprint options
EBAY_ORIGINAL_REPRINT = {
    "Original": ["original", "authentic", "genuine", "real"],
    "Licensed Reprint": ["reprint", "licensed reprint", "reproduction", "copy"]
}

# Vintage detection criteria
VINTAGE_YEAR_CUTOFF = 1990  # Cards from 1990 and earlier are considered vintage

# eBay Event/Tournament options (major tournaments)
EBAY_EVENTS_TOURNAMENTS = {
    "Olympic Games": ["olympic", "olympics"],
    "Summer Olympics": ["summer olympic", "summer olympics"],
    "Winter Olympics": ["winter olympic", "winter olympics"],
    "FIFA World Cup": ["fifa world cup", "world cup"],
    "FIFA Women's World Cup": ["fifa women's world cup", "women's world cup"],
    "Super Bowl": ["super bowl"],
    "NBA Finals": ["nba finals", "nba championship"],
    "WNBA Finals": ["wnba finals", "wnba championship"],
    "MLB World Series": ["mlb world series", "world series"],
    "Stanley Cup Finals": ["stanley cup", "stanley cup finals"],
    "UEFA European Football Championship": ["uefa", "european championship"],
    "UEFA European Women's Championship": ["uefa women's", "european women's championship"],
    "CONCACAF Gold Cup": ["concacaf gold cup", "gold cup"],
    "CONCACAF Women's Championship": ["concacaf women's"],
    "Rugby World Cup": ["rugby world cup"],
    "Rugby League World Cup": ["rugby league world cup"],
    "Rugby World Cup Sevens": ["rugby world cup sevens"],
    "Women's Rugby World Cup": ["women's rugby world cup"],
    "Women's Rugby League World Cup": ["women's rugby league world cup"],
    "Cricket World Cup": ["cricket world cup"],
    "Men's Cricket World Cup": ["men's cricket world cup"],
    "Men's CricketT20 World Cup": ["men's cricket t20", "t20 world cup"],
    "Cricket Champions Trophy": ["cricket champions trophy"],
    "Cricket Champions League Twenty20": ["cricket champions league"],
    "Indoor Cricket World Cup": ["indoor cricket world cup"],
    "Masters World Series of Indoor Cricket": ["masters world series"],
    "Baseball World Cup": ["baseball world cup"],
    "Baseball Premier12": ["baseball premier12", "premier12"],
    "World Baseball Classic": ["world baseball classic", "wbc"],
    "Carribean World Series": ["caribbean world series"],
    "Japan Series": ["japan series"],
    "Serie del Rey": ["serie del rey"],
    "Basketball Men's World Cup": ["basketball men's world cup"],
    "Basketball Women's World Cup": ["basketball women's world cup"],
    "Basketball Men's Diamond Ball": ["basketball men's diamond ball"],
    "Basketball Women's Diamond Ball": ["basketball women's diamond ball"],
    "EuroBasket": ["eurobasket"],
    "Basketball AfroBasket": ["basketball afrobasket", "afrobasket"],
    "Basketball AmeriCup": ["basketball americup", "americup"],
    "Basketball Asia Cup": ["basketball asia cup", "asia cup"],
    "Basketball Oceania Championship": ["basketball oceania"],
    "Basketball South American Championship": ["basketball south american"],
    "Ice Hockey World Championships": ["ice hockey world championships"],
    "Volleyball Men's World Championship": ["volleyball men's world championship"],
    "Volleyball Women's World Cup": ["volleyball women's world cup"],
    "Volleyball Men's Nations League": ["volleyball men's nations league"],
    "Volleyball Women's Nations League": ["volleyball women's nations league"],
    "Volleyball World Grand Prix": ["volleyball world grand prix"],
    "Volleyball World League": ["volleyball world league"],
    "Men's European Volleyball Championship": ["men's european volleyball"],
    "Women's European Volleyball Championship": ["women's european volleyball"],
    "Beach Volley World Championships": ["beach volley world championships"],
    "Artistic Gymnastics World Championships": ["artistic gymnastics world championships"],
    "Rhythmic Gymnastics World Championships": ["rhythmic gymnastics world championships"],
    "Acrobatic Gymnastics World Championships": ["acrobatic gymnastics world championships"],
    "Aerobic Gymnastics World Championships": ["aerobic gymnastics world championships"],
    "Trampoline & Tumbling Gymnastics World Championships": ["trampoline gymnastics world championships"],
    "World Aesthetic Group Gymnastics Championships": ["world aesthetic group gymnastics"],
    "European Women's Gymnastics Championships": ["european women's gymnastics"],
    "European Women's Individual Gymnastics Championships": ["european women's individual gymnastics"],
    "Asian Gymnastics Championships": ["asian gymnastics championships"],
    "South American Gymnastics Championships": ["south american gymnastics"],
    "African Artistic Gymnastics Championship": ["african artistic gymnastics"],
    "All-Japan Artistic Gymnastics Championships": ["all-japan artistic gymnastics"],
    "Gymnastic American Cup": ["gymnastic american cup"],
    "Gymnastic U.S. Classic": ["gymnastic u.s. classic"],
    "Rhythmic Gymnastics European Championships": ["rhythmic gymnastics european"],
    "Pacific Rim Championships": ["pacific rim championships"],
    "World Fencing Championships": ["world fencing championships"],
    "European Fencing Championships": ["european fencing championships"],
    "Asian Fencing Championships": ["asian fencing championships"],
    "African Fencing Championships": ["african fencing championships"],
    "Pan American Fencing Championships": ["pan american fencing"],
    "International Fencing Championships": ["international fencing"],
    "World Wrestling Championship": ["world wrestling championship"],
    "Cheerleading World Championships": ["cheerleading world championships"],
    "ICU World Cheerleading Championships": ["icu world cheerleading"],
    "Bowling World Cup": ["bowling world cup"],
    "World Tenpin Bowling Championships": ["world tenpin bowling"],
    "World Lacrosse Championship": ["world lacrosse championship"],
    "Major League Lacrosse Championship": ["major league lacrosse"],
    "European Lacrosse Championships": ["european lacrosse"],
    "Roller Hockey World Cup": ["roller hockey world cup"],
    "Men's Softball World Championship": ["men's softball world championship"],
    "Women's Softball World Championship": ["women's softball world championship"],
    "ISF Men's World Championship": ["isf men's world championship"],
    "ISF Women's World Championship": ["isf women's world championship"],
    "World Cup of Softball": ["world cup of softball"],
    "USA Softball International Cup": ["usa softball international cup"],
    "Men's World Curling Championships": ["men's world curling"],
    "Women's World Curling Championships": ["women's world curling"],
    "Commonwealth Games": ["commonwealth games"],
    "Asian Games": ["asian games"],
    "European Games": ["european games"],
    "African Games": ["african games"],
    "Pan American Games": ["pan american games"],
    "Universiade": ["universiade"],
    "Australian Football International Cup": ["australian football international cup"],
    "All-Ireland Senior Gaelic Football Championship": ["all-ireland senior gaelic football"],
    "All-Ireland Senior Hurling Championship": ["all-ireland senior hurling"],
    "European Senior Gaelic Football Championship": ["european senior gaelic football"],
    "All-Ireland Senior Men's Rounders Championship": ["all-ireland senior men's rounders"],
    "All-Ireland Senior Ladies Rounders Championship": ["all-ireland senior ladies rounders"],
    "All-Ireland Senior Hardball Singles": ["all-ireland senior hardball singles"],
    "All-Ireland Senior Softball Singles": ["all-ireland senior softball singles"],
    "Christy Ring Cup": ["christy ring cup"],
    "William Jones Cup": ["william jones cup"]
}

# eBay Autograph Authentication options (all 19 options)
EBAY_AUTOGRAPH_AUTH = {
    "Beckett Authentication Services (BAS)": ["beckett", "bas", "beckett authentication"],
    "Bowman": ["bowman"],
    "Certified Guaranty Company (CGC)": ["cgc", "certified guaranty"],
    "Certified Sports Guaranty (CSG)": ["csg", "certified sports"],
    "Donruss": ["donruss"],
    "Fanatics Authentic": ["fanatics", "fanatics authentic"],
    "Fleer": ["fleer"],
    "James Spence Authentication (JSA)": ["jsa", "james spence", "spence"],
    "Leaf": ["leaf"],
    "Panini Authentic": ["panini", "panini authentic"],
    "Professional Sports Authenticator (PSA)": ["psa", "professional sports"],
    "PROVA Group": ["prova", "prova group"],
    "Score": ["score"],
    "Sportscard Guaranty Corporation (SGC)": ["sgc", "sportscard guaranty"],
    "Sports Memorabilia": ["sports memorabilia"],
    "Steiner Sports": ["steiner", "steiner sports"],
    "Topps": ["topps"],
    "TRISTAR Productions": ["tristar", "tristar productions"],
    "Upper Deck": ["upper deck", "upperdeck"]
}

# eBay Autograph Format options (all 3 options)
EBAY_AUTOGRAPH_FORMAT = {
    "Cut": ["cut", "cut signature"],
    "Hard Signed": ["hard signed", "hard", "on-card", "on card"],
    "Label or Sticker": ["label", "sticker", "authentication sticker", "auth sticker"]
}

# Major Parallel/Variety options (most common from the 783 options)
MAJOR_PARALLEL_VARIETIES = {
    # Base and Common
    "[Base]": ["base", "base card"],
    
    # Color-based parallels
    "Black": ["black"],
    "Blue": ["blue"],
    "Gold": ["gold"],
    "Green": ["green"],
    "Orange": ["orange"],
    "Pink": ["pink"],
    "Purple": ["purple"],
    "Red": ["red"],
    "Silver": ["silver"],
    "White": ["white"],
    "Yellow": ["yellow"],
    
    # Refractor types
    "Refractor": ["refractor"],
    "Black Refractor": ["black refractor"],
    "Blue Refractor": ["blue refractor"],
    "Gold Refractor": ["gold refractor"],
    "Green Refractor": ["green refractor"],
    "Orange Refractor": ["orange refractor"],
    "Pink Refractor": ["pink refractor"],
    "Purple Refractor": ["purple refractor"],
    "Red Refractor": ["red refractor"],
    "Silver Refractor": ["silver refractor"],
    "White Refractor": ["white refractor"],
    
    # Prizm types
    "Prizm": ["prizm"],
    "Black Prizm": ["black prizm"],
    "Blue Prizm": ["blue prizm"],
    "Gold Prizm": ["gold prizm"],
    "Green Prizm": ["green prizm"],
    "Orange Prizm": ["orange prizm"],
    "Pink Prizm": ["pink prizm"],
    "Purple Prizm": ["purple prizm"],
    "Red Prizm": ["red prizm"],
    "Silver Prizm": ["silver prizm"],
    "White Prizm": ["white prizm"],
    
    # Special finishes
    "Cracked Ice": ["cracked ice"],
    "Disco": ["disco"],
    "Holographic": ["holographic", "holo"],
    "Rainbow": ["rainbow"],
    "Shimmer": ["shimmer"],
    "Spectrum": ["spectrum"],
    
    # Numbered parallels
    "Serial Numbered": ["/", "of", "numbered", "serial"],
    
    # Special editions
    "1st Edition": ["1st edition", "first edition"],
    "Limited Edition": ["limited edition", "limited"],
    "Chrome": ["chrome"],
    "Finite": ["finite"],
    "Prime": ["prime"],
    "Mojo": ["mojo"],
    "Mosaic": ["mosaic"],
    "Pulsar": ["pulsar"],
    "Wave": ["wave"],
    
    # Insert sets (common ones)
    "Flux Auto Red": ["flux auto red"],
    "Flux Auto": ["flux auto"],
    "Flux": ["flux"],
    "Auto": ["auto", "autograph"],
    "Patch": ["patch"],
    "Memorabilia": ["memorabilia", "mem", "relic"],
    "Jersey": ["jersey"],
    "Rookie": ["rookie", "rc"]
}

# eBay Manufacturer options (all 167 options)
EBAY_MANUFACTURERS = {
    "Unbranded": ["unbranded", "generic"],
    "5FINITY": ["5finity", "5finity"],
    "7th Inning Sketch": ["7th inning sketch"],
    "AAA Sports Memorabilia": ["aaa sports memorabilia"],
    "Ace Authentic": ["ace authentic"],
    "Action Packed": ["action packed"],
    "AEG": ["aeg"],
    "Allens": ["allens"],
    "American Caramel": ["american caramel"],
    "APBA": ["apba"],
    "Argus": ["argus"],
    "ArtBox": ["artbox"],
    "Atlantic": ["atlantic"],
    "AW Sports, Inc.": ["aw sports"],
    "Bandai": ["bandai"],
    "Baseball Magazine": ["baseball magazine"],
    "Bazooka": ["bazooka"],
    "Bench Warmer": ["bench warmer"],
    "Bleachers": ["bleachers"],
    "Blue Ocean Entertainment": ["blue ocean entertainment"],
    "Bowman": ["bowman"],
    "Breygent Marketing Inc.": ["breygent"],
    "Bushiroad": ["bushiroad"],
    "Calbee": ["calbee"],
    "Callahan HALL OF FAME": ["callahan"],
    "CARDZ Distribution": ["cardz distribution"],
    "Champion Cards": ["champion cards"],
    "Chicagoland Processing Corp.": ["chicagoland processing"],
    "Choice Marketing, Inc": ["choice marketing"],
    "Chris Martin Enterprises, Inc.": ["chris martin enterprises"],
    "Classic Games, Inc": ["classic games"],
    "Classic Marketing, Inc.": ["classic marketing"],
    "CMC": ["cmc"],
    "Coles": ["coles"],
    "Collector's Edge": ["collectors edge", "collector's edge"],
    "College Classics, Inc.": ["college classics"],
    "Collegiate Collection": ["collegiate collection"],
    "Comic Images": ["comic images"],
    "Courtside": ["courtside"],
    "Cracker Jack": ["cracker jack"],
    "Cryptozoic": ["cryptozoic"],
    "Dan Dee": ["dan dee"],
    "Decipher": ["decipher"],
    "Diamond Stars": ["diamond stars"],
    "Disney": ["disney"],
    "Donruss": ["donruss"],
    "Donruss/Playoff": ["donruss/playoff", "donruss playoff"],
    "Double Play": ["double play"],
    "Dynamite Entertainment": ["dynamite entertainment"],
    "Eclipse Cards": ["eclipse cards"],
    "Enor": ["enor"],
    "Exhibits": ["exhibits"],
    "Extreme Sports Cards Inc.": ["extreme sports cards"],
    "Fantasy Flight Games": ["fantasy flight games"],
    "Félix Potin": ["felix potin"],
    "Fleer": ["fleer"],
    "Fleer/SkyBox International": ["fleer/skybox", "fleer skybox"],
    "Futera": ["futera"],
    "Glendale Publishers, Inc.": ["glendale publishers"],
    "Goal Line": ["goal line"],
    "Goal Line Art": ["goal line art"],
    "Goudey": ["goudey"],
    "Grandstand": ["grandstand"],
    "H.O.F. Cards-I, LLC": ["hof cards", "h.o.f. cards"],
    "Hasbro": ["hasbro"],
    "Herald Sun": ["herald sun"],
    "Hi-Pro Marketing, Inc.": ["hi-pro marketing"],
    "Hoby Cards, Inc.": ["hoby cards"],
    "Homogenized Bond": ["homogenized bond"],
    "Horse Star Cards Inc.": ["horse star cards"],
    "Impel": ["impel"],
    "Imperial Tobacco Canada": ["imperial tobacco"],
    "In the Game": ["in the game"],
    "JOGO, Inc.": ["jogo"],
    "Jogo Novelties": ["jogo novelties"],
    "Just Memorabilia": ["just memorabilia"],
    "Just Minors": ["just minors"],
    "Kahn's": ["kahns", "kahn's"],
    "Kellogg's": ["kelloggs", "kellogg's"],
    "Kenner": ["kenner"],
    "Konami": ["konami"],
    "Kornies": ["kornies"],
    "Layton Sports Cards": ["layton sports cards"],
    "Leaf": ["leaf"],
    "Marvel": ["marvel"],
    "Meiji": ["meiji"],
    "Merlin": ["merlin"],
    "Milk Duds": ["milk duds"],
    "Mobil": ["mobil"],
    "Monty Gum": ["monty gum"],
    "MSA": ["msa"],
    "National Chicle": ["national chicle"],
    "Navarrete": ["navarrete"],
    "NBA Properties": ["nba properties"],
    "NetPro": ["netpro"],
    "NFL Players Association": ["nfl players association"],
    "NFL Properties": ["nfl properties"],
    "Nintendo": ["nintendo"],
    "NSI Marketing Limited": ["nsi marketing"],
    "Nu-Cards": ["nu-cards", "nu cards"],
    "Onyx Authenticated": ["onyx authenticated"],
    "O-Pee-Chee": ["o-pee-chee", "o pee chee"],
    "Pacific": ["pacific"],
    "Panini": ["panini"],
    "Parkhurst": ["parkhurst"],
    "Parkside": ["parkside"],
    "Philadelphia Gum": ["philadelphia gum"],
    "Pinnacle": ["pinnacle"],
    "Playball": ["playball"],
    "Playoff": ["playoff"],
    "Post": ["post"],
    "Press Pass": ["press pass"],
    "ProCards": ["procards"],
    "Pro Set": ["pro set"],
    "R.E.L.": ["rel", "r.e.l."],
    "Razor": ["razor"],
    "Red Man": ["red man"],
    "Regina": ["regina"],
    "Ringside": ["ringside"],
    "Rittenhouse": ["rittenhouse"],
    "Roox Limited Corp.": ["roox limited"],
    "SAGE": ["sage"],
    "Scanlens": ["scanlens"],
    "SCORE": ["score"],
    "Select": ["select"],
    "Sereal": ["sereal"],
    "Shirriff Coins": ["shirriff coins"],
    "Signature Rookies": ["signature rookies"],
    "SkyBox": ["skybox"],
    "Spin Master": ["spin master"],
    "Sportflics": ["sportflics"],
    "Sport Kings": ["sport kings"],
    "Sportscaster": ["sportscaster"],
    "Sports Illustrated": ["sports illustrated"],
    "Square Enix": ["square enix"],
    "Star Pics": ["star pics"],
    "Stimoral": ["stimoral"],
    "Strictly Ink": ["strictly ink"],
    "Sunicrust": ["sunicrust"],
    "Superior Pix": ["superior pix"],
    "Superior Rookies": ["superior rookies"],
    "Tazo": ["tazo"],
    "TCMA": ["tcma"],
    "Teamcoach": ["teamcoach"],
    "Team Issue": ["team issue"],
    "The Asher Candy Co.": ["asher candy"],
    "The Furst Group": ["furst group"],
    "The Score Board, Inc": ["score board"],
    "The Star Co.": ["star co"],
    "Topps": ["topps"],
    "Topps Supreme": ["topps supreme"],
    "Tristar": ["tristar"],
    "Ty": ["ty"],
    "Ultimate Guard": ["ultimate guard"],
    "Ultimate Trading Card Co.": ["ultimate trading card"],
    "Ultra PRO": ["ultra pro"],
    "Unstoppable Cards": ["unstoppable cards"],
    "Upper Deck": ["upper deck", "upperdeck"],
    "Vachon": ["vachon"],
    "WEG": ["weg"],
    "Wheaties": ["wheaties"],
    "Wheels": ["wheels"],
    "White Wolf": ["white wolf"],
    "Wild Card": ["wild card"],
    "Wills": ["wills"],
    "Wizards of the Coast": ["wizards of the coast"],
    "WOW": ["wow"]
}

# Country/Region mapping based on manufacturer
MANUFACTURER_COUNTRIES = {
    "Panini": "Italy",
    "Topps": "United States", 
    "Upper Deck": "United States",
    "Fleer": "United States",
    "Donruss": "United States",
    "Leaf": "United States",
    "Bowman": "United States",
    "SCORE": "United States",
    "Beckett": "United States",
    "PSA": "United States",
    "BGS": "United States",
    "SGC": "United States",
    "Konami": "Japan",
    "Bandai": "Japan",
    "Meiji": "Japan",
    "Calbee": "Japan",
    "Bushiroad": "Japan",
    "Square Enix": "Japan",
    "Nintendo": "Japan",
    "Marvel": "United States",
    "Disney": "United States",
    "Hasbro": "United States",
    "Wizards of the Coast": "United States",
    "Cryptozoic": "United States",
    "default": "United States"
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
        
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Shipping & Store Policies</h2>
        
        <p><strong>Flat Rate Shipping:</strong><br>
        All U.S. orders ship at one flat rate! Enjoy free shipping on all additional cards when you use the shopping cart and complete your purchase in a single transaction.</p>
        
        <p><strong>Card Variations:</strong><br>
        When selling multiple copies of the same card with different patches, serial numbers, etc., please note that the photo may not depict the exact card you receive. Rest assured, the card you receive will match the described condition and type.</p>
        
        <p><strong>Customer Service:</strong><br>
        For any inquiries, please contact us through eBay messages. We are here to help and respond promptly.</p>
        
        <p><strong>Shipping Schedule:</strong><br>
        We ship Monday through Saturday, ensuring that your order goes out within 1 business day of purchase via USPS mail.</p>
        
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">FAQs</h2>
        
        <p><strong>Card Condition:</strong><br>
        All of our cards are in near mint to mint condition. We offer a 30-day money-back guarantee if you're not fully satisfied with your order.</p>
        
        <p><strong>Combined Shipping:</strong><br>
        We offer free shipping on all domestic orders for an unlimited number of cards in a single transaction.</p>
        
        <p><strong>Shipping:</strong><br>
        Your order will be shipped within 1 business day of purchase via USPS mail.</p>
        
        <h2 style="border-bottom: 2px solid #eee; padding-bottom: 5px; color: #333;">Professional Protection</h2>
        <p>
            <strong>Secure Packaging:</strong> Your {player} card will be shipped in a penny sleeve, top loader, and team bag for maximum protection.
            <br><strong>Shipping Method:</strong> eBay Standard Envelope for cards under $20 or USPS Ground Advantage for cards over $20.
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
            'event_tournament': input("Event/Tournament (e.g., Olympic Games, Super Bowl, World Cup) [optional]: ").strip(),
            'card_condition': input("Card Condition (Near Mint, Excellent, etc.) [optional]: ").strip(),
            'card_type': input("Card Type (Standard, Jumbo, etc.) [optional]: ").strip(),
            'pricing_type': input("Pricing Type (Auction, Buy It Now) [optional]: ").strip(),
            'allow_offers': input("Allow Offers (Yes/No) [optional]: ").strip(),
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
    
    def detect_card_thickness(self, details: Dict[str, str]) -> str:
        """Detect card thickness from card details."""
        # Combine all text for thickness detection
        search_text = f"{details.get('attributes', '')} {details.get('parallel_variety', '')} {details.get('insert_set', '')} {details.get('card_type', '')}".lower()
        
        # Check each thickness option
        for thickness, keywords in EBAY_CARD_THICKNESS.items():
            for keyword in keywords:
                if keyword in search_text:
                    return thickness
        
        # Default to 55 Pt. for standard cards
        return "55 Pt."
    
    def detect_original_reprint(self, details: Dict[str, str]) -> str:
        """Detect if card is original or licensed reprint."""
        # Combine all text for detection
        search_text = f"{details.get('attributes', '')} {details.get('card_set', '')} {details.get('parallel_variety', '')}".lower()
        
        # Check for reprint indicators first
        for reprint_type, keywords in EBAY_ORIGINAL_REPRINT.items():
            for keyword in keywords:
                if keyword in search_text:
                    return reprint_type
        
        # Default to Original for most cards
        return "Original"
    
    def detect_vintage_status(self, details: Dict[str, str]) -> str:
        """Detect if card is vintage based on year."""
        try:
            year = int(details.get('year', '0'))
            return "Yes" if year <= VINTAGE_YEAR_CUTOFF else "No"
        except (ValueError, TypeError):
            return "No"
    
    def detect_autograph_auth(self, details: Dict[str, str]) -> str:
        """Detect autograph authentication service from card details."""
        auth_input = details.get('autograph_auth', '').lower()
        
        # Check each authentication service
        for auth_service, keywords in EBAY_AUTOGRAPH_AUTH.items():
            for keyword in keywords:
                if keyword in auth_input:
                    return auth_service
        
        # Default to Panini Authentic if no match found
        return "Panini Authentic"
    
    def detect_country_region(self, details: Dict[str, str]) -> str:
        """Detect country/region of manufacture based on manufacturer."""
        detected_manufacturer = self.detect_manufacturer(details.get('manufacturer', ''))
        
        # Check manufacturer mapping
        if detected_manufacturer in MANUFACTURER_COUNTRIES:
            return MANUFACTURER_COUNTRIES[detected_manufacturer]
        
        # Default to United States
        return MANUFACTURER_COUNTRIES["default"]
    
    def detect_autograph_format(self, details: Dict[str, str]) -> str:
        """Detect autograph format from card details."""
        # Combine all text for format detection
        search_text = f"{details.get('attributes', '')} {details.get('parallel_variety', '')} {details.get('insert_set', '')}".lower()
        
        # Check each format option
        for format_type, keywords in EBAY_AUTOGRAPH_FORMAT.items():
            for keyword in keywords:
                if keyword in search_text:
                    return format_type
        
        # Default to Label or Sticker for most modern cards
        return "Label or Sticker"
    
    def detect_parallel_variety(self, details: Dict[str, str]) -> str:
        """Detect parallel/variety from card details."""
        # Combine all text for parallel detection
        search_text = f"{details.get('attributes', '')} {details.get('parallel_variety', '')} {details.get('insert_set', '')}".lower()
        
        # Check each parallel option (prioritize more specific matches first)
        for parallel_name, keywords in MAJOR_PARALLEL_VARIETIES.items():
            for keyword in keywords:
                if keyword in search_text:
                    return parallel_name
        
        # If no specific parallel detected, check if it's a base card
        if not details.get('parallel_variety') and not details.get('insert_set'):
            return "[Base]"
        
        # Default to the user input if provided
        return details.get('parallel_variety', '[Base]')
    
    def detect_sport(self, sport_input: str) -> str:
        """Detect proper eBay sport from user input."""
        sport_lower = sport_input.lower().strip()
        
        # Check keyword mapping first
        if sport_lower in SPORT_KEYWORDS:
            return SPORT_KEYWORDS[sport_lower]
        
        # Check exact match in eBay sports
        for sport_name in EBAY_SPORTS.keys():
            if sport_lower == sport_name.lower():
                return sport_name
        
        # Check partial match
        for sport_name in EBAY_SPORTS.keys():
            if sport_lower in sport_name.lower() or sport_name.lower() in sport_lower:
                return sport_name
        
        # Default to Wrestling for WWE cards
        if 'wwe' in sport_lower or 'wrestling' in sport_lower:
            return "Wrestling"
        
        # Default fallback
        return sport_input.title()

    def detect_manufacturer(self, manufacturer_input: str) -> str:
        """Detect proper eBay manufacturer from user input."""
        if not manufacturer_input:
            return "Unbranded"
        
        manufacturer_lower = manufacturer_input.lower().strip()
        
        # Check exact match in eBay manufacturers
        for manufacturer_name, keywords in EBAY_MANUFACTURERS.items():
            for keyword in keywords:
                if manufacturer_lower == keyword.lower():
                    return manufacturer_name
        
        # Check partial match
        for manufacturer_name, keywords in EBAY_MANUFACTURERS.items():
            for keyword in keywords:
                if keyword.lower() in manufacturer_lower or manufacturer_lower in keyword.lower():
                    return manufacturer_name
        
        # Default fallback
        return manufacturer_input.title()

    def detect_event_tournament(self, event_input: str) -> str:
        """Detect proper eBay event/tournament from user input."""
        if not event_input:
            return ""
        
        event_lower = event_input.lower().strip()
        
        # Check each event option
        for event_name, keywords in EBAY_EVENTS_TOURNAMENTS.items():
            for keyword in keywords:
                if keyword.lower() in event_lower or event_lower in keyword.lower():
                    return event_name
        
        # Default fallback
        return event_input.title()

    def detect_card_condition_ebay(self, details):
        """Map user input to eBay's Card Condition options."""
        condition_input = details.get('card_condition', '').lower()
        if not condition_input:
            return None
        
        # eBay Card Condition options
        condition_mapping = {
            'near mint': 'Near mint or better: Comparable to a fresh pack',
            'near mint or better': 'Near mint or better: Comparable to a fresh pack',
            'nm': 'Near mint or better: Comparable to a fresh pack',
            'nm-mt': 'Near mint or better: Comparable to a fresh pack',
            'mint': 'Near mint or better: Comparable to a fresh pack',
            'excellent': 'Excellent: Has clearly visible signs of wear',
            'ex': 'Excellent: Has clearly visible signs of wear',
            'very good': 'Very good: Has moderate-to-heavy damage all over',
            'vg': 'Very good: Has moderate-to-heavy damage all over',
            'good': 'Very good: Has moderate-to-heavy damage all over',
            'poor': 'Poor: Is extremely worn and displays flaws all over',
            'fair': 'Poor: Is extremely worn and displays flaws all over'
        }
        
        # Direct match
        if condition_input in condition_mapping:
            return condition_mapping[condition_input]
        
        # Partial match
        for keyword, ebay_condition in condition_mapping.items():
            if keyword in condition_input:
                return ebay_condition
        
        return None

    def detect_pricing_type(self, details):
        """Detect pricing type from card details."""
        pricing_input = details.get('pricing_type', '').lower()
        if not pricing_input:
            return None
        
        # eBay Pricing options
        pricing_mapping = {
            'auction': 'Auction',
            'buy it now': 'Buy It Now',
            'bin': 'Buy It Now',
            'fixed price': 'Buy It Now',
            'fixed': 'Buy It Now'
        }
        
        # Direct match
        if pricing_input in pricing_mapping:
            return pricing_mapping[pricing_input]
        
        # Partial match
        for keyword, ebay_pricing in pricing_mapping.items():
            if keyword in pricing_input:
                return ebay_pricing
        
        return None

    def detect_allow_offers(self, details):
        """Detect allow offers setting from card details."""
        allow_offers_input = details.get('allow_offers', '').lower()
        if not allow_offers_input:
            return None
        
        # eBay Allow Offers options
        offers_mapping = {
            'yes': 'Yes',
            'y': 'Yes',
            'true': 'Yes',
            'no': 'No',
            'n': 'No',
            'false': 'No'
        }
        
        # Direct match
        if allow_offers_input in offers_mapping:
            return offers_mapping[allow_offers_input]
        
        return None

    def detect_item_category(self, details):
        """Detect item category based on card details."""
        # Check if it's an autographed wrestling card
        if (details.get('sport', '').lower() == 'wrestling' and 
            details.get('autographed', '').lower() in ['yes', 'y', 'true']):
            return "Sports Mem, Cards & Fan Shop > Autographs-Original > Wrestling > Other Autographed Wrestling"
        
        # Default to trading card singles for all other sports cards
        return "Sports Mem, Cards & Fan Shop>Sports Trading Cards>Trading Card Singles"

    def detect_store_category(self, details):
        """Detect store category based on card details."""
        sport = details.get('sport', '').lower()
        team = details.get('team', '').lower()
        
        # Check for wrestling categories
        if sport == 'wrestling':
            if 'aew' in team or 'all elite' in team:
                return "AEW"
            elif 'wwe' in team or 'world wrestling' in team:
                return "WWE"
            else:
                return "Other"
        
        # For non-wrestling sports, default to "All categories"
        return "All categories"

    def suggest_category(self, sport: str) -> Tuple[str, str]:
        """Suggests an eBay category ID based on the sport."""
        detected_sport = self.detect_sport(sport)
        category_id = EBAY_SPORTS.get(detected_sport, "261328")
        return category_id, detected_sport
    
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
            specifics["Manufacturer"] = self.detect_manufacturer(details['manufacturer'])
        
        # Use intelligent parallel/variety detection
        detected_parallel = self.detect_parallel_variety(details)
        if detected_parallel and detected_parallel != "[Base]":
            specifics["Parallel/Variety"] = detected_parallel
        
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
            specifics["Autograph Authentication"] = self.detect_autograph_auth(details)
            specifics["Autograph Format"] = self.detect_autograph_format(details)
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
        detected_condition = self.detect_card_condition_ebay(details)
        if detected_condition:
            specifics["Card Condition"] = detected_condition

        if details.get('card_type'):
            specifics["Card Size"] = details['card_type']

        # Condition Type - Graded vs Ungraded
        if details.get('grader') and details.get('grade'):
            specifics["Condition Type"] = "Graded: Professionally graded"
        else:
            specifics["Condition Type"] = "Ungraded: Not in original packaging or professionally graded"

        # Pricing Type
        detected_pricing = self.detect_pricing_type(details)
        if detected_pricing:
            specifics["Pricing"] = detected_pricing

        # Allow Offers
        detected_offers = self.detect_allow_offers(details)
        if detected_offers:
            specifics["Allow Offers"] = detected_offers

        # Item Category
        detected_category = self.detect_item_category(details)
        if detected_category:
            specifics["Item Category"] = detected_category

        # Store Category
        detected_store_category = self.detect_store_category(details)
        if detected_store_category:
            specifics["Store Category"] = detected_store_category
        
        # Additional common fields with intelligent detection
        specifics["Country/Region of Manufacture"] = self.detect_country_region(details)
        specifics["Language"] = "English"
        specifics["Card Thickness"] = self.detect_card_thickness(details)
        specifics["Original/Licensed Reprint"] = self.detect_original_reprint(details)
        specifics["Vintage"] = self.detect_vintage_status(details)
        
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
            'pricing_type', 'allow_offers', 'title', 'title_length', 'optimization_score', 
            'category_id', 'category_name', 'tracking_sku', 'avg_price', 'median_price', 
            'price_range', 'sales_count'
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
                'card_type': 'Standard',
                'pricing_type': 'Buy It Now',
                'allow_offers': 'Yes'
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
                'card_type': 'Standard',
                'pricing_type': 'Auction',
                'allow_offers': 'No'
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
                'card_type': 'Standard',
                'pricing_type': 'Buy It Now',
                'allow_offers': 'Yes'
            }
        ]
        
        fieldnames = [
            'player', 'year', 'card_set', 'card_number', 'sport', 'attributes', 
            'grader', 'grade', 'parallel_variety', 'insert_set', 'autographed', 
            'autograph_auth', 'team', 'manufacturer', 'card_condition', 'card_type', 'pricing_type', 'allow_offers'
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