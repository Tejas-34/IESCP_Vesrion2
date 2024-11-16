from flask import Blueprint, request,jsonify
from flask import current_app as app
from flask_login import login_required
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import json
from flask_security import Security, SQLAlchemyUserDatastore
from flask_security import current_user, login_user, roles_required,login_required
from werkzeug.security import generate_password_hash, check_password_hash
from Application.models import db, Influencer, Sponsor, User, Role, Campaign, AdRequest
from datetime import datetime

datastore = SQLAlchemyUserDatastore(db, User, Role)


api = Blueprint("api", __name__)


@api.route("/signin", methods=["POST"])
def signin():
    username = request.json.get("username")
    password = request.json.get("password")
    
    user = User.query.filter_by(username=username).first()
    
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={"id": user.id, "username": user.username,"role":user.get_roles()[0]})
        
        
    if user.get_roles()[0] == 'sponsor':
        return {"token": access_token,
            "roles": user.get_roles(),
            "approve": user.sponsor_profile.Approve,'user_id':user.id}
    else:
        return {"token": access_token,
                "roles": user.get_roles(), 'user_id':user.id}
    
    


@api.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    print(data)

    if(data['role'] == 'influencer'):
        name = data.get('name')
        username = data.get("username")
        password = data.get("password")
        reach = data.get("reach")
        niche = data.get("niche")
        email = data.get("email")
        category = data.get('category')
        bio = data.get('bio')

        # Check if all necessary fields are provided
        if not all([username, password, reach, niche,email,name,category]):
            return {"message": "Missing fields in request"}, 400

        # Check if user already exists
        if datastore.find_user(username=username):
            return {"message": "User already exists"}, 409

        # Create the new user
        hashed_password = generate_password_hash(password)
        user = datastore.create_user(
            name = name,
            username=username,
            password=hashed_password,
            Email = email, # Ensure fs_uniquifier is unique
            active=1,
            bio = bio
        )

        # Assign the "Influencer" role
        influencer_role = datastore.find_or_create_role(data.get('role'))
        datastore.add_role_to_user(user, influencer_role)

        # Create and associate influencer profile data
        influencer = Influencer(user_id=user.id, Reach=reach, Niche=niche, Category=category)
        db.session.add(influencer)
        db.session.commit()

        return jsonify({"message": "Influencer registered successfully", "user_id": user.id,"role":"influencer"}), 201
    else:
        name = data.get('name')
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        company_name = data.get('Cmpname')
        Budget = data.get('budget')
        Industry = data.get('industry')
        bio = data.get('bio')

        # Check if all necessary fields are provided
        if not all([username, password, email,name,company_name,Budget,Industry]):
            return {"message": "Missing fields in request"}, 400

        # Check if user already exists
        if datastore.find_user(username=username):
            return {"message": "User already exists"}, 409

        # Create the new user
        hashed_password = generate_password_hash(password)
        user = datastore.create_user(
            name = name,
            username=username,
            password=hashed_password,
            Email = email,
            active=1,
            bio=bio
        )

        # Assign the "Influencer" role
        Sponsor_role = datastore.find_or_create_role(data.get('role'))
        datastore.add_role_to_user(user, Sponsor_role)

        # Create and associate influencer profile data
        sponsor = Sponsor(user_id=user.id, Budget=Budget,company_name=company_name,Industry=Industry)
        db.session.add(sponsor)
        db.session.commit()

        return jsonify({"message": "Sponsor registered successfully", "user_id": user.id, "role":"sponsor"}), 201


@api.route('/influencer/<int:user_id>', methods=['GET'])
@jwt_required()
def influencer(user_id):
    curr_user  = get_jwt_identity()
    print(curr_user.get('id'))
    user = User.query.filter_by(id = user_id).first()
    if user:
        return jsonify({'name':user.name,'email':user.Email, 'Niche':user.influencer_profile.Niche,'Reach':user.influencer_profile.Reach,'Category':user.influencer_profile.Category,'bio':user.bio,'username':user.username }), 200
    return jsonify({"message": "Influencer not found"}), 404


