import os, dotenv   

dotenv.load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
HTTP_PROXY = os.getenv("HTTP_PROXY")
HTTPS_PROXY = os.getenv("HTTPS_PROXY")

LOG_LEVEL = "TRACE"
LOG_FILENAME = None
LOG_SHOW_DATE = False