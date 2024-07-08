import os
from dotenv import load_dotenv

load_dotenv()


api_key: str = os.environ["api_key"]
pay_token: str = os.environ["pay_token"]
server_url: str = os.environ.get("server_url") or "http://127.0.0.1:8000/"
files: str = os.environ.get("files") or "files/"
data_base_path: str = os.environ.get("data_base_path") or "users.db"
logs_path: str = os.environ.get("logs_path") or "logs/"
