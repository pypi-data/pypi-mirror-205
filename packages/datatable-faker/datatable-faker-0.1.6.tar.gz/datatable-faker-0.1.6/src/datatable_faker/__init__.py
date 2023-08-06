from typing import Type, List, Dict, Tuple, Union, Optional,get_type_hints

from faker import Faker
from pydantic import BaseModel

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


def generate_fake_data_from_pydentic(model_class: Type[BaseModel]) -> BaseModel:
    fake_data = {}
    for field in model_class.__fields__.values():
        field_type = field.type_
        if field_type is int:
            fake_data[field.name] = fake.random_int()
        elif field_type is float:
            fake_data[field.name] = fake.pyfloat()
        elif field_type is str:
            fake_data[field.name] = fake.word()
        elif field_type is bool:
            fake_data[field.name] = fake.boolean()
        elif issubclass(field_type, BaseModel):
            fake_data[field.name] = generate_fake_data_from_pydentic(field_type)
        elif field_type is List[int]:
            fake_data[field.name] = [fake.random_int() for _ in range(3)]
        elif field_type is List[float]:
            fake_data[field.name] = [fake.pyfloat() for _ in range(3)]
        elif field_type is List[str]:
            fake_data[field.name] = [fake.word() for _ in range(3)]
        elif field_type is List[bool]:
            fake_data[field.name] = [fake.boolean() for _ in range(3)]
        elif field_type.__origin__ is list:
            inner_type = field_type.__args__[0]
            fake_data[field.name] = [generate_fake_data_from_pydentic(inner_type) for _ in range(3)]
        elif field_type is Dict[str, int]:
            fake_data[field.name] = {fake.word(): fake.random_int() for _ in range(3)}
        elif field_type is Dict[str, float]:
            fake_data[field.name] = {fake.word(): fake.pyfloat() for _ in range(3)}
        elif field_type is Dict[str, str]:
            fake_data[field.name] = {fake.word(): fake.word() for _ in range(3)}
        elif field_type is Dict[str, bool]:
            fake_data[field.name] = {fake.word(): fake.boolean() for _ in range(3)}
        elif field_type.__origin__ is dict:
            key_type, value_type = field_type.__args__
            fake_data[field.name] = {generate_fake_data_from_pydentic(key_type): generate_fake_data_from_pydentic(value_type) for _ in range(3)}
        elif field_type is Tuple[int, str]:
            fake_data[field.name] = (fake.random_int(), fake.word())
        elif field_type is Tuple[int, str, bool]:
            fake_data[field.name] = (fake.random_int(), fake.word(), fake.boolean())
        elif field_type is Tuple[int, str, bool, float]:
            fake_data[field.name] = (fake.random_int(), fake.word(), fake.boolean(), fake.pyfloat())
        elif field_type.__origin__ is tuple:
            inner_types = field_type.__args__
            fake_data[field.name] = tuple(generate_fake_data_from_pydentic(inner_type) for inner_type in inner_types)
        elif field_type is Union[int, str]:
            fake_data[field.name] = fake.random_element([fake.random_int(), fake.word()])
        elif field_type is Optional[int]:
            fake_data[field.name] = fake.random_element([fake.random_int(), None])
        elif field_type.__origin__ is Union:
            inner_types = field_type.__args__
            fake_data[field.name] = fake.random_element([generate_fake_data_from_pydentic(inner_type) for inner_type in inner_types])
    return model_class(**fake_data)
