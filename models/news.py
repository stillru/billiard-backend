from datetime import datetime

from sqlalchemy import Column, String, Integer, Table, ForeignKey
from sqlalchemy.orm import relationship

from extensions import db

# Define the association table first
news_tags = Table(
    "news_tags",
    db.metadata,
    Column("news_id", Integer, ForeignKey("news.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)


class News(db.Model):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    body = Column(db.Text, nullable=False)
    source_type = Column(String(50), nullable=False)
    created_at = Column(db.DateTime, default=datetime.utcnow)

    tags = relationship("Tag", secondary=news_tags, back_populates="news")


class Tag(db.Model):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    news = relationship("News", secondary=news_tags, back_populates="tags")
