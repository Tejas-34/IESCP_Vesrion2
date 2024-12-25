from celery import shared_task
import time
from .models import db, User, Influencer, AdRequest,Sponsor, Campaign
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from csv import DictReader, DictWriter
from io import StringIO
from datetime import datetime, timedelta




@shared_task
def daily_reminder():
    print("i'm in daily reminder")
    influencers = db.session.query(User).join(Influencer).filter(User.active.is_(True)).all()
    GSPACE= "https://chat.googleapis.com/v1/spaces/AAAADz5PYxo/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=3pd6j3TUcWuPsmXAzmRpLdeMKiSwqUMr3x80Qurdx40"
    for influencer in influencers:
        has_pending_requests = (
            AdRequest.query
            .filter(
                AdRequest.influencer_id == influencer.id,
                AdRequest.status == 'Pending',
                AdRequest.request_type == 'sponsor_initiated'
            )
            .count() > 0
        )

        if has_pending_requests:
            # Formulate reminder message
            print(f"Sending reminder to {influencer.name}")
            requests.post(GSPACE, json={"text": f"Hello {influencer.name},\n"
                 "You have pending ad requests waiting for your response."
                "Please log in to review them or explore new public campaigns. Visit now!"})
            time.sleep(5)



@shared_task
def monthly_reminder():
    smtpObj = smtplib.SMTP('localhost',1025)

    with open('Backend/templates/monthly-reminder.html') as file: 
        content = Template(file.read())
        for sponsor in Sponsor.query.all():
            email = User.query.filter_by(id=sponsor.user_id).first().Email
            message = MIMEMultipart()
            report_data = get_sponsor_monthly_report(sponsor.id)
            html = MIMEText(content.render(report_data=report_data),'html')
            message.attach(html)
            print(f"Sending monthly report to {email}")

            smtpObj.sendmail("22f1001500@ds.study.iitm.ac.in", email, message.as_string())


@shared_task
def import_csv(id):
    csv_file = StringIO()
    writer = DictWriter(csv_file, fieldnames=["Name", "Description", "Start Date", "End Date", "Budget", "Visibility", "Goals", "Category"])
    writer.writeheader()
    
    print("i'm in import_csv")
    for camp in Campaign.query.filter_by(sponsor_id=id).all():
        writer.writerow({
            "Name": camp.name,
            "Description": camp.description,
            "Start Date": camp.start_date,
            "End Date": camp.end_date,
            "Budget": camp.budget,
            "Visibility": camp.visibility,
            "Goals": camp.goals,
            "Category": camp.category
        })
    
    csv_file.seek(0)
    return csv_file.read()




# Query for the last month
def get_sponsor_monthly_report(sponsor_id):
    current_date = datetime.now()
    first_day_of_month = datetime(current_date.year, current_date.month, 1)
    last_month_end = first_day_of_month - timedelta(days=1)
    last_month_start = datetime(last_month_end.year, last_month_end.month, 1)
    

    # Fetch data for the given sponsor
    sponsor = Sponsor.query.filter_by(id=sponsor_id).first()
    if not sponsor:
        return None

    user = User.query.filter_by(id=sponsor.user_id).first()

    print(last_month_start, last_month_end)
    campaigns = Campaign.query.filter(
        Campaign.sponsor_id == sponsor_id,
        Campaign.start_date >= last_month_start,
        Campaign.end_date <= last_month_end
    ).all()

    total_ads = sum(len(campaign.ad_requests) for campaign in campaigns)
    total_budget_used = sum(campaign.budget for campaign in campaigns)
    remaining_budget = sponsor.Budget - total_budget_used

    return {
        
        "name": user.name,
        "username": user.username, 
        "sponsor_name": sponsor.company_name,
        "industry": sponsor.Industry,
        "campaigns": campaigns,
        "total_ads": total_ads,
        "total_budget_used": total_budget_used,
        "remaining_budget": remaining_budget,
        "report_period": f"{last_month_start.strftime('%B %Y')}",
        "year": last_month_start.year,
    }
