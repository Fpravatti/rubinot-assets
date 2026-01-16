import json
import os
import requests
from urllib.parse import urlparse

BASE_URL = "https://cdn.tibiaroute.com"

JSON_FILES = [
    "task_monster.json",
    "task_item.json"
]

OUTPUT_DIRS = {
    "monsters": "monsters",
    "items": "items"
}

# Cria pastas
for folder in OUTPUT_DIRS.values():
    os.makedirs(folder, exist_ok=True)


def download_file(url):
    path = urlparse(url).path
    filename = os.path.basename(path)

    if "/monsters/" in path:
        folder = OUTPUT_DIRS["monsters"]
    elif "/items/" in path:
        folder = OUTPUT_DIRS["items"]
    else:
        print(f"⚠️ Pasta desconhecida para {url}")
        return

    output_path = os.path.join(folder, filename)

    if os.path.exists(output_path):
        print(f"⏩ Já existe: {output_path}")
        return

    print(f"⬇️ Baixando: {url}")
    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Salvo em: {output_path}")
    else:
        print(f"❌ Erro {response.status_code}: {url}")


def extract_images(obj):
    """
    Percorre recursivamente o JSON procurando chaves 'image'
    """
    if isinstance(obj, dict):
        for key, value in obj.items():
            if key == "image" and isinstance(value, str):
                image_url = value.replace("{{URL}}", BASE_URL)
                download_file(image_url)
            else:
                extract_images(value)

    elif isinstance(obj, list):
        for item in obj:
            extract_images(item)


for json_file in JSON_FILES:
    print(f"\n📂 Processando {json_file}")
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    extract_images(data)
