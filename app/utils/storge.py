import json
from pathlib import Path
from typing import Any, List, Dict
import os
import aiofiles
from datetime import datetime

utils_dir = os.path.dirname(os.path.abspath(__file__))
app_dir = os.path.dirname(utils_dir)
db_dir = os.path.join(app_dir, 'db')

def datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Converts datetime to ISO 8601 format
    raise TypeError(f"Type {type(obj)} not serializable")

async def create_file(file_name):
    file_path = os.path.join(db_dir, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    async with aiofiles.open(file_path, 'w') as file:
        await file.write("[]")  # Initialize with an empty list in JSON format
    print(f"file {file_name} created at {file_path}")


async def load_data(file_name: str) -> list[Any]:
    try:
        path = Path(os.path.join(db_dir, file_name))
        if not path.exists():
            print(f"file {file_name} doesn't exists, creating file")
            await create_file(file_name)
            return []
        async with aiofiles.open(path, mode='r') as file:
            content = await file.read()
            if not content:
                return []
            data = json.loads(content)
            return data
    except Exception as exe:
        print(f"Error occured while loading data: {str(exe)}")
        raise Exception(exe)


async def save_data(file_name: str, data: list[Any]):
    try:
        path = Path(os.path.join(db_dir, file_name))
        if not path.exists():
            print(f"file {file_name} doesn't exists, creating file")
            await create_file(file_name)
        async with aiofiles.open(path, mode="w") as file:
            content = json.dumps(data, default=datetime_to_string, indent=4)
            await file.write(content)
            return True
    except Exception as exe:
        print(f"Error occured while saving data: {str(exe)}")
        raise Exception(exe)

async def update_data(file_name: str, updated_data: Any, id: int):
    try:
        path = Path(os.path.join(db_dir, file_name))
        if not path.exists():
            print(f"file {file_name} doesn't exists, creating file")
            await create_file(file_name)
        async with aiofiles.open(path, mode='r') as file:
            content = await file.read()
            data: List[Dict[str, Any]] = json.loads(content)
        found = False
        for c in data:
            if c['id'] == id:
                c.update(updated_data)  # Update with new data
                found = True
                break
        if not found:
            print(f"content with id {id} not found.")
            raise Exception(f"content with id {id} not found.")
        async with aiofiles.open(path, mode='w') as file:
            await file.write(json.dumps(data, indent=4))
        return found
    except Exception as exe:
        print(f"Error occured while saving data: {str(exe)}")
        raise Exception(exe)