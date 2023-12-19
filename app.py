from googleapiclient.http import MediaIoBaseUpload
from googleapiclient.errors import HttpError
import io
from Google import Create_Service
from flask import Flask, render_template, request

app = Flask(__name__)

def create_folder(service, folder_name, parent_folder_id=None):
    body = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id] if parent_folder_id else [],
    }
    folder = service.files().create(body=body).execute()
    return folder['id']

def upload_to_google_drive(service, file_content, file_name, folder_id=None):
    media_body = MediaIoBaseUpload(io.BytesIO(file_content), mimetype='application/pdf', resumable=True)
    body = {
        'name': file_name,
        'parents': [folder_id] if folder_id else [],
    }
    response = service.files().create(body=body, media_body=media_body).execute()
    return response

@app.route('/', methods=['GET', 'POST'])
def index():
    success_message = None

    if request.method == 'POST':
        success_message = "UPLOAD UNSUCCESSFUL: Please select at least one file before submitting."
        email = request.form.get('email')
        deposition_file = request.files.get('depositionFile')
        medical_records_file = request.files.get('medicalRecordsFile')
        discovery_file = request.files.get('discoveryFile')
        miscellaneous_file = request.files.get('miscellaneousFile')

        # Check if at least one file input is not empty
        if not any([deposition_file and deposition_file.filename, medical_records_file and medical_records_file.filename, discovery_file and discovery_file.filename, miscellaneous_file and miscellaneous_file.filename]):
            return render_template('index.html', success_message=success_message)

        CLIENT_SECRET_FILE = 'client_secret_EssentialSummaries.json'
        API_NAME = 'drive'
        API_VERSION = 'v3'
        SCOPES = ['https://www.googleapis.com/auth/drive']

        service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

        # Get the ID of the "Website Uploads" folder
        website_uploads_folder_id = '1CgDFrdJ5NvO-EfIPpT3r99Ns2kxgz6yf'

        # Create a subfolder with the email as the folder name
        subfolder_id = create_folder(service, email, website_uploads_folder_id)

        # Upload files to Google Drive
        if deposition_file is not None:
            deposition_response = upload_to_google_drive(service, deposition_file.read(), "Deposition | " + deposition_file.filename, subfolder_id)
            print("Deposition File ID:", deposition_response['id'])

        if medical_records_file is not None:
            medical_records_response = upload_to_google_drive(service, medical_records_file.read(), "Medical Records | " + medical_records_file.filename, subfolder_id)
            print("Medical Records File ID:", medical_records_response['id'])

        if discovery_file is not None:
            discovery_response = upload_to_google_drive(service, discovery_file.read(), "Discovery | " + discovery_file.filename, subfolder_id)
            print("Discovery File ID:", discovery_response['id'])

        if miscellaneous_file is not None:
            miscellaneous_response = upload_to_google_drive(service, miscellaneous_file.read(), "Miscellaneous | " + miscellaneous_file.filename, subfolder_id)
            print("Miscellaneous File ID:", miscellaneous_response['id'])

        success_message = "UPLOAD SUCCESSFUL: We will be reviewing your documents and will reach out shortly."

    return render_template('index.html', success_message=success_message)

if __name__ == '__main__':
    app.run(debug=False)
