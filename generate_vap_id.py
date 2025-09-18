from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
import base64

# Generate a new private key
private_key = ec.generate_private_key(ec.SECP256R1())

# Convert the private key to PEM format
pem_private_key = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption(),
)

# Extract the public key
public_key = private_key.public_key().public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint,
)

# Encode in Base64 (URL safe)
vapid_private_key = base64.urlsafe_b64encode(pem_private_key).decode("utf-8")
vapid_public_key = base64.urlsafe_b64encode(public_key).decode("utf-8")

print("VAPID Public Key:", vapid_public_key)
print("VAPID Private Key:", vapid_private_key)


# # public id
# public_id = "BFpGQtsPz6TP2WKMCJqyvY4DQ751x6JqSEHRdIUcJmxTvuGDpc16qMUW7xvD2a9zdtmmlyS-KVJwC_0xLPoKz4Q="

# # private id 
# privete_id = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JR0hBZ0VBTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEJHMHdhd0lCQVFRZ0xOMHJHTCtxanpuZ3Q5MGkKM3pZWmZYRlZjVHdsYVZmekFheEsyQUliWm1TaFJBTkNBQVJhUmtMYkQ4K2t6OWxpakFpYXNyMk9BME8rZGNlaQpha2hCMFhTRkhDWnNVNzdoZzZYTmVxakZGdThidzltdmMzYlpwcGNrdmlsU2NBdjlNU3o2Q3MrRQotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg=="

public_key = "BDfi5sIHUc1z-8nJb62M7KL5bOLP9t29leG-nhSsPuVwvpCbBjQ26uTo2KVjq3ZXuIJx5OYQpYTmGKaAtZwqmsM="
private_id = "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JR0hBZ0VBTUJNR0J5cUdTTTQ5QWdFR0NDcUdTTTQ5QXdFSEJHMHdhd0lCQVFRZ2EvQ0hlc2JubU96Tm9KbG0KUGg5NndySnIyKzZ1OXQ2QVkzR2wxUjVxc2tHaFJBTkNBQVEzNHViQ0IxSE5jL3ZKeVcrdGpPeWkrV3ppei9iZAp2WlhodnA0VXJEN2xjTDZRbXdZME51cms2TmlsWTZ0MlY3aUNjZVRtRUtXRTVoaW1nTFdjS3ByRAotLS0tLUVORCBQUklWQVRFIEtFWS0tLS0tCg=="
