from socket import *
import ssl
from base64 import b64encode
from flask import Flask, render_template, request, jsonify
import email
import re
import imaplib
import email
import codecs
import string

# radix healthcare app password
APP_PASSWORD = "etjx qvrf pwnp xhrk"

class EmailClient:
    
    def __init__(self, email, password, destination_email, subject, body):
        self.email = email
        self.password = password
        self.destination_email = destination_email
        self.subject = subject
        self.body = body
        self.msg = '{}.\r\n'.format(body)
        self.endmsg = "\r\n.\r\n"
        self.mailserver = 'smtp.gmail.com'
        self.mail_port = 587
        self.client_socket = socket(AF_INET, SOCK_STREAM)

    def connect_to_server(self):
        self.client_socket.connect((self.mailserver, self.mail_port))
        recv = self.client_socket.recv(1024).decode()
        print(recv)
        if recv[:3] != '220':
            print('220 reply not received from server.')

    def send_helo_command(self):
        helo_command = 'HELO Alice\r\n'
        self.client_socket.send(helo_command.encode())
        recv1 = self.client_socket.recv(1024).decode()
        print(recv1)
        if recv1[:3] != '250':
            print('250 reply not received from server.')

    def start_tls(self):
        strtlscmd = "STARTTLS\r\n".encode()
        self.client_socket.send(strtlscmd)
        recv2 = self.client_socket.recv(1024)

        ssl_context = ssl.create_default_context()
        self.ssl_client_socket = ssl_context.wrap_socket(self.client_socket, server_hostname=self.mailserver)

    def authenticate(self):
        email_encoded = b64encode(self.email.encode())
        password_encoded = b64encode(self.password.encode())

        authorization_cmd = "AUTH LOGIN\r\n"
        self.ssl_client_socket.send(authorization_cmd.encode())
        recv2 = self.ssl_client_socket.recv(1024)
        print(recv2)

        self.ssl_client_socket.send(email_encoded + "\r\n".encode())
        recv3 = self.ssl_client_socket.recv(1024)
        print(recv3)

        self.ssl_client_socket.send(password_encoded + "\r\n".encode())
        recv4 = self.ssl_client_socket.recv(1024)
        print(recv4)

    def send_email(self):
        mail_from = "Mail from: <{}>\r\n".format(self.destination_email)
        self.ssl_client_socket.send(mail_from.encode())
        recv5 = self.ssl_client_socket.recv(1024)
        print(recv5)

        rcpt_to = "RCPT TO: <{}>\r\n".format(self.destination_email)
        self.ssl_client_socket.send(rcpt_to.encode())
        recv6 = self.ssl_client_socket.recv(1024)
        print(recv6)

        data = 'DATA\r\n'
        self.ssl_client_socket.send(data.encode())
        recv7 = self.ssl_client_socket.recv(1024)
        print(recv7)

        self.ssl_client_socket.send("Subject: {}\n\n{}".format(self.subject, self.msg).encode())
        self.ssl_client_socket.send(self.endmsg.encode())
        recv8 = self.ssl_client_socket.recv(1024)
        print(recv8)

    def quit(self):
        quit_cmd = 'QUIT\r\n'
        self.ssl_client_socket.send(quit_cmd.encode())
        recv9 = self.ssl_client_socket.recv(1024)
        print(recv9)

    def close_connection(self):
        self.ssl_client_socket.close()
        print('Success')

    def run_all(self):

        self.connect_to_server()
        self.send_helo_command()
        self.start_tls()
        self.authenticate()
        self.send_email()
        self.quit()
        self.close_connection()




app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    if request.method == 'POST':
        to_mail = request.form['to']
        from_mail = request.form['from']
        subject = request.form['subject']
        message = request.form['message']
        print(to_mail, from_mail, subject, message)

        runner = EmailClient(from_mail,APP_PASSWORD,to_mail,subject,message)
        runner.run_all()
        
        return render_template("home.html", show_tick=True)
    else:
        return render_template("home.html")