@api.route("/influencer/update", methods=["PUT"])
@jwt_required()
def update_profile():
    curr_user  = get_jwt_identity()
    if "influencer" not in curr_user.get("role"):
        return jsonify({"msg": "Influencer access required"}), 403
    
    user_id = curr_user.get('id')
    print(user_id)
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return {"message": "Influencer not found"}, 404
    
    data = request.get_json()

    user.name = data.get('name')
    user.username = data.get("username")
    user.influencer_profile.Reach = data.get("Reach")
    user.influencer_profile.Niche = data.get("Niche")
    user.Email = data.get("email")
    user.influencer_profile.Category = data.get('Category')
    user.bio = data.get('bio') 
    db.session.commit()

    return {"message": "Updated successfully"}, 200










@api.route('/sponsor/<int:user_id>', methods=['GET'])
@jwt_required()
def sponsor(user_id):
    curr_user  = get_jwt_identity()
    print(curr_user.get('id'))

    #total pending request

    user = User.query.filter_by(id = user_id).first()
    
    if user:
        total_camp = Campaign.query.filter_by(sponsor_id = user.sponsor_profile.id).count()
        total_pending = AdRequest.query.filter_by(sponsor_id = user_id, status = 'Pending').count()
        return jsonify({'name':user.name,'email':user.Email, 'Cname':user.sponsor_profile.company_name,'Budget':user.sponsor_profile.Budget,'Industry':user.sponsor_profile.Industry,'bio':user.bio,'username':user.username,'pending_req':total_pending,'active_camp':total_camp }), 200
    return jsonify({"message": "Influencer not found"}), 404


@api.route("/sponsor/update", methods=["PUT"])
@jwt_required()
def spon_update_profile():
    curr_user  = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403
    
    user_id = curr_user.get('id')
    print(user_id)
    user = User.query.filter_by(id = user_id).first()
    if not user:
        return {"message": "Influencer not found"}, 404
    
    data = request.get_json()

    user.name = data.get('name')
    user.username = data.get("username")
    user.sponsor_profile.company_name = data.get("Cname")
    user.sponsor_profile.Budget = data.get("Budget")
    user.Email = data.get("email")
    user.sponsor_profile.Industry = data.get('Industry')
    user.bio = data.get('bio') 
    db.session.commit()

    return {"message": "Updated successfully"}, 200


@api.route('/sponsor/create_campaign', methods=['POST'])
@jwt_required()
def create_campaign():
    curr_user = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403

    user_id = curr_user.get('id')
    data = request.get_json()

    Name = data.get('Name')
    Description = data.get('Description')
    Start_date = data.get('Start_date')
    End_date = data.get('End_date')
    Budget = data.get('Budget')
    goals = data.get('goal')
    category = data.get('category')
    visibility = data.get('visibility')

    # Convert date strings to datetime objects
    Start_date = datetime.strptime(Start_date, '%Y-%m-%d') 
    End_date = datetime.strptime(End_date, '%Y-%m-%d')

    user = User.query.filter_by(id=user_id).first()

    camp = Campaign(
        sponsor_id=user.sponsor_profile.id,
        name=Name,
        description=Description,
        start_date=Start_date,
        end_date=End_date,
        budget=Budget,
        goals=goals,
        category=category,
        visibility=visibility
    )

    db.session.add(camp)
    db.session.commit()
    return jsonify({"message": "Campaign created successfully"}), 201


@api.route('/sponsor/campaigns', methods=['GET'])
@jwt_required()
def get_campaigns():
    curr_user = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403

    user_id = curr_user.get('id')
    user = User.query.filter_by(id=user_id).first()
    campaigns = Campaign.query.filter_by(sponsor_id=user.sponsor_profile.id).all()
    return jsonify([{'id':camp.id,"name": camp.name, "description": camp.description, "start_date": camp.start_date.strftime("%a, %d %b %Y"), "end_date": camp.end_date.strftime("%a, %d %b %Y"), "budget": camp.budget, "goals": camp.goals, "category": camp.category, "visibility": camp.visibility} for camp in campaigns]), 200


