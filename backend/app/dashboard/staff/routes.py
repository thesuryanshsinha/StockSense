from flask import jsonify , Blueprint, redirect, request, url_for, flash, session
from flask_login import login_required
from ...auth.roles_checker import role_needed
from ...db.models import InternalTransfer

s_dash = Blueprint('s_dash',__name__)

@s_dash.route("/pending_transfers")
@login_required
@role_needed('inventory_manager')
def pending_transfer():
    return InternalTransfer.query.filter_by(status='waiting').count()