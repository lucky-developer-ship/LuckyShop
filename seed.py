from app.database import SessionLocal, engine, Base
from app.models import Product, User
from app.auth import get_password_hash

Base.metadata.create_all(bind=engine)

SAMPLE_PRODUCTS = [
    # Electronics
    {"name": "Wireless Mouse", "description": "Ergonomic wireless mouse with USB receiver. Features adjustable DPI settings, silent clicks, and a comfortable grip for extended use. Compatible with Windows, Mac, and Linux.", "price": 29.99, "stock": 50, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop"},
    {"name": "Mechanical Keyboard", "description": "RGB mechanical keyboard with Cherry MX switches. Full-size layout with numpad, programmable macro keys, and per-key RGB lighting. Built for gaming and typing enthusiasts.", "price": 89.99, "stock": 30, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop"},
    {"name": "USB-C Hub", "description": "7-in-1 USB-C hub with HDMI, USB-A 3.0, SD card reader, and PD charging. Supports 4K@60Hz output. Compact aluminum design for on-the-go professionals.", "price": 45.99, "stock": 40, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400&h=300&fit=crop"},
    {"name": "Webcam HD", "description": "1080p HD webcam with built-in microphone and auto-focus. Wide-angle lens with low-light correction. Perfect for video calls and streaming.", "price": 59.99, "stock": 20, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=400&h=300&fit=crop"},
    {"name": "Wireless Earbuds", "description": "True wireless earbuds with active noise cancellation. 30-hour total battery life with charging case. IPX5 water resistant, perfect for workouts.", "price": 79.99, "stock": 60, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12f032f55?w=400&h=300&fit=crop"},
    {"name": "Portable Bluetooth Speaker", "description": "Waterproof Bluetooth speaker with 360-degree sound. 12-hour battery life, built-in microphone for calls. Great for outdoor adventures.", "price": 49.99, "stock": 35, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=400&h=300&fit=crop"},
    {"name": "Wireless Charging Pad", "description": "Fast wireless charging pad supporting 15W output. Qi-certified, compatible with all Qi-enabled devices. Anti-slip surface and LED indicator.", "price": 24.99, "stock": 45, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400&h=300&fit=crop"},
    {"name": "Noise Cancelling Headphones", "description": "Over-ear wireless headphones with ANC. 40-hour battery life, premium comfort padding, and Hi-Res audio support. Ideal for travel and focused work.", "price": 199.99, "stock": 15, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop"},
    {"name": "Smart Watch", "description": "Fitness tracking smartwatch with heart rate monitor, GPS, and sleep tracking. Water-resistant to 50m, 7-day battery life. Notifications from your phone.", "price": 149.99, "stock": 25, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop"},
    {"name": "External SSD 1TB", "description": "Portable SSD with 1TB storage and USB 3.2 speeds up to 1050MB/s. Shock-resistant, lightweight design. Password protection and 256-bit AES encryption.", "price": 109.99, "stock": 30, "category": "Electronics", "image_url": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=400&h=300&fit=crop"},

    # Accessories
    {"name": "Laptop Stand", "description": "Adjustable aluminum laptop stand with ergonomic design. Improves airflow and posture. Foldable for portability, supports laptops up to 17 inches.", "price": 35.99, "stock": 25, "category": "Accessories", "image_url": "https://images.unsplash.com/photo-1611078489935-0cb964de46d6?w=400&h=300&fit=crop"},
    {"name": "Leather Wallet", "description": "Genuine leather bifold wallet with RFID blocking. 8 card slots, 2 bill compartments, and a coin pocket. Slim profile fits comfortably in pockets.", "price": 39.99, "stock": 50, "category": "Accessories", "image_url": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=400&h=300&fit=crop"},
    {"name": "Travel Backpack", "description": "Water-resistant travel backpack with 35L capacity. Laptop compartment fits 15.6 inch, USB charging port, and anti-theft back pocket. Perfect for daily commute.", "price": 54.99, "stock": 30, "category": "Accessories", "image_url": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop"},
    {"name": "Sunglasses", "description": "Polarized UV400 sunglasses with lightweight metal frame. Scratch-resistant lenses, comes with hard case and cleaning cloth. Classic aviator style.", "price": 29.99, "stock": 40, "category": "Accessories", "image_url": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=300&fit=crop"},
    {"name": "Watch Band", "description": "Silicone sport watch band with quick-release pins. Available in multiple sizes. Sweat-proof and comfortable for all-day wear. Fits most smartwatches.", "price": 14.99, "stock": 80, "category": "Accessories", "image_url": "https://images.unsplash.com/photo-1434493789847-2f02dc6ca35d?w=400&h=300&fit=crop"},
    {"name": "Phone Case", "description": "Clear protective phone case with military-grade drop protection. Raised edges protect camera and screen. Wireless charging compatible.", "price": 19.99, "stock": 70, "category": "Accessories", "image_url": "https://images.unsplash.com/photo-1601784551446-20c9e07cdbdb?w=400&h=300&fit=crop"},
    {"name": "Wireless Keyboard & Mouse Combo", "description": "Slim wireless keyboard and optical mouse combo. 2.4GHz wireless with 10m range. Full-size keyboard with quiet keys, ergonomic mouse.", "price": 34.99, "stock": 35, "category": "Accessories", "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop"},
    {"name": "Cable Organizer", "description": "Silicone cable management clips with adhesive base. Set of 5 clips keeps desk tidy. Compatible with all cable sizes from USB to HDMI.", "price": 9.99, "stock": 100, "category": "Accessories", "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop"},

    # Home Office
    {"name": "Desk Lamp", "description": "LED desk lamp with adjustable brightness and color temperature. Touch control with memory function. USB charging port, eye-care technology.", "price": 24.99, "stock": 35, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1507473885765-e6ed057ab6fe?w=400&h=300&fit=crop"},
    {"name": "Monitor Light Bar", "description": "Monitor-mounted LED light bar for eye care. Asymmetric optical design reduces screen glare. Wireless remote control, auto-dimming sensor.", "price": 39.99, "stock": 28, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1542451542907-6cf80ff362d6?w=400&h=300&fit=crop"},
    {"name": "Ergonomic Office Chair", "description": "Mesh ergonomic chair with lumbar support and adjustable armrests. Breathable mesh back, seat height adjustment, 135-degree recline. Supports up to 150kg.", "price": 249.99, "stock": 10, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=400&h=300&fit=crop"},
    {"name": "Standing Desk Converter", "description": "Height-adjustable standing desk converter. Smooth gas-spring lift mechanism. Large surface fits dual monitors. Keyboard tray included.", "price": 179.99, "stock": 12, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=400&h=300&fit=crop"},
    {"name": "Desk Organizer", "description": "Multi-compartment desk organizer with phone stand. Bamboo construction, holds pens, cards, and small accessories. Clean minimalist design.", "price": 22.99, "stock": 40, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=400&h=300&fit=crop"},
    {"name": "Whiteboard Calendar", "description": "Magnetic dry-erase monthly calendar board. 24x36 inches with markers and eraser. Frameless design, perfect for planning and reminders.", "price": 27.99, "stock": 20, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&h=300&fit=crop"},
    {"name": "Cable Management Box", "description": "Desk cable management box to hide messy cords. Ventilated design prevents overheating. Fits power strips up to 12 inches. Available in white or black.", "price": 15.99, "stock": 50, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400&h=300&fit=crop"},
    {"name": "Monitor Arm", "description": "Single monitor arm with full motion adjustability. Supports monitors up to 32 inches and 8kg. Cable management, VESA mount compatible.", "price": 49.99, "stock": 22, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=300&fit=crop"},
    {"name": "Footrest", "description": "Ergonomic under-desk footrest with adjustable height. Non-slip surface, promotes better posture and circulation. Quiet and sturdy construction.", "price": 32.99, "stock": 18, "category": "Home Office", "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400&h=300&fit=crop"},

    # Stationery
    {"name": "Notebook Set", "description": "Set of 3 premium lined notebooks with hardcover. 200 pages each, 100gsm paper. Lay-flat binding, ribbon bookmark, and inner pocket. A5 size.", "price": 12.99, "stock": 100, "category": "Stationery", "image_url": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&h=300&fit=crop"},
    {"name": "Fountain Pen", "description": "Classic fountain pen with fine nib. Brass body with lacquer finish. Comes with converter and 2 ink cartridges. Smooth writing experience.", "price": 34.99, "stock": 25, "category": "Stationery", "image_url": "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=400&h=300&fit=crop"},
    {"name": "Sticky Notes Set", "description": "Colorful sticky notes in 5 sizes and 12 colors. Strong adhesive, repositionable without residue. 1200 sheets total, perfect for organizing.", "price": 8.99, "stock": 120, "category": "Stationery", "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400&h=300&fit=crop"},
    {"name": "Desk Planner 2026", "description": "Undated weekly desk planner with 52 weeks. Thick paper, twin-wire binding, and monthly overview. Productivity stickers included.", "price": 16.99, "stock": 45, "category": "Stationery", "image_url": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=400&h=300&fit=crop"},
    {"name": "Art Markers Set", "description": "Dual-tip art markers set of 48 colors. Alcohol-based, blendable, and fade-resistant. Perfect for illustration, manga, and design work.", "price": 29.99, "stock": 30, "category": "Stationery", "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400&h=300&fit=crop"},
    {"name": "Washi Tape Collection", "description": "Set of 15 rolls decorative washi tape. Various patterns and colors, 15mm width. Perfect for journaling, crafts, and gift wrapping.", "price": 11.99, "stock": 60, "category": "Stationery", "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=400&h=300&fit=crop"},
    {"name": "Pencil Case", "description": "Canvas pencil case with multiple compartments. Fits up to 50 pens, waterproof material. Smooth YKK zipper, available in 8 colors.", "price": 12.99, "stock": 55, "category": "Stationery", "image_url": "https://images.unsplash.com/photo-1544816155-12df9643f363?w=400&h=300&fit=crop"},
    {"name": "Ruler & Protractor Set", "description": "Stainless steel ruler set with protractor. 12 inch and 6 inch rulers, 180-degree protractor. Etched markings, non-glare finish.", "price": 7.99, "stock": 70, "category": "Stationery", "image_url": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=400&h=300&fit=crop"},

    # Home & Kitchen
    {"name": "Coffee Maker", "description": "Programmable drip coffee maker with 12-cup capacity. Built-in grinder, thermal carafe, and auto-brew timer. Perfect morning brew every time.", "price": 89.99, "stock": 22, "category": "Home & Kitchen", "image_url": "https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=400&h=300&fit=crop"},
    {"name": "Air Fryer", "description": "5.8QT digital air fryer with 8 presets. Oil-free cooking, 1700W rapid air technology. Dishwasher-safe basket, perfect for healthy meals.", "price": 119.99, "stock": 18, "category": "Home & Kitchen", "image_url": "https://images.unsplash.com/photo-1626509653291-18d9a934b9db?w=400&h=300&fit=crop"},
    {"name": "Electric Kettle", "description": "Stainless steel cordless electric kettle, 1.7L. 1500W fast boil, auto shut-off, and boil-dry protection. Boil water in under 5 minutes.", "price": 39.99, "stock": 40, "category": "Home & Kitchen", "image_url": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=400&h=300&fit=crop"},
    {"name": "Knife Set", "description": "15-piece kitchen knife set with wooden block. German stainless steel blades, ergonomic handles. Includes chef, paring, bread, and steak knives.", "price": 149.99, "stock": 15, "category": "Home & Kitchen", "image_url": "https://images.unsplash.com/photo-1593618998160-e34014e67546?w=400&h=300&fit=crop"},
    {"name": "Blender", "description": "High-powered 1200W blender with 52oz glass jar. 7 variable speeds, pulse function, and self-cleaning mode. Crushes ice and frozen fruit effortlessly.", "price": 79.99, "stock": 28, "category": "Home & Kitchen", "image_url": "https://images.unsplash.com/photo-1570222094114-d054a817e56b?w=400&h=300&fit=crop"},
    {"name": "Cookware Set", "description": "10-piece non-stick cookware set. PFOA-free granite coating, induction compatible. Includes pans, pots, and lids for all your cooking needs.", "price": 179.99, "stock": 12, "category": "Home & Kitchen", "image_url": "https://images.unsplash.com/photo-1584990347449-a8b13e8a3a47?w=400&h=300&fit=crop"},

    # Fitness
    {"name": "Yoga Mat", "description": "Premium 6mm thick yoga mat with carrying strap. Non-slip texture, eco-friendly TPE material. Lightweight and perfect for all yoga styles.", "price": 29.99, "stock": 60, "category": "Fitness", "image_url": "https://images.unsplash.com/photo-1601925260368-ae2f83cf8b7f?w=400&h=300&fit=crop"},
    {"name": "Dumbbell Set", "description": "Adjustable dumbbell set 5-50lbs. Quick-change weight system, space-saving design. Perfect for home gym strength training.", "price": 299.99, "stock": 10, "category": "Fitness", "image_url": "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?w=400&h=300&fit=crop"},
    {"name": "Resistance Bands", "description": "Set of 5 resistance bands with door anchor and handles. 10-150lbs resistance levels, carry bag included. Full-body workout anywhere.", "price": 24.99, "stock": 75, "category": "Fitness", "image_url": "https://images.unsplash.com/photo-1598289431512-b97b0917dc41?w=400&h=300&fit=crop"},
    {"name": "Foam Roller", "description": "High-density foam roller for muscle recovery. 36-inch length, textured surface for deep tissue massage. Relieves muscle soreness and tension.", "price": 19.99, "stock": 50, "category": "Fitness", "image_url": "https://images.unsplash.com/photo-1518611012118-696072aa579a?w=400&h=300&fit=crop"},
    {"name": "Fitness Tracker", "description": "Slim fitness tracker with heart rate, sleep monitor, and 14-day battery. 5ATM water resistant, smartphone notifications. Track steps, calories, and workouts.", "price": 69.99, "stock": 35, "category": "Fitness", "image_url": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=300&fit=crop"},
    {"name": "Jump Rope", "description": "Speed jump rope with ball bearings for smooth rotation. Adjustable length, foam handles. Great for cardio and coordination training.", "price": 12.99, "stock": 90, "category": "Fitness", "image_url": "https://images.unsplash.com/photo-1601422407692-ec4eeec1d9b3?w=400&h=300&fit=crop"},

    # Books & Games
    {"name": "Classic Novel Collection", "description": "Set of 5 timeless classic novels in hardcover. Includes Pride and Prejudice, 1984, To Kill a Mockingbird, The Great Gatsby, and Jane Eyre.", "price": 59.99, "stock": 25, "category": "Books", "image_url": "https://images.unsplash.com/photo-1495446815901-a7297e633e8d?w=400&h=300&fit=crop"},
    {"name": "Chess Set", "description": "Wooden chess set with folding board. Hand-carved pieces, 15-inch board. Perfect for beginners and grandmasters alike.", "price": 44.99, "stock": 30, "category": "Games", "image_url": "https://images.unsplash.com/photo-1528819622765-d6bcf132f793?w=400&h=300&fit=crop"},
    {"name": "Puzzle 1000 Pieces", "description": "1000-piece jigsaw puzzle featuring world map artwork. Premium quality, 26x18 inches finished size. Great for relaxation and family time.", "price": 19.99, "stock": 45, "category": "Games", "image_url": "https://images.unsplash.com/photo-1494059980473-813e73ee784b?w=400&h=300&fit=crop"},
    {"name": "Coloring Book Set", "description": "Adult coloring book set of 3 with 60 colored pencils. Stress-relief designs including mandalas, flowers, and patterns.", "price": 24.99, "stock": 55, "category": "Books", "image_url": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=400&h=300&fit=crop"},
    {"name": "Board Game Strategy", "description": "Award-winning strategy board game for 2-4 players. 60-minute playtime, ages 10+. Build cities, manage resources, and trade with rivals.", "price": 49.99, "stock": 20, "category": "Games", "image_url": "https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=400&h=300&fit=crop"},

    # Outdoor & Travel
    {"name": "Camping Tent", "description": "4-person waterproof dome tent with rainfly. Easy 10-minute setup, 7x4 feet floor. Great for family camping and outdoor adventures.", "price": 129.99, "stock": 14, "category": "Outdoor", "image_url": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=400&h=300&fit=crop"},
    {"name": "Sleeping Bag", "description": "3-season mummy sleeping bag rated to 20°F. Lightweight, compressible, water-resistant shell. Perfect for backpacking and camping.", "price": 69.99, "stock": 22, "category": "Outdoor", "image_url": "https://images.unsplash.com/photo-1578897367107-77d39ba0837b?w=400&h=300&fit=crop"},
    {"name": "Hiking Boots", "description": "Waterproof hiking boots with ankle support. Vibram sole for superior grip, breathable mesh lining. Available in men and women sizes.", "price": 119.99, "stock": 30, "category": "Outdoor", "image_url": "https://images.unsplash.com/photo-1542840843-3349799cded6?w=400&h=300&fit=crop"},
    {"name": "Water Bottle", "description": "Insulated stainless steel water bottle 32oz. Keeps drinks cold 24hrs or hot 12hrs. BPA-free, leak-proof lid, wide mouth for ice.", "price": 29.99, "stock": 80, "category": "Outdoor", "image_url": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=400&h=300&fit=crop"},
    {"name": "Headlamp", "description": "USB rechargeable LED headlamp 350 lumens. 5 modes, 60-degree adjustable beam. Waterproof, lightweight for running and camping.", "price": 22.99, "stock": 65, "category": "Outdoor", "image_url": "https://images.unsplash.com/photo-1542856204-00101eb6def4?w=400&h=300&fit=crop"},
    {"name": "Daypack", "description": "20L lightweight daypack for hiking and travel. Padded straps, hydration compatible, multiple pockets. Folds into its own pocket.", "price": 39.99, "stock": 40, "category": "Outdoor", "image_url": "https://images.unsplash.com/photo-1622260614153-03223fb72052?w=400&h=300&fit=crop"},

    # Beauty & Personal Care
    {"name": "Hair Dryer", "description": "Professional ionic hair dryer 1875W. 3 heat settings, 2 speed settings, cool shot button. Includes concentrator and diffuser attachments.", "price": 59.99, "stock": 35, "category": "Beauty", "image_url": "https://images.unsplash.com/photo-1522338242992-e1a54906a8da?w=400&h=300&fit=crop"},
    {"name": "Electric Toothbrush", "description": "Sonic electric toothbrush with 5 brushing modes. 30-day battery life, smart timer, and pressure sensor. 4 brush heads included.", "price": 79.99, "stock": 28, "category": "Beauty", "image_url": "https://images.unsplash.com/photo-1559591935-c6c92c6a5f5e?w=400&h=300&fit=crop"},
    {"name": "Skincare Set", "description": "Complete 5-step skincare routine set. Cleanser, toner, serum, moisturizer, and SPF. Suitable for all skin types, paraben-free.", "price": 89.99, "stock": 20, "category": "Beauty", "image_url": "https://images.unsplash.com/photo-1556228720-195a672e8a03?w=400&h=300&fit=crop"},
    {"name": "Perfume Collection", "description": "Set of 3 signature fragrances 30ml each. Floral, citrus, and woody scents. Long-lasting eau de parfum, elegant gift packaging.", "price": 69.99, "stock": 18, "category": "Beauty", "image_url": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=400&h=300&fit=crop"},

    # Pet Supplies
    {"name": "Pet Bed", "description": "Orthopedic memory foam pet bed for dogs and cats. Removable washable cover, non-slip bottom. Available in small, medium, and large.", "price": 49.99, "stock": 30, "category": "Pet Supplies", "image_url": "https://images.unsplash.com/photo-1591946614720-90a587da4a36?w=400&h=300&fit=crop"},
    {"name": "Cat Toy Set", "description": "Interactive cat toy set of 6. Includes feather wand, laser pointer, catnip mice, and crinkle balls. Hours of feline entertainment.", "price": 14.99, "stock": 70, "category": "Pet Supplies", "image_url": "https://images.unsplash.com/photo-1574144611937-0df059b5ef3e?w=400&h=300&fit=crop"},
    {"name": "Dog Leash", "description": "Heavy-duty reflective dog leash 6ft. Padded handle, 360-degree swivel clasp. Strong nylon webbing for medium and large dogs.", "price": 19.99, "stock": 55, "category": "Pet Supplies", "image_url": "https://images.unsplash.com/photo-1583511655857-d19b40a7a54e?w=400&h=300&fit=crop"},
]


def seed():
    db = SessionLocal()
    try:
        existing = db.query(Product).count()
        existing_names = {p.name for p in db.query(Product).all()}
        new_products = [Product(**p) for p in SAMPLE_PRODUCTS if p["name"] not in existing_names]
        for p in new_products:
            db.add(p)

        admin = None
        if existing == 0:
            admin = User(
                username="admin",
                email="admin@luckyshop.com",
                hashed_password=get_password_hash("admin123"),
                is_admin=True,
            )
            db.add(admin)

        db.commit()
        print(f"Added {len(new_products)} new products." + (" Created admin user (admin / admin123)." if admin else ""))
    finally:
        db.close()


if __name__ == "__main__":
    seed()
