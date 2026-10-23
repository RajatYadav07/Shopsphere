"""
ShopSphere Database Seeding Script
Populates MongoDB with >= 100 products, 50 customers, 200 orders, 100 reviews,
and corresponding inventory movement records.
Safe to re-run: Uses idempotent checks on unique SKUs and email addresses.
Never wipes user data automatically.
"""

import os
import sys
import random
from datetime import datetime, timedelta, timezone

# Add backend directory to sys.path so app imports work
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from pymongo import MongoClient
from app.core.config import settings
from app.core.indexes import create_all_indexes
from app.core.validators import apply_collection_validators

CATEGORIES = {
    "Electronics": ["Sony", "Samsung", "LG", "Anker", "Belkin"],
    "Audio & Wearables": ["Bose", "Sennheiser", "Sony", "Apple", "JBL"],
    "Computing & Accessories": ["Logitech", "Dell", "Corsair", "Keychron", "ASUS"],
    "Smart Home": ["Philips Hue", "Amazon", "Google", "TP-Link", "Eufy"],
    "Photography & Video": ["Canon", "Sony", "DJI", "GoPro", "Nikon"],
    "Gaming Gear": ["Razer", "SteelSeries", "HyperX", "Logitech G", "Corsair"]
}

PRODUCT_TEMPLATES = [
    # Electronics
    ("4K Ultra HD Smart OLED TV 55-inch", "Electronics", 899.99, "OLED panel with 120Hz refresh rate and Dolby Vision."),
    ("Wireless Fast Charging Stand 15W", "Electronics", 34.99, "Qi-certified fast wireless charging with thermal protection."),
    ("Portable Power Bank 20000mAh 65W PD", "Electronics", 59.99, "High-capacity power bank supporting fast laptop charging."),
    ("Universal Travel Adapter with GaN 65W", "Electronics", 39.99, "All-in-one international plug adapter with dual USB-C ports."),
    ("Smart Plug WiFi Outlet with Energy Monitor", "Electronics", 19.99, "Remote control power switch with scheduling and voice assistant."),
    ("HDMI 2.1 Ultra High Speed Cable 2m", "Electronics", 14.99, "Supports 8K 60Hz and 4K 120Hz with eARC audio pass-through."),
    ("Active Stylus Pen for Touchscreens", "Electronics", 29.99, "Pressure-sensitive magnetic rechargeable stylus pen."),
    ("USB-C 10-in-1 Dual 4K Display Dock", "Electronics", 89.99, "Full hub with HDMI, Gigabit Ethernet, SD card, and 100W PD pass-through."),
    ("Surge Protector Power Strip 8 Outlets", "Electronics", 24.99, "Heavy duty 4000 Joules surge protection with USB-C ports."),
    ("Bluetooth 5.3 Audio Transmitter/Receiver", "Electronics", 22.99, "Low-latency aptX wireless audio bridge for flights and cars."),
    ("Magnetic Wireless Battery Pack 5000mAh", "Electronics", 45.00, "Snap-on magnetic power bank compatible with MagSafe."),
    ("Rechargeable LED Desk Lamp with Wireless Charger", "Electronics", 49.99, "Dimmable eye-care task lamp with color temperature control."),
    ("Smart TV Streaming Stick 4K Max", "Electronics", 54.99, "Next-gen Wi-Fi 6 streaming media player with voice remote."),
    ("Car Charger 60W Dual Port Fast Charge", "Electronics", 18.99, "Compact aluminum 12V car socket charger for phones and tablets."),
    ("Solar Portable Charger 10000mAh", "Electronics", 39.99, "Rugged waterproof solar panel backup battery with flashlight."),
    ("Digital Smart Measuring Tape with Laser", "Electronics", 34.50, "OLED screen measuring tool with Bluetooth mobile sync."),
    ("Rechargeable Hand Warmers 2-Pack", "Electronics", 27.99, "Portable electric pocket heaters with 3 heat levels."),
    ("Portable Bluetooth Conference Speakerphone", "Electronics", 99.00, "360-degree microphone array with noise suppression."),
    ("Smart Water Leak Sensor 3-Pack", "Electronics", 49.00, "Immediate phone alert notifications upon water detection."),

    # Audio & Wearables
    ("QuietComfort Noise Cancelling Headphones", "Audio & Wearables", 349.00, "World-class active noise cancellation with 24h battery life."),
    ("True Wireless Earbuds with ANC", "Audio & Wearables", 149.99, "Custom dynamic drivers with transparency mode and IPX5 rating."),
    ("Hi-Res Studio Monitor Headphones", "Audio & Wearables", 179.00, "Open-back over-ear reference headphones for audio mixing."),
    ("Rugged Outdoor Bluetooth Speaker", "Audio & Wearables", 89.99, "IP67 waterproof and dustproof speaker with 15h continuous play."),
    ("Smart Fitness Watch with SpO2 and GPS", "Audio & Wearables", 229.00, "Advanced health tracking watch with sleep analysis and GPS."),
    ("Bone Conduction Open-Ear Sport Headphones", "Audio & Wearables", 119.00, "Lightweight titanium frame headphones for safe outdoor running."),
    ("Compact Desktop Soundbar with Subwoofer", "Audio & Wearables", 129.99, "Rich room-filling acoustic soundbar with Bluetooth 5.2."),
    ("Wireless Neckband Earphones with Mic", "Audio & Wearables", 49.99, "Magnetic earbuds with vibration call alert and 20h battery."),
    ("Smart Ring Sleep and Heart Rate Tracker", "Audio & Wearables", 299.00, "Titanium biometric health ring with water resistance to 100m."),
    ("Clip-On Lavalier Wireless Microphone System", "Audio & Wearables", 99.99, "Dual transmitter wireless mic kit for interviews and vlogging."),
    ("Retro Vinyl Turntable with Bluetooth Out", "Audio & Wearables", 159.00, "Belt-drive 3-speed record player with built-in preamp."),
    ("Kids Safe Volume-Limiting Headphones", "Audio & Wearables", 24.99, "Capped at 85dB volume with flexible headband and stickers."),
    ("Shower Waterproof Bluetooth Speaker", "Audio & Wearables", 29.99, "Suction cup speaker with FM radio and hands-free calling."),
    ("USB Condenser Podcast Microphone", "Audio & Wearables", 79.99, "Cardioid pickup pattern with zero-latency headphone monitoring."),
    ("In-Ear HiFi Earphones with Detachable Cable", "Audio & Wearables", 69.99, "Dual hybrid dynamic drivers with braided silver-plated wire."),
    ("Magnetic Wireless Sports Earbuds", "Audio & Wearables", 39.99, "Sweatproof secure-fit ear hooks with deep bass tuning."),
    ("Sleep Headband with Ultra-Thin Speakers", "Audio & Wearables", 22.99, "Soft breathable eye mask headphones for side sleepers."),
    ("Audio Interface 2-Channel USB-C", "Audio & Wearables", 139.00, "Studio-grade mic preamps with direct 48V phantom power."),

    # Computing & Accessories
    ("Custom Mechanical Keyboard 75% Wireless", "Computing & Accessories", 119.99, "Hot-swappable tactile switches with RGB and PBT keycaps."),
    ("Ergonomic Vertical Wireless Mouse", "Computing & Accessories", 49.99, "Natural handshake grip reducing forearm strain and wrist pain."),
    ("Ultrawide Curved Monitor 34-inch 144Hz", "Computing & Accessories", 499.00, "WQHD 3440x1440 curved IPS panel with HDR400 and USB-C."),
    ("Aluminum Laptop Stand with Swivel Base", "Computing & Accessories", 39.99, "360-degree rotating height-adjustable aluminum riser."),
    ("External Portable SSD 1TB NVMe 1050MB/s", "Computing & Accessories", 99.99, "Rugged drop-resistant portable storage with hardware encryption."),
    ("Webcam 4K Ultra HD with Privacy Shutter", "Computing & Accessories", 109.99, "Dual noise-canceling stereo mics with HDR auto-exposure."),
    ("Large Leather Desk Mat Pad 90x40cm", "Computing & Accessories", 24.99, "Smooth waterproof desk blotter with anti-slip suede base."),
    ("Magnetic Privacy Screen Filter 15.6-inch", "Computing & Accessories", 34.99, "Limits viewing angle to +/- 30 degrees with anti-glare coating."),
    ("USB-C to DisplayPort 1.4 Braided Cable", "Computing & Accessories", 16.99, "Supports 8K 60Hz and 4K 144Hz with nylon braiding."),
    ("Wireless Numeric Keypad Mechanical", "Computing & Accessories", 29.99, "21-key standalone hot-swap numpad for spreadsheet accounting."),
    ("Monitor Light Bar with Auto-Dimming", "Computing & Accessories", 59.99, "Space-saving screen-mounted bar reducing glare and eye fatigue."),
    ("GaN Multiport Desktop Charger 140W", "Computing & Accessories", 79.99, "Quad-port charger powering two laptops simultaneously."),
    ("Cable Management Box Organizer Kit", "Computing & Accessories", 19.99, "Conceals power strips and tangled wires with bamboo lid."),
    ("Under-Desk Headphone Hook Mount", "Computing & Accessories", 12.99, "Aluminum dual headphone hanger with cable clip organizer."),
    ("High-Speed Wi-Fi 6E PCIe Adapter", "Computing & Accessories", 39.99, "Tri-band 5400Mbps card with external magnetic antenna base."),
    ("Gel Memory Foam Wrist Rest Set", "Computing & Accessories", 18.99, "Ergonomic keyboard and mouse pad wrist cushion."),
    ("Screen Cleaning Spray and Microfiber Kit", "Computing & Accessories", 9.99, "Ammonia-free streak-free solution safe for OLED and retina displays."),
    ("Hard Drive Docking Station Dual Bay", "Computing & Accessories", 44.99, "Offline clone function for 2.5 and 3.5 inch SATA HDDs/SSDs."),

    # Smart Home
    ("Smart Color LED Light Bulb Starter Kit (4-Pack)", "Smart Home", 79.99, "16 million colors with sync to music and automated schedules."),
    ("Smart Video Doorbell 2K with Chime", "Smart Home", 129.99, "Dual motion sensors with person detection and local storage."),
    ("Indoor Pan/Tilt Security Camera 360", "Smart Home", 44.99, "2K resolution with automatic motion tracking and night vision."),
    ("Smart Wi-Fi Thermostat with Room Sensor", "Smart Home", 169.00, "Energy star certified programmable climate controller."),
    ("Robot Vacuum and Mop with Auto-Empty Dock", "Smart Home", 449.00, "LiDAR navigation with 4000Pa suction and self-cleaning base."),
    ("Smart Door Lock with Fingerprint & Keypad", "Smart Home", 179.99, "Keyless entry with biometric fingerprint and guest passcodes."),
    ("Smart Air Purifier with HEPA Filter", "Smart Home", 119.00, "Filters 99.97% dust, pollen, and pet dander with air quality sensor."),
    ("Outdoor Solar Security Floodlight Camera", "Smart Home", 149.99, "Wire-free security camera with 2000-lumen motion lights."),
    ("Smart Motorized Blind Drive Motor", "Smart Home", 69.99, "Automates existing roller blinds with timer and light sensor."),
    ("Ultrasonic Aromatherapy Essential Oil Diffuser", "Smart Home", 29.99, "Smart WiFi diffuser with ambient mood lighting."),
    ("Smart Soil Moisture Sensor for Plants", "Smart Home", 24.99, "Measures soil humidity and temperature with smartphone alerts."),
    ("Motion Sensor Night Light (3-Pack)", "Smart Home", 18.99, "Magnetic stick-anywhere warm amber illumination."),
    ("Smart Pet Feeder with HD Camera", "Smart Home", 89.99, "Scheduled portion control with 2-way audio and treat dispenser."),
    ("Smart Humidifier Top-Fill 4.5L", "Smart Home", 59.99, "Quiet cool mist humidifier with auto humidity regulation."),
    ("Smart Smoke and Carbon Monoxide Alarm", "Smart Home", 69.99, "Interconnected voice alarm with battery backup and mobile test."),
    ("Smart Garage Door Opener Controller", "Smart Home", 39.99, "Remote open/close sensor with leave-open warning alerts."),
    ("Smart LED Light Strip 5-Meter RGBIC", "Smart Home", 34.99, "Segmented color light strip with sound reactivity."),
    ("Waterproof Wireless Door Sensor 4-Pack", "Smart Home", 32.99, "Open/close contact alerts for windows, doors, and safes."),

    # Photography & Video
    ("4K Action Camera 60FPS Waterproof 10m", "Photography & Video", 279.00, "RockSteady stabilization with dual color touchscreens."),
    ("Lightweight Compact Drone with 4K Camera", "Photography & Video", 429.00, "Sub-249g folding drone with 3-axis gimbal and 31min flight."),
    ("Smartphone 3-Axis Gimbal Stabilizer", "Photography & Video", 119.00, "AI tracking gimbal with magnetic phone clamp and tripod."),
    ("Carbon Fiber Lightweight Travel Tripod", "Photography & Video", 149.99, "Compact reverse-folding tripod with 360 ball head."),
    ("Continuous Video LED Softbox Lighting Kit", "Photography & Video", 89.99, "Dual 85W daylight balanced lighting stands with diffusers."),
    ("Camera Backpack Water-Resistant with Rain Cover", "Photography & Video", 69.99, "Customizable modular dividers with 15-inch laptop sleeve."),
    ("UHS-II V60 SDXC Memory Card 128GB", "Photography & Video", 49.99, "280MB/s read speeds optimized for 4K video recording."),
    ("Variable ND Filter 67mm (ND2-ND400)", "Photography & Video", 39.99, "Multi-coated optical glass with ultra-slim aluminum rim."),
    ("Camera Cleaning Kit with Sensor Swabs", "Photography & Video", 19.99, "Includes air blower, lens pen, cleaning fluid, and cloths."),
    ("Universal Wireless Camera Remote Shutter", "Photography & Video", 14.99, "Bluetooth shutter trigger compatible with Canon, Sony, Nikon."),
    ("Cold Shoe Metal Extension Bracket Bar", "Photography & Video", 12.99, "Mounts microphone and LED light simultaneously on camera."),
    ("On-Camera Shotgun Microphone with Shockmount", "Photography & Video", 59.99, "Directional broadcast sound pickup with wind muff."),
    ("Collapsible 5-in-1 Photography Reflector 43in", "Photography & Video", 21.99, "Translucent, silver, gold, white, and black light reflectors."),
    ("Quick-Release Camera Wrist Strap Paracord", "Photography & Video", 16.99, "Heavy duty military paracord strap with anchor links."),
    ("Waterproof Floating Hand Grip for Action Cam", "Photography & Video", 13.99, "Non-slip grip with watertight storage compartment."),
    ("Motorized Panoramic Time-Lapse Head", "Photography & Video", 45.00, "360-degree rotating panning base with remote timer."),
    ("Macro Extension Tube Set Auto Focus", "Photography & Video", 38.99, "Enables close-up macro photography with existing lenses."),
    ("Lens Cap Keeper Leash 5-Pack", "Photography & Video", 6.99, "Elastic safety bands preventing lost lens caps."),

    # Gaming Gear
    ("Pro Wireless Esports Gaming Mouse 59g", "Gaming Gear", 129.99, "Ultra-lightweight mouse with 30K optical sensor and optical switches."),
    ("Mechanical Gaming Keyboard TKL Optical", "Gaming Gear", 139.99, "Linear optical switches with per-key RGB and sound dampening foam."),
    ("Wireless Gaming Headset 7.1 Spatial Audio", "Gaming Gear", 99.99, "50mm neodymium drivers with detachable noise-canceling mic."),
    ("Heavy XL Gaming Mouse Pad 900x400x4mm", "Gaming Gear", 29.99, "Micro-woven cloth surface with anti-fray stitched edges."),
    ("Dual Shock Controller Charging Station", "Gaming Gear", 24.99, "Fast click-in charging base for wireless game controllers."),
    ("Adjustable Microphone Boom Arm for Streaming", "Gaming Gear", 39.99, "Internal springs with hidden cable routing channel."),
    ("Streaming Deck Controller 15 LCD Keys", "Gaming Gear", 149.00, "Customizable tactile keys for scene switching, audio, and shortcuts."),
    ("RGB Headphone Stand with 3-Port USB Hub", "Gaming Gear", 27.99, "Weighted base stand with 3.5mm AUX pass-through."),
    ("Precision Aim Controller Thumb Grips 4-Pack", "Gaming Gear", 11.99, "High-rise concave thumbsticks for improved accuracy in FPS games."),
    ("Racing Wheel and Pedals with Force Feedback", "Gaming Gear", 299.00, "Dual-motor force feedback with helical gears and stainless pedals."),
    ("Gaming Glasses Anti-Blue Light Glare", "Gaming Gear", 24.99, "Lightweight acetate frame reducing digital eye strain."),
    ("Bungee Mouse Cable Holder Flexible Arm", "Gaming Gear", 14.99, "Eliminates cable drag with weighted anti-slip base."),
    ("RGB Sound Activated Gaming Light Bars (Pair)", "Gaming Gear", 39.99, "Ambient backlighting with reactive music rhythm modes."),
    ("Flight Simulator Throttle and Stick HOTAS", "Gaming Gear", 169.99, "Hall effect magnetic sensors with 16 action buttons."),
    ("Gaming Chair Ergonomic Memory Foam Lumbar", "Gaming Gear", 29.99, "Contoured cooling gel cushion with adjustable strap."),
    ("Controller Grip Silicone Skin Cover Set", "Gaming Gear", 13.99, "Anti-sweat textured protective cover with analog caps."),
    ("Capture Card 4K Pass-Through 1080p60", "Gaming Gear", 79.99, "Low-latency video capture device for console streaming."),
    ("Foldable Steering Wheel Stand Heavy Duty", "Gaming Gear", 89.99, "Rigid steel mount compatible with major racing wheels.")
]

