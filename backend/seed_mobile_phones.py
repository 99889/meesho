import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from models.product import Product
import random

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'meesho_db')

# Comprehensive mobile phones list with realistic prices and images
MOBILE_PHONES = [
    # Budget Phones (₹5,000 - ₹15,000)
    {"name": "Redmi 13C 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (8999, 10999)},
    {"name": "Realme C55 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (9999, 11999)},
    {"name": "Poco M6 5G 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (9499, 11499)},
    {"name": "Samsung Galaxy M14 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (11999, 13999)},
    {"name": "Redmi 12 5G 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (10999, 12999)},
    {"name": "Realme Narzo 60 5G 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (12999, 14999)},
    {"name": "Poco C55 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (7999, 9999)},
    {"name": "Redmi A3 64GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (6999, 8499)},
    {"name": "Realme C53 64GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (8999, 10499)},
    {"name": "Samsung Galaxy F14 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (10999, 12999)},
    {"name": "Redmi Note 12 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (13999, 15999)},
    {"name": "Realme 11 5G 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (14999, 16999)},
    {"name": "Poco M6 Pro 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (12999, 14999)},
    {"name": "Motorola G54 5G 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (13999, 15999)},
    {"name": "Vivo T2x 5G 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (12999, 14999)},
    
    # Mid-Range Phones (₹15,000 - ₹40,000)
    {"name": "Samsung Galaxy A54 5G 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (34999, 40999)},
    {"name": "OnePlus Nord CE 3 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (26999, 31999)},
    {"name": "Vivo V29 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (36999, 41999)},
    {"name": "OPPO Reno 11 Pro 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (39999, 44999)},
    {"name": "Realme GT 3 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (42999, 47999)},
    {"name": "Nothing Phone 2 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (44999, 49999)},
    {"name": "Motorola Edge 50 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (31999, 36999)},
    {"name": "Samsung Galaxy M54 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (29999, 34999)},
    {"name": "Vivo V27 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (32999, 37999)},
    {"name": "OnePlus Nord 3 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (33999, 38999)},
    {"name": "OPPO Reno 10 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (35999, 40999)},
    {"name": "Realme 12 Pro Plus 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (28999, 33999)},
    {"name": "Poco X6 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (24999, 29999)},
    {"name": "Redmi Note 13 Pro Max 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (26999, 31999)},
    {"name": "Motorola Edge 40 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (27999, 32999)},
    {"name": "Samsung Galaxy A35 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (28999, 33999)},
    {"name": "Vivo T2 Pro 5G 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (22999, 27999)},
    {"name": "OnePlus Nord CE 2 5G 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (18999, 23999)},
    {"name": "Realme 11 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (24999, 29999)},
    {"name": "Poco F5 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (29999, 34999)},
    
    # Premium Flagship (₹40,000+)
    {"name": "iPhone 15 Pro Max 256GB", "img": "https://images.unsplash.com/photo-1634403665481-74948d815f03", "price": (129900, 139900)},
    {"name": "iPhone 15 Pro 128GB", "img": "https://images.unsplash.com/photo-1634403665481-74948d815f03", "price": (119900, 129900)},
    {"name": "iPhone 15 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (79900, 89900)},
    {"name": "iPhone 14 Pro Max 256GB", "img": "https://images.unsplash.com/photo-1634403665481-74948d815f03", "price": (109900, 119900)},
    {"name": "iPhone 14 Pro 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (99900, 109900)},
    {"name": "iPhone 14 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (69900, 79900)},
    {"name": "iPhone 13 Pro 256GB", "img": "https://images.unsplash.com/photo-1634403665481-74948d815f03", "price": (89900, 99900)},
    {"name": "iPhone 13 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (54900, 64900)},
    {"name": "iPhone 12 Pro 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (74900, 84900)},
    {"name": "iPhone 12 64GB", "img": "https://images.unsplash.com/photo-1634403665481-74948d815f03", "price": (42900, 49900)},
    {"name": "iPhone SE 3rd Gen 64GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (38900, 44900)},
    {"name": "iPhone 11 64GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (34900, 39900)},
    
    {"name": "Samsung Galaxy S24 Ultra 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (89999, 99999)},
    {"name": "Samsung Galaxy S23 Ultra 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (74999, 84999)},
    {"name": "Samsung Galaxy S23 Plus 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (64999, 74999)},
    {"name": "Samsung Galaxy S23 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (54999, 64999)},
    {"name": "OnePlus 12 5G 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (64999, 71999)},
    {"name": "OnePlus 11 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (54999, 61999)},
    {"name": "Google Pixel 8 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (79999, 89999)},
    {"name": "Google Pixel 8 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (59999, 69999)},
    {"name": "Xiaomi 14 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (64999, 71999)},
    {"name": "Xiaomi 13 Pro 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (54999, 61999)},
    {"name": "Vivo X100 Pro 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (69999, 79999)},
    {"name": "OPPO Find X7 Ultra 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (74999, 84999)},
    {"name": "Sony Xperia 1 V 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (89999, 99999)},
    
    # More Budget & Mid-Range Options
    {"name": "Redmi Note 12 Pro 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (20999, 25999)},
    {"name": "Realme 10 Pro Plus 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (19999, 24999)},
    {"name": "Samsung Galaxy M34 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (18999, 23999)},
    {"name": "Vivo Y100 5G 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (21999, 26999)},
    {"name": "OPPO F25 Pro 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (22999, 27999)},
    {"name": "Motorola G84 5G 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (17999, 22999)},
    {"name": "Poco X5 Pro 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (19999, 24999)},
    {"name": "Redmi 13 Pro 5G 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (18999, 23999)},
    {"name": "Realme Narzo 70 Pro 5G 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (16999, 21999)},
    {"name": "Samsung Galaxy F54 5G 256GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (25999, 30999)},
    
    # Entry Level
    {"name": "Redmi 12C 64GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (6999, 8999)},
    {"name": "Realme C33 64GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (7499, 9499)},
    {"name": "Poco C51 64GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (6499, 8499)},
    {"name": "Samsung Galaxy A04 64GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (7999, 9999)},
    {"name": "Motorola G32 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (8999, 10999)},
    {"name": "Redmi A2 32GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (5999, 7499)},
    {"name": "Realme C30s 32GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (6499, 7999)},
    {"name": "Lava Blaze 2 64GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (7999, 9499)},
    {"name": "Tecno Spark 10 Pro 128GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (9999, 11999)},
    {"name": "Infinix Hot 30 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (8999, 10999)},
]

COLORS = ["Black", "White", "Blue", "Silver", "Gold", "Green", "Purple", "Red"]
STORAGE_OPTIONS = ["64GB", "128GB", "256GB", "512GB", "1TB"]

async def seed_mobile_phones():
    """Add 70+ mobile phones to Electronics category"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("📱 Adding 70+ Mobile Phones to Database...")
    print("=" * 60)
    
    all_products = []
    
    for phone in MOBILE_PHONES:
        original_price = random.randint(phone['price'][0], phone['price'][1])
        
        # Realistic discounts based on price range
        if original_price > 50000:
            discount = random.choice([5, 8, 10, 12, 15])
        elif original_price > 20000:
            discount = random.choice([10, 15, 20, 25])
        else:
            discount = random.choice([15, 20, 25, 30])
        
        price = int(original_price * (100 - discount) / 100)
        rating = round(random.uniform(4.0, 5.0), 1)
        reviews_count = random.randint(500, 10000)
        
        # Determine RAM based on price
        if original_price > 50000:
            ram_options = ["8GB", "12GB", "16GB"]
        elif original_price > 20000:
            ram_options = ["6GB", "8GB", "12GB"]
        else:
            ram_options = ["4GB", "6GB", "8GB"]
        
        selected_colors = random.sample(COLORS, random.randint(3, 5))
        
        # Build description
        ram = random.choice(ram_options)
        storage = "128GB" if "128GB" in phone['name'] else ("256GB" if "256GB" in phone['name'] else "64GB")
        
        product = {
            "name": phone["name"],
            "price": price,
            "original_price": original_price,
            "discount": discount,
            "rating": rating,
            "reviews": reviews_count,
            "image": phone['img'],
            "category": "Electronics",
            "sizes": [storage],
            "colors": selected_colors,
            "description": f"{phone['name']} | {ram} RAM | {storage} Storage | 5G Network | Fast Charging | Premium Display | {random.choice(['50MP', '64MP', '108MP'])} Camera | Long Battery Life | Latest Android | In Stock",
            "free_delivery": True,
            "cod": True,
            "seller_name": random.choice(["Official Store", "Authorized Dealer", "Top Seller", "Premium Mobile Store"]),
            "return_policy": "10 days return",
            "stock": random.randint(20, 500),
            "material": "Glass & Metal",
            "occasion": "Daily Use",
            "care_instructions": "Handle with care, use screen protector"
        }
        
        all_products.append(Product(**product).model_dump())
    
    # Insert all phones
    if all_products:
        await db.products.insert_many(all_products)
    
    print(f"\n✅ Successfully added {len(all_products)} mobile phones!")
    print(f"📊 Price Range: ₹{min(p['price'] for p in all_products)} - ₹{max(p['price'] for p in all_products)}")
    print(f"📱 Budget: {len([p for p in all_products if p['price'] < 15000])} phones")
    print(f"📱 Mid-Range: {len([p for p in all_products if 15000 <= p['price'] < 40000])} phones")
    print(f"📱 Premium: {len([p for p in all_products if p['price'] >= 40000])} phones")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_mobile_phones())
