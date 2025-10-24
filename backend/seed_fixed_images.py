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

# Better structured product data with matching images
PRODUCT_DATA = {
    "Women Ethnic": {
        "templates": [
            {"name": "Cotton Kurti", "price_range": (299, 699)},
            {"name": "Designer Kurti Set", "price_range": (499, 999)},
            {"name": "Silk Saree", "price_range": (599, 1499)},
            {"name": "Anarkali Gown", "price_range": (799, 1999)},
            {"name": "Palazzo Suit Set", "price_range": (449, 899)},
            {"name": "Embroidered Kurti", "price_range": (399, 799)},
            {"name": "Party Wear Lehenga", "price_range": (999, 2499)},
            {"name": "Straight Kurti", "price_range": (299, 599)},
            {"name": "A-Line Kurti", "price_range": (349, 699)},
            {"name": "Georgette Saree", "price_range": (499, 1299)}
        ],
        "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500",
        "materials": ["Cotton", "Silk", "Georgette", "Rayon", "Chiffon"],
        "occasions": ["Casual", "Party", "Wedding", "Festival"]
    },
    "Women Western": {
        "templates": [
            {"name": "Casual Dress", "price_range": (399, 899)},
            {"name": "Denim Jeans", "price_range": (549, 1299)},
            {"name": "Formal Blazer", "price_range": (799, 1999)},
            {"name": "Party Dress", "price_range": (699, 1499)},
            {"name": "Crop Top", "price_range": (249, 599)},
            {"name": "Palazzo Pants", "price_range": (349, 799)},
            {"name": "Maxi Dress", "price_range": (599, 1299)},
            {"name": "Jumpsuit", "price_range": (699, 1499)},
            {"name": "Formal Shirt", "price_range": (449, 999)},
            {"name": "Casual T-Shirt", "price_range": (199, 499)}
        ],
        "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=500",
        "materials": ["Cotton", "Denim", "Polyester", "Lycra"],
        "occasions": ["Casual", "Party", "Office", "Daily Wear"]
    },
    "Men": {
        "templates": [
            {"name": "Casual Shirt", "price_range": (399, 999)},
            {"name": "Formal Shirt", "price_range": (449, 1199)},
            {"name": "Cotton T-Shirt", "price_range": (199, 499)},
            {"name": "Denim Jeans", "price_range": (699, 1699)},
            {"name": "Formal Trousers", "price_range": (599, 1299)},
            {"name": "Track Pants", "price_range": (349, 799)},
            {"name": "Polo T-Shirt", "price_range": (399, 899)},
            {"name": "Casual Jacket", "price_range": (999, 2499)},
            {"name": "Sports Wear", "price_range": (449, 999)},
            {"name": "Ethnic Kurta", "price_range": (599, 1499)}
        ],
        "image": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=500",
        "materials": ["Cotton", "Polyester", "Denim", "Linen"],
        "occasions": ["Casual", "Formal", "Sports", "Party"]
    },
    "Kids": {
        "templates": [
            {"name": "Kids T-Shirt Set", "price_range": (299, 699)},
            {"name": "Girls Dress", "price_range": (399, 899)},
            {"name": "Boys Shirt", "price_range": (299, 699)},
            {"name": "Kids Jeans", "price_range": (449, 999)},
            {"name": "Ethnic Wear Set", "price_range": (499, 1199)},
            {"name": "Kids Track Suit", "price_range": (399, 899)},
            {"name": "Party Dress", "price_range": (599, 1299)},
            {"name": "School Uniform", "price_range": (349, 799)},
            {"name": "Kids Nightwear", "price_range": (249, 599)},
            {"name": "Winter Jacket", "price_range": (699, 1499)}
        ],
        "image": "https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=500",
        "materials": ["Cotton", "Polyester", "Cotton Blend"],
        "occasions": ["Casual", "Party", "School", "Daily Wear"]
    },
    "Mobiles & Tablets": {
        "templates": [
            {"name": "Smartphone 6GB RAM 128GB", "price_range": (8999, 15999)},
            {"name": "Smartphone 4GB RAM 64GB", "price_range": (6999, 11999)},
            {"name": "Smartphone 8GB RAM 256GB", "price_range": (12999, 24999)},
            {"name": "iPhone 12 64GB", "price_range": (45999, 52999)},
            {"name": "iPhone 13 128GB", "price_range": (55999, 64999)},
            {"name": "iPhone 14 256GB", "price_range": (75999, 85999)},
            {"name": "Android Tablet 10 inch", "price_range": (9999, 16999)},
            {"name": "iPad 10th Gen", "price_range": (34999, 42999)},
            {"name": "Gaming Phone 12GB RAM", "price_range": (24999, 34999)},
            {"name": "Budget Smartphone 3GB", "price_range": (4999, 7999)}
        ],
        "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500",
        "materials": ["Glass & Metal", "Aluminum", "Polycarbonate"],
        "occasions": ["Daily Use", "Gaming", "Business"]
    },
    "Electronics": {
        "templates": [
            {"name": "Wireless Earbuds", "price_range": (449, 1999)},
            {"name": "Bluetooth Speaker", "price_range": (599, 2499)},
            {"name": "Smart Watch", "price_range": (799, 3999)},
            {"name": "Power Bank 10000mAh", "price_range": (499, 1499)},
            {"name": "Wireless Mouse", "price_range": (299, 999)},
            {"name": "Keyboard", "price_range": (399, 1499)},
            {"name": "USB Cable Set", "price_range": (149, 499)},
            {"name": "Phone Charger Fast", "price_range": (299, 899)},
            {"name": "Headphones", "price_range": (699, 2499)},
            {"name": "Fitness Band", "price_range": (999, 2999)}
        ],
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
        "materials": ["Plastic", "Metal", "Silicone"],
        "occasions": ["Daily Use", "Travel", "Sports"]
    },
    "Home & Kitchen": {
        "templates": [
            {"name": "Cookware Set 7pcs", "price_range": (899, 2499)},
            {"name": "Dinner Set 24pcs", "price_range": (799, 1999)},
            {"name": "Bed Sheet Double", "price_range": (549, 1299)},
            {"name": "Storage Container Set", "price_range": (399, 999)},
            {"name": "Kitchen Organizer", "price_range": (299, 799)},
            {"name": "Non-stick Pan Set", "price_range": (699, 1799)},
            {"name": "Pressure Cooker", "price_range": (899, 2299)},
            {"name": "Water Bottle Set", "price_range": (249, 699)},
            {"name": "Cushion Cover Set", "price_range": (299, 799)},
            {"name": "Curtain Set", "price_range": (599, 1499)}
        ],
        "image": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=500",
        "materials": ["Stainless Steel", "Aluminum", "Cotton", "Plastic"],
        "occasions": ["Daily Use", "Kitchen", "Bedroom"]
    },
    "Beauty & Health": {
        "templates": [
            {"name": "Makeup Kit Complete", "price_range": (399, 1299)},
            {"name": "Skincare Combo", "price_range": (449, 1199)},
            {"name": "Hair Care Set", "price_range": (349, 999)},
            {"name": "Face Cream SPF", "price_range": (249, 699)},
            {"name": "Lipstick Set 6pcs", "price_range": (299, 899)},
            {"name": "Serum & Moisturizer", "price_range": (399, 1099)},
            {"name": "Hair Oil Combo", "price_range": (249, 699)},
            {"name": "Body Lotion Set", "price_range": (349, 899)},
            {"name": "Face Mask Pack", "price_range": (199, 599)},
            {"name": "Nail Care Kit", "price_range": (249, 699)}
        ],
        "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=500",
        "materials": ["Natural Ingredients", "Dermatologist Tested"],
        "occasions": ["Daily Use", "Party", "Special Care"]
    },
    "Bags & Footwear": {
        "templates": [
            {"name": "Women Handbag", "price_range": (449, 1499)},
            {"name": "Men Casual Shoes", "price_range": (599, 1999)},
            {"name": "Sports Shoes", "price_range": (649, 2199)},
            {"name": "Backpack", "price_range": (499, 1499)},
            {"name": "Formal Shoes", "price_range": (799, 2499)},
            {"name": "Sandals", "price_range": (299, 999)},
            {"name": "Laptop Bag", "price_range": (699, 1799)},
            {"name": "Travel Bag", "price_range": (899, 2499)},
            {"name": "Wallet Leather", "price_range": (249, 799)},
            {"name": "Belt Premium", "price_range": (199, 699)}
        ],
        "image": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=500",
        "materials": ["PU Leather", "Canvas", "Synthetic"],
        "occasions": ["Casual", "Formal", "Travel", "Sports"]
    }
}

