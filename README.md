# TurboMail
# Send Recieve Email Communication with Web Based Client Using Socket Programming

Turbo Mail is a Flask-based web application that allows users to compose and send emails via Gmail SMTP and view their inbox.

## Features

- Compose and send emails with custom recipients, subjects, and messages.
- View inbox messages and their details.
- Responsive design for seamless usage on various devices.
- Utilizes Gmail SMTP for sending emails securely.

## Dependencies

- **Flask**: Web framework for Python.
- **Jinja2**: Template engine for Flask.
- **Bootstrap**: Front-end framework for styling.
- **jQuery**: JavaScript library for DOM manipulation.
- **popper.js**: Dependency for Bootstrap's dropdowns, tooltips, and popovers.

## Installation

1. Clone the repository to your local machine:

```bash
git clone <repository_url>
```

2. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

3. Run the Flask application:

```bash
python app.py
```

4. Open a web browser and navigate to `http://localhost:5000` to access the application.

## Usage

1. **Compose Email**:
   - Click on the "Compose" button to navigate to the compose screen.
   - Enter the recipient's email address, subject, and message content.
   - Click on the "Send" button to send the email.

2. **View Inbox**:
   - Click on the "Inbox" button to view your inbox messages.
   - Click on any message to view its details.

## Configuration

Before running the application, make sure to set up the following environment variables:

- **APP_PASSWORD**: Gmail application password for SMTP authentication.
- **GMAIL_USERNAME**: Your Gmail email address.
  
## Troubleshooting

If you encounter any issues while using Turbo Mail, try the following steps:

1. Check your internet connection.
2. Ensure that your Gmail credentials and application password are correct.
3. Verify that your SMTP settings are configured properly.
4. Check the Flask logs for any error messages.

## Contributing

Contributions to Turbo Mail are welcome! If you find any bugs or have suggestions for new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Feel free to customize this README according to your project's specific requirements and branding. Let me know if you need further assistance!
