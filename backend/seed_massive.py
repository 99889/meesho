import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from models.product import Product
from models.category import Category
import uuid
from datetime import datetime, timedelta
import random

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'meesho_db')

# Product name templates for each category
PRODUCT_TEMPLATES = {
    "Women Ethnic": [
        "Floral Print Kurti", "Embroidered Kurti", "Cotton Kurti Set", "Anarkali Gown",
        "Saree with Blouse", "Designer Lehenga", "Palazzo Suit Set", "Salwar Kameez",
        "Kurta with Dupatta", "Ethnic Gown", "Party Wear Kurti", "Straight Kurti",
        "A-Line Kurti", "Georgette Saree", "Silk Saree", "Banarasi Saree",
        "Chanderi Kurti", "Block Print Kurti", "Chikankari Kurti", "Bandhani Saree"
    ],
    "Women Western": [
        "Casual Dress", "Party Dress", "Denim Jeans", "Formal Blazer", 
        "Crop Top", "Long Top", "Palazzo Pants", "Jeggings",
        "Maxi Dress", "Midi Dress", "Jumpsuit", "Romper",
        "Formal Shirt", "Casual Shirt", "T-Shirt", "Tank Top",
        "Skirt", "Shorts", "Trousers", "Capri Pants"
    ],
    "Men": [
        "Casual Shirt", "Formal Shirt", "T-Shirt", "Polo T-Shirt",
        "Denim Jeans", "Casual Trousers", "Formal Trousers", "Track Pants",
        "Shorts", "Cargo Pants", "Kurta", "Ethnic Wear",
        "Blazer", "Jacket", "Sweatshirt", "Hoodie",
        "Sports Wear", "Gym Wear", "Athleisure", "Nehru Jacket"
    ],
    "Kids": [
        "Cotton T-Shirt Set", "Dress for Girls", "Shorts Set", "Ethnic Wear",
        "Party Dress", "Casual Dress", "Jeans", "Track Pants",
        "Shirt", "Top", "Skirt", "Frock",
        "Nightwear", "Innerwear", "Jacket", "Sweater",
        "Romper", "Jumpsuit", "Dungaree", "Lehenga Choli"
    ],
    "Home & Kitchen": [
        "Cookware Set", "Bed Sheet Set", "Curtains", "Kitchen Storage",
        "Dinner Set", "Cutlery Set", "Water Bottle", "Lunch Box",
        "Pillow", "Cushion Cover", "Bath Towel Set", "Blanket",
        "Kitchen Organizer", "Spice Box", "Food Container", "Kettle",
        "Mixer Grinder", "Pressure Cooker", "Non-stick Pan", "Kadai"
    ],
    "Beauty & Health": [
        "Makeup Kit", "Skincare Combo", "Hair Care Set", "Face Cream",
        "Body Lotion", "Face Wash", "Shampoo", "Conditioner",
        "Hair Oil", "Serum", "Sunscreen", "Moisturizer",
        "Lipstick Set", "Kajal", "Eyeliner", "Mascara",
        "Foundation", "Compact Powder", "Face Mask", "Scrub"
    ],
    "Electronics": [
        "Wireless Earbuds", "Bluetooth Speaker", "Smart Watch", "Fitness Band",
        "Power Bank", "Mobile Charger", "USB Cable", "Phone Case",
        "Screen Protector", "Phone Holder", "Selfie Stick", "Tripod",
        "LED Bulb", "Table Lamp", "Desk Fan", "Extension Board",
        "Headphones", "Neckband", "Keyboard", "Mouse"
    ],
    "Bags & Footwear": [
        "Handbag", "Shoulder Bag", "Backpack", "Laptop Bag",
        "Casual Shoes", "Formal Shoes", "Sports Shoes", "Sneakers",
        "Sandals", "Slippers", "Boots", "Loafers",
        "Wallet", "Belt", "Sling Bag", "Clutch",
        "Travel Bag", "Duffle Bag", "School Bag", "Gym Bag"
    ]
}

COLORS = [
    "Black", "White", "Blue", "Red", "Green", "Yellow", "Pink", "Purple",
    "Orange", "Brown", "Grey", "Navy", "Maroon", "Beige", "Cream", "Multi"
]

