from sqlalchemy import String, Integer, create_engine, ForeignKey, Column, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

Base = declarative_base()

# ========================
# Association Table
# ========================
bank_customer = Table(
    "bank_customer",
    Base.metadata,
    Column("bank_id", Integer, ForeignKey("banks.id"), primary_key=True),
    Column("customer_id", Integer, ForeignKey(
        "customers.id"), primary_key=True)
)

# ========================
# Bank Table
# ========================


class Bank(Base):
    __tablename__ = "banks"
    id = Column(Integer, primary_key=True)
    # unique prevents duplicates at DB level
    bank_name = Column(String, nullable=False, unique=True)

    customers = relationship(
        "Customer",
        secondary=bank_customer,
        back_populates="banks"
    )

# ========================
# Customer Table
# ========================


class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    customer_name = Column(String, nullable=False, unique=True)

    banks = relationship(
        "Bank",
        secondary=bank_customer,
        back_populates="customers"
    )


# ========================
# Engine & Session
# ========================
engine = create_engine("sqlite:///banks.db", echo=True)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# ========================
# Helper Functions
# ========================


def get_or_create_bank(session, name):
    bank = session.query(Bank).filter_by(bank_name=name).first()
    if bank:
        print(f"Bank '{name}' already exists.")
        return bank
    else:
        bank = Bank(bank_name=name)
        session.add(bank)
        session.commit()
        print(f"Bank '{name}' created.")
        return bank


def get_or_create_customer(session, name):
    customer = session.query(Customer).filter_by(customer_name=name).first()
    if customer:
        print(f"Customer '{name}' already exists.")
        return customer
    else:
        customer = Customer(customer_name=name)
        session.add(customer)
        session.commit()
        print(f"Customer '{name}' created.")
        return customer


# ========================
# Example Usage
# ========================
cust1 = get_or_create_customer(session, "Francis")
bank1 = get_or_create_bank(session, "Equity Bank")

# ✅ Link the customer to the bank (many-to-many)
if bank1 not in cust1.banks:
    cust1.banks.append(bank1)
    session.commit()
    print(
        f"Linked Customer '{cust1.customer_name}' to Bank '{bank1.bank_name}'")
else:
    print(
        f"Customer '{cust1.customer_name}' is already linked to Bank '{bank1.bank_name}'")

# ========================
# Verify Relationships
# ========================
print("\n=== Banks of Francis ===")
for b in cust1.banks:
    print(b.bank_name)

print("\n=== Customers of Equity Bank ===")
for c in bank1.customers:
    print(c.customer_name)
