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
    customers = relationship(
       "Customer",
       secondary=bank_customer,
       back_populates="banks"

    )
# customers table
class Customer(Base):
    __tablename__ = "customers"
    # attributes of the customer table
    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable= False)

    # creating the backpopulates to confirm the relationship

    banks = relationship(
        "Bank",
        secondary=bank_customer,
        back_populates="customers"
    )
    
    # create engine
    engine = create_engine("sqlite:///banks.db")