MATERIALS = {
    "Women Ethnic": ["Cotton", "Silk", "Georgette", "Rayon", "Chiffon", "Crepe", "Chanderi", "Linen"],
    "Women Western": ["Cotton", "Denim", "Polyester", "Viscose", "Lycra", "Georgette", "Crepe"],
    "Men": ["Cotton", "Polyester", "Denim", "Linen", "Silk", "Cotton Blend", "Lycra"],
    "Kids": ["Cotton", "Polyester", "Cotton Blend", "Fleece", "Denim"],
    "Home & Kitchen": ["Stainless Steel", "Aluminum", "Cotton", "Plastic", "Glass", "Ceramic"],
    "Beauty & Health": ["Natural Ingredients", "Dermatologist Tested", "Paraben Free", "Sulfate Free"],
    "Electronics": ["ABS Plastic", "Silicone", "Metal", "Aluminum Alloy"],
    "Bags & Footwear": ["PU Leather", "Canvas", "Synthetic", "Genuine Leather", "Mesh"]
}

SIZES = {
    "Women Ethnic": ["S", "M", "L", "XL", "XXL", "Free Size"],
    "Women Western": ["S", "M", "L", "XL", "XXL", "28", "30", "32", "34"],
    "Men": ["S", "M", "L", "XL", "XXL", "38", "40", "42", "44", "46"],
    "Kids": ["2-3Y", "4-5Y", "6-7Y", "8-9Y", "10-11Y", "12-13Y"],
    "Home & Kitchen": ["Standard", "Small", "Medium", "Large"],
    "Beauty & Health": ["Standard", "50ml", "100ml", "200ml"],
    "Electronics": ["Standard"],
    "Bags & Footwear": ["6", "7", "8", "9", "10", "Standard"]
}

OCCASIONS = {
    "Women Ethnic": ["Casual", "Party", "Wedding", "Festival", "Office", "Daily Wear"],
    "Women Western": ["Casual", "Party", "Office", "Daily Wear", "Beach", "Sports"],
    "Men": ["Casual", "Formal", "Party", "Sports", "Office", "Daily Wear"],
    "Kids": ["Casual", "Party", "School", "Daily Wear", "Sports"],
    "Home & Kitchen": ["Daily Use", "Kitchen", "Dining", "Bedroom"],
    "Beauty & Health": ["Daily Use", "Party", "Special Occasion"],
    "Electronics": ["Daily Use", "Travel", "Home", "Office"],
    "Bags & Footwear": ["Casual", "Formal", "Party", "Sports", "Travel", "Daily Wear"]
}

IMAGES = {
    "Women Ethnic": [
        "https://images.unsplash.com/photo-1732709470611-670308da8c5e?w=500",
        "https://images.unsplash.com/photo-1740750047392-0d48b5fc23e4?w=500",
        "https://images.pexels.com/photos/34346734/pexels-photo-34346734.jpeg?w=500",
        "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500",
        "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=500",
        "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=500"
    ],
    "Women Western": [
        "https://images.unsplash.com/photo-1445205170230-053b83016050?w=500",
        "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
        "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=500"
    ],
    "Men": [
        "https://images.unsplash.com/photo-1602810320073-1230c46d89d4?w=500",
        "https://images.unsplash.com/photo-1729717949731-a2f4d6fcd8a1?w=500",
        "https://images.unsplash.com/photo-1630435664004-8e6d54780dd8?w=500",
        "https://images.unsplash.com/photo-1542272454315-7e6c29e2e6d7?w=500",
        "https://images.unsplash.com/photo-1571731956672-f2b94d7dd0cb?w=500"
    ],
    "Kids": [
        "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500",
        "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500"
    ],
    "Home & Kitchen": [
        "https://images.pexels.com/photos/279648/pexels-photo-279648.jpeg?w=500",
        "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=500",
        "https://images.unsplash.com/photo-1584085646196-0c5c85e0dc13?w=500"
    ],
    "Beauty & Health": [
        "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=500",
        "https://images.unsplash.com/photo-1580870069867-74c57ee1bb07?w=500",
        "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500"
    ],
    "Electronics": [
        "https://images.pexels.com/photos/1599791/pexels-photo-1599791.jpeg?w=500",
        "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500",
        "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500"
    ],
    "Bags & Footwear": [
        "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500",
        "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500",
        "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=500"
    ]
}

