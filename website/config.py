
# This configures the app for the create_app function in __init__.py
# Eventually, these should be configured with environment variables for security

TESTING = True
DEBUG = True
SECRET_KEY = "development"
SESSION_TYPE = 'filesystem'