@app.route('/inbox')
def display_mail():  # put application's code here
    mail = [
        # {'subject': 'Welcome to our service', 'sender': 'info@example.com', 'id': 1},
        # {'subject': 'Your order confirmation', 'sender': 'sales@shop.com', 'id': 2}

    ]
    message_id = 1  # Initialize a message ID counter
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    username = 'healthcere.radix@gmail.com'
    password = APP_PASSWORD
    imap.login(username, password)

    for i in imap.list()[1]:
        l = i.decode().split(' "/" ')
        print(l[0] + " = " + l[1])

    imap.select('"INBOX"')
    status, messages = imap.search(None, 'ALL')

    for num in messages[0].split()[::-1]:
        _, msg = imap.fetch(num, '(RFC822)')
        message = email.message_from_bytes(msg[0][1])
        subject_header = message['Subject']
        decoded_subject = email.header.decode_header(subject_header)
        subject = decoded_subject[0][0]
        print("Subject: ", subject)
        print("From: ", message["From"])
        print("Date: ", message["Date"])
        print(message["Body"])  # Prints none

        # Get the message body
        if message.is_multipart():
            # If message is multipart, iterate over each part
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    # Print the plain text part of the message
                    print("Body: ", body)
                    email_dict = {
                        'id': message_id,
                        'Subject': subject,
                        'From': message["From"],
                        'Date_n': message["Date"],
                        'Body': body
                    }
                    mail.append(email_dict)
        else:
            # If message is not multipart, print the body directly
            body = message.get_payload(decode=True).decode()
            print("Body: ", body)
            email_dict = {
                'id': message_id,
                'Subject': subject,
                'From': message["From"],
                'Date_n': message["Date"],
                'Body': body
            }
            mail.append(email_dict)

        # Increment the message ID
        message_id += 1
        print("----------------------")

        # Print the list of dictionaries
        print("Mail List:", mail)

    # mail = [
    #         {'subject': 'Welcome to our service', 'sender': 'info@example.com', 'id': 1},
    #         {'subject': 'Your order confirmation', 'sender': 'sales@shop.com', 'id': 2}
    #     ]
    return render_template("inbox.html",mail_inbox_items = mail)



@app.route('/mail/<int:message_id>')
def get_message(message_id):
    particular_mail = [
        # {'subject': 'Welcome to our service', 'sender': 'info@example.com', 'id': 1,
        #  'content': 'this is first message'},
        # {'subject': 'Your order confirmation', 'sender': 'sales@shop.com', 'id': 2, 'content': 'this is second message'}
    ]
    message_id_int = 1  # Initialize a message ID counter
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    username = 'healthcere.radix@gmail.com'
    password = APP_PASSWORD
    imap.login(username, password)

    for i in imap.list()[1]:
        l = i.decode().split(' "/" ')
        print(l[0] + " = " + l[1])

    imap.select('"INBOX"')
    status, messages = imap.search(None, 'ALL')

    for num in messages[0].split()[::-1]:
        _, msg = imap.fetch(num, '(RFC822)')
        message = email.message_from_bytes(msg[0][1])
        subject_header = message['Subject']
        decoded_subject = email.header.decode_header(subject_header)
        subject = decoded_subject[0][0]
        print("Subject: ", subject)
        print("From: ", message["From"])
        print("Date: ", message["Date"])
        print(message["Body"])  # Prints none

        # Get the message body
        if message.is_multipart():
            # If message is multipart, iterate over each part
            for part in message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                try:
                    body = part.get_payload(decode=True).decode()
                except:
                    pass
                if content_type == "text/plain" and "attachment" not in content_disposition:
                    # Print the plain text part of the message
                    print("Body: ", body)
                    email_dict = {
                        'id': message_id_int,
                        'Subject': subject,
                        'From': message["From"],
                        'Date_n': message["Date"],
                        'Body': body
                    }
                    particular_mail.append(email_dict)
        else:
            # If message is not multipart, print the body directly
            body = message.get_payload(decode=True).decode()
            print("Body: ", body)
            email_dict = {
                'id': message_id_int,
                'Subject': subject,
                'From': message["From"],
                'Date_n': message["Date"],
                'Body': body
            }
            particular_mail.append(email_dict)

        # Increment the message ID
        message_id_int += 1
        print("----------------------")

        # Print the list of dictionaries
        print("Mail List:", particular_mail)

    message = particular_mail[message_id-1]
    print(message)
    return jsonify(message)



if __name__ == '__main__':
    app.run()