SELLERS = [
    "Fashion Hub", "Style Mart", "Ethnic Store", "Trendy Fashion", "Premium Store",
    "Quality Shop", "Best Deals", "Super Store", "Value Shop", "Top Seller",
    "Elite Store", "Shopping Paradise", "Budget Store", "Luxury Shop", "Daily Store"
]

async def generate_products(category_name, count=100):
    products = []
    templates = PRODUCT_TEMPLATES[category_name]
    
    for i in range(count):
        base_name = random.choice(templates)
        variant = random.choice(["Premium", "Designer", "Stylish", "Classic", "Modern", "Elegant", "Trendy", ""])
        
        if variant:
            name = f"{variant} {base_name}"
        else:
            name = base_name
        
        # Random pricing
        base_price = random.randint(200, 1500)
        discount = random.choice([60, 65, 70, 75, 80])
        price = int(base_price * (100 - discount) / 100)
        
        # Random ratings
        rating = round(random.uniform(3.5, 5.0), 1)
        reviews = random.randint(50, 5000)
        
        # Select colors and sizes
        num_colors = random.randint(3, 6)
        selected_colors = random.sample(COLORS, num_colors)
        
        size_options = SIZES[category_name]
        if len(size_options) > 1:
            num_sizes = random.randint(1, min(4, len(size_options)))
            selected_sizes = random.sample(size_options, num_sizes)
        else:
            selected_sizes = size_options
        
        product = {
            "name": name,
            "price": price,
            "original_price": base_price,
            "discount": discount,
            "rating": rating,
            "reviews": reviews,
            "image": random.choice(IMAGES[category_name]),
            "category": category_name,
            "sizes": selected_sizes,
            "colors": selected_colors,
            "description": f"High-quality {name.lower()} with excellent finish and durability. Perfect for {random.choice(OCCASIONS[category_name]).lower()}. Made from premium {random.choice(MATERIALS[category_name]).lower()}.",
            "free_delivery": random.choice([True, True, True, False]),  # 75% free delivery
            "cod": True,
            "seller_name": random.choice(SELLERS),
            "return_policy": random.choice(["7 days return", "10 days return", "15 days return"]),
            "stock": random.randint(50, 500),
            "material": random.choice(MATERIALS[category_name]),
            "occasion": random.choice(OCCASIONS[category_name]),
            "care_instructions": random.choice([
                "Machine wash cold", "Hand wash only", "Dry clean only",
                "Machine wash", "Wipe with dry cloth", "Hand wash recommended"
            ])
        }
        
        products.append(Product(**product).model_dump())
    
    return products

async def generate_reviews_for_products(products):
    review_texts = {
        "5": [
            "Excellent quality! Exactly as shown in pictures. Highly recommended!",
            "Amazing product! Worth every penny. Will definitely buy again.",
            "Superb quality and great packaging. Very satisfied with purchase.",
            "Perfect product! Better than expected. Fast delivery too.",
            "Outstanding quality! Loved it. Great value for money.",
            "Fantastic product! Exactly what I wanted. Very happy!",
            "Top quality product! Highly satisfied. Recommend to everyone.",
            "Brilliant purchase! Quality is superb. Worth the price."
        ],
        "4": [
            "Very good quality. Satisfied with the purchase.",
            "Good product at this price point. Value for money.",
            "Nice product. Good quality and fast delivery.",
            "Good purchase. Quality is decent. Happy with it.",
            "Pretty good product. Meets expectations well.",
            "Nice quality. Good value for money. Recommended."
        ],
        "3": [
            "Product is okay. Average quality for the price.",
            "Decent product. Could be better but acceptable.",
            "It's good but not great. Fair purchase.",
            "Average quality. Nothing special but okay.",
            "Product matches description. Fair deal."
        ]
    }
    
    reviewer_names = [
        "Priya Sharma", "Rahul Kumar", "Anjali Patel", "Vikram Singh", "Neha Gupta",
        "Amit Shah", "Pooja Reddy", "Arjun Mehta", "Divya Iyer", "Rohan Verma",
        "Kavita Joshi", "Sanjay Pandey", "Ritu Agarwal", "Manoj Desai", "Sneha Nair",
        "Karan Malhotra", "Simran Kaur", "Aditya Rao", "Meera Menon", "Varun Chopra"
    ]
    
    reviews = []
    
    for product in products:
        num_reviews = min(random.randint(10, 100), product["reviews"])
        
        for _ in range(num_reviews):
            rating = random.choices([5, 4, 3], weights=[0.6, 0.3, 0.1])[0]  # 60% 5-star, 30% 4-star, 10% 3-star
            review_text = random.choice(review_texts[str(rating)])
            
            review = {
                "id": str(uuid.uuid4()),
                "product_id": product["id"],
                "user_name": random.choice(reviewer_names),
                "rating": rating,
                "review": review_text,
                "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 365))).isoformat(),
                "verified_purchase": random.choice([True, True, True, False])
            }
            reviews.append(review)
    
    return reviews

