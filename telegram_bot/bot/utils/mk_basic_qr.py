import requests
from config import server_url, files
from PIL import Image
import time

def create_basic_qr(data: str) -> tuple:
    """
    Функция которая отправляет на сервер server_url информацию data,
    сервер генерирует qr код и сохраняет его по указанному пути files.

    возвращает путь сохранённого куара и ссылку на сервер
    """
    create_url = server_url + "api/qrs/basic"
    get_qr_by_key_url = server_url + "api/qrs/get-result/{}"
    qr_path_tiff: str = files + "qr.tiff"
    qr_path_png: str = files + "qr.png"
    response = requests.post(url=create_url, json={"data": data})
    key: str = response.json()["key"]
    for _ in range(10):
        response = requests.get(
            get_qr_by_key_url.format(key)
        )
        if response.json().get("result"):

            qr_server_path = server_url + response.json()["result"]["qr_code"]
            response = requests.get(qr_server_path)
            with open(qr_path_tiff, "wb") as file:
                file.write(response.content)
            tiff = Image.open(qr_path_tiff)
            tiff.save(qr_path_png, format="PNG")
            tiff.close()

            return qr_path_png, qr_path_tiff
        time.sleep(1)
    return (0, 0)