COLORS = ["Black", "White", "Blue", "Red", "Green", "Pink", "Grey", "Brown", "Navy", "Beige"]
SIZES_MAP = {
    "Women Ethnic": ["S", "M", "L", "XL", "XXL", "Free Size"],
    "Women Western": ["S", "M", "L", "XL", "28", "30", "32"],
    "Men": ["S", "M", "L", "XL", "XXL", "38", "40", "42"],
    "Kids": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"],
    "Mobiles & Tablets": ["64GB", "128GB", "256GB"],
    "Electronics": ["Standard"],
    "Home & Kitchen": ["Standard", "Small", "Medium", "Large"],
    "Beauty & Health": ["Standard"],
    "Bags & Footwear": ["6", "7", "8", "9", "10", "Standard"]
}

SELLERS = [
    "Fashion Hub", "Style Store", "Ethnic Corner", "Modern Shop", "Quality Mart",
    "Best Deals", "Premium Store", "Value Shop", "Top Seller", "Elite Store"
]

async def generate_products(category_name, count=100):
    products = []
    category_data = PRODUCT_DATA[category_name]
    templates = category_data["templates"]
    
    for i in range(count):
        template = random.choice(templates)
        
        # Add variant prefix
        variants = ["Premium", "Designer", "Classic", "Stylish", "Elite", "Luxury", "Modern", ""]
        variant = random.choice(variants)
        name = f"{variant} {template['name']}" if variant else template['name']
        
        # Price calculation
        original_price = random.randint(template['price_range'][0], template['price_range'][1])
        discount = random.choice([60, 65, 70, 75, 80])
        price = int(original_price * (100 - discount) / 100)
        
        # Ratings
        rating = round(random.uniform(3.8, 5.0), 1)
        reviews = random.randint(100, 5000)
        
        # Colors and sizes
        num_colors = random.randint(3, 5)
        selected_colors = random.sample(COLORS, min(num_colors, len(COLORS)))
        
        size_options = SIZES_MAP[category_name]
        num_sizes = random.randint(1, min(3, len(size_options)))
        selected_sizes = random.sample(size_options, num_sizes) if len(size_options) > 1 else size_options
        
        product = {
            "name": name,
            "price": price,
            "original_price": original_price,
            "discount": discount,
            "rating": rating,
            "reviews": reviews,
            "image": category_data["image"],
            "category": category_name,
            "sizes": selected_sizes,
            "colors": selected_colors,
            "description": f"High-quality {name.lower()} with premium finish. Perfect for {random.choice(category_data['occasions']).lower()}. Made from {random.choice(category_data['materials']).lower()}. Durable and long-lasting product.",
            "free_delivery": random.choice([True, True, True, False]),
            "cod": True,
            "seller_name": random.choice(SELLERS),
            "return_policy": random.choice(["7 days return", "10 days return"]),
            "stock": random.randint(50, 500),
            "material": random.choice(category_data['materials']),
            "occasion": random.choice(category_data['occasions']),
            "care_instructions": random.choice([
                "Handle with care", "Machine wash cold", "Hand wash only",
                "Dry clean only", "Wipe with dry cloth"
            ])
        }
        
        products.append(Product(**product).model_dump())
    
    return products

