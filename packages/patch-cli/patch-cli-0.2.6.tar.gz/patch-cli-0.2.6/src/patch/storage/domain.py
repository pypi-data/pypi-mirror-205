import os

def get_patch_domain():
    domain = os.environ.get('PATCH_ENDPOINT')
    if domain == None:
        domain = "https://api.patch.tech"
    return domain