from flask_security import UserMixin, RoleMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import JSON
import json

db = SQLAlchemy()

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    Email = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=True)
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    flag = db.Column(db.Boolean, default=False)
    bio = db.Column(db.String(150), nullable=True)


    roles = db.relationship('Role', secondary='roles_users',
                            backref=db.backref('users', lazy='dynamic'))
    influencer_profile = db.relationship("Influencer", backref="user", uselist=False, cascade='all, delete-orphan')
    sponsor_profile = db.relationship("Sponsor", backref="user", uselist=False, cascade='all, delete-orphan')

    def get_roles(self):
        return [role.name for role in self.roles]


class RolesUsers(db.Model):
    __tablename__ = 'roles_users'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)


class Influencer(db.Model):
    __tablename__ = "influencer"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), unique=True)
    earning = db.Column(db.Integer, nullable=False, default=0)
    Niche = db.Column(db.String(80), nullable=False)
    Reach = db.Column(db.Integer, nullable=False)
    Category = db.Column(db.String(80), nullable=False)

    ad_requests = db.relationship('AdRequest', back_populates='influencer', cascade='all, delete-orphan')


class Sponsor(db.Model):
    __tablename__ = "sponsor"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete='CASCADE'), unique=True)
    company_name = db.Column(db.String, nullable=False)
    Budget = db.Column(db.Integer, nullable=False)
    Industry = db.Column(db.String(80), nullable=False)
    Approve = db.Column(db.Boolean, default=False)
    pending = db.Column(db.Boolean, default=True)

    ad_requests = db.relationship('AdRequest', back_populates='sponsor', cascade='all, delete-orphan')


class Campaign(db.Model):
    __tablename__ = "campaign"
    
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id', ondelete='CASCADE'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(Enum('public', 'private', name='visibility_enum'), nullable=False, default='public')
    goals = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), nullable=True)
    flagged = db.Column(db.Boolean, nullable=False, default=False)

    ad_requests = db.relationship('AdRequest', back_populates='campaign', cascade='all, delete-orphan')


class AdRequest(db.Model):
    __tablename__ = "ad_request"
    
    id = db.Column(db.Integer, primary_key=True)
    influencer_id = db.Column(db.Integer, db.ForeignKey('influencer.id', ondelete='CASCADE'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id', ondelete='CASCADE'), nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.id', ondelete='CASCADE'), nullable=False)
    request_type = db.Column(Enum('influencer_initiated', 'sponsor_initiated', name='request_type_enum'), nullable=False)
    requirements = db.Column(db.Text, nullable=True)
    payment_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='Pending')
    messages = db.Column(JSON, nullable=True, default=[]) 
    flagged = db.Column(db.Boolean, nullable=False, default=False)

    influencer = db.relationship('Influencer', back_populates='ad_requests')
    campaign = db.relationship('Campaign', back_populates='ad_requests')
    sponsor = db.relationship('Sponsor', back_populates='ad_requests')

    def get_messages(self):
        if isinstance(self.messages, list):
            return self.messages
        return json.loads(self.messages or "[]")  

    def add_message(self, message_entry):
        messages = self.get_messages()
        messages.append(message_entry)
        self.messages = json.dumps(messages)
