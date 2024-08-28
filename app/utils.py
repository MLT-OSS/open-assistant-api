from base64 import b64encode, b64decode

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from config.config import settings as app_settings


def aes_encrypt(plain_text: str):
    cipher = AES.new(bytes.fromhex(app_settings.AES_ENCRYPTION_KEY), AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode("utf-8")
    ct = b64encode(ct_bytes).decode("utf-8")
    return f"{iv},{ct}"


def aes_decrypt(encrypted_text: str):
    if encrypted_text is None or "," not in encrypted_text:
        return None
    iv, ct = encrypted_text.split(",", 1)
    iv = b64decode(iv)
    ct = b64decode(ct)
    cipher = AES.new(bytes.fromhex(app_settings.AES_ENCRYPTION_KEY), AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode("utf-8")


def revise_tool_names(tools: list):
    if not tools:
        return
    for tool in tools:
        if tool.get('type') != "retrieval":
            continue
        tool['type'] = 'file_search'
