from typing import get_type_hints, List, Dict
from faker import Faker

import dataclasses

fake = Faker()

def generate_fake_data(cls):
    fake_data = {}
    type_hints = get_type_hints(cls)
    for attribute_name in type_hints:
        attribute_type = type_hints[attribute_name]
        if attribute_type == str:
            fake_data[attribute_name] = fake.word()
        elif attribute_type == int:
            fake_data[attribute_name] = fake.random_int()
        elif attribute_type == float:
            fake_data[attribute_name] = fake.pyfloat()
        elif attribute_type == bool:
            fake_data[attribute_name] = fake.boolean()
        elif attribute_type == List[str]:
            fake_data[attribute_name] = [fake.word() for _ in range(3)]
        elif attribute_type == List[int]:
            fake_data[attribute_name] = [fake.random_int() for _ in range(3)]
        elif attribute_type == List[float]:
            fake_data[attribute_name] = [fake.pyfloat() for _ in range(3)]
        elif attribute_type == List[bool]:
            fake_data[attribute_name] = [fake.boolean() for _ in range(3)]
        elif attribute_type == Dict[str, str]:
            fake_data[attribute_name] = {fake.word(): fake.word() for _ in range(3)}
        elif attribute_type == Dict[str, int]:
            fake_data[attribute_name] = {fake.word(): fake.random_int() for _ in range(3)}
        elif attribute_type == Dict[str, float]:
            fake_data[attribute_name] = {fake.word(): fake.pyfloat() for _ in range(3)}
        elif attribute_type == Dict[str, bool]:
            fake_data[attribute_name] = {fake.word(): fake.boolean() for _ in range(3)}
        elif dataclasses.is_dataclass(attribute_type):
            fake_data[attribute_name] = generate_fake_data(attribute_type)
    return cls(**fake_data)
