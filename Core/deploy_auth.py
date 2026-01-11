# Tell Claude to save this as 'deploy_auth.py' in your /Core folder
import firebase_admin
from firebase_admin import auth, credentials

# Initialize with Google Application Default Credentials (IAM)
# This is high leverage because it uses the environment's identity
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
    'projectId': 'ADAM-ZERO-PROJECT-ID',
})

def get_secure_lattice_token(uid):
    # Generates a custom token for your 'Atomic Identity'
    return auth.create_custom_token(uid)
