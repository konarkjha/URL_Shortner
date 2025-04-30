import shortuuid
import uuid

def encode_id(id: int) -> str:
    """
    Encodes an integer ID into a short, URL-safe string using shortuuid
    after converting the integer to a UUID.
    """
    # Create a UUID from the integer (this isn't strictly sequential but is unique)
    new_uuid = uuid.uuid5(uuid.NAMESPACE_DNS, str(id))
    return shortuuid.encode(new_uuid)