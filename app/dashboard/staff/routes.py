from flask import jsonify , Blueprint, redirect, request, url_for, flash, session
from flask_login import login_required
from ...auth.roles_checker import role_needed
from ...db.models import InternalTransfer

s_dash = Blueprint('s_dash',__name__)

@s_dash.route("/pending_transfers")
@login_required
@role_needed('warehouse_staff')
def pending_transfer():
    return InternalTransfer.query.filter_by(status='waiting').count()



###############. Receipts ################

def add_receipt(): #Draft, Waiting, Ready, Done, Canceled
    status = 'All'
    location='All'
    sort = 'Highest Amount' # amount, date

    if request.method=='POST':
        data = request.get_json()
        status = data['status']
        location = data['location']
        sort = data['sort']
        
    query = Trek.query.filter(Trek.status=='Open')
    if gender != 'All':
        query = query.filter_by(gender_req=gender)
    if location != 'All':
        query = query.filter_by(location=location)
    if difficulty != 'All':
        query = query.filter_by(difficulty=difficulty)
    if sort == 'cost':
        query = query.order_by(Trek.cost)
    elif sort == 'costd':
        query = query.order_by(Trek.cost.desc())
    elif sort == 'slots':
        query = query.order_by(Trek.slots)
    elif sort == 'slotsd':
        query = query.order_by(Trek.slots.desc())
        
    temp = query.all()

    result = [
        {'id':i.trek_id,
        'isBooked':'Yes' if current_user.isBooked(i.trek_id) else 'No' ,
        'isRefunded':'Yes' if current_user.isRefunded(i.trek_id) else 'No' ,
        'isPaid':'Yes' if current_user.isPaid(i.trek_id) else 'No' ,
        'isCancelled':'Yes' if current_user.isCancelled(i.trek_id) else 'No' ,
        'amount': get_booking_amount(i.trek_id) if current_user.isPaid(i.trek_id) else 0,
        'insurance': "Yes" if (current_user.isBooked(i.trek_id) and get_insurance(i.trek_id)) else "No",
        'name':i.tname,
        'location':i.location,
        'cost':i.cost,
        'insurance_cost':i.insurance_cost,
        'difficulty':i.difficulty,
        'gender_req':i.gender_req,
        'description':i.description,
        'slots':i.slots-i.get_participant_count(),
        'start_date':i.start_date,
        'end_date':i.end_date,
        'duration': (datetime.strptime(i.end_date, "%Y-%m-%d") - datetime.strptime(i.start_date, "%Y-%m-%d")).days,
        'status':i.status}
        for i in temp ]
    
    if sort == 'duration':
        result = sorted(result, key=lambda x: x["duration"],reverse=False)
    elif sort == 'durationd':
        result = sorted(result, key=lambda x: x["duration"],reverse=True)
    
    if request.method=='POST':
        return jsonify(result)
    return result