import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
import random
from datetime import datetime, timedelta

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'meesho_db')

# Sample review templates by category
REVIEW_TEMPLATES = {
    "Women Ethnic": [
        "Beautiful saree! The fabric quality is excellent and color is vibrant.",
        "Perfect kurti for daily wear. Comfortable and stylish.",
        "Amazing lehenga! Got so many compliments at the wedding.",
        "Good quality material and perfect stitching. Highly recommended!",
        "Lovely design and great fit. Worth every penny!",
        "The color is exactly as shown in pictures. Very satisfied!",
        "Comfortable to wear all day. Great purchase!",
        "Excellent quality for the price. Will buy again.",
        "Beautiful ethnic wear. Perfect for festive occasions.",
        "Great product! Fast delivery and good packaging.",
        "Value for money. Good quality fabric.",
        "Loved it! Fits perfectly and looks elegant.",
        "Nice design and good material quality.",
        "Perfect for party wear. Received many compliments!",
        "Good purchase. Matches the description perfectly.",
        "Beautiful colors and comfortable fabric.",
        "Exactly what I was looking for! Super happy.",
        "Great quality at this price point.",
        "Impressed with the quality and design.",
        "Will definitely recommend to friends and family!",
    ],
    "Women Western": [
        "Perfect fit and great quality! Love this dress.",
        "Comfortable jeans. Good stretch and perfect length.",
        "Beautiful dress for casual outings. Highly recommend!",
        "Great top! Fabric is soft and breathable.",
        "Stylish and comfortable. Worth the price!",
        "Good quality material. Fits perfectly.",
        "Loved the design! Exactly as shown in pictures.",
        "Comfortable for all-day wear. Very satisfied!",
        "Great for casual and formal both. Versatile piece!",
        "Excellent purchase! Will buy more colors.",
        "Perfect summer wear. Light and airy fabric.",
        "Good quality denim. Fits well.",
        "Beautiful dress! Got many compliments.",
        "Comfortable and stylish. Highly recommended!",
        "Great product at reasonable price.",
    ],
    "Men": [
        "Perfect fit shirt! Good quality fabric.",
        "Comfortable t-shirt. Good for daily wear.",
        "Great quality jeans. Worth the money!",
        "Nice shirt for office wear. Good stitching.",
        "Comfortable and stylish. Highly recommend!",
        "Good quality material and perfect fit.",
        "Excellent product! Will order again.",
        "Perfect casual wear. Comfortable fabric.",
        "Great shirt! Exactly as described.",
        "Good quality at this price. Very satisfied!",
        "Comfortable jeans. Good fit and quality.",
        "Nice t-shirt! Soft fabric and good print.",
        "Perfect for daily use. Good purchase!",
        "Great quality shirt. Professional look.",
        "Value for money product!",
    ],
    "Kids": [
        "My kid loves this! Comfortable and cute.",
        "Great quality kids wear. Soft fabric.",
        "Perfect size and good quality. Happy with purchase!",
        "Cute design! My daughter loves it.",
        "Comfortable for kids. Good material quality.",
        "Exactly what I wanted for my son. Great!",
        "Good quality at affordable price.",
        "Perfect for daily wear. Durable fabric.",
        "My kid is very happy! Will buy more.",
        "Great product! Fast delivery too.",
        "Nice colors and comfortable for kids.",
        "Good quality kids clothing. Recommended!",
        "Perfect fit and cute design!",
        "Durable and comfortable. Worth it!",
        "Great for active kids. Good quality!",
    ],
    "Electronics": [
        "Amazing phone! Great camera and battery life.",
        "Excellent earbuds! Sound quality is superb.",
        "Perfect tablet for work and entertainment.",
        "Great smartwatch! Tracks everything perfectly.",
        "Good quality power bank. Charges fast!",
        "Excellent product! Works perfectly.",
        "Great phone at this price. Smooth performance!",
        "Amazing sound quality! Worth every penny.",
        "Perfect gadget! Highly recommended.",
        "Good battery backup. Very satisfied!",
        "Excellent build quality. Premium feel!",
        "Great purchase! Fast charging works well.",
        "Perfect for daily use. No issues!",
        "Amazing features at this price point!",
        "Highly recommend! Great value for money.",
        "Works perfectly! No complaints.",
        "Great product! Fast delivery.",
        "Excellent quality! Very happy with purchase.",
        "Perfect gadget for everyday use!",
        "Amazing performance! Worth buying.",
    ],
    "Home & Kitchen": [
        "Great quality cookware! Non-stick works perfectly.",
        "Perfect dinner set. Good quality and design.",
        "Excellent product! Very happy with quality.",
        "Good quality utensils. Worth the money!",
        "Perfect for daily cooking. Durable!",
        "Great kitchen product. Highly recommend!",
        "Excellent quality at this price!",
        "Perfect size and good quality.",
        "Very useful product. Good purchase!",
        "Great for home use. Durable quality.",
        "Exactly what I needed! Perfect!",
        "Good quality material. Will last long.",
        "Perfect product! Very satisfied.",
        "Great addition to my kitchen!",
        "Excellent quality and design!",
    ],
    "Beauty & Health": [
        "Amazing makeup kit! Good quality products.",
        "Perfect for daily use. Love the products!",
        "Great quality cosmetics. Highly recommend!",
        "Excellent skincare set. Visible results!",
        "Perfect makeup brushes. Good quality!",
        "Love this product! Using daily.",
        "Great quality at affordable price!",
        "Perfect for daily skincare routine.",
        "Excellent product! Skin feels great.",
        "Highly recommend! Good quality.",
        "Perfect for makeup lovers!",
        "Great products in the set!",
        "Excellent quality cosmetics!",
        "Love it! Will buy again.",
        "Perfect for beginners too!",
    ],
    "Bags & Footwear": [
        "Beautiful handbag! Good quality leather.",
        "Comfortable shoes! Perfect fit.",
        "Great backpack! Spacious and durable.",
        "Perfect shoes for daily wear!",
        "Excellent quality bag. Love the design!",
        "Comfortable footwear! Highly recommend.",
        "Great quality at this price!",
        "Perfect size bag. Very useful!",
        "Comfortable shoes for long walks!",
        "Excellent leather quality!",
        "Perfect for office use!",
        "Great product! Very satisfied.",
        "Comfortable and stylish!",
        "Perfect fit and good quality!",
        "Love this bag! Using daily.",
    ]
}

