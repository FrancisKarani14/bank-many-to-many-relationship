from sqlalchemy import String, Integer, create_engine, ForeignKey, Column, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# association table
bank_customer = Table(
    "bank_customer",
    Base.metadata,
    Column("bank_id", Integer, ForeignKey("banks.id"), primary_key=True),
    Column("customer_id", Integer, ForeignKey(
        "customers.id"), primary_key=True)
)

# bank table


class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    bank_name = Column(String, nullable=False)

    customers = relationship(
        "Customer",
        secondary=bank_customer,
        back_populates="banks"
    )

# customer table


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False)

    banks = relationship(
        "Bank",
        secondary=bank_customer,
        back_populates="customers"
    )


# ✅ Engine and table creation AFTER class definitions
engine = create_engine("sqlite:///banks.db", echo=True)
Base.metadata.create_all(engine)
