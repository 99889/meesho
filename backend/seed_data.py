import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from models.product import Product
from models.category import Category

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'meesho_db')

async def seed_database():
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Clear existing data
    await db.products.delete_many({})
    await db.categories.delete_many({})
    
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
    
    category_docs = [Category(**cat).dict() for cat in categories]
    await db.categories.insert_many(category_docs)
    print(f"✓ Seeded {len(categories)} categories")
    
    # Seed products
    products = [
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
            "colors": ["Red", "Blue", "Green", "Yellow"],
            "description": "Beautiful floral print kurti perfect for casual and semi-formal occasions. Made from premium quality fabric.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Fashion Hub",
            "return_policy": "7 days return"
        },
        {
            "name": "Men Casual Cotton Shirt",
            "price": 399,
            "original_price": 1299,
            "discount": 69,
            "rating": 4.0,
            "reviews": 890,
            "image": "https://images.unsplash.com/photo-1602810320073-1230c46d89d4?w=500",
            "category": "Men",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["White", "Blue", "Black"],
            "description": "Premium cotton casual shirt for men. Comfortable and stylish for everyday wear.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "StyleMart",
            "return_policy": "7 days return"
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
            "colors": ["Pink", "Red", "Green", "Blue"],
            "description": "Traditional saree with modern design. Perfect for weddings and festivals.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Ethnic Store",
            "return_policy": "7 days return"
        },
        {
            "name": "Makeup Cosmetics Kit",
            "price": 249,
            "original_price": 799,
            "discount": 69,
            "rating": 4.3,
            "reviews": 1567,
            "image": "https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=500",
            "category": "Beauty & Health",
            "sizes": ["Standard"],
            "colors": ["Multi"],
            "description": "Complete makeup kit with all essentials. High-quality cosmetics at affordable prices.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Beauty Plus",
            "return_policy": "7 days return"
        },
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
            "colors": ["Black", "Red", "Blue"],
            "description": "Trendy western dress for modern women. Perfect for parties and casual outings.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Fashion Store",
            "return_policy": "7 days return"
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
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["White", "Blue", "Black", "Grey"],
            "description": "Premium formal shirt for office and business meetings. Comfortable fabric.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Formal Hub",
            "return_policy": "7 days return"
        },
        {
            "name": "Kitchen Cookware Set",
            "price": 599,
            "original_price": 1999,
            "discount": 70,
            "rating": 4.2,
            "reviews": 876,
            "image": "https://images.pexels.com/photos/279648/pexels-photo-279648.jpeg?w=500",
            "category": "Home & Kitchen",
            "sizes": ["Standard"],
            "colors": ["Silver", "Black"],
            "description": "Complete kitchen cookware set. Non-stick coating and durable quality.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Home Essentials",
            "return_policy": "7 days return"
        },
        {
            "name": "Wireless Earbuds",
            "price": 349,
            "original_price": 1299,
            "discount": 73,
            "rating": 4.0,
            "reviews": 2345,
            "image": "https://images.pexels.com/photos/1599791/pexels-photo-1599791.jpeg?w=500",
            "category": "Electronics",
            "sizes": ["Standard"],
            "colors": ["Black", "White"],
            "description": "High-quality wireless earbuds with long battery life and clear sound.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Tech Store",
            "return_policy": "7 days return"
        },
        {
            "name": "Designer Kurti Set",
            "price": 349,
            "original_price": 1199,
            "discount": 71,
            "rating": 4.3,
            "reviews": 1456,
            "image": "https://images.pexels.com/photos/34346734/pexels-photo-34346734.jpeg?w=500",
            "category": "Women Ethnic",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Pink", "Blue", "Green"],
            "description": "Designer kurti set with matching dupatta. Premium fabric and comfortable fit.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Ethnic Wear",
            "return_policy": "7 days return"
        },
        {
            "name": "Men Casual T-Shirt",
            "price": 199,
            "original_price": 599,
            "discount": 67,
            "rating": 4.1,
            "reviews": 3456,
            "image": "https://images.unsplash.com/photo-1630435664004-8e6d54780dd8?w=500",
            "category": "Men",
            "sizes": ["S", "M", "L", "XL", "XXL"],
            "colors": ["Black", "White", "Blue", "Grey", "Red"],
            "description": "Comfortable cotton t-shirt for casual wear. Available in multiple colors.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Casual Store",
            "return_policy": "7 days return"
        },
        {
            "name": "Skincare Combo Pack",
            "price": 299,
            "original_price": 999,
            "discount": 70,
            "rating": 4.4,
            "reviews": 1890,
            "image": "https://images.unsplash.com/photo-1580870069867-74c57ee1bb07?w=500",
            "category": "Beauty & Health",
            "sizes": ["Standard"],
            "colors": ["Multi"],
            "description": "Complete skincare routine pack. Includes cleanser, toner, and moisturizer.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Beauty Care",
            "return_policy": "7 days return"
        },
        {
            "name": "Women Palazzo Set",
            "price": 329,
            "original_price": 1099,
            "discount": 70,
            "rating": 4.2,
            "reviews": 1123,
            "image": "https://images.pexels.com/photos/27155552/pexels-photo-27155552.jpeg?w=500",
            "category": "Women Western",
            "sizes": ["S", "M", "L", "XL"],
            "colors": ["Black", "Navy", "Maroon"],
            "description": "Comfortable palazzo set for everyday wear. Stylish and trendy design.",
            "free_delivery": True,
            "cod": True,
            "seller_name": "Trendy Fashion",
            "return_policy": "7 days return"
        }
    ]
    
    product_docs = [Product(**prod).dict() for prod in products]
    await db.products.insert_many(product_docs)
    print(f"✓ Seeded {len(products)} products")
    
    client.close()
    print("\n✅ Database seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