@api.route('/sponsor/campaign/<int:camp_id>', methods=['GET'])
@jwt_required()
def get_campaign(camp_id):
    curr_user = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403

    camp = Campaign.query.filter_by(id=camp_id).first()
    if not camp:
        return jsonify({"message": "Campaign not found"}), 404

    return jsonify({"id":camp.id,"name": camp.name, "description": camp.description, "start_date": camp.start_date.strftime('%Y-%m-%d'), "end_date": camp.end_date.strftime('%Y-%m-%d'), "budget": camp.budget, "goals": camp.goals, "category": camp.category, "visibility": camp.visibility}), 200


@api.route("/sponsor/CampUpdate/<int:camp_id>", methods=["PUT"])
@jwt_required()
def spon_update_camp(camp_id):
    curr_user  = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403
    
    camp = Campaign.query.filter_by(id = camp_id).first()
    if not camp:
        return {"message": "Campaign not found"}, 404
    
    data = request.get_json()

    camp.name = data.get('name')
    camp.description = data.get("description")
    camp.start_date = datetime.strptime(data.get("start_date"),'%Y-%m-%d') 
    camp.end_date = datetime.strptime(data.get("end_date"),'%Y-%m-%d')
    camp.budget = data.get('budget')
    camp.goals = data.get('goals')
    camp.category = data.get('category')
    camp.visibility = data.get('visibility')



    db.session.commit()

    return {"message": "Updated successfully"}, 200


@api.route("/sponsor/CampDelete/<int:camp_id>", methods=["DELETE"])
@jwt_required()
def spon_delete_camp(camp_id):
    curr_user  = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403
    
    camp = Campaign.query.filter_by(id = camp_id).first()
    if not camp:
        return {"message": "Campaign not found"}, 404
    
    db.session.delete(camp)
    db.session.commit()

    return {"message": "Deleted successfully"}, 200




@api.route('/influencers/search', methods=['GET'])
@jwt_required()
def search_influencers():
    curr_user  = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403
    
    name = request.args.get('name', '').lower()
    category = request.args.get('category', '').lower()
    min_followers = request.args.get('followers', type=int, default=0)

    query = db.session.query(Influencer).join(User).filter(User.active == True)

    if name:
        query = query.filter(User.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Influencer.Category.ilike(f"%{category}%"))
    if min_followers:
        query = query.filter(Influencer.Reach >= min_followers)

    influencers = query.all()

    influencer_data = [
        {
            "name": influencer.user.name,
            "category": influencer.Category,
            "followers": influencer.Reach,
            "bio": influencer.user.bio,
            "niche" : influencer.Niche,
            "email" : influencer.user.Email,
            "id" : influencer.user.id
        }
        for influencer in influencers
    ]

    return jsonify(influencer_data), 200





#----------------------------------        ad request routesss   ------------------------


@api.route('/sponsor/request', methods=['POST'])
@jwt_required()
def create_ad_request():
    curr_user = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403

    user_id = curr_user.get('id')
    data = request.get_json()

    influencer_id = data.get('influencer_id')
    campaign_id = data.get('campaign_id')
    message = data.get('message')
    requirements = data.get('requirements')
    payment_amount = data.get('payment')

    influencer = Influencer.query.filter_by(user_id=influencer_id).first()
    campaign = Campaign.query.filter_by(id=campaign_id).first()

    if not influencer or not campaign:
        return jsonify({"message": "Influencer or Campaign not found"}), 404
    
    message_entry = {
        "role": 'sponsor',
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }

    ad_request = AdRequest(
        sponsor_id=user_id,
        influencer_id=influencer_id,
        campaign_id=campaign_id,
        request_type = 'sponsor_initiated',
        messages=[message_entry],
        requirements=requirements,
        payment_amount=payment_amount
    )

    db.session.add(ad_request)
    db.session.commit()

    return jsonify({"message": "Ad request created successfully"}), 201



@api.route('/Sponsor/CampRequests/<int:camp_id>', methods=['GET'])
@jwt_required()
def get_campaign_requests(camp_id):
    curr_user = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403

    user_id = curr_user.get('id')
    requests = AdRequest.query.filter_by(sponsor_id=user_id, campaign_id=camp_id).all()

    data = [{'id':req.id, "influencer_id": req.influencer_id, "campaign_id": req.campaign_id, "request_type": req.request_type, "requirements": req.requirements, "payment_amount": req.payment_amount, "status": req.status, "messages": req.messages} for req in requests]
    influencer_data = [{'name':User.query.filter_by(id=req.influencer_id).first().name, 'email':User.query.filter_by(id=req.influencer_id).first().Email} for req in requests]
    
    combined_data = [
    {**req_data, **inf_data} 
    for req_data, inf_data in zip(data, influencer_data)
]
    
    return jsonify({'request': combined_data}), 200