async def generate_reviews(products):
    reviews = []
    review_texts = {
        5: [
            "Excellent quality! Exactly as shown. Highly recommended!",
            "Amazing product! Worth every penny.",
            "Superb quality. Very satisfied with purchase.",
            "Perfect! Better than expected.",
            "Outstanding quality! Loved it."
        ],
        4: [
            "Very good quality. Satisfied.",
            "Good product at this price.",
            "Nice product. Good quality.",
            "Good purchase. Happy with it.",
            "Pretty good. Meets expectations."
        ],
        3: [
            "Product is okay. Average quality.",
            "Decent product. Could be better.",
            "It's good but not great.",
            "Average quality. Fair deal."
        ]
    }
    
    names = [
        "Priya S", "Rahul K", "Anjali P", "Vikram M", "Neha G",
        "Amit S", "Pooja R", "Arjun M", "Divya I", "Rohan V"
    ]
    
    for product in products:
        num_reviews = min(random.randint(20, 100), product["reviews"])
        
        for _ in range(num_reviews):
            rating = random.choices([5, 4, 3], weights=[0.6, 0.3, 0.1])[0]
            
            review = {
                "id": str(uuid.uuid4()),
                "product_id": product["id"],
                "user_name": random.choice(names),
                "rating": rating,
                "review": random.choice(review_texts[rating]),
                "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 200))).isoformat(),
                "verified_purchase": random.choice([True, True, True, False])
            }
            reviews.append(review)
    
    return reviews

