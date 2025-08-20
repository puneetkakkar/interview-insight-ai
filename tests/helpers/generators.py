from typing import Dict, Any

from faker import Faker

fake = Faker()


def generate_item_data(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate fake item data for testing."""
    data = {
        "title": fake.word().title(),
        "description": fake.text(max_nb_chars=200),
        "price": round(fake.random_number(digits=3, fix_len=False) / 100, 2),
    }
    
    if overrides:
        data.update(overrides)
    
    return data


def generate_user_data(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate fake user data for testing."""
    data = {
        "name": fake.name(),
        "username": fake.user_name(),
        "email": fake.email(),
        "password": fake.password(length=12),
    }
    
    if overrides:
        data.update(overrides)
    
    return data