@api.route('/sponsor/request/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_ad_request(id):
    curr_user = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403

    user_id = curr_user.get('id')
    data = request.get_json()

    ad_request = AdRequest.query.filter_by(id=id).first()
    if not ad_request:
        return jsonify({"message": "Ad request not found"}), 404

    ad_request.requirements = data.get('requirements')
    ad_request.payment_amount = data.get('payment_amount')
    db.session.commit()

    return jsonify({"message": "Ad request updated successfully"}), 200



@api.route('/sponsor/request/delete/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ad_request(id):
    curr_user = get_jwt_identity()
    if "sponsor" not in curr_user.get("role"):
        return jsonify({"msg": "Sponsor access required"}), 403

    user_id = curr_user.get('id')

    ad_request = AdRequest.query.filter_by(id=id).first()
    if not ad_request:
        return jsonify({"message": "Ad request not found"}), 404

    db.session.delete(ad_request)
    db.session.commit()

    return jsonify({"message": "Ad request deleted successfully"}), 200


@api.route('/ad_request/add_message/<int:id>', methods=['PUT'])
@jwt_required()
def add_message(id):
    ad_request = AdRequest.query.filter_by(id=id).first()
    if not ad_request:
        return jsonify({"error": "Ad request not found"}), 404

    curr_user = get_jwt_identity()
    new_message = request.json.get("message")
    role = curr_user.get("role")  # "Sponsor" or "Influencer"

    if not new_message or role not in ["sponsor", "influencer"]:
        return jsonify({"error": "Message and role are required"}), 400

    # Create a new message entry
    message_entry = {
        "role": role,
        "message": new_message,
        "timestamp": datetime.utcnow().isoformat()
    }

    # Append the message and explicitly assign it back
    ad_request.add_message(message_entry)
    ad_request.messages = json.dumps(ad_request.get_messages())  # Re-assign for SQLAlchemy detection

    db.session.add(ad_request)  # Ensure the object is marked for update
    db.session.commit()         # Commit the change to the database

    return jsonify(ad_request.get_messages()), 200




@api.route('/influencer/requests', methods=['GET'])
@jwt_required()
def get_influencer_requests():
    curr_user = get_jwt_identity()
    user_id = curr_user.get('id')
    
    if "influencer" in curr_user.get("role"):
        requests = AdRequest.query.filter_by(influencer_id=user_id, request_type="sponsor_initiated").all()
    elif("sponsor" in curr_user.get("role")):
        requests = AdRequest.query.filter_by(sponsor_id=user_id, request_type="influencer_initiated").all()
    else:
        return jsonify({"msg": "Sponsor or Influencer access required"}), 403
    
    # Serialize ad requests
    request = [
        {
            'id': req.id,
            'sponsor_id': req.sponsor_id,
            'campaign_id': req.campaign_id,
            'request_type': req.request_type,
            'requirements': req.requirements,
            'payment_amount': req.payment_amount,
            'status': req.status,
            'message': req.messages,
        }
        for req in requests
    ]

    # Serialize campaign data
    Camp = [
        {
            'CampName': campaign.name,
            'budget': campaign.budget,
            'start_date': campaign.start_date.strftime("%a, %d %b %Y"),
            'end_date': campaign.end_date.strftime("%a, %d %b %Y"),
            'description': campaign.description,
            'goals': campaign.goals,
            'category': campaign.category
        }
        for campaign in [Campaign.query.filter_by(id=req.campaign_id).first() for req in requests]
    ]

    # Serialize sponsor data
    sponsor_data = [
        {
            'SpoName': sponsor.name,
            'SpoEmail': sponsor.Email,
            'CompanyName': sponsor.sponsor_profile.company_name
        }
        for sponsor in [User.query.filter_by(id=req.sponsor_id).first() for req in requests]
    ]

    # Serialize influencer data
    influencer_data = [
        {
            'InfName': influencer.name,
            'InfEmail': influencer.Email,
            'InfReach': influencer.influencer_profile.Reach
        }
        for influencer in [User.query.filter_by(id=req.influencer_id).first() for req in requests]
    ]

    # Combine all data
    combined_data = [
        {**req_data, **sp_data, **Camp_data, **Inf_data}
        for req_data, sp_data, Camp_data, Inf_data in zip(request, sponsor_data, Camp, influencer_data)
    ]

    return jsonify({
        'combine': combined_data,
        'sponsor_data': sponsor_data,
        'campaign': Camp,
        'request': request,
        'influencer_data': influencer_data
    }), 200


#route to accpet reject or negotiate request
@api.route('/influencer/request/update/<int:id>', methods=['PUT'])
@jwt_required()
def update_influencer_request(id):
    curr_user = get_jwt_identity()
    if "influencer" not in curr_user.get("role") and 'sponsor' not in curr_user.get("role"):
        return jsonify({"msg": "Influencer access required"}), 403

    data = request.get_json()

    ad_request = AdRequest.query.filter_by(id=id).first()
    if not ad_request:
        return jsonify({"message": "Ad request not found"}), 404

    ad_request.status = data.get('status')
    if(data.get('status') == 'Accepted'):
        sponsor_pro  = User.query.filter_by(id=ad_request.sponsor_id).first()
        sponsor_pro.sponsor_profile.Budget -= ad_request.payment_amount
        influencer_pro = User.query.filter_by(id=ad_request.influencer_id).first()
        influencer_pro.influencer_profile.earning += ad_request.payment_amount
        get_campaign = Campaign.query.filter_by(id=ad_request.campaign_id).first()
        get_campaign.budget -= ad_request.payment_amount
    db.session.commit()


    return jsonify({"message": "Ad request updated successfully"}), 200


#route to send request details
@api.route('/request/<int:id>', methods=['GET'])
@jwt_required()
def get_request(id):
    curr_user = get_jwt_identity()

    user = User.query.filter_by(id=curr_user.get('id')).first()
    if "influencer" in user.get_roles():
        request = AdRequest.query.filter_by(id=id, influencer_id=user.id).first()
    else:
        request = AdRequest.query.filter_by(id=id, sponsor_id=user.id).first()

    if not request:
        return jsonify({"message": "Ad request not found"}), 404
    camp = Campaign.query.filter_by(id=request.campaign_id).first()
    
    msg = request.get_messages()
    

    return jsonify({"id":request.id,
                    "sponsor_id": request.sponsor_id,
                    "campaign_name": camp.name,
                    "sponsor_name": User.query.filter_by(id=request.sponsor_id).first().name,
                    "influencer_id": request.influencer_id,
                    "influencer_name": User.query.filter_by(id=request.influencer_id).first().name, 
                    "campaign_id": request.campaign_id, 
                    "request_type": request.request_type, 
                    "requirements": request.requirements, 
                    "payment_amount": request.payment_amount, 
                    "status": request.status, 
                    "messages": msg}), 200





#route for searchin public campaigns
@api.route('/campaigns/search', methods=['GET'])
@jwt_required()
def search_campaigns():
    curr_user = get_jwt_identity()
    if "influencer" not in curr_user.get("role"):
        return jsonify({"msg": "Influencer access required"}), 403

    name = request.args.get('name', '').lower()
    category = request.args.get('category', '').lower()
    min_budget = request.args.get('budget', type=int, default=0)

    query = db.session.query(Campaign).join(Sponsor).filter( Campaign.visibility == 'public')

    if name:
        query = query.filter(Campaign.name.ilike(f"%{name}%"))
    if category:
        query = query.filter(Campaign.category.ilike(f"%{category}%"))
    if min_budget:
        query = query.filter(Campaign.budget >= min_budget)

    campaigns = query.all()

    campaign_data = [
        {
            "id": campaign.id,
            "name": campaign.name,
            "description": campaign.description,
            "start_date": campaign.start_date.strftime("%a, %d %b %Y"),
            "end_date": campaign.end_date.strftime("%a, %d %b %Y"),
            "budget": campaign.budget,
            "goals": campaign.goals,
            "category": campaign.category,
            "sponsor_id": campaign.sponsor_id
        }
        for campaign in campaigns
    ]

    return jsonify(campaign_data), 200


#influencer request to sponsor with payment amount and message
@api.route('/influencer/request', methods=['POST'])
@jwt_required()
def create_influencer_request():
    curr_user = get_jwt_identity()
    if "influencer" not in curr_user.get("role"):
        return jsonify({"msg": "Influencer access required"}), 403

    user_id = curr_user.get('id')
    data = request.get_json()

    sponsor_id = data.get('sponsor_id')
    campaign_id = data.get('campaign_id')
    message = data.get('message')
    payment_amount = data.get('payment')



    sponsor = Sponsor.query.filter_by(id=sponsor_id).first()
    campaign = Campaign.query.filter_by(id=campaign_id).first()

    spo_user = User.query.filter_by(id=sponsor.user_id).first()
    if not sponsor or not campaign:
        return jsonify({"message": "Sponsor or Campaign not found"}), 404
    
    message_entry = {
        "role": 'influencer',
        "message": message,
        "timestamp": datetime.utcnow().isoformat()
    }

    # message_entry = json.dumps(message_entry)

    ad_request = AdRequest(
        sponsor_id=spo_user.id,
        influencer_id=user_id,
        campaign_id=campaign_id,
        request_type = 'influencer_initiated',
        messages=[message_entry],
        payment_amount=payment_amount
    )

    db.session.add(ad_request)
    db.session.commit()

    return jsonify({"message": "Ad request created successfully"}), 201


#route to see all request of influencer and sponsor
@api.route('/allrequests', methods=['GET'])
@jwt_required()
def get_total_request():
    curr_user = get_jwt_identity()
    user_id = curr_user.get('id')
    if "influencer" in curr_user.get("role"):
        requests = AdRequest.query.filter_by(influencer_id=user_id).all()
    elif("sponsor" in curr_user.get("role")):
        requests = AdRequest.query.filter_by(sponsor_id=user_id).all()
    else:
        return jsonify({"msg": "Sponsor or Influencer access required"}), 403
    
    # Serialize ad requests
    request = [
        {
            'id': req.id,
            'sponsor_id': req.sponsor_id,
            'payment_amount': req.payment_amount,
            'status': req.status,
            'type': req.request_type,
        }
        for req in requests
    ]

    influencer_data = [{'InfName':User.query.filter_by(id=req.influencer_id).first().name} for req in requests]

    sponsor_data = [{'SpoName':User.query.filter_by(id=req.sponsor_id).first().name} for req in requests]

    campaign_data = [{'CampName':Campaign.query.filter_by(id=req.campaign_id).first().name} for req in requests]

    combined_data = [
    {**req_data, **inf_data, **sp_data, **camp_data}
    for req_data, inf_data, sp_data, camp_data in zip(request, influencer_data, sponsor_data, campaign_data)
    ]

    return jsonify({'request': combined_data}), 200

#route to get data of influcer accepted request
@api.route('/influencer/accepted', methods=['GET'])
@jwt_required()
def get_influencer_accepted():
    curr_user = get_jwt_identity()
    user_id = curr_user.get('id')
    if "influencer" in curr_user.get("role"):
        requests = AdRequest.query.filter_by(influencer_id=user_id, status='Accepted').all()
    else:
        return jsonify({"msg": "Influencer access required"}), 403
    
    
    #coount of pending request
    pending = AdRequest.query.filter_by(influencer_id=user_id, status='Pending').count()
    earning = User.query.filter_by(id=user_id).first().influencer_profile.earning

    req = [
        {
            'payment_amount': req.payment_amount,
        }
        for req in requests]
    
    campaing = [{'CampName':Campaign.query.filter_by(id=req.campaign_id).first().name,
                 'duration':(Campaign.query.filter_by(id=req.campaign_id).first().end_date-Campaign.query.filter_by(id=req.campaign_id).first().start_date).days,
                 } for req in requests]
    
    combined_data = [
    {**req_data,  **camp_data}
    for req_data,  camp_data in zip(req, campaing)
    ]


    return jsonify({'data': combined_data, 'pending':pending, 'earning':earning}), 200