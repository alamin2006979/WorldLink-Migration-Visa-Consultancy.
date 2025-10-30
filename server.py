from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'jpeg', 'png'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Email configuration - Using Mailtrap for testing (free service)
# Sign up at https://mailtrap.io and get your SMTP credentials
SMTP_SERVER = 'sandbox.smtp.mailtrap.io'
SMTP_PORT = 2525
SENDER_EMAIL = '890dcc9ee9a612'  # Your Mailtrap username
SENDER_PASSWORD = '****3d23'  # Your Mailtrap password
RECEIVER_EMAIL = 'enuires.worldlinkmigration@gmail.com'

def send_email(application_data):
    """Send application details via email"""
    try:
        # For now, just print the email content to console
        # You can enable actual email sending later by uncommenting the SMTP code below
        print("=== NEW APPLICATION RECEIVED ===")
        print(f"From: {application_data['firstName']} {application_data['surname']}")
        print(f"Email: {application_data.get('email', 'Not provided')}")
        print(f"WhatsApp: {application_data['whatsapp']}")
        print(f"Country: {application_data['country']}")
        print(f"University: {application_data['university']}")
        print(f"Status: {application_data['status']}")
        print("=================================")

        # Enable email sending with Mailtrap
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECEIVER_EMAIL
        msg['Subject'] = f'New Visa Application from {application_data["firstName"]} {application_data["surname"]}'

        body = f'''
New Visa Application Received:

Personal Information:
- Name: {application_data["firstName"]} {application_data["surname"]}
- Date of Birth: {application_data["dob"]}
- Gender: {application_data["gender"]}
- WhatsApp: {application_data["whatsapp"]}

Education & Language:
- Highest Qualification: {application_data["qualification"]}
- English Proficiency: {application_data["englishProficiency"]}

Study Preferences:
- Interested Course: {application_data["interestedCourse"]}
- Country: {application_data["country"]}
- University: {application_data["university"]}

Documents Submitted:
- Certificate/Transcript: {application_data.get("certificateTranscript", "Not provided")}
- Passport First Page: {application_data.get("passportFirstPage", "Not provided")}
- Photo: {application_data.get("photo", "Not provided")}

Application Details:
- User ID: {application_data["userId"]}
- Status: {application_data["status"]}
- Submitted: {datetime.fromisoformat(application_data["submittedAt"]).strftime('%Y-%m-%d %H:%M:%S')}

Please review this application in the admin panel.
        '''

        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, text)
        server.quit()

        return True
    except Exception as e:
        print(f"Email sending failed: {e}")
        return False

@app.route('/submit-application', methods=['POST'])
def submit_application():
    try:
        # Handle file uploads
        certificate_file = request.files.get('certificateTranscript')
        passport_file = request.files.get('passportFirstPage')
        photo_file = request.files.get('photo')

        # Get form data
        data = request.form.to_dict()

        # Save uploaded files
        certificate_path = None
        passport_path = None
        photo_path = None

        if certificate_file and allowed_file(certificate_file.filename):
            certificate_filename = secure_filename(certificate_file.filename)
            certificate_path = os.path.join(app.config['UPLOAD_FOLDER'], certificate_filename)
            certificate_file.save(certificate_path)
            data['certificateTranscript'] = certificate_filename

        if passport_file and allowed_file(passport_file.filename):
            passport_filename = secure_filename(passport_file.filename)
            passport_path = os.path.join(app.config['UPLOAD_FOLDER'], passport_filename)
            passport_file.save(passport_path)
            data['passportFirstPage'] = passport_filename

        if photo_file and allowed_file(photo_file.filename):
            photo_filename = secure_filename(photo_file.filename)
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo_filename)
            photo_file.save(photo_path)
            data['photo'] = photo_filename

        # Add timestamp and status
        data['submittedAt'] = datetime.now().isoformat()
        data['status'] = 'pending'

        # Send email to admin
        email_sent = send_email(data)

        # Store in local applications.json file (simulating localStorage)
        applications_file = 'applications.json'
        applications = []

        if os.path.exists(applications_file):
            with open(applications_file, 'r') as f:
                applications = json.load(f)

        applications.append(data)

        with open(applications_file, 'w') as f:
            json.dump(applications, f, indent=2)

        response = {
            'success': True,
            'message': 'Application submitted successfully!',
            'email_sent': email_sent
        }

        if not email_sent:
            response['message'] += ' (Note: Email notification failed, but application was saved)'

        return jsonify(response)

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error submitting application: {str(e)}'
        }), 500

@app.route('/get-applications', methods=['GET'])
def get_applications():
    """Get all applications for admin panel"""
    try:
        applications_file = 'applications.json'
        if os.path.exists(applications_file):
            with open(applications_file, 'r') as f:
                applications = json.load(f)
        else:
            applications = []

        return jsonify(applications)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/update-status/<int:index>', methods=['POST'])
def update_status(index):
    """Update application status"""
    try:
        data = request.get_json()
        new_status = data.get('status')

        applications_file = 'applications.json'
        if os.path.exists(applications_file):
            with open(applications_file, 'r') as f:
                applications = json.load(f)

            if 0 <= index < len(applications):
                applications[index]['status'] = new_status

                with open(applications_file, 'w') as f:
                    json.dump(applications, f, indent=2)

                return jsonify({'success': True})
            else:
                return jsonify({'success': False, 'message': 'Application not found'}), 404
        else:
            return jsonify({'success': False, 'message': 'No applications found'}), 404

    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download uploaded files"""
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("Starting Flask server...")
    print("Make sure to update email credentials in server.py")
    app.run(debug=True, port=8000)
