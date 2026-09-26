from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


# ============================================================
# Users / Authentication
# ============================================================

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum("inventory_manager", "warehouse_staff", name="user_roles"),
        nullable=False,
        default="warehouse_staff",
    )
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Relationships
    created_receipts = db.relationship(
        "Receipt", foreign_keys="Receipt.created_by_id", back_populates="created_by"
    )
    created_deliveries = db.relationship(
        "DeliveryOrder",
        foreign_keys="DeliveryOrder.created_by_id",
        back_populates="created_by",
    )
    created_transfers = db.relationship(
        "InternalTransfer",
        foreign_keys="InternalTransfer.created_by_id",
        back_populates="created_by",
    )
    created_adjustments = db.relationship(
        "StockAdjustment",
        foreign_keys="StockAdjustment.created_by_id",
        back_populates="created_by",
    )
    ledger_entries = db.relationship("StockLedger", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# ============================================================
# Product Master Data
# ============================================================

class ProductCategory(db.Model):
    __tablename__ = "product_categories"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)

    products = db.relationship("Product", back_populates="category")


class UnitOfMeasure(db.Model):
    __tablename__ = "units_of_measure"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    symbol = db.Column(db.String(20), unique=True, nullable=False)

    products = db.relationship("Product", back_populates="unit_of_measure")


class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category_id = db.Column(
        db.Integer, db.ForeignKey("product_categories.id"), nullable=False
    )
    unit_of_measure_id = db.Column(
        db.Integer, db.ForeignKey("units_of_measure.id"), nullable=False
    )
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    category = db.relationship("ProductCategory", back_populates="products")
    unit_of_measure = db.relationship("UnitOfMeasure", back_populates="products")
    stock_levels = db.relationship(
        "StockLevel", back_populates="product", cascade="all, delete-orphan"
    )
    reorder_rules = db.relationship(
        "ReorderRule", back_populates="product", cascade="all, delete-orphan"
    )
    receipt_lines = db.relationship("ReceiptLine", back_populates="product")
    delivery_lines = db.relationship("DeliveryLine", back_populates="product")
    transfer_lines = db.relationship("TransferLine", back_populates="product")
    adjustment_lines = db.relationship("AdjustmentLine", back_populates="product")
    ledger_entries = db.relationship("StockLedger", back_populates="product")


# ============================================================
# Warehouse / Locations
# ============================================================

class Warehouse(db.Model):
    __tablename__ = "warehouses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    locations = db.relationship(
        "Location", back_populates="warehouse", cascade="all, delete-orphan"
    )
    stock_levels = db.relationship("StockLevel", back_populates="warehouse")


class Location(db.Model):
    __tablename__ = "locations"

    id = db.Column(db.Integer, primary_key=True)
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False
    )
    name = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    warehouse = db.relationship("Warehouse", back_populates="locations")
    stock_levels = db.relationship("StockLevel", back_populates="location")

    __table_args__ = (
        db.UniqueConstraint(
            "warehouse_id", "code", name="uq_location_warehouse_code"
        ),
    )


# ============================================================
# Current Stock
# ============================================================

class StockLevel(db.Model):
    """
    Current quantity of one product at one warehouse/location.

    This is the current-state table. StockLedger is the historical
    transaction/audit table.
    """

    __tablename__ = "stock_levels"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False
    )
    quantity = db.Column(db.Numeric(18, 3), nullable=False, default=0)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    product = db.relationship("Product", back_populates="stock_levels")
    warehouse = db.relationship("Warehouse", back_populates="stock_levels")
    location = db.relationship("Location", back_populates="stock_levels")

    __table_args__ = (
        db.UniqueConstraint(
            "product_id",
            "warehouse_id",
            "location_id",
            name="uq_stock_product_warehouse_location",
        ),
    )


# ============================================================
# Reordering Rules
# ============================================================

