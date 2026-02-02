import hashlib
from Constants import Constants

api_id = str(Constants.API_ID)
api_hash = str(Constants.API_HASH)

print("api_id_last3:", api_id[-3:])
print("api_hash_sha6:", hashlib.sha256(api_hash.encode()).hexdigest()[:6])
