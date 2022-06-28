import os
from typing import List

from dotenv import load_dotenv
from src.modules.predictions.models.documents import MachineStatus
from src.modules.users.models.documents import User

load_dotenv()

DOCUMENT_MODELS: List = [User, MachineStatus]
MONGODB_URL = os.getenv("MONGO_URL")
API_URL = os.getenv("API_URL")
