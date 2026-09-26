from flask import jsonify , Blueprint, redirect, request, url_for, flash, session
from flask_login import login_required
from ...auth.roles_checker import role_needed
from ...db.models import Product, DeliveryOrder, Receipt, InternalTransfer

m_dash = Blueprint('m_dash',__name__)


@m_dash.route("/total_products")
@login_required
@role_needed('inventory_manager')
def total_products():
    return Product.query.count()

@m_dash.route("/pending_delivery")
@login_required
@role_needed('inventory_manager')
def pending_delivery():
    return DeliveryOrder.query.filter_by(status='waiting').count()

@m_dash.route("/pending_receipt")
@login_required
@role_needed('inventory_manager')
def pending_receipts():
    return Receipt.query.filter_by(status='waiting').count()

@m_dash.route("/pending_receipt")
@login_required
@role_needed('inventory_manager')
def pending_receipts():
    return Receipt.query.filter_by(status='waiting').count()