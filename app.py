from flask import Flask, render_template, request
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# Configure Flask app for file uploads
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Configure Flask app for email sending
app.config['MAIL_SERVER'] = 'your_mail_server'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'MAILUSERNAME'
app.config['MAIL_PASSWORD'] = 'MAILPASSWORD'

mail = Mail(app)

# Check if the file has a permitted extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for handling file uploads and sending email
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'depositionFile' not in request.files or 'medicalRecordsFile' not in request.files or 'discoveryFile' not in request.files:
            return 'No file part'

        # Process each file input
        for file_key in request.files:
            file = request.files[file_key]

            # Check if the file is allowed and has a filename
            if file and allowed_file(file.filename):
                filename = file.filename
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Send email with file details
        send_email()

        return 'Files uploaded and email sent successfully'

# Function to send email
def send_email():
    msg = Message('Files Uploaded', sender='your_email@example.com', recipients=['recipient_email@example.com'])
    msg.body = 'Files have been uploaded.'
    
    # Attach each uploaded file to the email
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with app.open_resource(file_path) as attachment:
            msg.attach(filename, 'application/pdf', attachment.read())

    mail.send(msg)

if __name__ == '__main__':
    app.run(debug=True)