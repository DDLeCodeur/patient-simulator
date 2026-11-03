"""Patient Simulator - Système physique pour la boucle fermée.

Service FastAPI simulant le metabolisme d'un patient diabetique de type 1.
"""

import logging
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from dynaconf import Dynaconf
from fastapi import FastAPI, Request
from google.cloud import firestore
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

# ============================================================================
# CONFIGURATION (Dynaconf)
# ============================================================================

settings = Dynaconf(
    settings_files=["settings.toml"],
    envvar_prefix="PATIENT",  # Variables d'env: PATIENT_FIRESTORE_DATABASE, etc.
)

# ============================================================================
# LOGGING
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)

# ============================================================================
# FIRESTORE CLIENT
# ============================================================================

db = firestore.Client(database=settings.FIRESTORE_DATABASE)