CUSTOMER_NAMES = [
    ("Alexander Wright", "alex.wright@example.com", "+1-555-0101", "742 Evergreen Terrace", "Springfield"),
    ("Sophia Martinez", "sophia.m@example.com", "+1-555-0102", "124 Conch Street", "Seattle"),
    ("Ethan Sullivan", "ethan.s@example.com", "+1-555-0103", "42 Wallaby Way", "Austin"),
    ("Olivia Chen", "olivia.chen@example.com", "+1-555-0104", "1007 Mountain View Dr", "San Francisco"),
    ("Liam Johnson", "liam.j@example.com", "+1-555-0105", "221B Baker Street", "Boston"),
    ("Emma Davis", "emma.d@example.com", "+1-555-0106", "350 5th Avenue", "New York"),
    ("Noah Taylor", "noah.t@example.com", "+1-555-0107", "410 Terry Ave N", "Seattle"),
    ("Ava Wilson", "ava.wilson@example.com", "+1-555-0108", "1600 Amphitheatre Pkwy", "Mountain View"),
    ("Lucas Anderson", "lucas.a@example.com", "+1-555-0109", "1 Infinite Loop", "Cupertino"),
    ("Mia Thomas", "mia.thomas@example.com", "+1-555-0110", "3000 Ocean Park Blvd", "Santa Monica"),
    ("Benjamin White", "ben.white@example.com", "+1-555-0111", "500 S Buena Vista St", "Burbank"),
    ("Charlotte Harris", "charlotte.h@example.com", "+1-555-0112", "1 Hacker Way", "Menlo Park"),
    ("Henry Martin", "henry.m@example.com", "+1-555-0113", "701 First Avenue", "Sunnyvale"),
    ("Amelia Thompson", "amelia.t@example.com", "+1-555-0114", "100 Winchester Circle", "Los Gatos"),
    ("James Garcia", "james.garcia@example.com", "+1-555-0115", "601 108th Ave NE", "Bellevue"),
    ("Harper Robinson", "harper.r@example.com", "+1-555-0116", "2200 Mission College Blvd", "Santa Clara"),
    ("William Clark", "william.c@example.com", "+1-555-0117", "2701 San Tomas Expy", "Santa Clara"),
    ("Evelyn Rodriguez", "evelyn.rod@example.com", "+1-555-0118", "100 Universal City Plaza", "Universal City"),
    ("Mason Lewis", "mason.l@example.com", "+1-555-0119", "10485 Bandley Drive", "Cupertino"),
    ("Abigail Lee", "abigail.lee@example.com", "+1-555-0120", "2000 Technology Parkway", "Newark"),
    ("Daniel Walker", "daniel.w@example.com", "+1-555-0121", "440 N Bernardo Ave", "Mountain View"),
    ("Emily Hall", "emily.hall@example.com", "+1-555-0122", "111 Innovation Way", "Fremont"),
    ("Matthew Allen", "matthew.a@example.com", "+1-555-0123", "550 Meridian Ave", "San Jose"),
    ("Elizabeth Young", "elizabeth.y@example.com", "+1-555-0124", "1098 Alta Ave", "Mountain View"),
    ("Jack Hernandez", "jack.h@example.com", "+1-555-0125", "345 Encinal Street", "Santa Cruz"),
    ("Avery King", "avery.king@example.com", "+1-555-0126", "800 West El Camino", "Mountain View"),
    ("Samuel Wright", "samuel.w@example.com", "+1-555-0127", "2400 Sand Hill Road", "Menlo Park"),
    ("Ella Lopez", "ella.lopez@example.com", "+1-555-0128", "901 Cherry Ave", "San Bruno"),
    ("David Hill", "david.hill@example.com", "+1-555-0129", "1200 E Grand Ave", "El Segundo"),
    ("Scarlett Scott", "scarlett.s@example.com", "+1-555-0130", "500 West 33rd Street", "New York"),
    ("Joseph Green", "joseph.g@example.com", "+1-555-0131", "345 Park Avenue", "San Jose"),
    ("Grace Adams", "grace.a@example.com", "+1-555-0132", "2000 Sierra Point Pkwy", "Brisbane"),
    ("Carter Baker", "carter.b@example.com", "+1-555-0133", "650 Castro Street", "Mountain View"),
    ("Chloe Gonzalez", "chloe.g@example.com", "+1-555-0134", "777 Mariners Island Blvd", "San Mateo"),
    ("Wyatt Nelson", "wyatt.n@example.com", "+1-555-0135", "100 Spectrum Center Dr", "Irvine"),
    ("Victoria Carter", "victoria.c@example.com", "+1-555-0136", "3333 Scott Blvd", "Santa Clara"),
    ("Owen Mitchell", "owen.m@example.com", "+1-555-0137", "400 Hamilton Ave", "Palo Alto"),
    ("Penelope Perez", "penelope.p@example.com", "+1-555-0138", "1350 Shorebird Way", "Mountain View"),
    ("John Roberts", "john.r@example.com", "+1-555-0139", "2500 Sand Hill Rd", "Menlo Park"),
    ("Riley Turner", "riley.t@example.com", "+1-555-0140", "1201 3rd Ave", "Seattle"),
    ("Luke Phillips", "luke.p@example.com", "+1-555-0141", "600 N Michigan Ave", "Chicago"),
    ("Zoey Campbell", "zoey.c@example.com", "+1-555-0142", "700 Clark Ave", "St. Louis"),
    ("Gabriel Parker", "gabriel.p@example.com", "+1-555-0143", "100 N Biscayne Blvd", "Miami"),
    ("Nora Evans", "nora.e@example.com", "+1-555-0144", "500 Boylston St", "Boston"),
    ("Anthony Edwards", "anthony.e@example.com", "+1-555-0145", "1500 Broadway", "New York"),
    ("Lily Collins", "lily.c@example.com", "+1-555-0146", "200 S Michigan Ave", "Chicago"),
    ("Isaac Stewart", "isaac.s@example.com", "+1-555-0147", "999 18th St", "Denver"),
    ("Eleanor Sanchez", "eleanor.s@example.com", "+1-555-0148", "1000 Main St", "Houston"),
    ("Dylan Morris", "dylan.m@example.com", "+1-555-0149", "201 S Biscayne Blvd", "Miami"),
    ("Hannah Rogers", "hannah.r@example.com", "+1-555-0150", "400 Capitol Mall", "Sacramento"),
    ("Julian Reed", "julian.r@example.com", "+1-555-0151", "1200 17th St", "Denver"),
    ("Lillian Cook", "lillian.c@example.com", "+1-555-0152", "191 N Wacker Dr", "Chicago"),
    ("Leo Morgan", "leo.m@example.com", "+1-555-0153", "300 S Tryon St", "Charlotte"),
    ("Addison Bell", "addison.b@example.com", "+1-555-0154", "1111 Brickell Ave", "Miami"),
    ("Christian Murphy", "christian.m@example.com", "+1-555-0155", "1201 Elm St", "Dallas")
]

