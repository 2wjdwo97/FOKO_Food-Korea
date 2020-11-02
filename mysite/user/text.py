
def msg_Email(domain, uidb64, token):
    return f"Click on the link below to complete the verification.\n\nlink : http://{domain}/users/activate/{uidb64}/{token}"
