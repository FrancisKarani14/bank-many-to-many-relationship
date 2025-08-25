from sqlalchemy import String, Integer, create_engine, ForeignKey, Column, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

# create an engine

Base = declarative_base()

# the association table

bank_customer = Table(
    "bank_customer",
    Base.metadata,
    Column("bank_id", Integer, ForeignKey("bank.id"), primary_key=True),
    Column("customer_id", Integer, ForeignKey("customer.id"), primary_key=True)


)

# bank table


class Bank(Base):
    __tablename__ = "banks"
    # attributes of the table bank
    id = Column(Integer, nullable=False)
    bank_name = Column(String, nullable=False)

    # many to many relationships
    