# Common positive review words
POSITIVE_WORDS = ["Amazing", "Excellent", "Perfect", "Great", "Good", "Love", "Superb", "Fantastic", "Awesome", "Outstanding"]
REVIEW_ENDINGS = ["!", ".", " Highly recommended!", " Worth buying!", " Very satisfied!", " Will buy again!"]

# Indian names for reviewers
INDIAN_NAMES = [
    "Priya Sharma", "Rahul Kumar", "Anjali Patel", "Amit Singh", "Sneha Reddy",
    "Rohan Mehta", "Neha Gupta", "Vikram Joshi", "Pooja Iyer", "Arjun Nair",
    "Kavya Desai", "Sanjay Rao", "Divya Shah", "Karan Verma", "Riya Kapoor",
    "Aditya Pillai", "Meera Chatterjee", "Nikhil Agarwal", "Shreya Kulkarni", "Varun Malhotra",
    "Ananya Menon", "Rohit Pandey", "Sakshi Jain", "Mohit Bansal", "Tanvi Deshpande",
    "Akash Chopra", "Nikita Shetty", "Gaurav Saxena", "Priyanka Mishra", "Siddharth Dubey",
    "Aarti Bhatt", "Manish Tiwari", "Swati Arora", "Deepak Singhal", "Isha Kaul",
    "Abhishek Sinha", "Ritu Batra", "Vishal Yadav", "Simran Kohli", "Rajesh Kumar",
    "Megha Trivedi", "Harsh Goyal", "Nidhi Mathur", "Ashish Varma", "Kritika Soni",
]

async def seed_reviews():
    """Seed realistic reviews for all products"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🌟 Seeding product reviews...")
    print("=" * 60)
    
    # Clear existing reviews
    await db.reviews.delete_many({})
    print("🗑️  Cleared existing reviews\n")
    
    # Get all products
    products = await db.products.find().to_list(length=None)
    print(f"📦 Found {len(products)} products\n")
    
    total_reviews_created = 0
    
    for product in products:
        category = product.get('category', 'Women Ethnic')
        product_name = product.get('name', 'Product')
        product_rating = product.get('rating', 4.5)
        num_reviews = product.get('reviews', 0)
        
        # Generate 5-15 reviews per product
        reviews_to_create = random.randint(5, 15)
        
        # Get review templates for this category
        templates = REVIEW_TEMPLATES.get(category, REVIEW_TEMPLATES["Women Ethnic"])
        
        reviews = []
        for i in range(reviews_to_create):
            # Random date in last 6 months
            days_ago = random.randint(1, 180)
            review_date = datetime.utcnow() - timedelta(days=days_ago)
            
            # Random rating (weighted towards product's average rating)
            if product_rating >= 4.5:
                rating = random.choices([5, 4, 5, 5, 4], weights=[40, 20, 20, 15, 5])[0]
            elif product_rating >= 4.0:
                rating = random.choices([5, 4, 3, 5, 4], weights=[30, 30, 10, 20, 10])[0]
            else:
                rating = random.choices([5, 4, 3, 2, 4], weights=[20, 30, 25, 15, 10])[0]
            
            # Select random review text
            review_text = random.choice(templates)
            
            # Randomly add variation
            if random.random() > 0.7:
                review_text = f"{random.choice(POSITIVE_WORDS)}! {review_text}"
            
            # Add verified purchase randomly (80% chance)
            verified = random.random() > 0.2
            
            review = {
                "product_id": product_name,  # Using product name as ID
                "user_name": random.choice(INDIAN_NAMES),
                "rating": rating,
                "review": review_text,
                "verified_purchase": verified,
                "created_at": review_date,
                "helpful_count": random.randint(0, 50)
            }
            
            reviews.append(review)
        
        # Insert all reviews for this product
        if reviews:
            await db.reviews.insert_many(reviews)
            total_reviews_created += len(reviews)
            print(f"✓ Added {len(reviews)} reviews for: {product_name[:40]}...")
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully seeded {total_reviews_created} reviews!")
    print(f"📊 Average {total_reviews_created // len(products)} reviews per product")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_reviews())
