from .workers import celery
from flask import current_app as app
from jinja2 import Template
from application.db import User, RolesUsers, Purchase, Role, Product
from application.access import acs_user_all
from application.message import dailyRemainderEmail, mail
from sqlalchemy import func
from sqlalchemy import and_, not_
from datetime import datetime
from io import StringIO
import csv

# @celery.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # sender.add_periodic_task(
#     #     crontab(day_of_month=1, month_of_year='*'),
#     #     monthlyMail.s(),
#     # )
#     # sender.add_periodic_task(
#     #     crontab(minute=0, hour=18, day_of_month='*'),
#     #     dailyRemainder.s(),
#     # )
#     print("something supposed to happen")
#     sender.add_periodic_task(20,
#                              send_example_mail.s(),
#                              name='send example mail every 5 seconds')

# def send_email(to_address, subject, message):
#     msg = MIMEMultipart()
#     msg['From'] = "email@sahil.com"
#     msg['To'] = to_address
#     msg['Subject'] = subject
#     msg.attach(MIMEText(message, 'html'))

#     # s = smtplib.SMTP(SMTP_SERVER_HOST, SMTP_SERVER_PORT)
#     # s.login(SENDER_ADDRESS, SENDER_PASSWORD)
#     s = smtplib.SMTP('127.0.0.1', 1025)
#     s.login("email@sahil.com", "password")
#     s.send_message(msg)
#     s.quit()

#     return True


@celery.task()
def sendDailyReminder():
    print('sending example mail')
    # for each user_id, get the user email
    # send email to each user
    user_role = Role.query.filter_by(name='user').first()

    today = datetime.today().date()
    all_users = User.query.join(RolesUsers).filter(
        and_(
            RolesUsers.role_id == user_role.id,
            not_(User.purchases.any(Purchase.purchase_date == today))
        )
    ).with_entities(User.id, User.email).all()

    id_email = {user.id: user.email for user in all_users}
    all_user_id = set([user.id for user in all_users])
    
    # send email to all the user_id who have not booked today
    for user_id in all_user_id:
        print("sending email to", id_email[user_id])
        dailyRemainderEmail(id_email[user_id])


@celery.task()
def sendMonthlyMail(id, email):
    
    # Join with Product table and filter by user_id
    bookings = (
        Purchase.query
        .join(Product, Purchase.product_id == Product.id)
        .filter(Purchase.user_id==id)
        .all()
    )

    # Calculate the number of orders, number of products, and the total amount paid
    no_of_orders = len(set([booking.order_id for booking in bookings]))
    no_of_products = len(bookings)
    # Calculate amount paid based on product price
    amount_paid = sum([booking.product.price * booking.quantity for booking in bookings])

    with open(f'{app.config["EMAIL_TEMPLATE"]}report.mail.html') as file:
        template = Template(file.read())
        message = template.render(email=email, no_of_orders=no_of_orders, no_of_products=no_of_products, amount_paid=amount_paid)
    print(email)
    mail(email, 'Monthly Review Report', message)

    return 'Sent Mail'


@celery.task()
def monthlyMail():
    user_role = Role.query.filter_by(name='user').first()

    all_users = User.query.join(RolesUsers).filter(
            RolesUsers.role_id == user_role.id).all()
    print(len(all_users))
    for user in all_users:
        # print(user.email)
        sendMonthlyMail.delay(user.id, user.email)

    return 'Monthly Mail Sent'

@celery.task()
def test():
    print('RUNNING TEST')



@celery.task()
def create_products_csv():

    products_with_quantity_sold = (
        Product.query
        .join(User, Product.seller_id == User.id)
        .outerjoin(Purchase, Product.id == Purchase.product_id)
        .with_entities(
            Product.id.label('id'),
            Product.name.label('name'),
            Product.description.label('description'),
            Product.price.label('price'),
            Product.stock.label('stock'),
            func.sum(Purchase.quantity).label('sold-units')
        )
        .group_by(Product.id)
        .all()
    )

    all_products = [product._asdict() for product in products_with_quantity_sold]

    csv_data = StringIO()
    csv_writer = csv.DictWriter(csv_data, fieldnames=["id", "name", "description", "price", "stock", "sold-units"])
    csv_writer.writeheader()
    csv_writer.writerows(all_products)

    filename = "test.csv"
    with open(filename, 'w', newline='') as f:
        f.write(csv_data.getvalue())

    return filename