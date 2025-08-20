from typing import Dict, Any, List
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


def generate_items_batch(
    count: int = 5, overrides: Dict[str, Any] = None
) -> List[Dict[str, Any]]:
    """Generate a batch of fake items for testing."""
    items = []
    for i in range(count):
        item_data = generate_item_data(overrides)
        if overrides and "id" not in overrides:
            item_data["id"] = i + 1
        items.append(item_data)
    return items


def generate_invalid_item_data() -> List[Dict[str, Any]]:
    """Generate various invalid item data for testing validation."""
    return [
        {"title": "", "price": 10.0},  # Empty title
        {"title": "Valid Title", "price": -10.0},  # Negative price
        {"title": "A" * 101, "price": 10.0},  # Title too long
        {"description": "Only description"},  # Missing required fields
        {"title": 123, "price": "invalid"},  # Wrong data types
        {},  # Empty data
    ]


def generate_pagination_test_cases() -> List[Dict[str, Any]]:
    """Generate pagination test cases."""
    return [
        {"skip": 0, "limit": 10},  # Normal case
        {"skip": 10, "limit": 20},  # Offset case
        {"skip": 100, "limit": 50},  # Large offset
        {"skip": 0, "limit": 1},  # Single item
        {"skip": 0, "limit": 1000},  # Maximum limit
    ]


def generate_search_test_cases() -> List[str]:
    """Generate search test cases."""
    return [
        "test",
        "item",
        "product",
        "sample",
        "example",
        "nonexistent",
        "",  # Empty search
        "a" * 50,  # Long search term
    ]
