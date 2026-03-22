"""
Configuration file for LLM-based fine-tuning data generation
"""
import os
from dotenv import load_dotenv

load_dotenv()

# ============== API Settings ==============
# Providers: "anthropic", "openai", "gemini"
LLM_PROVIDER = "gemini"
MODEL_NAME = "gemini-3-flash-preview"  # For gemini: "gemini-3-flash", for claude: "claude-3-5-sonnet-20241022"
API_KEY = os.getenv("API_KEY")

# Legacy API keys (if LLM_PROVIDER is different)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", API_KEY)  # Fallback to API_KEY

# API Configuration
API_TIMEOUT = 120  # seconds per request
MAX_RETRIES = 3
RETRY_BACKOFF = 2

# ============== Generation Settings ==============
NUM_RECORDS = 100
BATCH_SIZE = 10  # số records generate cùng một lúc
CONCURRENT_REQUESTS = 5  # số request async cùng lúc

# Focus Area Distribution (% trong tổng records)
FOCUS_DISTRIBUTIONS = {
    "DEBUG_FOCUS": 0.25,
    "OPTIMIZATION_FOCUS": 0.25,
    "EDGE_CASE_FOCUS": 0.25,
    "CONCEPT_FOCUS": 0.15,
    "SCAFFOLDING_FOCUS": 0.10,
}

# Contexts (Ngữ cảnh bài toán)
CONTEXTS = [
    "Bank",
    "Game",
    "E-commerce",
    "Social Media",
    "Healthcare",
    "Logistics",
    "Education",
    "Finance",
]

# Difficulty Levels
DIFFICULTIES = [
    "Mới bắt đầu",
    "Trung bình",
    "Giỏi",
]

# Bug Types for Debug Focus
BUG_TYPES = [
    "Off-by-one error",
    "Uninitialized variable",
    "Segmentation fault",
    "Buffer overflow",
    "Type mismatch",
    "Null pointer dereference",
    "Memory leak",
    "Integer overflow",
]

# ============== Output Settings ==============
OUTPUT_FILE = "data.json"
LOG_FILE = "generation.log"
BACKUP_FILE = "data_backup.json"

# JSON Lines format (một object JSON per dòng)
USE_JSONL = False  # False: Standard JSON array, True: JSON Lines

# ============== Token Management ==============
# Ước tính token per request
TOKENS_PER_PROBLEM_GEN = 800  # LLM call 1
TOKENS_PER_TEACHING_GEN = 600  # LLM call 2
TOTAL_TOKENS_PER_RECORD = TOKENS_PER_PROBLEM_GEN + TOKENS_PER_TEACHING_GEN

# API Rate Limits (tùy từng provider)
RATE_LIMIT_RPM = 60  # requests per minute
RATE_LIMIT_TPM = 60000  # tokens per minute

# ============== Validation Settings ==============
MIN_CODE_LENGTH = 50  # Minimum buggy code length
MAX_CODE_LENGTH = 2000  # Maximum code length
MIN_EXPLANATION_LENGTH = 200  # Minimum explanation length
VALIDATE_SYNTAX = False  # Try to validate C code syntax

# ============== Logging ==============
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
