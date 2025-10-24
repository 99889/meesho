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

# Specific products with matching images
PRODUCTS_WITH_IMAGES = {
    "Women Ethnic": [
        {"name": "Cotton Kurti", "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500", "price": (299, 699)},
        {"name": "Silk Saree", "img": "https://images.unsplash.com/photo-1617396900799-f4ec2b43c7ae?w=500", "price": (599, 1499)},
        {"name": "Anarkali Gown", "img": "https://images.unsplash.com/photo-1583391733981-5edd0d5a4d52?w=500", "price": (799, 1999)},
        {"name": "Palazzo Suit", "img": "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=500", "price": (449, 899)},
        {"name": "Designer Kurti Set", "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500", "price": (499, 999)},
        {"name": "Lehenga Choli", "img": "https://images.unsplash.com/photo-1617396900799-f4ec2b43c7ae?w=500", "price": (999, 2499)},
        {"name": "Straight Kurti", "img": "https://images.unsplash.com/photo-1583391733981-5edd0d5a4d52?w=500", "price": (299, 599)},
        {"name": "Embroidered Saree", "img": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500", "price": (699, 1699)},
    ],
    "Women Western": [
        {"name": "Casual Dress", "img": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=500", "price": (399, 899)},
        {"name": "Denim Jeans", "img": "https://images.unsplash.com/photo-1542272454315-7e6c29e2e6d7?w=500", "price": (549, 1299)},
        {"name": "Formal Blazer", "img": "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=500", "price": (799, 1999)},
        {"name": "Party Dress", "img": "https://images.unsplash.com/photo-1566174053879-31528523f8ae?w=500", "price": (699, 1499)},
        {"name": "Palazzo Pants", "img": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1?w=500", "price": (349, 799)},
        {"name": "Crop Top", "img": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=500", "price": (249, 599)},
    ],
    "Men": [
        {"name": "Casual Shirt", "img": "https://images.unsplash.com/photo-1602810320073-1230c46d89d4?w=500", "price": (399, 999)},
        {"name": "Formal Shirt", "img": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=500", "price": (449, 1199)},
        {"name": "T-Shirt", "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500", "price": (199, 499)},
        {"name": "Denim Jeans", "img": "https://images.unsplash.com/photo-1542272454315-7e6c29e2e6d7?w=500", "price": (699, 1699)},
        {"name": "Track Pants", "img": "https://images.unsplash.com/photo-1506629082955-511b1aa562c8?w=500", "price": (349, 799)},
        {"name": "Polo Shirt", "img": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77?w=500", "price": (399, 899)},
    ],
    "Kids": [
        {"name": "T-Shirt Set", "img": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500", "price": (299, 699)},
        {"name": "Girls Dress", "img": "https://images.unsplash.com/photo-1518831959646-742c3a14ebf7?w=500", "price": (399, 899)},
        {"name": "Boys Shirt", "img": "https://images.unsplash.com/photo-1622290291468-a28f7a7dc6a8?w=500", "price": (299, 699)},
        {"name": "Kids Jeans", "img": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500", "price": (449, 999)},
    ],
    "Electronics": [
        # Mobiles & Tablets
        {"name": "iPhone 14 Pro 256GB", "img": "https://images.unsplash.com/photo-1678652197950-267e0c4c68e2?w=500", "price": (75999, 89999)},
        {"name": "iPhone 13 128GB", "img": "https://images.unsplash.com/photo-1632661674596-df8be070a5c5?w=500", "price": (55999, 64999)},
        {"name": "iPhone 12 64GB", "img": "https://images.unsplash.com/photo-1611472173362-3f53dbd65d80?w=500", "price": (45999, 52999)},
        {"name": "Smartphone 8GB RAM 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500", "price": (12999, 24999)},
        {"name": "Smartphone 6GB RAM 64GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500", "price": (8999, 15999)},
        {"name": "Smartphone 4GB RAM 64GB", "img": "https://images.unsplash.com/photo-1585060544812-6b45742d762f?w=500", "price": (6999, 11999)},
        {"name": "iPad 10th Gen", "img": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500", "price": (34999, 42999)},
        {"name": "Android Tablet 10 inch", "img": "https://images.unsplash.com/photo-1585790050230-5dd28404f8ae?w=500", "price": (9999, 16999)},
        {"name": "Gaming Phone 12GB RAM", "img": "https://images.unsplash.com/photo-1592286927505-2fd0660b149c?w=500", "price": (24999, 34999)},
        {"name": "Budget Smartphone 3GB", "img": "https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=500", "price": (4999, 7999)},
        
        # Audio Products
        {"name": "Wireless Earbuds", "img": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=500", "price": (449, 1999)},
        {"name": "Bluetooth Speaker", "img": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500", "price": (599, 2499)},
        {"name": "Headphones", "img": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500", "price": (699, 2499)},
        {"name": "Neckband", "img": "https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500", "price": (499, 1499)},
        
        # Accessories
        {"name": "Smart Watch", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500", "price": (799, 3999)},
        {"name": "Fitness Band", "img": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500", "price": (999, 2999)},
        {"name": "Power Bank 10000mAh", "img": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500", "price": (499, 1499)},
        {"name": "Phone Charger Fast 33W", "img": "https://images.unsplash.com/photo-1583863788434-e58a36330cf0?w=500", "price": (299, 899)},
        {"name": "USB Cable Set", "img": "https://images.unsplash.com/photo-1625948515291-69613efd103f?w=500", "price": (149, 499)},
        {"name": "Wireless Mouse", "img": "https://images.unsplash.com/photo-1527814050087-3793815479db?w=500", "price": (299, 999)},
        {"name": "Keyboard Wireless", "img": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500", "price": (399, 1499)},
        {"name": "Phone Case", "img": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=500", "price": (99, 499)},
    ],
    "Home & Kitchen": [
        {"name": "Cookware Set", "img": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=500", "price": (899, 2499)},
        {"name": "Dinner Set", "img": "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61?w=500", "price": (799, 1999)},
        {"name": "Bed Sheet Set", "img": "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?w=500", "price": (549, 1299)},
        {"name": "Storage Container", "img": "https://images.unsplash.com/photo-1584085646196-0c5c85e0dc13?w=500", "price": (399, 999)},
        {"name": "Pressure Cooker", "img": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=500", "price": (899, 2299)},
        {"name": "Non-stick Pan", "img": "https://images.unsplash.com/photo-1556910638-d1d01c4a4c5d?w=500", "price": (699, 1799)},
    ],
    "Beauty & Health": [
        {"name": "Makeup Kit", "img": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=500", "price": (399, 1299)},
        {"name": "Skincare Combo", "img": "https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=500", "price": (449, 1199)},
        {"name": "Hair Care Set", "img": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500", "price": (349, 999)},
        {"name": "Face Cream", "img": "https://images.unsplash.com/photo-1611930022073-b7a4ba5fcccd?w=500", "price": (249, 699)},
        {"name": "Lipstick Set", "img": "https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=500", "price": (299, 899)},
    ],
    "Bags & Footwear": [
        {"name": "Women Handbag", "img": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500", "price": (449, 1499)},
        {"name": "Men Casual Shoes", "img": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500", "price": (599, 1999)},
        {"name": "Sports Shoes", "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500", "price": (649, 2199)},
        {"name": "Backpack", "img": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500", "price": (499, 1499)},
        {"name": "Sandals", "img": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=500", "price": (299, 999)},
        {"name": "Wallet", "img": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=500", "price": (249, 799)},
    ]
}

COLORS = ["Black", "White", "Blue", "Red", "Green", "Pink", "Grey", "Brown"]
SIZES_MAP = {
    "Women Ethnic": ["S", "M", "L", "XL", "XXL"],
    "Women Western": ["S", "M", "L", "XL"],
    "Men": ["S", "M", "L", "XL", "XXL"],
    "Kids": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"],
    "Electronics": ["Standard", "64GB", "128GB", "256GB"],
    "Home & Kitchen": ["Standard"],
    "Beauty & Health": ["Standard"],
    "Bags & Footwear": ["Standard", "6", "7", "8", "9", "10"]
}

MATERIALS = {
    "Women Ethnic": ["Cotton", "Silk", "Georgette", "Rayon"],
    "Women Western": ["Cotton", "Denim", "Polyester"],
    "Men": ["Cotton", "Polyester", "Denim"],
    "Kids": ["Cotton", "Cotton Blend"],
    "Electronics": ["Metal & Glass", "Plastic", "Aluminum"],
    "Home & Kitchen": ["Stainless Steel", "Cotton", "Plastic"],
    "Beauty & Health": ["Natural Ingredients"],
    "Bags & Footwear": ["Leather", "Canvas", "Synthetic"]
}

SELLERS = ["Fashion Hub", "Style Store", "Quality Mart", "Best Deals", "Premium Store"]

async def generate_products(category_name, count=100):
    products = []
    templates = PRODUCTS_WITH_IMAGES[category_name]
    
    # Generate products based on templates
    products_per_template = count // len(templates)
    
    for template in templates:
        for i in range(products_per_template):
            variants = ["Premium", "Designer", "Classic", "Stylish", "Elite", "Modern", "Luxury", ""]
            variant = random.choice(variants) if i % 3 == 0 else ""
            name = f"{variant} {template['name']}" if variant else template['name']
            
            original_price = random.randint(template['price'][0], template['price'][1])
            discount = random.choice([60, 65, 70, 75, 80])
            price = int(original_price * (100 - discount) / 100)
            
            rating = round(random.uniform(3.8, 5.0), 1)
            reviews = random.randint(100, 5000)
            
            num_colors = random.randint(3, 5)
            selected_colors = random.sample(COLORS, num_colors)
            
            size_options = SIZES_MAP[category_name]
            selected_sizes = random.sample(size_options, min(3, len(size_options))) if len(size_options) > 1 else size_options
            
            product = {
                "name": name,
                "price": price,
                "original_price": original_price,
                "discount": discount,
                "rating": rating,
                "reviews": reviews,
                "image": template['img'],
                "category": category_name,
                "sizes": selected_sizes,
                "colors": selected_colors,
                "description": f"High-quality {name.lower()} with premium finish. Perfect for daily use. Made from {random.choice(MATERIALS[category_name]).lower()}.",
                "free_delivery": random.choice([True, True, True, False]),
                "cod": True,
                "seller_name": random.choice(SELLERS),
                "return_policy": "7 days return",
                "stock": random.randint(50, 500),
                "material": random.choice(MATERIALS[category_name]),
                "occasion": "Daily Use",
                "care_instructions": "Handle with care"
            }
            
            products.append(Product(**product).model_dump())
    
    # Fill remaining to reach count
    while len(products) < count:
        template = random.choice(templates)
        variant = random.choice(["", "Premium", "Designer"])
        name = f"{variant} {template['name']}" if variant else template['name']
        
        original_price = random.randint(template['price'][0], template['price'][1])
        discount = random.choice([60, 70, 75])
        price = int(original_price * (100 - discount) / 100)
        
        product = {
            "name": name,
            "price": price,
            "original_price": original_price,
            "discount": discount,
            "rating": round(random.uniform(3.9, 5.0), 1),
            "reviews": random.randint(100, 3000),
            "image": template['img'],
            "category": category_name,
            "sizes": random.sample(SIZES_MAP[category_name], min(2, len(SIZES_MAP[category_name]))),
            "colors": random.sample(COLORS, 3),
            "description": f"High-quality {name.lower()}. Premium product.",
            "free_delivery": True,
            "cod": True,
            "seller_name": random.choice(SELLERS),
            "return_policy": "7 days return",
            "stock": random.randint(50, 300),
            "material": random.choice(MATERIALS[category_name]),
            "occasion": "Daily Use",
            "care_instructions": "Handle with care"
        }
        products.append(Product(**product).model_dump())
    
    return products[:count]

async def seed_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🚀 Seeding with proper product images...")
    
    await db.products.delete_many({})
    await db.categories.delete_many({})
    await db.reviews.delete_many({})
    print("🗑️  Cleared data")
    
    categories = [
        {"name": "Women Ethnic", "icon": "Shirt", "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=400"},
        {"name": "Women Western", "icon": "Shirt", "image": "https://images.unsplash.com/photo-1595777457583-95e059d581b8?w=400"},
        {"name": "Men", "icon": "User", "image": "https://images.unsplash.com/photo-1602810320073-1230c46d89d4?w=400"},
        {"name": "Kids", "icon": "Baby", "image": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=400"},
        {"name": "Electronics", "icon": "Smartphone", "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400"},
        {"name": "Home & Kitchen", "icon": "Home", "image": "https://images.unsplash.com/photo-1556911220-bff31c812dba?w=400"},
        {"name": "Beauty & Health", "icon": "Sparkles", "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400"},
        {"name": "Bags & Footwear", "icon": "ShoppingBag", "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=400"}
    ]
    
    category_docs = [Category(**cat).model_dump() for cat in categories]
    await db.categories.insert_many(category_docs)
    print(f"✓ Seeded {len(categories)} categories")
    
    all_products = []
    for category in categories:
        print(f"⏳ Generating products for {category['name']}...")
        products = await generate_products(category["name"], 100)
        all_products.extend(products)
        print(f"✓ Generated {len(products)} products for {category['name']}")
    
    for i in range(0, len(all_products), 100):
        await db.products.insert_many(all_products[i:i+100])
    
    print(f"\n✅ Seeded {len(all_products)} products with proper images!")
    print(f"📱 Electronics includes: iPhones, Android phones, tablets, earbuds, speakers, smartwatches")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
