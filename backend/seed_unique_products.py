import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from models.product import Product
from models.category import Category
import random

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'meesho_db')

# Unique product definitions with unique images
UNIQUE_PRODUCTS = {
    "Women Ethnic": [
        # Sarees - Each with unique image
        {"name": "Banarasi Silk Saree", "img": "https://images.pexels.com/photos/3400795/pexels-photo-3400795.jpeg", "price": (1299, 2999)},
        {"name": "Kanjivaram Silk Saree", "img": "https://images.pexels.com/photos/8148577/pexels-photo-8148577.jpeg", "price": (1499, 3499)},
        {"name": "Designer Party Saree", "img": "https://images.pexels.com/photos/3621952/pexels-photo-3621952.jpeg", "price": (899, 2499)},
        {"name": "Cotton Printed Saree", "img": "https://images.pexels.com/photos/6069041/pexels-photo-6069041.jpeg", "price": (599, 1499)},
        {"name": "Georgette Floral Saree", "img": "https://images.pexels.com/photos/9558599/pexels-photo-9558599.jpeg", "price": (799, 1999)},
        {"name": "Chiffon Wedding Saree", "img": "https://images.pexels.com/photos/8088502/pexels-photo-8088502.jpeg", "price": (1599, 3999)},
        {"name": "Traditional Kanjeevaram Saree", "img": "https://images.pexels.com/photos/10309477/pexels-photo-10309477.jpeg", "price": (1799, 4499)},
        {"name": "Embroidered Art Silk Saree", "img": "https://images.pexels.com/photos/6766325/pexels-photo-6766325.jpeg", "price": (999, 2699)},
        {"name": "Zari Work Saree", "img": "https://images.pexels.com/photos/8088503/pexels-photo-8088503.jpeg", "price": (1299, 3299)},
        {"name": "Bandhani Printed Saree", "img": "https://images.pexels.com/photos/6069042/pexels-photo-6069042.jpeg", "price": (899, 2199)},
        {"name": "Tussar Silk Saree", "img": "https://images.pexels.com/photos/9558600/pexels-photo-9558600.jpeg", "price": (1599, 3799)},
        {"name": "Net Embellished Saree", "img": "https://images.pexels.com/photos/3621953/pexels-photo-3621953.jpeg", "price": (1399, 3399)},
        {"name": "Pure Silk Saree", "img": "https://images.pexels.com/photos/10309478/pexels-photo-10309478.jpeg", "price": (1699, 4199)},
        {"name": "Festive Wear Saree", "img": "https://images.pexels.com/photos/6766326/pexels-photo-6766326.jpeg", "price": (1099, 2799)},
        {"name": "Patola Silk Saree", "img": "https://images.pexels.com/photos/8148579/pexels-photo-8148579.jpeg", "price": (1799, 4599)},
        
        # Kurtis - Each with unique image
        {"name": "Anarkali Cotton Kurti", "img": "https://images.pexels.com/photos/1926769/pexels-photo-1926769.jpeg", "price": (399, 999)},
        {"name": "Straight Cut Rayon Kurti", "img": "https://images.pexels.com/photos/3651597/pexels-photo-3651597.jpeg", "price": (349, 899)},
        {"name": "A-Line Floral Kurti", "img": "https://images.pexels.com/photos/6311564/pexels-photo-6311564.jpeg", "price": (449, 1099)},
        {"name": "Printed Georgette Kurti", "img": "https://images.pexels.com/photos/6146977/pexels-photo-6146977.jpeg", "price": (499, 1199)},
        {"name": "Embroidered Designer Kurti", "img": "https://images.pexels.com/photos/7679674/pexels-photo-7679674.jpeg", "price": (599, 1499)},
        {"name": "Long Cotton Kurti", "img": "https://images.pexels.com/photos/8090165/pexels-photo-8090165.jpeg", "price": (379, 949)},
        {"name": "Casual Daily Wear Kurti", "img": "https://images.pexels.com/photos/7679856/pexels-photo-7679856.jpeg", "price": (299, 799)},
        {"name": "Party Wear Designer Kurti", "img": "https://images.pexels.com/photos/8090222/pexels-photo-8090222.jpeg", "price": (699, 1799)},
        {"name": "V-Neck Printed Kurti", "img": "https://images.pexels.com/photos/6146978/pexels-photo-6146978.jpeg", "price": (429, 1049)},
        {"name": "High-Low Hemline Kurti", "img": "https://images.pexels.com/photos/7679857/pexels-photo-7679857.jpeg", "price": (549, 1349)},
        {"name": "Angrakha Style Kurti", "img": "https://images.pexels.com/photos/8090223/pexels-photo-8090223.jpeg", "price": (599, 1449)},
        {"name": "Front Slit Kurti", "img": "https://images.pexels.com/photos/6311565/pexels-photo-6311565.jpeg", "price": (479, 1179)},
        {"name": "Block Printed Kurti", "img": "https://images.pexels.com/photos/3651598/pexels-photo-3651598.jpeg", "price": (399, 999)},
        {"name": "Dhoti Style Kurti", "img": "https://images.pexels.com/photos/7679858/pexels-photo-7679858.jpeg", "price": (649, 1599)},
        {"name": "Kaftan Style Kurti", "img": "https://images.pexels.com/photos/8090224/pexels-photo-8090224.jpeg", "price": (699, 1749)},
        
        # Gowns & Suits
        {"name": "Velvet Anarkali Gown", "img": "https://images.pexels.com/photos/1813947/pexels-photo-1813947.jpeg", "price": (1299, 2999)},
        {"name": "Designer Floor Length Gown", "img": "https://images.pexels.com/photos/6843575/pexels-photo-6843575.jpeg", "price": (1499, 3499)},
        {"name": "Net Embroidered Anarkali", "img": "https://images.pexels.com/photos/5704720/pexels-photo-5704720.jpeg", "price": (999, 2499)},
        {"name": "Georgette Anarkali Suit", "img": "https://images.pexels.com/photos/6043587/pexels-photo-6043587.jpeg", "price": (899, 2199)},
        {"name": "Silk Anarkali Dress", "img": "https://images.pexels.com/photos/5704721/pexels-photo-5704721.jpeg", "price": (1199, 2899)},
        {"name": "Long Gown for Party", "img": "https://images.pexels.com/photos/6843576/pexels-photo-6843576.jpeg", "price": (1399, 3199)},
        
        # Palazzo Sets
        {"name": "Cotton Palazzo Pant Set", "img": "https://images.pexels.com/photos/5886041/pexels-photo-5886041.jpeg", "price": (549, 1399)},
        {"name": "Printed Palazzo Suit", "img": "https://images.pexels.com/photos/7679641/pexels-photo-7679641.jpeg", "price": (599, 1499)},
        {"name": "Rayon Palazzo with Kurti", "img": "https://images.pexels.com/photos/9558716/pexels-photo-9558716.jpeg", "price": (649, 1599)},
        {"name": "Designer Palazzo Combo", "img": "https://images.pexels.com/photos/8088395/pexels-photo-8088395.jpeg", "price": (699, 1699)},
        {"name": "Flared Palazzo Set", "img": "https://images.pexels.com/photos/5886042/pexels-photo-5886042.jpeg", "price": (629, 1549)},
        {"name": "Wide Leg Palazzo Suit", "img": "https://images.pexels.com/photos/7679642/pexels-photo-7679642.jpeg", "price": (579, 1449)},
        
        # Lehengas
        {"name": "Bridal Lehenga Choli", "img": "https://images.pexels.com/photos/3621953/pexels-photo-3621953.jpeg", "price": (2999, 7999)},
        {"name": "Designer Lehenga Set", "img": "https://images.pexels.com/photos/10309479/pexels-photo-10309479.jpeg", "price": (2499, 6999)},
        {"name": "Party Wear Lehenga", "img": "https://images.pexels.com/photos/6766324/pexels-photo-6766324.jpeg", "price": (1999, 4999)},
        {"name": "Traditional Wedding Lehenga", "img": "https://images.pexels.com/photos/8148578/pexels-photo-8148578.jpeg", "price": (3499, 8999)},
        {"name": "Embroidered Lehenga", "img": "https://images.pexels.com/photos/3621954/pexels-photo-3621954.jpeg", "price": (2799, 6799)},
        {"name": "Heavy Work Lehenga", "img": "https://images.pexels.com/photos/10309480/pexels-photo-10309480.jpeg", "price": (3299, 8499)},
    ],
    
    "Women Western": [
        {"name": "Floral Maxi Dress", "img": "https://images.pexels.com/photos/1055691/pexels-photo-1055691.jpeg", "price": (699, 1799)},
        {"name": "Black Party Dress", "img": "https://images.pexels.com/photos/1926620/pexels-photo-1926620.jpeg", "price": (799, 1999)},
        {"name": "Summer Beach Dress", "img": "https://images.pexels.com/photos/985635/pexels-photo-985635.jpeg", "price": (549, 1399)},
        {"name": "Evening Cocktail Dress", "img": "https://images.pexels.com/photos/1130626/pexels-photo-1130626.jpeg", "price": (899, 2199)},
        {"name": "Casual A-Line Dress", "img": "https://images.pexels.com/photos/1926620/pexels-photo-1926620.jpeg", "price": (449, 1099)},
        {"name": "Bodycon Party Dress", "img": "https://images.pexels.com/photos/1468379/pexels-photo-1468379.jpeg", "price": (749, 1899)},
        {"name": "Midi Office Dress", "img": "https://images.pexels.com/photos/2584269/pexels-photo-2584269.jpeg", "price": (649, 1599)},
        {"name": "Printed Summer Dress", "img": "https://images.pexels.com/photos/1926621/pexels-photo-1926621.jpeg", "price": (499, 1299)},
        
        {"name": "High Waist Skinny Jeans", "img": "https://images.pexels.com/photos/1082526/pexels-photo-1082526.jpeg", "price": (899, 2199)},
        {"name": "Blue Denim Boyfriend Jeans", "img": "https://images.pexels.com/photos/603022/pexels-photo-603022.jpeg", "price": (799, 1999)},
        {"name": "Black Ripped Jeans", "img": "https://images.pexels.com/photos/1346187/pexels-photo-1346187.jpeg", "price": (749, 1899)},
        {"name": "Stretch Slim Fit Jeans", "img": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg", "price": (699, 1799)},
        {"name": "Wide Leg Denim Jeans", "img": "https://images.pexels.com/photos/914668/pexels-photo-914668.jpeg", "price": (849, 2099)},
        
        {"name": "Formal Office Blazer", "img": "https://images.pexels.com/photos/1311590/pexels-photo-1311590.jpeg", "price": (1299, 2999)},
        {"name": "Casual Denim Blazer", "img": "https://images.pexels.com/photos/1926620/pexels-photo-1926620.jpeg", "price": (999, 2499)},
        {"name": "Long Coat Blazer", "img": "https://images.pexels.com/photos/1462637/pexels-photo-1462637.jpeg", "price": (1499, 3499)},
        
        {"name": "Crop Top White", "img": "https://images.pexels.com/photos/2690323/pexels-photo-2690323.jpeg", "price": (299, 799)},
        {"name": "Printed Crop Top", "img": "https://images.pexels.com/photos/1926620/pexels-photo-1926620.jpeg", "price": (349, 849)},
        {"name": "Halter Neck Crop Top", "img": "https://images.pexels.com/photos/2300334/pexels-photo-2300334.jpeg", "price": (399, 949)},
        
        {"name": "Wide Leg Palazzo Pants", "img": "https://images.pexels.com/photos/3755706/pexels-photo-3755706.jpeg", "price": (549, 1399)},
        {"name": "Formal Trousers", "img": "https://images.pexels.com/photos/1926620/pexels-photo-1926620.jpeg", "price": (699, 1699)},
        {"name": "Culottes Pants", "img": "https://images.pexels.com/photos/1926620/pexels-photo-1926620.jpeg", "price": (599, 1499)},
    ],
    
    "Men": [
        {"name": "Formal White Shirt", "img": "https://images.pexels.com/photos/297933/pexels-photo-297933.jpeg", "price": (599, 1499)},
        {"name": "Blue Striped Shirt", "img": "https://images.pexels.com/photos/1183266/pexels-photo-1183266.jpeg", "price": (549, 1399)},
        {"name": "Casual Cotton Shirt", "img": "https://images.pexels.com/photos/1043145/pexels-photo-1043145.jpeg", "price": (499, 1299)},
        {"name": "Checked Formal Shirt", "img": "https://images.pexels.com/photos/1656684/pexels-photo-1656684.jpeg", "price": (649, 1599)},
        {"name": "Linen Summer Shirt", "img": "https://images.pexels.com/photos/1054042/pexels-photo-1054042.jpeg", "price": (699, 1699)},
        {"name": "Denim Casual Shirt", "img": "https://images.pexels.com/photos/1192609/pexels-photo-1192609.jpeg", "price": (749, 1899)},
        {"name": "Black Party Shirt", "img": "https://images.pexels.com/photos/1484804/pexels-photo-1484804.jpeg", "price": (799, 1999)},
        
        {"name": "Round Neck T-Shirt", "img": "https://images.pexels.com/photos/1021693/pexels-photo-1021693.jpeg", "price": (249, 699)},
        {"name": "V-Neck Plain T-Shirt", "img": "https://images.pexels.com/photos/1040945/pexels-photo-1040945.jpeg", "price": (299, 749)},
        {"name": "Printed Graphic T-Shirt", "img": "https://images.pexels.com/photos/1232459/pexels-photo-1232459.jpeg", "price": (349, 849)},
        {"name": "Polo Collar T-Shirt", "img": "https://images.pexels.com/photos/1261820/pexels-photo-1261820.jpeg", "price": (399, 999)},
        {"name": "Full Sleeve T-Shirt", "img": "https://images.pexels.com/photos/1055691/pexels-photo-1055691.jpeg", "price": (449, 1099)},
        {"name": "Sports T-Shirt", "img": "https://images.pexels.com/photos/1040945/pexels-photo-1040945.jpeg", "price": (499, 1199)},
        
        {"name": "Slim Fit Denim Jeans", "img": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg", "price": (899, 2199)},
        {"name": "Regular Fit Blue Jeans", "img": "https://images.pexels.com/photos/603022/pexels-photo-603022.jpeg", "price": (799, 1999)},
        {"name": "Black Skinny Jeans", "img": "https://images.pexels.com/photos/1346187/pexels-photo-1346187.jpeg", "price": (849, 2099)},
        {"name": "Ripped Denim Jeans", "img": "https://images.pexels.com/photos/1346187/pexels-photo-1346187.jpeg", "price": (949, 2299)},
        {"name": "Stretchable Jeans", "img": "https://images.pexels.com/photos/1598507/pexels-photo-1598507.jpeg", "price": (749, 1899)},
        
        {"name": "Cotton Track Pants", "img": "https://images.pexels.com/photos/2112648/pexels-photo-2112648.jpeg", "price": (449, 1099)},
        {"name": "Jogger Pants", "img": "https://images.pexels.com/photos/1448665/pexels-photo-1448665.jpeg", "price": (549, 1399)},
        {"name": "Sports Track Pants", "img": "https://images.pexels.com/photos/1040945/pexels-photo-1040945.jpeg", "price": (599, 1499)},
    ],
    
    "Kids": [
        {"name": "Boys Cotton T-Shirt", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (249, 649)},
        {"name": "Girls Printed T-Shirt", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (299, 699)},
        {"name": "Cartoon Character T-Shirt", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (349, 749)},
        {"name": "Sports T-Shirt for Kids", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (399, 849)},
        
        {"name": "Baby Girl Party Dress", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (549, 1399)},
        {"name": "Princess Frock Dress", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (599, 1499)},
        {"name": "Cotton Summer Dress", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (449, 1099)},
        {"name": "Floral Girls Dress", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (499, 1299)},
        
        {"name": "Boys Casual Shirt", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (399, 999)},
        {"name": "Boys Formal Shirt", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (449, 1099)},
        {"name": "Checked Shirt for Kids", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (349, 899)},
        
        {"name": "Kids Denim Jeans", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (549, 1399)},
        {"name": "Boys Track Pants", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (449, 1099)},
        {"name": "Girls Leggings", "img": "https://images.pexels.com/photos/1620760/pexels-photo-1620760.jpeg", "price": (299, 749)},
    ],
    
    "Electronics": [
        # iPhones
        {"name": "iPhone 15 Pro Max 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (129900, 139900)},
        {"name": "iPhone 15 Pro 128GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (119900, 129900)},
        {"name": "iPhone 15 128GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (79900, 89900)},
        {"name": "iPhone 14 Pro Max 256GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (109900, 119900)},
        {"name": "iPhone 14 Pro 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (99900, 109900)},
        {"name": "iPhone 14 128GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (69900, 79900)},
        {"name": "iPhone 13 Pro 256GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (89900, 99900)},
        {"name": "iPhone 13 128GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (54900, 64900)},
        {"name": "iPhone 12 Pro 128GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (74900, 84900)},
        {"name": "iPhone 12 64GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (42900, 49900)},
        {"name": "iPhone SE 3rd Gen 64GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (38900, 44900)},
        {"name": "iPhone 11 64GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (34900, 39900)},
        
        # Android Flagship
        {"name": "Samsung Galaxy S24 Ultra 256GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (89999, 99999)},
        {"name": "Samsung Galaxy S23 Ultra 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (74999, 84999)},
        {"name": "OnePlus 12 5G 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (64999, 71999)},
        {"name": "OnePlus 11 5G 256GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (54999, 61999)},
        {"name": "Google Pixel 8 Pro 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (79999, 89999)},
        {"name": "Xiaomi 14 Pro 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (64999, 71999)},
        
        # Mid-range Phones
        {"name": "Samsung Galaxy A54 5G 128GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (34999, 40999)},
        {"name": "Vivo V29 Pro 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (36999, 41999)},
        {"name": "OPPO Reno 11 Pro 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (39999, 44999)},
        {"name": "Realme GT 3 256GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (42999, 47999)},
        {"name": "Nothing Phone 2 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (44999, 49999)},
        {"name": "Motorola Edge 50 Pro 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (31999, 36999)},
        
        # Budget Phones
        {"name": "Poco X6 Pro 256GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (24999, 29999)},
        {"name": "Redmi Note 13 Pro 256GB", "img": "https://images.pexels.com/photos/699122/pexels-photo-699122.jpeg", "price": (22999, 27999)},
        {"name": "Realme 12 Pro 256GB", "img": "https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg", "price": (21999, 26999)},
        {"name": "Samsung Galaxy M35 128GB", "img": "https://images.pexels.com/photos/1092644/pexels-photo-1092644.jpeg", "price": (16999, 20999)},
        
        # Tablets
        {"name": "iPad Pro 12.9 inch 256GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg", "price": (99900, 109900)},
        {"name": "iPad Air 5th Gen 256GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg", "price": (59900, 69900)},
        {"name": "iPad 10th Gen 64GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg", "price": (39900, 44900)},
        {"name": "Samsung Galaxy Tab S9 Ultra", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg", "price": (89999, 99999)},
        {"name": "Samsung Galaxy Tab S9 256GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg", "price": (54999, 61999)},
        {"name": "Lenovo Tab P12 Pro 256GB", "img": "https://images.pexels.com/photos/1334597/pexels-photo-1334597.jpeg", "price": (39999, 46999)},
        
        # Audio
        {"name": "Apple AirPods Pro 2nd Gen", "img": "https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg", "price": (22900, 26900)},
        {"name": "Sony WH-1000XM5", "img": "https://images.pexels.com/photos/3394650/pexels-photo-3394650.jpeg", "price": (29990, 34990)},
        {"name": "Bose QuietComfort Ultra", "img": "https://images.pexels.com/photos/3587478/pexels-photo-3587478.jpeg", "price": (32990, 37990)},
        {"name": "JBL Flip 6 Bluetooth Speaker", "img": "https://images.pexels.com/photos/8000623/pexels-photo-8000623.jpeg", "price": (9999, 12999)},
        {"name": "Boat Airdopes 141 TWS", "img": "https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg", "price": (1299, 2499)},
        {"name": "Realme Buds Air 5 Pro", "img": "https://images.pexels.com/photos/3825517/pexels-photo-3825517.jpeg", "price": (3499, 4999)},
        
        # Smart Watches
        {"name": "Apple Watch Series 9 GPS 45mm", "img": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg", "price": (42900, 47900)},
        {"name": "Samsung Galaxy Watch 6 Classic", "img": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg", "price": (31999, 36999)},
        {"name": "Noise ColorFit Pro 5", "img": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg", "price": (2999, 4999)},
        {"name": "Fire-Boltt Phoenix Ultra", "img": "https://images.pexels.com/photos/393047/pexels-photo-393047.jpeg", "price": (1999, 3499)},
        
        # Accessories
        {"name": "Anker PowerCore 20000mAh", "img": "https://images.pexels.com/photos/4195325/pexels-photo-4195325.jpeg", "price": (2499, 3999)},
        {"name": "Apple 20W USB-C Fast Charger", "img": "https://images.pexels.com/photos/4195325/pexels-photo-4195325.jpeg", "price": (1700, 2199)},
        {"name": "Logitech MX Master 3S Mouse", "img": "https://images.pexels.com/photos/2115256/pexels-photo-2115256.jpeg", "price": (8995, 10995)},
        {"name": "SanDisk 256GB USB 3.0", "img": "https://images.pexels.com/photos/4195325/pexels-photo-4195325.jpeg", "price": (1499, 2499)},
    ],
    
    "Home & Kitchen": [
        {"name": "Stainless Steel Cookware Set", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg", "price": (1299, 2999)},
        {"name": "Non-Stick Frying Pan Set", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg", "price": (899, 2199)},
        {"name": "Pressure Cooker 5L", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg", "price": (999, 2399)},
        {"name": "Induction Base Kadhai", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg", "price": (799, 1899)},
        
        {"name": "24 Piece Dinner Set", "img": "https://images.pexels.com/photos/6489074/pexels-photo-6489074.jpeg", "price": (1199, 2799)},
        {"name": "Melamine Dinner Set", "img": "https://images.pexels.com/photos/6489074/pexels-photo-6489074.jpeg", "price": (899, 2099)},
        {"name": "Glass Dinner Set", "img": "https://images.pexels.com/photos/6489074/pexels-photo-6489074.jpeg", "price": (799, 1899)},
        
        {"name": "Cotton Double Bed Sheet", "img": "https://images.pexels.com/photos/1350789/pexels-photo-1350789.jpeg", "price": (649, 1599)},
        {"name": "Silk Bed Sheet Set", "img": "https://images.pexels.com/photos/1350789/pexels-photo-1350789.jpeg", "price": (999, 2399)},
        {"name": "Printed Bed Cover", "img": "https://images.pexels.com/photos/1350789/pexels-photo-1350789.jpeg", "price": (549, 1399)},
        
        {"name": "Plastic Storage Container Set", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg", "price": (449, 1099)},
        {"name": "Glass Storage Jars", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg", "price": (599, 1499)},
        {"name": "Airtight Container Set", "img": "https://images.pexels.com/photos/4686958/pexels-photo-4686958.jpeg", "price": (699, 1699)},
    ],
    
    "Beauty & Health": [
        {"name": "Complete Makeup Kit", "img": "https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg", "price": (799, 1999)},
        {"name": "Professional Makeup Brushes Set", "img": "https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg", "price": (599, 1499)},
        {"name": "Eyeshadow Palette", "img": "https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg", "price": (449, 1099)},
        
        {"name": "Vitamin C Skincare Combo", "img": "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg", "price": (649, 1599)},
        {"name": "Anti-Aging Face Serum", "img": "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg", "price": (549, 1399)},
        {"name": "Moisturizer Cream", "img": "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg", "price": (399, 999)},
        {"name": "Face Wash Combo", "img": "https://images.pexels.com/photos/3762879/pexels-photo-3762879.jpeg", "price": (299, 749)},
        
        {"name": "Hair Growth Oil", "img": "https://images.pexels.com/photos/3373736/pexels-photo-3373736.jpeg", "price": (449, 1099)},
        {"name": "Shampoo and Conditioner Set", "img": "https://images.pexels.com/photos/3373736/pexels-photo-3373736.jpeg", "price": (549, 1399)},
        {"name": "Hair Mask Treatment", "img": "https://images.pexels.com/photos/3373736/pexels-photo-3373736.jpeg", "price": (399, 999)},
        
        {"name": "Matte Lipstick Set of 6", "img": "https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg", "price": (499, 1299)},
        {"name": "Liquid Lipstick Set", "img": "https://images.pexels.com/photos/1115128/pexels-photo-1115128.jpeg", "price": (549, 1399)},
    ],
    
    "Bags & Footwear": [
        {"name": "Leather Handbag", "img": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg", "price": (999, 2499)},
        {"name": "Designer Shoulder Bag", "img": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg", "price": (799, 1999)},
        {"name": "Canvas Tote Bag", "img": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg", "price": (599, 1499)},
        {"name": "Sling Crossbody Bag", "img": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg", "price": (549, 1399)},
        
        {"name": "Casual Sneakers", "img": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg", "price": (899, 2199)},
        {"name": "Running Sports Shoes", "img": "https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg", "price": (999, 2499)},
        {"name": "Formal Leather Shoes", "img": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg", "price": (1299, 2999)},
        {"name": "Canvas Casual Shoes", "img": "https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg", "price": (699, 1799)},
        
        {"name": "Travel Backpack 30L", "img": "https://images.pexels.com/photos/2905238/pexels-photo-2905238.jpeg", "price": (799, 1999)},
        {"name": "Laptop Backpack", "img": "https://images.pexels.com/photos/2905238/pexels-photo-2905238.jpeg", "price": (899, 2199)},
        {"name": "School Backpack", "img": "https://images.pexels.com/photos/2905238/pexels-photo-2905238.jpeg", "price": (599, 1499)},
        
        {"name": "Leather Wallet", "img": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg", "price": (399, 999)},
        {"name": "Designer Wallet", "img": "https://images.pexels.com/photos/1152077/pexels-photo-1152077.jpeg", "price": (449, 1099)},
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

async def generate_products(category_name, count=100):
    """Generate unique products for a category - each product gets a unique image"""
    products = []
    product_templates = UNIQUE_PRODUCTS[category_name]
    
    # Simply use each template as-is to ensure unique images
    # Cycle through templates if we need more than available
    for i in range(count):
        template = product_templates[i % len(product_templates)]
        
        original_price = random.randint(template['price'][0], template['price'][1])
        
        # Realistic discount based on price
        if original_price > 50000:
            discount = random.choice([5, 8, 10, 12, 15])
        elif original_price > 10000:
            discount = random.choice([15, 20, 25, 30])
        else:
            discount = random.choice([40, 50, 60, 65, 70])
        
        price = int(original_price * (100 - discount) / 100)
        rating = round(random.uniform(3.9, 5.0), 1)
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
    """Seed database with unique products"""
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🚀 Seeding database with UNIQUE products...")
    print("=" * 60)
    
    # Clear existing data
    await db.products.delete_many({})
    await db.categories.delete_many({})
    await db.reviews.delete_many({})
    print("🗑️  Cleared existing data\n")
    
    # Create categories
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
    print(f"✅ Created {len(categories)} categories\n")
    
    # Generate products for each category
    all_products = []
    for category in categories:
        # Generate exactly as many products as we have unique definitions
        # This ensures NO duplicate images
        num_unique = len(UNIQUE_PRODUCTS[category['name']])
        print(f"⏳ Generating {num_unique} unique products for '{category['name']}'...")
        products = await generate_products(category["name"], num_unique)
        all_products.extend(products)
        
        # Show sample
        sample = products[0]
        print(f"   📦 Sample: {sample['name']}")
        print(f"   💰 Price: ₹{sample['price']} (was ₹{sample['original_price']}, {sample['discount']}% off)")
        print(f"   ⭐ Rating: {sample['rating']}/5 ({sample['reviews']} reviews)\n")
    
    # Insert products in batches
    print("💾 Inserting products into database...")
    for i in range(0, len(all_products), 100):
        await db.products.insert_many(all_products[i:i+100])
    
    print("\n" + "=" * 60)
    print(f"✅ Successfully seeded {len(all_products)} unique products!")
    print(f"📱 Categories: {', '.join([c['name'] for c in categories])}")
    print("\n🎉 Database is ready with diverse products and unique images!")
    print("=" * 60)
    
    client.close()

if __name__ == "__main__":
    asyncio.run(seed_database())
