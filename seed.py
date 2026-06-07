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
]


def seed():
    db = SessionLocal()
    try:
        if db.query(Product).count() > 0:
            print("Database already seeded.")
            return
        for p in SAMPLE_PRODUCTS:
            db.add(Product(**p))

        admin = User(
            username="admin",
            email="admin@luckyshop.com",
            hashed_password=get_password_hash("admin123"),
            is_admin=True,
        )
        db.add(admin)
        db.commit()
        print(f"Seeded {len(SAMPLE_PRODUCTS)} products and admin user (admin / admin123).")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