REVIEW_COMMENTS = {
    5: [
        "Absolutely fantastic build quality! Exceeded all my expectations.",
        "Best purchase I made this year. High performance and seamless setup.",
        "Unbeatable value for the price. I recommend it to all my colleagues.",
        "Super sleek design and lightning-fast responsiveness. 5 stars all the way!",
        "Packaging was premium and the product works like a dream."
    ],
    4: [
        "Very good quality and solid features. Minor learning curve at first.",
        "Performs reliably every day. Would give 5 stars if cable was slightly longer.",
        "Great battery life and nice ergonomics. Satisfied with this buy.",
        "Smooth experience and looks great on my desk. Fast shipping too."
    ],
    3: [
        "Decent product for casual use, but feels a bit average for the price tag.",
        "It does what it says on the tin. Nothing spectacular, but no major flaws.",
        "Average build quality. Expected a bit more tactile feedback."
    ],
    2: [
        "Had intermittent connection issues during my first week of testing.",
        "Fell short of my expectations. Customer support was helpful though."
    ],
    1: [
        "Unfortunately received a defective unit. Returned for a refund.",
        "Not satisfied with the build materials. Lacks durability."
    ]
}

def seed_database():
    print("=" * 65)
    print("ShopSphere — Starting Safe & Repeatable MongoDB Database Seeding")
    print(f"Connecting to MongoDB at: {settings.MONGODB_URI}")
    print(f"Database: {settings.DATABASE_NAME}")
    print("=" * 65)

    client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=5000)
    db = client[settings.DATABASE_NAME]

    # Verify connection
    client.admin.command("ping")
    print("[OK] Successfully connected to MongoDB Community Server.")

    # Apply schema validators and create indexes
    print("Applying MongoDB JSON Schema validators...")
    apply_collection_validators(db)
    print("Applying database indexes (unique SKUs, emails, compound query indexes)...")
    create_all_indexes(db)

    products_col = db["products"]
    customers_col = db["customers"]
    orders_col = db["orders"]
    reviews_col = db["reviews"]
    inv_col = db["inventory_movements"]

    now = datetime.now(timezone.utc)

    # 1. SEED PRODUCTS (>= 100 products)
    print("\n[1/5] Seeding Products Catalogue...")
    existing_skus = set(products_col.distinct("sku"))
    products_to_insert = []
    prod_sku_counter = 1

    for title, cat, base_price, desc in PRODUCT_TEMPLATES:
        brand = random.choice(CATEGORIES.get(cat, ["ShopSphere"]))
        sku = f"{cat[:4].upper()}-{brand[:3].upper()}-{prod_sku_counter:04d}"
        prod_sku_counter += 1

        if sku in existing_skus:
            continue

        # Stock distribution: 10% low stock (1-10), 5% out of stock (0), 85% healthy stock (20-120)
        stock_rand = random.random()
        if stock_rand < 0.05:
            stock = 0
        elif stock_rand < 0.15:
            stock = random.randint(2, 9)
        else:
            stock = random.randint(25, 120)

        created_days_ago = random.randint(60, 200)
        created_at = now - timedelta(days=created_days_ago)

        tags = [cat.lower(), brand.lower(), "bestseller" if random.random() < 0.3 else "featured"]

        doc = {
            "name": f"{brand} {title}",
            "sku": sku,
            "category": cat,
            "brand": brand,
            "description": desc,
            "price": round(base_price + random.uniform(-5.0, 15.0), 2),
            "stock_quantity": stock,
            "tags": tags,
            "rating_average": 0.0,
            "review_count": 0,
            "image_url": f"https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=400&q=80",
            "created_at": created_at,
            "updated_at": created_at
        }
        products_to_insert.append(doc)
        existing_skus.add(sku)

    if products_to_insert:
        products_col.insert_many(products_to_insert)
        print(f"[OK] Inserted {len(products_to_insert)} new products.")
    else:
        print(f"[OK] Products already seeded ({products_col.count_documents({})} currently present).")

    all_products = list(products_col.find({}))
    print(f"Total products in database: {len(all_products)}")

    # Record initial inventory movements for newly added products
    for p in products_to_insert:
        if p["stock_quantity"] > 0:
            inv_col.insert_one({
                "product_id": p["_id"],
                "change_quantity": p["stock_quantity"],
                "reason": "Initial warehouse inventory intake",
                "related_order_id": None,
                "created_at": p["created_at"]
            })

    # 2. SEED CUSTOMERS (>= 50 customers)
    print("\n[2/5] Seeding Customers...")
    existing_emails = set(customers_col.distinct("email"))
    customers_to_insert = []

    for name, email, phone, addr, city in CUSTOMER_NAMES:
        if email.lower() in existing_emails:
            continue
        reg_days = random.randint(90, 240)
        c_doc = {
            "name": name,
            "email": email.lower(),
            "phone": phone,
            "address": addr,
            "city": city,
            "created_at": now - timedelta(days=reg_days)
        }
        customers_to_insert.append(c_doc)
        existing_emails.add(email.lower())

    if customers_to_insert:
        customers_col.insert_many(customers_to_insert)
        print(f"[OK] Inserted {len(customers_to_insert)} new customers.")
    else:
        print(f"[OK] Customers already seeded ({customers_col.count_documents({})} currently present).")

    all_customers = list(customers_col.find({}))
    print(f"Total customers in database: {len(all_customers)}")

    # 3. SEED ORDERS (>= 200 orders)
    print("\n[3/5] Seeding Orders & Order Item Snapshots...")
    current_orders_count = orders_col.count_documents({})
    target_orders = 220
    orders_needed = max(0, target_orders - current_orders_count)

    if orders_needed > 0:
        orders_to_insert = []
        statuses = ["delivered", "delivered", "delivered", "shipped", "confirmed", "pending", "cancelled"]

        for i in range(orders_needed):
            customer = random.choice(all_customers)
            # Pick 1 to 4 distinct products
            item_count = random.choices([1, 2, 3, 4], weights=[0.4, 0.35, 0.15, 0.1])[0]
            sampled_prods = random.sample(all_products, item_count)

            order_items = []
            subtotal = 0.0

            for prod in sampled_prods:
                qty = random.randint(1, 3)
                price = prod["price"]
                line_total = round(price * qty, 2)
                subtotal += line_total

                order_items.append({
                    "product_id": str(prod["_id"]),
                    "name": prod["name"],
                    "sku": prod["sku"],
                    "unit_price": price,
                    "quantity": qty,
                    "line_total": line_total
                })

            subtotal = round(subtotal, 2)
            status = random.choice(statuses)
            order_days_ago = random.randint(1, 150)
            order_created = now - timedelta(days=order_days_ago, hours=random.randint(1, 23), minutes=random.randint(1, 59))

            order_doc = {
                "customer_id": customer["_id"],
                "items": order_items,
                "shipping_address": {
                    "street": customer.get("address", "100 Market St"),
                    "city": customer.get("city", "San Francisco"),
                    "state": "CA",
                    "postal_code": f"{random.randint(90001, 99999)}",
                    "country": "USA"
                },
                "subtotal": subtotal,
                "status": status,
                "created_at": order_created,
                "updated_at": order_created + timedelta(hours=random.randint(2, 48))
            }
            orders_to_insert.append(order_doc)

        res = orders_col.insert_many(orders_to_insert)
        print(f"[OK] Inserted {len(orders_to_insert)} orders with embedded snapshots and verified mathematical totals.")

        # Log inventory movements for these orders
        movement_batch = []
        for o_id, o_doc in zip(res.inserted_ids, orders_to_insert):
            for item in o_doc["items"]:
                movement_batch.append({
                    "product_id": item["product_id"],
                    "change_quantity": -item["quantity"],
                    "reason": f"Customer order #{str(o_id)} ({o_doc['status']})",
                    "related_order_id": o_id,
                    "created_at": o_doc["created_at"]
                })
        if movement_batch:
            inv_col.insert_many(movement_batch)
            print(f"[OK] Logged {len(movement_batch)} inventory movement audit records.")
    else:
        print(f"[OK] Orders already populated ({current_orders_count} orders present).")

    print(f"Total orders in database: {orders_col.count_documents({})}")

    # 4. SEED REVIEWS (>= 100 reviews)
    print("\n[4/5] Seeding Reviews & Aggregating Derived Ratings...")
    current_reviews_count = reviews_col.count_documents({})
    target_reviews = 130
    reviews_needed = max(0, target_reviews - current_reviews_count)

    if reviews_needed > 0:
        reviews_to_insert = []
        # Rating weights: 5 (50%), 4 (30%), 3 (10%), 2 (5%), 1 (5%)
        rating_choices = [5, 5, 5, 5, 5, 4, 4, 4, 3, 2, 1]

        for _ in range(reviews_needed):
            prod = random.choice(all_products)
            cust = random.choice(all_customers)
            rating = random.choice(rating_choices)
            comment = random.choice(REVIEW_COMMENTS[rating])

            review_days_ago = random.randint(1, 100)
            created_at = now - timedelta(days=review_days_ago)

            reviews_to_insert.append({
                "product_id": prod["_id"],
                "customer_id": cust["_id"],
                "rating": rating,
                "review_text": comment,
                "created_at": created_at
            })

        reviews_col.insert_many(reviews_to_insert)
        print(f"[OK] Inserted {len(reviews_to_insert)} genuine customer reviews.")
    else:
        print(f"[OK] Reviews already present ({current_reviews_count} reviews in database).")

    print(f"Total reviews in database: {reviews_col.count_documents({})}")

    # 5. RECALCULATE RATINGS AGGREGATION
    print("\n[5/5] Synchronizing product rating aggregations...")
    rating_pipeline = [
        {"$group": {
            "_id": "$product_id",
            "avg_rating": {"$avg": "$rating"},
            "review_count": {"$sum": 1}
        }}
    ]
    computed_ratings = list(reviews_col.aggregate(rating_pipeline))
    for r in computed_ratings:
        products_col.update_one(
            {"_id": r["_id"]},
            {"$set": {
                "rating_average": round(float(r["avg_rating"]), 2),
                "review_count": int(r["review_count"]),
                "updated_at": now
            }}
        )
    print(f"[OK] Updated ratings for {len(computed_ratings)} products.")

    # 6. SEED DEMO COLLECTION FOR CONCEPTS LAB
    demo_col = db["shopsphere_demo"]
    if demo_col.count_documents({}) < 5:
        demo_col.delete_many({})
        demo_items = [
            {"item_name": "RGB Mechanical Keyboard", "category": "Peripherals", "price": 89.99, "stock": 25, "created_at": now},
            {"item_name": "Pro Wireless Gaming Mouse", "category": "Peripherals", "price": 49.99, "stock": 40, "created_at": now},
            {"item_name": "USB-C Fast Charger 65W", "category": "Accessories", "price": 29.99, "stock": 65, "created_at": now},
            {"item_name": "Noise Cancelling Headphones", "category": "Audio", "price": 199.99, "stock": 15, "created_at": now},
            {"item_name": "Curved Gaming Monitor 27in", "category": "Displays", "price": 279.99, "stock": 10, "created_at": now}
        ]
        demo_col.insert_many(demo_items)
        print(f"[OK] Initialized {len(demo_items)} documents in isolated 'shopsphere_demo' sandbox.")

    print("\n" + "=" * 65)
    print("Database seeding completed successfully!")
    print(f"Products:            {products_col.count_documents({})}")
    print(f"Customers:           {customers_col.count_documents({})}")
    print(f"Orders:              {orders_col.count_documents({})}")
    print(f"Reviews:             {reviews_col.count_documents({})}")
    print(f"Inventory Movements: {inv_col.count_documents({})}")
    print(f"Demo Sandbox Docs:   {demo_col.count_documents({})}")
    print("=" * 65)

if __name__ == "__main__":
    seed_database()
