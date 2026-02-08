from sqlalchemy import Column, String, Text, DateTime, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from database import Base
import uuid

class SavedItem(Base):
    __tablename__ = "saved_items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    item_type = Column(String, nullable=False) # 'url', 'image', 'text'
    content_text = Column(Text, nullable=True)
    storage_path = Column(Text, nullable=True)
    status = Column(String, default="ready_to_swipe") # 'ready_to_swipe', 'archived', 'deleted', 'trash'
    analysis_status = Column(String, default="pending") # 'pending', 'processing', 'completed', 'failed'
    ai_result = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
