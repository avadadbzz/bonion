import json

class JsonLoader:
    def __init__(self, json_file_path):
        self.json_file_path = json_file_path

    def load(self, fields):
        try:
            with open(self.json_file_path, 'r') as json_file:
                data = json.load(json_file)
        except Exception as e:
            print(f"An error occurred while loading the JSON file: {e}")
            return []

        selected_fields = []
        for item in data:
            field_values = {}
            for field in fields:
                keys = field.split('.')
                value = item
                for key in keys:
                    if isinstance(value, dict):
                        value = value.get(key, None)
                    else:
                        value = None
                        break
                field_values[keys[-1].lower()] = value if value is not None else None
            selected_fields.append(field_values)

        return selected_fields
