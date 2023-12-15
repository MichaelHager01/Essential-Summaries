from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'michaelhswe@gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

@app.route('/home', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])

def home():
    # if request.method == 'POST':
    #     msg = Message("HEY", sender='noreply@demo.com', recipients=['rmagaly042@gmail.com'])
    #     msg.body = "Hey how are you, this is for testing!"
    #     mail.send(msg)
    #     return "Sent email."

    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)