class ReorderRule(db.Model):
    __tablename__ = "reorder_rules"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False
    )
    minimum_quantity = db.Column(db.Numeric(18, 3), nullable=False, default=0)
    reorder_quantity = db.Column(db.Numeric(18, 3), nullable=False, default=0)
    maximum_quantity = db.Column(db.Numeric(18, 3))
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    product = db.relationship("Product", back_populates="reorder_rules")
    warehouse = db.relationship("Warehouse")

    __table_args__ = (
        db.UniqueConstraint(
            "product_id",
            "warehouse_id",
            name="uq_reorder_product_warehouse",
        ),
    )


# ============================================================
# Suppliers / Vendors
# ============================================================

class Supplier(db.Model):
    __tablename__ = "suppliers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(255))
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    receipts = db.relationship("Receipt", back_populates="supplier")


# ============================================================
# Receipts - Incoming Stock
# ============================================================

class Receipt(db.Model):
    __tablename__ = "receipts"

    id = db.Column(db.Integer, primary_key=True)
    receipt_number = db.Column(db.String(80), unique=True, nullable=False, index=True)
    supplier_id = db.Column(
        db.Integer, db.ForeignKey("suppliers.id"), nullable=False
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False
    )
    status = db.Column(
        db.Enum("draft", "waiting", "ready", "done", "canceled", name="receipt_status"),
        nullable=False,
        default="draft",
    )
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    validated_at = db.Column(db.DateTime)

    supplier = db.relationship("Supplier", back_populates="receipts")
    warehouse = db.relationship("Warehouse")
    created_by = db.relationship(
        "User", foreign_keys=[created_by_id], back_populates="created_receipts"
    )
    lines = db.relationship(
        "ReceiptLine", back_populates="receipt", cascade="all, delete-orphan"
    )


class ReceiptLine(db.Model):
    __tablename__ = "receipt_lines"

    id = db.Column(db.Integer, primary_key=True)
    receipt_id = db.Column(
        db.Integer, db.ForeignKey("receipts.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False
    )
    quantity = db.Column(db.Numeric(18, 3), nullable=False)

    receipt = db.relationship("Receipt", back_populates="lines")
    product = db.relationship("Product", back_populates="receipt_lines")
    location = db.relationship("Location")


# ============================================================
# Delivery Orders - Outgoing Stock
# ============================================================

class DeliveryOrder(db.Model):
    __tablename__ = "delivery_orders"

    id = db.Column(db.Integer, primary_key=True)
    delivery_number = db.Column(
        db.String(80), unique=True, nullable=False, index=True
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False
    )
    status = db.Column(
        db.Enum(
            "draft", "waiting", "ready", "done", "canceled",
            name="delivery_status",
        ),
        nullable=False,
        default="draft",
    )
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    validated_at = db.Column(db.DateTime)

    warehouse = db.relationship("Warehouse")
    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
        back_populates="created_deliveries",
    )
    lines = db.relationship(
        "DeliveryLine", back_populates="delivery", cascade="all, delete-orphan"
    )


class DeliveryLine(db.Model):
    __tablename__ = "delivery_lines"

    id = db.Column(db.Integer, primary_key=True)
    delivery_id = db.Column(
        db.Integer, db.ForeignKey("delivery_orders.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False
    )
    quantity = db.Column(db.Numeric(18, 3), nullable=False)

    delivery = db.relationship("DeliveryOrder", back_populates="lines")
    product = db.relationship("Product", back_populates="delivery_lines")
    location = db.relationship("Location")


# ============================================================
# Internal Transfers
# ============================================================

class InternalTransfer(db.Model):
    __tablename__ = "internal_transfers"

    id = db.Column(db.Integer, primary_key=True)
    transfer_number = db.Column(
        db.String(80), unique=True, nullable=False, index=True
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False
    )
    status = db.Column(
        db.Enum(
            "draft", "waiting", "ready", "done", "canceled",
            name="transfer_status",
        ),
        nullable=False,
        default="draft",
    )
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)

    warehouse = db.relationship("Warehouse")
    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
        back_populates="created_transfers",
    )
    lines = db.relationship(
        "TransferLine", back_populates="transfer", cascade="all, delete-orphan"
    )


