from .base import register_handlers as register_base_handlers
from .media import register_handlers as register_media_handlers

def register_all_handlers(dp):
    """Register all handlers from all modules."""
    register_base_handlers(dp)
    register_media_handlers(dp)