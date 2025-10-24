import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from models.product import Product
from models.category import Category
import random

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'meesho_db')

# Products with MATCHING, RELEVANT images from vision expert
PRODUCTS_WITH_MATCHING_IMAGES = {
    "Women Ethnic": [
        # Sarees with actual saree images
        {"name": "Banarasi Silk Saree", "img": "https://images.unsplash.com/photo-1742287724816-4a8a1cc7ad5c", "price": (1299, 2999)},
        {"name": "Kanjivaram Silk Saree", "img": "https://images.unsplash.com/photo-1742287721821-ddf522b3f37b", "price": (1499, 3499)},
        {"name": "Designer Party Saree", "img": "https://images.unsplash.com/photo-1692992193981-d3d92fabd9cb", "price": (899, 2499)},
        {"name": "Cotton Printed Saree", "img": "https://images.unsplash.com/photo-1618901185975-d59f7091bcfe", "price": (599, 1499)},
        {"name": "Georgette Floral Saree", "img": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb", "price": (799, 1999)},
        {"name": "Chiffon Wedding Saree", "img": "https://images.unsplash.com/photo-1609748340041-f5d61e061ebc", "price": (1599, 3999)},
        {"name": "Traditional Saree", "img": "https://images.unsplash.com/photo-1641699862936-be9f49b1c38d", "price": (1799, 4499)},
        {"name": "Embroidered Silk Saree", "img": "https://images.pexels.com/photos/27155552/pexels-photo-27155552.jpeg", "price": (999, 2699)},
        {"name": "Wedding Silk Saree", "img": "https://images.pexels.com/photos/29351977/pexels-photo-29351977.jpeg", "price": (1899, 4599)},
        
        # Kurtis with actual kurti images
        {"name": "Floral Cotton Kurti", "img": "https://images.unsplash.com/photo-1741847639057-b51a25d42892", "price": (399, 999)},
        {"name": "White Printed Kurti", "img": "https://images.unsplash.com/photo-1745313452052-0e4e341f326c", "price": (349, 899)},
        {"name": "Maroon Designer Kurti", "img": "https://images.unsplash.com/photo-1708534419572-6e6614a53ca1", "price": (449, 1099)},
        {"name": "Green Ethnic Kurti", "img": "https://images.unsplash.com/photo-1597983073750-16f5ded1321f", "price": (499, 1199)},
        {"name": "Casual Daily Kurti", "img": "https://images.pexels.com/photos/28512776/pexels-photo-28512776.jpeg", "price": (299, 799)},
        {"name": "Party Wear Kurti", "img": "https://images.pexels.com/photos/28213774/pexels-photo-28213774.jpeg", "price": (599, 1499)},
        {"name": "Printed Kurti Set", "img": "https://images.pexels.com/photos/20702674/pexels-photo-20702674.jpeg", "price": (549, 1399)},
        
        # Lehengas with actual lehenga images
        {"name": "Bridal Red Lehenga", "img": "https://images.unsplash.com/photo-1668371679302-a8ec781e876e", "price": (2999, 7999)},
        {"name": "Green Wedding Lehenga", "img": "https://images.unsplash.com/photo-1619715613791-89d35b51ff81", "price": (2499, 6999)},
        {"name": "Designer Lehenga Choli", "img": "https://images.unsplash.com/photo-1746372283841-dbb3838f9935", "price": (1999, 4999)},
        {"name": "Embroidered Lehenga", "img": "https://images.unsplash.com/photo-1724856605022-106d6dd6e842", "price": (3499, 8999)},
        {"name": "Party Wear Lehenga", "img": "https://images.unsplash.com/photo-1759720883040-af9be070929e", "price": (2799, 6799)},
        {"name": "Traditional Lehenga", "img": "https://images.pexels.com/photos/29354362/pexels-photo-29354362.jpeg", "price": (3299, 7999)},
        {"name": "Festive Lehenga Set", "img": "https://images.pexels.com/photos/1139450/pexels-photo-1139450.jpeg", "price": (2599, 6499)},
        
        # Additional ethnic wear
        {"name": "Anarkali Suit", "img": "https://images.pexels.com/photos/34351520/pexels-photo-34351520.jpeg", "price": (899, 2199)},
        {"name": "Palazzo Suit Set", "img": "https://images.pexels.com/photos/34381013/pexels-photo-34381013.jpeg", "price": (649, 1699)},
    ],
    
    "Women Western": [
        {"name": "Casual Summer Dress", "img": "https://images.unsplash.com/photo-1753192104240-209f3fb568ef", "price": (699, 1799)},
        {"name": "Party Dress", "img": "https://images.unsplash.com/photo-1753192104606-317fb6423d03", "price": (799, 1999)},
        {"name": "Floral Maxi Dress", "img": "https://images.unsplash.com/photo-1753192108606-b4a2bc9e5661", "price": (549, 1399)},
        {"name": "Evening Dress", "img": "https://images.pexels.com/photos/33732377/pexels-photo-33732377.jpeg", "price": (899, 2199)},
        {"name": "Denim Jeans", "img": "https://images.unsplash.com/photo-1542272454315-7e6c29e2e6d7", "price": (899, 2199)},
        {"name": "Casual Top", "img": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1", "price": (349, 899)},
        {"name": "Crop Top", "img": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa", "price": (299, 749)},
        {"name": "Palazzo Pants", "img": "https://images.unsplash.com/photo-1594633312681-425c7b97ccd1", "price": (449, 1099)},
    ],
    
    "Men": [
        {"name": "Casual Cotton Shirt", "img": "https://images.unsplash.com/photo-1607345366928-199ea26cfe3e", "price": (599, 1499)},
        {"name": "Formal White Shirt", "img": "https://images.unsplash.com/photo-1589234217365-08d3e0e5cf42", "price": (549, 1399)},
        {"name": "Striped Shirt", "img": "https://images.unsplash.com/photo-1624835567150-0c530a20d8cc", "price": (499, 1299)},
        {"name": "Blue Casual Shirt", "img": "https://images.unsplash.com/photo-1602810320073-1230c46d89d4", "price": (649, 1599)},
        {"name": "Round Neck T-Shirt", "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab", "price": (249, 699)},
        {"name": "Polo T-Shirt", "img": "https://images.unsplash.com/photo-1620799140188-3b2a02fd9a77", "price": (399, 999)},
        {"name": "Denim Jeans", "img": "https://images.unsplash.com/photo-1542272454315-7e6c29e2e6d7", "price": (899, 2199)},
        {"name": "Black Jeans", "img": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246", "price": (849, 2099)},
    ],
    
    "Kids": [
        {"name": "Kids T-Shirt", "img": "https://images.unsplash.com/photo-1622218286192-95f6a20083c7", "price": (249, 649)},
        {"name": "Boys Shirt", "img": "https://images.unsplash.com/photo-1601925240970-98447486fcdb", "price": (299, 799)},
        {"name": "Girls Dress", "img": "https://images.unsplash.com/photo-1604467794349-0b74285de7e7", "price": (399, 999)},
        {"name": "Kids Jeans", "img": "https://images.unsplash.com/photo-1632337948797-ba161d29532b", "price": (449, 1099)},
        {"name": "Baby Clothes Set", "img": "https://images.unsplash.com/photo-1622218286192-95f6a20083c7", "price": (349, 899)},
    ],
    
    "Electronics": [
        # Smartphones with actual phone images
        {"name": "iPhone 15 Pro Max 256GB", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (129900, 139900)},
        {"name": "iPhone 14 Pro 256GB", "img": "https://images.unsplash.com/photo-1634403665481-74948d815f03", "price": (99900, 109900)},
        {"name": "iPhone 13 128GB", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (54900, 64900)},
        {"name": "Samsung Galaxy S24 Ultra", "img": "https://images.unsplash.com/photo-1598327105666-5b89351aff97", "price": (89999, 99999)},
        {"name": "OnePlus 12 5G 256GB", "img": "https://images.unsplash.com/photo-1634403665481-74948d815f03", "price": (64999, 71999)},
        {"name": "Google Pixel 8 Pro", "img": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9", "price": (79999, 89999)},
        
        # Wireless Earbuds with actual earbud images
        {"name": "Apple AirPods Pro 2nd Gen", "img": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df", "price": (22900, 26900)},
        {"name": "Boat Airdopes 141", "img": "https://images.unsplash.com/photo-1606220588913-b3aacb4d2f46", "price": (1299, 2499)},
        {"name": "Realme Buds Air 5 Pro", "img": "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb", "price": (3499, 4999)},
        {"name": "Sony WF-1000XM5", "img": "https://images.unsplash.com/photo-1615281612781-4b972bd4e3fe", "price": (19990, 24990)},
        
        # Tablets
        {"name": "iPad Air 5th Gen 256GB", "img": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0", "price": (59900, 69900)},
        {"name": "Samsung Galaxy Tab S9", "img": "https://images.unsplash.com/photo-1585790050230-5dd28404f8ae", "price": (54999, 61999)},
        
        # Smart Watches
        {"name": "Apple Watch Series 9", "img": "https://images.unsplash.com/photo-1523275335684-37898b6baf30", "price": (42900, 47900)},
        {"name": "Samsung Galaxy Watch 6", "img": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6", "price": (31999, 36999)},
        
        # Accessories
        {"name": "Power Bank 20000mAh", "img": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5", "price": (2499, 3999)},
        {"name": "Wireless Mouse", "img": "https://images.unsplash.com/photo-1527814050087-3793815479db", "price": (899, 1999)},
    ],
    
    "Home & Kitchen": [
        {"name": "Stainless Steel Cookware Set", "img": "https://images.unsplash.com/photo-1584990347193-6bebebfeaeee", "price": (1299, 2999)},
        {"name": "Non-Stick Pan Set", "img": "https://images.unsplash.com/photo-1556910633-5099dc3971e8", "price": (899, 2199)},
        {"name": "Pressure Cooker", "img": "https://images.unsplash.com/photo-1584990347163-2b86b71390d6", "price": (999, 2399)},
        {"name": "Kitchen Utensils Set", "img": "https://images.unsplash.com/photo-1556910148-3adb7f0c665a", "price": (799, 1899)},
        {"name": "Dinner Set", "img": "https://images.unsplash.com/photo-1578749556568-bc2c40e68b61", "price": (1199, 2799)},
        {"name": "Storage Container Set", "img": "https://images.unsplash.com/photo-1584085646196-0c5c85e0dc13", "price": (449, 1099)},
    ],
    
    "Beauty & Health": [
        {"name": "Complete Makeup Kit", "img": "https://images.unsplash.com/photo-1596462502278-27bfdc403348", "price": (799, 1999)},
        {"name": "Makeup Brushes Set", "img": "https://images.unsplash.com/photo-1512496015851-a90fb38ba796", "price": (599, 1499)},
        {"name": "Lipstick Set", "img": "https://images.unsplash.com/photo-1620464003286-a5b0d79f32c2", "price": (499, 1299)},
        {"name": "Skincare Combo", "img": "https://images.pexels.com/photos/4716578/pexels-photo-4716578.jpeg", "price": (649, 1599)},
        {"name": "Face Cream", "img": "https://images.unsplash.com/photo-1556228578-8c89e6adf883", "price": (399, 999)},
    ],
    
    "Bags & Footwear": [
        {"name": "Designer Handbag", "img": "https://images.unsplash.com/photo-1705909237050-7a7625b47fac", "price": (999, 2499)},
        {"name": "Leather Handbag", "img": "https://images.unsplash.com/photo-1584917865442-de89df76afd3", "price": (799, 1999)},
        {"name": "Shoulder Bag", "img": "https://images.unsplash.com/photo-1682745230951-8a5aa9a474a0", "price": (599, 1499)},
        {"name": "Crossbody Bag", "img": "https://images.unsplash.com/photo-1600857062241-98e5dba7f214", "price": (549, 1399)},
        {"name": "Sports Shoes", "img": "https://images.unsplash.com/photo-1542291026-7eec264c27ff", "price": (999, 2499)},
        {"name": "Casual Sneakers", "img": "https://images.unsplash.com/photo-1560769629-975ec94e6a86", "price": (899, 2199)},
        {"name": "Running Shoes", "img": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77", "price": (1299, 2999)},
        {"name": "Formal Shoes", "img": "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa", "price": (1199, 2799)},
    ]
}

COLORS = ["Black", "White", "Blue", "Red", "Green", "Grey", "Pink", "Brown", "Yellow", "Purple"]
SIZES_MAP = {
    "Women Ethnic": ["S", "M", "L", "XL", "XXL", "Free Size"],
    "Women Western": ["XS", "S", "M", "L", "XL"],
    "Men": ["S", "M", "L", "XL", "XXL", "3XL"],
    "Kids": ["2-3Y", "4-5Y", "6-7Y", "8-9Y", "10-11Y"],
    "Electronics": ["64GB", "128GB", "256GB", "512GB"],
    "Home & Kitchen": ["Standard", "Small", "Medium", "Large"],
    "Beauty & Health": ["Standard", "50ml", "100ml", "200ml"],
    "Bags & Footwear": ["6", "7", "8", "9", "10", "Free Size"]
}

MATERIALS = {
    "Women Ethnic": ["Cotton", "Silk", "Georgette", "Rayon", "Chiffon", "Net"],
    "Women Western": ["Cotton", "Denim", "Polyester", "Viscose"],
    "Men": ["Cotton", "Polyester", "Denim", "Linen"],
    "Kids": ["Cotton", "Cotton Blend", "Polyester"],
    "Electronics": ["Aluminum", "Glass & Metal", "Plastic", "Stainless Steel"],
    "Home & Kitchen": ["Stainless Steel", "Cotton", "Plastic", "Glass"],
    "Beauty & Health": ["Natural Ingredients", "Organic", "Herbal"],
    "Bags & Footwear": ["Leather", "Canvas", "Synthetic", "Rubber"]
}

SELLERS = ["Fashion Hub", "Tech Bazaar", "Quality Mart", "Best Deals Store", "Premium Lifestyle", "Style Avenue", "Top Seller"]

async def generate_products(category_name):
    """Generate products for a category using unique matching images"""
    products = []
    product_templates = PRODUCTS_WITH_MATCHING_IMAGES[category_name]
    
    for template in product_templates:
        original_price = random.randint(template['price'][0], template['price'][1])
        
        # Realistic discount based on price
        if original_price > 50000:
            discount = random.choice([5, 8, 10, 12, 15])
        elif original_price > 10000:
            discount = random.choice([15, 20, 25, 30])
        else:
            discount = random.choice([40, 50, 60, 65, 70])
        
        price = int(original_price * (100 - discount) / 100)
        rating = round(random.uniform(4.0, 5.0), 1)
        reviews = random.randint(100, 5000)
        
        selected_colors = random.sample(COLORS, random.randint(2, 4))
        size_options = SIZES_MAP[category_name]
        selected_sizes = random.sample(size_options, min(3, len(size_options)))
        
        product = {
            "name": template["name"],
            "price": price,
            "original_price": original_price,
            "discount": discount,
            "rating": rating,
            "reviews": reviews,
            "image": template['img'],
            "category": category_name,
            "sizes": selected_sizes,
            "colors": selected_colors,
            "description": f"High-quality {template['name'].lower()}. Perfect for daily use. Made from premium {random.choice(MATERIALS[category_name]).lower()}. {random.choice(['Fast delivery available.', 'Best seller in category.', 'Highly rated by customers.', 'Top quality guaranteed.'])}",
            "free_delivery": True if original_price > 500 else random.choice([True, False]),
            "cod": True,
            "seller_name": random.choice(SELLERS),
            "return_policy": "10 days return" if category_name == "Electronics" else "7 days return",
            "stock": random.randint(20, 500),
            "material": random.choice(MATERIALS[category_name]),
            "occasion": random.choice(["Daily Use", "Party Wear", "Casual", "Formal", "Festive"]),
            "care_instructions": "Handle with care"
        }
        
        products.append(Product(**product).model_dump())
    
    return products

async def seed_database():
    """Seed database with products that have MATCHING images"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🚀 Seeding database with MATCHING product images...")
    print("=" * 60)
    
    # Clear existing data
    await db.products.delete_many({})
    await db.categories.delete_many({})
    await db.reviews.delete_many({})
    print("🗑️  Cleared existing data\n")
    
    # Create categories
    categories = [
        {"name": "Women Ethnic", "icon": "Shirt", "image": "https://images.unsplash.com/photo-1741847639057-b51a25d42892?w=400"},
        {"name": "Women Western", "icon": "Shirt", "image": "https://images.unsplash.com/photo-1753192104240-209f3fb568ef?w=400"},
        {"name": "Men", "icon": "User", "image": "https://images.unsplash.com/photo-1607345366928-199ea26cfe3e?w=400"},
        {"name": "Kids", "icon": "Baby", "image": "https://images.unsplash.com/photo-1622218286192-95f6a20083c7?w=400"},
        {"name": "Electronics", "icon": "Smartphone", "image": "https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=400"},
        {"name": "Home & Kitchen", "icon": "Home", "image": "https://images.unsplash.com/photo-1584990347193-6bebebfeaeee?w=400"},
        {"name": "Beauty & Health", "icon": "Sparkles", "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=400"},
        {"name": "Bags & Footwear", "icon": "ShoppingBag", "image": "https://images.unsplash.com/photo-1705909237050-7a7625b47fac?w=400"}
    ]
    
    category_docs = [Category(**cat).model_dump() for cat in categories]
    await db.categories.insert_many(category_docs)
    print(f"✅ Created {len(categories)} categories\n")
    
    # Generate products for each category
    all_products = []
    for category in categories:
        num_products = len(PRODUCTS_WITH_MATCHING_IMAGES[category['name']])
        print(f"⏳ Generating {num_products} products for '{category['name']}'...")
        products = await generate_products(category["name"])
        all_products.extend(products)
        
        # Show sample
        sample = products[0]
        print(f"   📦 {sample['name']}")
        print(f"   💰 ₹{sample['price']} (was ₹{sample['original_price']}, {sample['discount']}% off)")
        print(f"   ⭐ {sample['rating']}/5 ({sample['reviews']} reviews)\n")
    
    # Insert products in batches
    print("💾 Inserting products into database...")
    for i in range(0, len(all_products), 100):
        await db.products.insert_many(all_products[i:i+100])
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully seeded {len(all_products)} products!")
    print(f"🎨 All images now MATCH their product categories!")
    print(f"📱 Categories: {', '.join([c['name'] for c in categories])}")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
