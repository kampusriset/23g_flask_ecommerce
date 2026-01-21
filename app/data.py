
def get_new_arrivals():
    return [
        {"id": 1, "name": "Scania L 300", "price": 2650 , "rating": 4.5, "image": "truck1.jpg", "old_price": None},
        {"id": 2, "name": "Thunder 2000", "price": 3720, "rating": 3.0, "image": "truck2.jpg", "old_price": "260 jt"},
        {"id": 3, "name": "MAN TGS 220", "price": 2800, "rating": 4.0, "image": "truck3.jpg", "old_price": None},
        {"id": 4, "name": "Blue V8 500 GIGA", "price": 2000, "rating": 4.8, "image": "truck4.jpg", "old_price": "160 jt"},
    ]

def get_top_selling():
    return [
        {"id": 5, "name": "MAN TGX 220", "price": 3300 , "rating": 5.0, "image": "truck5.jpg", "old_price": "232 jt"},
        {"id": 6, "name": "Volvo Europe 500", "price": 2250, "rating": 4.0, "image": "truck6.jpg", "old_price": None},
        {"id": 7, "name": "MAN TGX 41.000", "price": 1250, "rating": 3.5, "image": "truck7.jpg", "old_price": None},
        {"id": 8, "name": "Arocs 2645", "price": 3250, "rating": 4.5, "image": "truck8.jpg", "old_price": None},
    ]

def get_styles():
    return [
        {"name": "Casual", "image": "style_casual.jpg"},
        {"name": "Ranger", "image": "style_ranger.jpg"},
        {"name": "E-Trucks", "image": "style_etruck.jpg"},
        {"name": "Sport", "image": "style_sport.jpg"},
    ]

def get_brands():
    return [
        {"name": "Scania", "image":"scania.jpg"},
        {"name": "Volvo", "image":"volvo.jpg"},
        {"name": "Mercedes", "image":"mercedes.jpg"},
        {"name": "Man", "image":"man.jpg"},
    ]

def get_all_products():
    """Returns all products from both new arrivals and top selling"""
    return get_new_arrivals() + get_top_selling()

def get_product_by_id(product_id):
    """Returns a single product by ID"""
    all_products = get_all_products()
    for product in all_products:
        if product["id"] == product_id:
            return product
    return None

def format_price_display(price):
    """Format price integer to display string with jt suffix"""
    if isinstance(price, str):
        return price
    return f"{price} jt"