async def seed_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🚀 Starting comprehensive database seeding...")
    
    # Clear existing data
    await db.products.delete_many({})
    await db.categories.delete_many({})
    await db.reviews.delete_many({})
    print("🗑️  Cleared existing data")
    
    # Seed categories
    categories = [
        {"name": "Women Ethnic", "icon": "Shirt", "image": "https://images.unsplash.com/photo-1732709470611-670308da8c5e?w=400"},
        {"name": "Women Western", "icon": "Shirt", "image": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=400"},
        {"name": "Men", "icon": "User", "image": "https://images.unsplash.com/photo-1602810320073-1230c46d89d4?w=400"},
        {"name": "Kids", "icon": "Baby", "image": "https://images.unsplash.com/photo-1532453288672-3a27e9be9efd?w=400"},
        {"name": "Home & Kitchen", "icon": "Home", "image": "https://images.pexels.com/photos/279648/pexels-photo-279648.jpeg?w=400"},
        {"name": "Beauty & Health", "icon": "Sparkles", "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400"},
        {"name": "Electronics", "icon": "Smartphone", "image": "https://images.pexels.com/photos/1599791/pexels-photo-1599791.jpeg?w=400"},
        {"name": "Bags & Footwear", "icon": "ShoppingBag", "image": "https://images.unsplash.com/photo-1567401893414-76b7b1e5a7a5?w=400"}
    ]
    
    category_docs = [Category(**cat).model_dump() for cat in categories]
    await db.categories.insert_many(category_docs)
    print(f"✓ Seeded {len(categories)} categories")
    
    # Generate and seed products for each category
    all_products = []
    for category in categories:
        print(f"⏳ Generating 100 products for {category['name']}...")
        products = await generate_products(category["name"], 100)
        all_products.extend(products)
        print(f"✓ Generated 100 products for {category['name']}")
    
    # Insert all products in batches
    batch_size = 100
    for i in range(0, len(all_products), batch_size):
        batch = all_products[i:i+batch_size]
        await db.products.insert_many(batch)
        print(f"✓ Inserted products batch {i//batch_size + 1}/{len(all_products)//batch_size}")
    
    total_products = len(all_products)
    print(f"✅ Seeded {total_products} products")
    
    # Generate reviews
    print("⏳ Generating reviews for all products...")
    reviews = await generate_reviews_for_products(all_products)
    
    # Insert reviews in batches
    batch_size = 500
    for i in range(0, len(reviews), batch_size):
        batch = reviews[i:i+batch_size]
        await db.reviews.insert_many(batch)
        print(f"✓ Inserted reviews batch {i//batch_size + 1}/{len(reviews)//batch_size}")
    
    print(f"✅ Seeded {len(reviews)} reviews")
    
    client.close()
    
    print("\n" + "="*60)
    print("🎉 DATABASE SEEDING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"📦 Total Categories: {len(categories)}")
    print(f"🛍️  Total Products: {total_products}")
    print(f"⭐ Total Reviews: {len(reviews)}")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(seed_database())
