import uuid

def format_variable_param(key, value, type_="category"):
    return [
        {
            "id": uuid.uuid4(),
            "type": type_,
            "value": value,
            "target": ["variable", ["template-tag", key]],
        }
    ]
