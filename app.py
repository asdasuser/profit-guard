import secrets
import requests
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, session
from models import db, ChargeClient, ContactForm


app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///survey.db'
db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def index():
    if session.get('form_submitted', False):
        return render_template('index.html', form_submitted=True)
    return render_template('index.html')


@app.route('/target_form', methods=['POST'])
def target_form():
    if session.get('form_submitted', False):
        return render_template('index.html', form_submitted=True)
    
    fraud_type = request.form.get('fraudType')
    lost_amount = request.form.get('lostAmount')
    contact_method = request.form['contact']
    name = request.form['name']
    email = request.form['email']
    phone = clean_phone_number(request.form['phone'])
    agree_terms = request.form.get('agree') == 'on'
    agree_age = request.form.get('agree-1') == 'on'
    
    new_chargeback_client = ChargeClient(
        fraud_type=fraud_type,
        lost_amount=lost_amount,
        contact_method=contact_method,
        name=name,
        email=email,
        phone=phone,
        agree_terms=agree_terms,
        agree_age=agree_age
    )
    
    db.session.add(new_chargeback_client)
    db.session.commit()
    
    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M')
    message = f'#клиент\nНомер: {phone}\nСвязь: {contact_method}\nИмя:{name}\nЕмейл: {email}\nАфера: {fraud_type}\nПотерял: {lost_amount}\n\n{current_datetime}'
    send_telegram(message)
    
    
    
    session['form_submitted'] = True
    return redirect(url_for('index'))


@app.route('/contact_form', methods=['POST'])
def contact_form():
    contact_method = request.form['select-38ed']
    name = request.form['name-1492']
    email = request.form['email-1492']
    phone = clean_phone_number(request.form['phone-f013'])
    agree_terms = request.form.get('agree') == 'on'
    agree_age = request.form.get('agree-1') == 'on'
    
    new_contact_form = ContactForm(
        contact_method=contact_method,
        name=name,
        email=email,
        phone=phone,
        agree_terms=agree_terms,
        agree_age=agree_age
    )
    
    current_datetime = datetime.now().strftime('%d-%m-%Y %H:%M')
    message = f'#контакт\nНомер: {phone}\nСвязь: {contact_method}Имя:{name}\nЕмейл: {email}\n\n{current_datetime}'

    send_telegram(message)
    
    db.session.add(new_contact_form)
    db.session.commit()

    session['form_submitted'] = True
    return redirect(url_for('index'))


@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')


def clean_phone_number(phone : str):
    cleaned_phone = phone.replace('+', '')    
    cleaned_phone = cleaned_phone.replace('(', '')    
    cleaned_phone = cleaned_phone.replace(')', '')    
    cleaned_phone = cleaned_phone.replace('-', '')
    cleaned_phone = cleaned_phone.replace(' ', '')
    
    return cleaned_phone


def send_telegram(msg):
    TOKEN = '6027394638:AAEL-4dQpZzmJc6TVs28fDJP7I1-LbyDPgM'
    CHAT_ID = '-994909117'
    api = 'https://api.telegram.org/bot'
    method = api + TOKEN + '/sendMessage'
    
    req = requests.post(method, data={
        'chat_id': CHAT_ID,
        'text': msg,
    })

if __name__ == '__main__':
    app.run(debug=True)