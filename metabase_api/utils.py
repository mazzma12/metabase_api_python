import uuid

def format_variable_param(key, value, type_="category"):
    return [
        {
            "id": str(uuid.uuid4()),
            "type": type_,
            "value": value,
            "target": ["variable", ["template-tag", key]],
        }
    ]

if __name__ == "__main__":
    res = format_variable_param("organization", "1234")
    print(res)
