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

# Extended product data with reviews
async def seed_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
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
    
    # Comprehensive product data
    products_data = [
        # Women Ethnic (20 products)
        {
            "name": "Women Floral Print Kurti",
            "price": 299,
            "original_price": 999,
            "discount": 70,
            "rating": 4.2,
            "reviews": 1250,
            "image": "https://images.unsplash.com/photo-1732709470611-670308da8c5e?w=500",
            "category": "Women Ethnic",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["Red", "Blue", "Green", "Yellow", "Pink"],
            "description": "Beautiful floral print kurti perfect for casual and semi-formal occasions. Made from premium quality rayon fabric with intricate design. Comfortable fit with side slits for ease of movement.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Fashion Hub",
            "return_policy": "7 days return",
            "stock": 150,
            "material": "Pure Cotton",
            "occasion": "Casual, Festive",
            "care_instructions": "Machine wash cold, Do not bleach"
        },
        {
            "name": "Elegant Saree Collection",
            "price": 499,
            "original_price": 1999,
            "discount": 75,
            "rating": 4.5,
            "reviews": 2100,
            "image": "https://images.unsplash.com/photo-1740750047392-0d48b5fc23e4?w=500",
            "category": "Women Ethnic",
            "sizes": ["Free Size"],
            "colors": ["Pink", "Red", "Green", "Blue", "Maroon"],
            "description": "Traditional saree with modern design. Perfect for weddings and festivals. Premium silk blend fabric with beautiful embroidery work.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Ethnic Store",
            "return_policy": "7 days return",
            "stock": 80,
            "material": "Silk Blend",
            "occasion": "Wedding, Festival",
            "care_instructions": "Dry clean only"
        },
        {
            "name": "Designer Kurti Set with Palazzo",
            "price": 549,
            "original_price": 1899,
            "discount": 71,
            "rating": 4.3,
            "reviews": 1456,
            "image": "https://images.pexels.com/photos/34346734/pexels-photo-34346734.jpeg?w=500",
            "category": "Women Ethnic",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["Pink", "Blue", "Green", "White", "Yellow"],
            "description": "Designer kurti set with matching palazzo and dupatta. Premium fabric with beautiful prints. Complete ethnic wear set.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Ethnic Wear",
            "return_policy": "7 days return",
            "stock": 120,
            "material": "Rayon",
            "occasion": "Party, Casual",
            "care_instructions": "Hand wash recommended"
        },
        {
            "name": "Anarkali Gown with Dupatta",
            "price": 699,
            "original_price": 2499,
            "discount": 72,
            "rating": 4.4,
            "reviews": 987,
            "image": "https://images.unsplash.com/photo-1610030469983-98e550d6193c?w=500",
            "category": "Women Ethnic",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Red", "Blue", "Green", "Pink"],
            "description": "Stunning Anarkali gown with matching dupatta. Perfect for festive occasions and parties.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Royal Fashion",
            "return_policy": "7 days return",
            "stock": 60,
            "material": "Georgette",
            "occasion": "Party, Wedding",
            "care_instructions": "Dry clean preferred"
        },
        {
            "name": "Cotton Kurti with Embroidery",
            "price": 399,
            "original_price": 1299,
            "discount": 69,
            "rating": 4.1,
            "reviews": 1834,
            "image": "https://images.unsplash.com/photo-1583496661160-fb5886a0aaaa?w=500",
            "category": "Women Ethnic",
            "sizes": ["M", "L", "XL", "XXL"],
            "colors": ["White", "Cream", "Peach"],
            "description": "Pure cotton kurti with delicate embroidery work. Breathable and comfortable for daily wear.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Cotton House",
            "return_policy": "7 days return",
            "stock": 200,
            "material": "Pure Cotton",
            "occasion": "Daily Wear, Office",
            "care_instructions": "Machine wash"
        },
        {
            "name": "Traditional Lehenga Choli",
            "price": 899,
            "original_price": 3499,
            "discount": 74,
            "rating": 4.6,
            "reviews": 756,
            "image": "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?w=500",
            "category": "Women Ethnic",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Red", "Pink", "Green", "Blue"],
            "description": "Beautiful traditional lehenga choli with intricate work. Perfect for weddings and special occasions.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Bridal Collection",
            "return_policy": "7 days return",
            "stock": 45,
            "material": "Silk",
            "occasion": "Wedding, Festival",
            "care_instructions": "Dry clean only"
        },
        
        # Women Western (15 products)
        {
            "name": "Women Western Dress",
            "price": 399,
            "original_price": 1499,
            "discount": 73,
            "rating": 4.1,
            "reviews": 987,
            "image": "https://images.unsplash.com/photo-1445205170230-053b83016050?w=500",
            "category": "Women Western",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Black", "Red", "Blue", "Navy"],
            "description": "Trendy western dress for modern women. Perfect for parties and casual outings. Comfortable polyester fabric.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Fashion Store",
            "return_policy": "7 days return",
            "stock": 110,
            "material": "Polyester",
            "occasion": "Party, Casual",
            "care_instructions": "Machine wash cold"
        },
        {
            "name": "Women Denim Jeans",
            "price": 549,
            "original_price": 1899,
            "discount": 71,
            "rating": 4.3,
            "reviews": 2341,
            "image": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=500",
            "category": "Women Western",
            "sizes": ["28", "30", "32", "34", "36"],
            "colors": ["Blue", "Black", "Grey"],
            "description": "High-quality denim jeans with perfect fit. Stretchable and comfortable for all-day wear.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Denim World",
            "return_policy": "7 days return",
            "stock": 180,
            "material": "Denim",
            "occasion": "Casual, Daily Wear",
            "care_instructions": "Machine wash"
        },
        {
            "name": "Women Formal Blazer",
            "price": 799,
            "original_price": 2499,
            "discount": 68,
            "rating": 4.4,
            "reviews": 654,
            "image": "https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=500",
            "category": "Women Western",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Black", "Navy", "Grey"],
            "description": "Professional formal blazer for office wear. Premium quality fabric with perfect tailoring.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Professional Wear",
            "return_policy": "7 days return",
            "stock": 75,
            "material": "Polyester Blend",
            "occasion": "Office, Formal",
            "care_instructions": "Dry clean recommended"
        },
        
        # Men (20 products)
        {
            "name": "Men Casual Cotton Shirt",
            "price": 399,
            "original_price": 1299,
            "discount": 69,
            "rating": 4.0,
            "reviews": 890,
            "image": "https://images.unsplash.com/photo-1602810320073-1230c46d89d4?w=500",
            "category": "Men",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["White", "Blue", "Black", "Grey"],
            "description": "Premium cotton casual shirt for men. Comfortable and stylish for everyday wear. Breathable fabric perfect for all seasons.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "StyleMart",
            "return_policy": "7 days return",
            "stock": 200,
            "material": "Pure Cotton",
            "occasion": "Casual, Daily Wear",
            "care_instructions": "Machine wash"
        },
        {
            "name": "Men Formal Shirt",
            "price": 449,
            "original_price": 1499,
            "discount": 70,
            "rating": 4.4,
            "reviews": 1234,
            "image": "https://images.unsplash.com/photo-1729717949731-a2f4d6fcd8a1?w=500",
            "category": "Men",
            "sizes": ["38", "40", "42", "44", "46"],
            "colors": ["White", "Blue", "Black", "Grey", "Pink"],
            "description": "Premium formal shirt for office and business meetings. Wrinkle-free comfortable fabric. Perfect collar and fit.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Formal Hub",
            "return_policy": "7 days return",
            "stock": 180,
            "material": "Cotton Blend",
            "occasion": "Office, Formal",
            "care_instructions": "Machine wash or dry clean"
        },
        {
            "name": "Men Casual T-Shirt Pack of 3",
            "price": 399,
            "original_price": 1299,
            "discount": 69,
            "rating": 4.2,
            "reviews": 3456,
            "image": "https://images.unsplash.com/photo-1630435664004-8e6d54780dd8?w=500",
            "category": "Men",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["Black", "White", "Blue", "Grey", "Red"],
            "description": "Pack of 3 comfortable cotton t-shirts. Premium quality fabric that lasts long. Available in multiple colors.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Casual Store",
            "return_policy": "7 days return",
            "stock": 250,
            "material": "Cotton",
            "occasion": "Casual, Gym",
            "care_instructions": "Machine wash"
        },
        {
            "name": "Men Denim Jeans",
            "price": 699,
            "original_price": 2299,
            "discount": 70,
            "rating": 4.3,
            "reviews": 2187,
            "image": "https://images.unsplash.com/photo-1542272454315-7e6c29e2e6d7?w=500",
            "category": "Men",
            "sizes": ["30", "32", "34", "36", "38"],
            "colors": ["Blue", "Black", "Grey"],
            "description": "Premium quality denim jeans with perfect fit. Stretchable and comfortable. Durable fabric.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Jeans World",
            "return_policy": "7 days return",
            "stock": 160,
            "material": "Denim",
            "occasion": "Casual",
            "care_instructions": "Machine wash"
        },
        {
            "name": "Men Sports Track Pants",
            "price": 349,
            "original_price": 1199,
            "discount": 71,
            "rating": 4.1,
            "reviews": 1876,
            "image": "https://images.unsplash.com/photo-1571731956672-f2b94d7dd0cb?w=500",
            "category": "Men",
            "sizes": ["M", "L", "XL", "XXL"],
            "colors": ["Black", "Navy", "Grey"],
            "description": "Comfortable sports track pants for gym and outdoor activities. Breathable fabric with side pockets.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Sports Wear",
            "return_policy": "7 days return",
            "stock": 140,
            "material": "Polyester",
            "occasion": "Sports, Gym",
            "care_instructions": "Machine wash"
        },
        
        # Kids (10 products)
        {
            "name": "Kids Cotton T-Shirt Set",
            "price": 299,
            "original_price": 999,
            "discount": 70,
            "rating": 4.3,
            "reviews": 876,
            "image": "https://images.unsplash.com/photo-1519238263530-99bdd11df2ea?w=500",
            "category": "Kids",
            "sizes": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"],
            "colors": ["Multi"],
            "description": "Pack of 3 colorful cotton t-shirts for kids. Soft and comfortable fabric. Perfect for daily wear.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Kids Fashion",
            "return_policy": "7 days return",
            "stock": 120,
            "material": "Cotton",
            "occasion": "Casual, School",
            "care_instructions": "Machine wash"
        },
        {
            "name": "Kids Ethnic Wear Set",
            "price": 449,
            "original_price": 1499,
            "discount": 70,
            "rating": 4.4,
            "reviews": 654,
            "image": "https://images.unsplash.com/photo-1503944583220-79d8926ad5e2?w=500",
            "category": "Kids",
            "sizes": ["2-3Y", "4-5Y", "6-7Y", "8-9Y"],
            "colors": ["Red", "Blue", "Green"],
            "description": "Beautiful ethnic wear for kids. Perfect for festivals and special occasions.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Kids Ethnic",
            "return_policy": "7 days return",
            "stock": 80,
            "material": "Cotton Blend",
            "occasion": "Festival, Party",
            "care_instructions": "Hand wash"
        },
        
        # Home & Kitchen (15 products)
        {
            "name": "Kitchen Cookware Set - 7 Pieces",
            "price": 899,
            "original_price": 2999,
            "discount": 70,
            "rating": 4.2,
            "reviews": 1876,
            "image": "https://images.pexels.com/photos/279648/pexels-photo-279648.jpeg?w=500",
            "category": "Home & Kitchen",
            "sizes": ["Standard"],
            "colors": ["Silver", "Black"],
            "description": "Complete 7-piece kitchen cookware set. Non-stick coating, induction compatible. Includes frying pans, kadai, and sauce pans. Durable aluminum body.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Home Essentials",
            "return_policy": "7 days return",
            "stock": 90,
            "material": "Aluminum Non-stick",
            "occasion": "Daily Use",
            "care_instructions": "Hand wash recommended"
        },
        {
            "name": "Cotton Bed Sheet Set",
            "price": 549,
            "original_price": 1899,
            "discount": 71,
            "rating": 4.3,
            "reviews": 2341,
            "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?w=500",
            "category": "Home & Kitchen",
            "sizes": ["Double", "King"],
            "colors": ["White", "Blue", "Pink", "Grey"],
            "description": "Premium cotton bed sheet set with 2 pillow covers. Soft and comfortable. Easy to maintain.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Linen Store",
            "return_policy": "7 days return",
            "stock": 150,
            "material": "Cotton",
            "occasion": "Daily Use",
            "care_instructions": "Machine wash"
        },
        {
            "name": "Kitchen Storage Containers - Set of 12",
            "price": 399,
            "original_price": 1299,
            "discount": 69,
            "rating": 4.1,
            "reviews": 1567,
            "image": "https://images.unsplash.com/photo-1584085646196-0c5c85e0dc13?w=500",
            "category": "Home & Kitchen",
            "sizes": ["Standard"],
            "colors": ["Transparent"],
            "description": "Set of 12 airtight kitchen storage containers. BPA-free plastic. Perfect for organizing your kitchen.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Storage Solutions",
            "return_policy": "7 days return",
            "stock": 200,
            "material": "Plastic",
            "occasion": "Daily Use",
            "care_instructions": "Dishwasher safe"
        },
        
        # Beauty & Health (12 products)
        {
            "name": "Complete Makeup Kit - 24 Items",
            "price": 399,
            "original_price": 1599,
            "discount": 75,
            "rating": 4.3,
            "reviews": 2567,
            "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=500",
            "category": "Beauty & Health",
            "sizes": ["Standard"],
            "colors": ["Multi"],
            "description": "Complete professional makeup kit with 24 items. Includes eyeshadow palette, lipsticks, brushes, and more. Perfect for beginners and professionals.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Beauty Plus",
            "return_policy": "7 days return",
            "stock": 100,
            "material": "Cosmetic Grade",
            "occasion": "Daily Use, Party",
            "care_instructions": "Store in cool place"
        },
        {
            "name": "Skincare Combo - Complete Routine",
            "price": 449,
            "original_price": 1499,
            "discount": 70,
            "rating": 4.4,
            "reviews": 1890,
            "image": "https://images.unsplash.com/photo-1580870069867-74c57ee1bb07?w=500",
            "category": "Beauty & Health",
            "sizes": ["Standard"],
            "colors": ["Multi"],
            "description": "Complete skincare routine pack. Includes face wash, toner, serum, moisturizer, and sunscreen. Suitable for all skin types.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Beauty Care",
            "return_policy": "7 days return",
            "stock": 120,
            "material": "Dermatologist Tested",
            "occasion": "Daily Use",
            "care_instructions": "Keep away from sunlight"
        },
        {
            "name": "Hair Care Combo Set",
            "price": 349,
            "original_price": 1199,
            "discount": 71,
            "rating": 4.2,
            "reviews": 1456,
            "image": "https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=500",
            "category": "Beauty & Health",
            "sizes": ["Standard"],
            "colors": ["Multi"],
            "description": "Complete hair care set with shampoo, conditioner, hair oil, and serum. Strengthens and nourishes hair.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Hair Care Pro",
            "return_policy": "7 days return",
            "stock": 140,
            "material": "Natural Ingredients",
            "occasion": "Daily Use",
            "care_instructions": "Store in cool place"
        },
        
        # Electronics (10 products)
        {
            "name": "Wireless Bluetooth Earbuds",
            "price": 449,
            "original_price": 1999,
            "discount": 78,
            "rating": 4.1,
            "reviews": 3456,
            "image": "https://images.pexels.com/photos/1599791/pexels-photo-1599791.jpeg?w=500",
            "category": "Electronics",
            "sizes": ["Standard"],
            "colors": ["Black", "White"],
            "description": "High-quality wireless earbuds with 20 hours battery life. Crystal clear sound, touch controls, and IPX5 water resistance.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Tech Store",
            "return_policy": "7 days return",
            "stock": 180,
            "material": "ABS Plastic",
            "occasion": "Daily Use",
            "care_instructions": "Keep away from water"
        },
        {
            "name": "Wireless Bluetooth Speaker",
            "price": 599,
            "original_price": 2499,
            "discount": 76,
            "rating": 4.3,
            "reviews": 2187,
            "image": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500",
            "category": "Electronics",
            "sizes": ["Standard"],
            "colors": ["Black", "Blue", "Red"],
            "description": "Portable wireless speaker with powerful bass. 10 hours playback time. Perfect for parties.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Audio World",
            "return_policy": "7 days return",
            "stock": 120,
            "material": "ABS Plastic",
            "occasion": "Party, Travel",
            "care_instructions": "Handle with care"
        },
        {
            "name": "Smart Watch Fitness Tracker",
            "price": 799,
            "original_price": 2999,
            "discount": 73,
            "rating": 4.2,
            "reviews": 1876,
            "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500",
            "category": "Electronics",
            "sizes": ["Standard"],
            "colors": ["Black", "Silver"],
            "description": "Smart fitness watch with heart rate monitor, sleep tracking, and 15 sports modes. Water resistant.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Wearables Pro",
            "return_policy": "7 days return",
            "stock": 90,
            "material": "Silicone & Metal",
            "occasion": "Daily Use, Sports",
            "care_instructions": "Avoid extreme temperatures"
        },
        
        # Bags & Footwear (10 products)
        {
            "name": "Women Handbag - Premium Quality",
            "price": 449,
            "original_price": 1499,
            "discount": 70,
            "rating": 4.3,
            "reviews": 1567,
            "image": "https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=500",
            "category": "Bags & Footwear",
            "sizes": ["Standard"],
            "colors": ["Black", "Brown", "Beige"],
            "description": "Stylish women's handbag with multiple compartments. Premium quality leather finish. Perfect for daily use.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Bag House",
            "return_policy": "7 days return",
            "stock": 130,
            "material": "PU Leather",
            "occasion": "Daily Use, Office",
            "care_instructions": "Wipe with dry cloth"
        },
        {
            "name": "Men Casual Shoes",
            "price": 599,
            "original_price": 1999,
            "discount": 70,
            "rating": 4.2,
            "reviews": 2341,
            "image": "https://images.unsplash.com/photo-1549298916-b41d501d3772?w=500",
            "category": "Bags & Footwear",
            "sizes": ["6", "7", "8", "9", "10"],
            "colors": ["Black", "Brown", "Blue"],
            "description": "Comfortable casual shoes for men. Breathable material with cushioned sole. Perfect for everyday wear.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Footwear Store",
            "return_policy": "7 days return",
            "stock": 150,
            "material": "Canvas & Rubber",
            "occasion": "Casual",
            "care_instructions": "Wipe with damp cloth"
        },
        {
            "name": "Women Sports Shoes",
            "price": 649,
            "original_price": 2199,
            "discount": 71,
            "rating": 4.4,
            "reviews": 1876,
            "image": "https://images.unsplash.com/photo-1605348532760-6753d2c43329?w=500",
            "category": "Bags & Footwear",
            "sizes": ["5", "6", "7", "8", "9"],
            "colors": ["White", "Black", "Pink"],
            "description": "Lightweight sports shoes for women. Perfect for gym, running, and outdoor activities. Breathable mesh upper.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Sports Footwear",
            "return_policy": "7 days return",
            "stock": 140,
            "material": "Mesh & Synthetic",
            "occasion": "Sports, Gym",
            "care_instructions": "Hand wash"
        }
    ]
    
    product_docs = [Product(**prod).model_dump() for prod in products_data]
    await db.products.insert_many(product_docs)
    print(f"✓ Seeded {len(products_data)} products")
    
    # Generate reviews for products
    review_texts = {
        "positive": [
            "Excellent quality! Exactly as shown in pictures.",
            "Very satisfied with the purchase. Highly recommended!",
            "Good product at this price point. Value for money.",
            "Great quality and fast delivery. Will buy again.",
            "Perfect fit and nice material. Happy with the purchase.",
            "Superb quality! Better than expected.",
            "Amazing product! Love it.",
            "Good quality product. Satisfied with the purchase.",
            "Nice product, good packaging. Recommended!",
            "Worth the price. Good quality material."
        ],
        "neutral": [
            "Product is okay. Average quality.",
            "Decent product for the price.",
            "It's good but not great.",
            "Product matches description. Fair purchase.",
            "Average quality. Could be better."
        ],
        "negative": [
            "Not as expected. Quality could be better.",
            "Product is okay but delivery was delayed.",
            "Size is not perfect. Had to exchange."
        ]
    }
    
    reviewer_names = [
        "Priya Sharma", "Rahul Kumar", "Anjali Patel", "Vikram Singh", "Neha Gupta",
        "Amit Shah", "Pooja Reddy", "Arjun Mehta", "Divya Iyer", "Rohan Verma",
        "Kavita Joshi", "Sanjay Pandey", "Ritu Agarwal", "Manoj Desai", "Sneha Nair"
    ]
    
    reviews = []
    for product in product_docs:
        num_reviews = min(product["reviews"], 50)  # Generate up to 50 reviews per product
        for i in range(num_reviews):
            rating = random.choice([3, 4, 4, 4, 5, 5, 5])  # More positive ratings
            if rating >= 4:
                review_text = random.choice(review_texts["positive"])
            elif rating == 3:
                review_text = random.choice(review_texts["neutral"])
            else:
                review_text = random.choice(review_texts["negative"])
            
            review = {
                "id": str(uuid.uuid4()),
                "product_id": product["id"],
                "user_name": random.choice(reviewer_names),
                "rating": rating,
                "review": review_text,
                "created_at": (datetime.utcnow() - timedelta(days=random.randint(1, 180))).isoformat(),
                "verified_purchase": random.choice([True, True, True, False])  # 75% verified
            }
            reviews.append(review)
    
    if reviews:
        await db.reviews.insert_many(reviews)
        print(f"✓ Seeded {len(reviews)} product reviews")
    
    client.close()
    print("\n✅ Database seeded successfully with enhanced products and reviews!")

if __name__ == "__main__":
    asyncio.run(seed_database())
