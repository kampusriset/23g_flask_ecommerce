
def get_new_arrivals():
    return [
        {"id": 1, "name": "Scania L 300", "price": 170, "rating": 4.5, "image": "truck1.jpg", "old_price": None},
        {"id": 2, "name": "Thunder 2000", "price": 240, "rating": 3.0, "image": "truck2.jpg", "old_price": 260},
        {"id": 3, "name": "MAN TGS 220", "price": 180, "rating": 4.0, "image": "truck3.jpg", "old_price": None},
        {"id": 4, "name": "Blue V8 500 GIGA", "price": 130, "rating": 4.8, "image": "truck4.jpg", "old_price": 160},
    ]

def get_top_selling():
    return [
        {"id": 5, "name": "MAN TGX 220", "price": 212, "rating": 5.0, "image": "truck5.jpg", "old_price": 232},
        {"id": 6, "name": "Volvo Europe 500", "price": 145, "rating": 4.0, "image": "truck6.jpg", "old_price": None},
        {"id": 7, "name": "MAN TGX 41.000", "price": 80, "rating": 3.5, "image": "truck7.jpg", "old_price": None},
        {"id": 8, "name": "Arocs 2645", "price": 210, "rating": 4.5, "image": "truck8.jpg", "old_price": None},
    ]

def get_styles():
    return [
        {"name": "Casual", "image": "style_casual.jpg"},
        {"name": "Ranger", "image": "style_ranger.jpg"},
        {"name": "E-Trucks", "image": "style_etruck.jpg"},
        {"name": "Sport", "image": "style_sport.jpg"},
    ]