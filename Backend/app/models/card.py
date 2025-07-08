from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text, ARRAY
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Card(Base):
    __tablename__ = "cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hp = Column(Integer)
    type = Column(String, nullable=False)
    retreat_cost = Column(Integer, default=0)
    weakness = Column(String)
    description = Column(Text)


class Ability(Base):
    __tablename__ = "abilities"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    text = Column(Text, nullable=False)


class Attack(Base):
    __tablename__ = "attacks"
    id = Column(Integer, primary_key=True, index=True)
    card_id = Column(Integer, ForeignKey("cards.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    cost = Column(ARRAY(String))  # PostgreSQL array of strings
    damage = Column(Integer, default=0)
    text = Column(Text)