async def seed_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🚀 Starting database seeding with proper image matching...")
    
    # Clear existing data
    await db.products.delete_many({})
    await db.categories.delete_many({})
    await db.reviews.delete_many({})
    print("🗑️  Cleared existing data")
    
    # Seed categories
    categories = [
        {"name": "Women Ethnic", "icon": "Shirt", "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400"},
        {"name": "Women Western", "icon": "Shirt", "image": "https://images.unsplash.com/photo-1515886657613-9f3515b0c78f?w=400"},
        {"name": "Men", "icon": "User", "image": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=400"},
        {"name": "Kids", "icon": "Baby", "image": "https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=400"},
        {"name": "Mobiles & Tablets", "icon": "Smartphone", "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"},
        {"name": "Electronics", "icon": "Headphones", "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400"},
        {"name": "Home & Kitchen", "icon": "Home", "image": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400"},
        {"name": "Beauty & Health", "icon": "Sparkles", "image": "https://images.unsplash.com/photo-1522335789203-aabd1fc54bc9?w=400"},
        {"name": "Bags & Footwear", "icon": "ShoppingBag", "image": "https://images.unsplash.com/photo-1491553895911-0055eca6402d?w=400"}
    ]
    
    category_docs = [Category(**cat).model_dump() for cat in categories]
    await db.categories.insert_many(category_docs)
    print(f"✓ Seeded {len(categories)} categories")
    
    # Generate products
    all_products = []
    for category in categories:
        print(f"⏳ Generating 100 products for {category['name']}...")
        products = await generate_products(category["name"], 100)
        all_products.extend(products)
        print(f"✓ Generated 100 products for {category['name']}")
    
    # Insert products in batches
    batch_size = 100
    for i in range(0, len(all_products), batch_size):
        batch = all_products[i:i+batch_size]
        await db.products.insert_many(batch)
    
    print(f"✅ Seeded {len(all_products)} products")
    
    # Generate reviews
    print("⏳ Generating reviews...")
    reviews = await generate_reviews(all_products)
    
    # Insert reviews in batches
    for i in range(0, len(reviews), 500):
        batch = reviews[i:i+500]
        await db.reviews.insert_many(batch)
    
    print(f"✅ Seeded {len(reviews)} reviews")
    
    client.close()
    
    print("\n" + "="*70)
    print("🎉 DATABASE SEEDING COMPLETED!")
    print("="*70)
    print(f"📦 Categories: {len(categories)}")
    print(f"🛍️  Products: {len(all_products)}")
    print(f"⭐ Reviews: {len(reviews)}")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(seed_database())