class TransferLine(db.Model):
    __tablename__ = "transfer_lines"

    id = db.Column(db.Integer, primary_key=True)
    transfer_id = db.Column(
        db.Integer, db.ForeignKey("internal_transfers.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    source_location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False
    )
    destination_location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False
    )
    quantity = db.Column(db.Numeric(18, 3), nullable=False)

    transfer = db.relationship("InternalTransfer", back_populates="lines")
    product = db.relationship("Product", back_populates="transfer_lines")
    source_location = db.relationship(
        "Location", foreign_keys=[source_location_id]
    )
    destination_location = db.relationship(
        "Location", foreign_keys=[destination_location_id]
    )


# ============================================================
# Stock Adjustments
# ============================================================

class StockAdjustment(db.Model):
    __tablename__ = "stock_adjustments"

    id = db.Column(db.Integer, primary_key=True)
    adjustment_number = db.Column(
        db.String(80), unique=True, nullable=False, index=True
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False
    )
    status = db.Column(
        db.Enum("draft", "done", "canceled", name="adjustment_status"),
        nullable=False,
        default="draft",
    )
    reason = db.Column(db.Text)
    created_by_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    validated_at = db.Column(db.DateTime)

    warehouse = db.relationship("Warehouse")
    created_by = db.relationship(
        "User",
        foreign_keys=[created_by_id],
        back_populates="created_adjustments",
    )
    lines = db.relationship(
        "AdjustmentLine",
        back_populates="adjustment",
        cascade="all, delete-orphan",
    )


class AdjustmentLine(db.Model):
    __tablename__ = "adjustment_lines"

    id = db.Column(db.Integer, primary_key=True)
    adjustment_id = db.Column(
        db.Integer, db.ForeignKey("stock_adjustments.id"), nullable=False
    )
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False
    )
    recorded_quantity = db.Column(db.Numeric(18, 3), nullable=False)
    counted_quantity = db.Column(db.Numeric(18, 3), nullable=False)
    difference = db.Column(db.Numeric(18, 3), nullable=False)

    adjustment = db.relationship("StockAdjustment", back_populates="lines")
    product = db.relationship("Product", back_populates="adjustment_lines")
    location = db.relationship("Location")


# ============================================================
# Stock Ledger / Audit Trail
# ============================================================

class StockLedger(db.Model):
    """
    Immutable-style inventory movement history.

    Every validated receipt, delivery, transfer, or adjustment should
    create one or more ledger entries.
    """

    __tablename__ = "stock_ledger"

    id = db.Column(db.BigInteger, primary_key=True)
    product_id = db.Column(
        db.Integer, db.ForeignKey("products.id"), nullable=False, index=True
    )
    warehouse_id = db.Column(
        db.Integer, db.ForeignKey("warehouses.id"), nullable=False, index=True
    )
    location_id = db.Column(
        db.Integer, db.ForeignKey("locations.id"), nullable=False, index=True
    )

    # receipt / delivery / transfer / adjustment
    transaction_type = db.Column(
        db.Enum(
            "receipt",
            "delivery",
            "transfer_in",
            "transfer_out",
            "adjustment",
            name="ledger_transaction_types",
        ),
        nullable=False,
    )

    # ID of the originating transaction record.
    reference_id = db.Column(db.Integer, nullable=False, index=True)
    reference_number = db.Column(db.String(80))

    quantity_change = db.Column(db.Numeric(18, 3), nullable=False)
    quantity_after = db.Column(db.Numeric(18, 3), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    product = db.relationship("Product", back_populates="ledger_entries")
    warehouse = db.relationship("Warehouse")
    location = db.relationship("Location")
    user = db.relationship("User", back_populates="ledger_entries")
