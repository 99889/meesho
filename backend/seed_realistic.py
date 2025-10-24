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

# Products with reliable images and realistic pricing
PRODUCTS_DATA = {
    "Women Ethnic": {
        "products": [
            {"name": "Cotton Kurti", "img": "https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg?w=500", "price": (299, 799)},
            {"name": "Silk Saree", "img": "https://images.pexels.com/photos/3400795/pexels-photo-3400795.jpeg?w=500", "price": (599, 1499)},
            {"name": "Anarkali Suit", "img": "https://images.pexels.com/photos/1813947/pexels-photo-1813947.jpeg?w=500", "price": (799, 1999)},
            {"name": "Palazzo Set", "img": "https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg?w=500", "price": (449, 999)},
            {"name": "Designer Kurti", "img": "https://images.pexels.com/photos/3400795/pexels-photo-3400795.jpeg?w=500", "price": (499, 1199)},
            {"name": "Ethnic Gown", "img": "https://images.pexels.com/photos/1813947/pexels-photo-1813947.jpeg?w=500", "price": (899, 2199)},
        ]
    },
    "Women Western": {
        "products": [
            {"name": "Casual Dress", "img": "https://images.pexels.com/photos/1055691/pexels-photo-1055691.jpeg?w=500", "price": (399, 999)},
            {"name": "Denim Jeans", "img": "https://images.pexels.com/photos/1082526/pexels-photo-1082526.jpeg?w=500", "price": (549, 1499)},
            {"name": "Party Dress", "img": "https://images.pexels.com/photos/1055691/pexels-photo-1055691.jpeg?w=500", "price": (699, 1799)},
            {"name": "Formal Top", "img": "https://images.pexels.com/photos/1082526/pexels-photo-1082526.jpeg?w=500", "price": (349, 899)},
            {"name": "Skirt", "img": "https://images.pexels.com/photos/1055691/pexels-photo-1055691.jpeg?w=500", "price": (299, 799)},
        ]
    },
    "Men": {
        "products": [
            {"name": "Casual Shirt", "img": "https://images.pexels.com/photos/297933/pexels-photo-297933.jpeg?w=500", "price": (399, 1099)},
            {"name": "Formal Shirt", "img": "https://images.pexels.com/photos/297933/pexels-photo-297933.jpeg?w=500", "price": (499, 1299)},
            {"name": "T-Shirt", "img": "https://images.pexels.com/photos/1192609/pexels-photo-1192609.jpeg?w=500", "price": (199, 599)},
            {"name": "Denim Jeans", "img": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg?w=500", "price": (699, 1899)},
            {"name": "Track Pants", "img": "https://images.pexels.com/photos/1192609/pexels-photo-1192609.jpeg?w=500", "price": (349, 899)},
        ]
    },
    "Kids": {
        "products": [
            {"name": "Kids T-Shirt", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg?w=500", "price": (199, 599)},
            {"name": "Girls Dress", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg?w=500", "price": (399, 999)},
            {"name": "Boys Shirt", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg?w=500", "price": (299, 799)},
            {"name": "Kids Jeans", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg?w=500", "price": (449, 1099)},
        ]
    },
    "Electronics": {
        "products": [
            # iPhones - REALISTIC PRICING
            {"name": "iPhone 14 Pro Max 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=500", "price": (109900, 129900)},
            {"name": "iPhone 14 Pro 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=500", "price": (99900, 119900)},
            {"name": "iPhone 14 128GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=500", "price": (69900, 79900)},
            {"name": "iPhone 13 128GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=500", "price": (54900, 64900)},
            {"name": "iPhone 13 Pro 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=500", "price": (89900, 99900)},
            {"name": "iPhone 12 64GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=500", "price": (42900, 49900)},
            {"name": "iPhone 12 Pro 128GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=500", "price": (74900, 84900)},
            {"name": "iPhone SE 64GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=500", "price": (38900, 44900)},
            
            # Android Phones - REALISTIC PRICING
            {"name": "Samsung Galaxy S23 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (64999, 74999)},
            {"name": "OnePlus 11 5G 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (54999, 61999)},
            {"name": "Samsung Galaxy A54 128GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (34999, 40999)},
            {"name": "Xiaomi 13 Pro 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (59999, 66999)},
            {"name": "Realme GT 2 Pro 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (44999, 49999)},
            {"name": "Vivo V27 Pro 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (34999, 39999)},
            {"name": "OPPO Reno 10 Pro 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (39999, 44999)},
            {"name": "Poco F5 5G 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (27999, 32999)},
            {"name": "Nothing Phone 2 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (42999, 47999)},
            {"name": "Motorola Edge 40 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg?w=500", "price": (29999, 34999)},
            
            # Tablets - REALISTIC PRICING
            {"name": "iPad Air 5th Gen 256GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg?w=500", "price": (59900, 69900)},
            {"name": "iPad 10th Gen 64GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg?w=500", "price": (39900, 44900)},
            {"name": "Samsung Galaxy Tab S9 256GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg?w=500", "price": (54999, 61999)},
            {"name": "Lenovo Tab P11 Plus 128GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg?w=500", "price": (19999, 24999)},
            
            # Audio - REALISTIC PRICING
            {"name": "Apple AirPods Pro 2nd Gen", "img": "https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg?w=500", "price": (22900, 26900)},
            {"name": "Sony WH-1000XM5 Headphones", "img": "https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg?w=500", "price": (29990, 34990)},
            {"name": "JBL Flip 6 Speaker", "img": "https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg?w=500", "price": (9999, 12999)},
            {"name": "Boat Airdopes 141", "img": "https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg?w=500", "price": (1299, 2499)},
            {"name": "Realme Buds Air 3", "img": "https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg?w=500", "price": (2499, 3999)},
            
            # Smart Watches - REALISTIC PRICING
            {"name": "Apple Watch Series 9 GPS", "img": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg?w=500", "price": (39900, 44900)},
            {"name": "Samsung Galaxy Watch 6", "img": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg?w=500", "price": (26999, 31999)},
            {"name": "Noise ColorFit Pro 4", "img": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg?w=500", "price": (2499, 4499)},
            {"name": "Fire-Boltt Phoenix Pro", "img": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg?w=500", "price": (1499, 2999)},
            
            # Accessories - REALISTIC PRICING
            {"name": "Anker PowerCore 20000mAh", "img": "https://images.pexels.com/photos/4195325/pexels-photo-4195325.jpeg?w=500", "price": (2499, 3999)},
            {"name": "Apple 20W USB-C Charger", "img": "https://images.pexels.com/photos/4195325/pexels-photo-4195325.jpeg?w=500", "price": (1700, 2199)},
            {"name": "Logitech MX Master 3", "img": "https://images.pexels.com/photos/4195325/pexels-photo-4195325.jpeg?w=500", "price": (8995, 10995)},
            {"name": "SanDisk 128GB USB Drive", "img": "https://images.pexels.com/photos/4195325/pexels-photo-4195325.jpeg?w=500", "price": (899, 1499)},
        ]
    },
    "Home & Kitchen": {
        "products": [
            {"name": "Cookware Set", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg?w=500", "price": (899, 2499)},
            {"name": "Dinner Set", "img": "https://images.pexels.com/photos/6489074/pexels-photo-6489074.jpeg?w=500", "price": (799, 1999)},
            {"name": "Bed Sheet", "img": "https://images.pexels.com/photos/1350789/pexels-photo-1350789.jpeg?w=500", "price": (549, 1399)},
            {"name": "Storage Box", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg?w=500", "price": (299, 899)},
            {"name": "Pressure Cooker", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg?w=500", "price": (899, 2299)},
        ]
    },
    "Beauty & Health": {
        "products": [
            {"name": "Makeup Kit", "img": "https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg?w=500", "price": (399, 1299)},
            {"name": "Skincare Set", "img": "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg?w=500", "price": (449, 1199)},
            {"name": "Hair Care", "img": "https://images.pexels.com/photos/3373736/pexels-photo-3373736.jpeg?w=500", "price": (349, 999)},
            {"name": "Face Cream", "img": "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg?w=500", "price": (249, 699)},
            {"name": "Lipstick Set", "img": "https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg?w=500", "price": (299, 899)},
        ]
    },
    "Bags & Footwear": {
        "products": [
            {"name": "Women Handbag", "img": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?w=500", "price": (449, 1499)},
            {"name": "Men Shoes", "img": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?w=500", "price": (599, 1999)},
            {"name": "Sports Shoes", "img": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?w=500", "price": (649, 2199)},
            {"name": "Backpack", "img": "https://images.pexels.com/photos/2905238/pexels-photo-2905238.jpeg?w=500", "price": (499, 1499)},
            {"name": "Wallet", "img": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?w=500", "price": (249, 799)},
        ]
    }
}

COLORS = ["Black", "White", "Blue", "Red", "Green", "Grey", "Pink", "Brown"]
SIZES_MAP = {
    "Women Ethnic": ["S", "M", "L", "XL", "XXL"],
    "Women Western": ["S", "M", "L", "XL"],
    "Men": ["S", "M", "L", "XL", "XXL"],
    "Kids": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"],
    "Electronics": ["64GB", "128GB", "256GB", "512GB"],
    "Home & Kitchen": ["Standard"],
    "Beauty & Health": ["Standard"],
    "Bags & Footwear": ["Standard", "6", "7", "8", "9", "10"]
}

MATERIALS = {
    "Women Ethnic": ["Cotton", "Silk", "Georgette", "Rayon"],
    "Women Western": ["Cotton", "Denim", "Polyester"],
    "Men": ["Cotton", "Polyester", "Denim"],
    "Kids": ["Cotton", "Cotton Blend"],
    "Electronics": ["Aluminum", "Glass & Metal", "Plastic"],
    "Home & Kitchen": ["Stainless Steel", "Cotton"],
    "Beauty & Health": ["Natural Ingredients"],
    "Bags & Footwear": ["Leather", "Canvas"]
}

SELLERS = ["Tech Store", "Fashion Hub", "Quality Mart", "Best Deals", "Premium Store", "Style Store", "Top Seller"]

async def generate_products(category_name, count=100):
    products = []
    product_list = PRODUCTS_DATA[category_name]["products"]
    products_per_type = count // len(product_list)
    
    for product_template in product_list:
        for i in range(products_per_type):
            # No discount for high-value items, small discount for medium, normal discount for cheap
            base_price = product_template["price"][0]
            max_price = product_template["price"][1]
            original_price = random.randint(base_price, max_price)
            
            # Realistic discount based on price
            if original_price > 50000:  # Premium items like iPhone
                discount = random.choice([5, 8, 10, 12])  # Small discount
                price = int(original_price * (100 - discount) / 100)
            elif original_price > 10000:  # Mid-range
                discount = random.choice([10, 15, 20, 25])
                price = int(original_price * (100 - discount) / 100)
            else:  # Budget items
                discount = random.choice([30, 40, 50, 60])
                price = int(original_price * (100 - discount) / 100)
            
            variant = random.choice(["", "Premium", "Classic", "Pro"]) if i % 4 == 0 else ""
            name = f"{variant} {product_template['name']}" if variant else product_template['name']
            
            rating = round(random.uniform(4.0, 5.0), 1)
            reviews = random.randint(150, 4500)
            
            num_colors = random.randint(2, 4)
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
                "image": product_template['img'],
                "category": category_name,
                "sizes": selected_sizes,
                "colors": selected_colors,
                "description": f"High-quality {name.lower()}. Premium product with excellent build quality. {random.choice(['Fast shipping available.', 'Best seller in category.', 'Highly rated by customers.'])}",
                "free_delivery": True if original_price > 500 else False,
                "cod": True,
                "seller_name": random.choice(SELLERS),
                "return_policy": "7 days return" if category_name != "Electronics" else "10 days return",
                "stock": random.randint(10, 200),
                "material": random.choice(MATERIALS[category_name]),
                "occasion": "Daily Use",
                "care_instructions": "Handle with care"
            }
            
            products.append(Product(**product).model_dump())
    
    # Fill remaining
    while len(products) < count:
        template = random.choice(product_list)
        original_price = random.randint(template["price"][0], template["price"][1])
        
        if original_price > 50000:
            discount = random.choice([5, 10, 12])
        elif original_price > 10000:
            discount = random.choice([15, 20, 25])
        else:
            discount = random.choice([40, 50, 60])
        
        price = int(original_price * (100 - discount) / 100)
        
        product = {
            "name": template['name'],
            "price": price,
            "original_price": original_price,
            "discount": discount,
            "rating": round(random.uniform(4.0, 5.0), 1),
            "reviews": random.randint(100, 3000),
            "image": template['img'],
            "category": category_name,
            "sizes": random.sample(SIZES_MAP[category_name], min(2, len(SIZES_MAP[category_name]))),
            "colors": random.sample(COLORS, 3),
            "description": f"Quality {template['name'].lower()}. Great product.",
            "free_delivery": True,
            "cod": True,
            "seller_name": random.choice(SELLERS),
            "return_policy": "7 days return",
            "stock": random.randint(20, 150),
            "material": random.choice(MATERIALS[category_name]),
            "occasion": "Daily Use",
            "care_instructions": "Handle with care"
        }
        products.append(Product(**product).model_dump())
    
    return products[:count]

async def seed_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🚀 Seeding with REALISTIC PRICING and WORKING IMAGES...")
    
    await db.products.delete_many({})
    await db.categories.delete_many({})
    print("🗑️  Cleared data")
    
    categories = [
        {"name": "Women Ethnic", "icon": "Shirt", "image": "https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg?w=400"},
        {"name": "Women Western", "icon": "Shirt", "image": "https://images.pexels.com/photos/1055691/pexels-photo-1055691.jpeg?w=400"},
        {"name": "Men", "icon": "User", "image": "https://images.pexels.com/photos/297933/pexels-photo-297933.jpeg?w=400"},
        {"name": "Kids", "icon": "Baby", "image": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg?w=400"},
        {"name": "Electronics", "icon": "Smartphone", "image": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?w=400"},
        {"name": "Home & Kitchen", "icon": "Home", "image": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg?w=400"},
        {"name": "Beauty & Health", "icon": "Sparkles", "image": "https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg?w=400"},
        {"name": "Bags & Footwear", "icon": "ShoppingBag", "image": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg?w=400"}
    ]
    
    category_docs = [Category(**cat).model_dump() for cat in categories]
    await db.categories.insert_many(category_docs)
    print(f"✓ Seeded {len(categories)} categories")
    
    all_products = []
    for category in categories:
        print(f"⏳ Generating 100 products for {category['name']}...")
        products = await generate_products(category["name"], 100)
        all_products.extend(products)
        
        # Show sample pricing
        if category['name'] == 'Electronics':
            sample = products[0]
            print(f"   📱 Sample: {sample['name']} - ₹{sample['price']} (was ₹{sample['original_price']}, {sample['discount']}% off)")
    
    for i in range(0, len(all_products), 100):
        await db.products.insert_many(all_products[i:i+100])
    
    print(f"\n✅ Seeded {len(all_products)} products!")
    print(f"💰 REALISTIC PRICING:")
    print(f"   • iPhones: ₹38,900 - ₹1,29,900")
    print(f"   • Android Phones: ₹27,999 - ₹74,999")
    print(f"   • Tablets: ₹19,999 - ₹69,900")
    print(f"   • Accessories: ₹899 - ₹34,990")
    print(f"🖼️  All images from Pexels (reliable & fast loading)")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
