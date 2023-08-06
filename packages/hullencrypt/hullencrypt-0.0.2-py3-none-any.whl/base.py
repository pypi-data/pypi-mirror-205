from cryptography import fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import uuid
import base64

class ChildNotFoundException(Exception):
    pass

class Node:
    def __init__(self,
                 parent_key: bytes,
                 key: bytes = None,
                 name: bytes = None,
                 children: list["Node"] = None,
                 content: bytes = None,
                 password: bytes = None
                ):
        assert key == None or parent_key == None, "Only one of key or parent_key can be set"
        self.name = name
        self.uuid = uuid.uuid4().bytes

        self.children = []
        if children:
            self.children = children

        key = self.get_key(parent_key=parent_key) if parent_key else key
        
        f = fernet.Fernet(key)
        if content == None:
            content = b"no content"

        self.content = f.encrypt(content)

        self.enc_key = None

        if password:
            self.set_password(parent_key=parent_key, password=password)

    def get_key(self, parent_key: bytes=None, password: bytes=None):
        assert parent_key != None or password != None
        
        if parent_key:
            key_hash = hashlib.sha256(parent_key, usedforsecurity=True)
            key_hash = key_hash.digest()

            return key_from_hash(key_hash, self.uuid)
        elif password:
            assert self.enc_key != None
            passw_key = self.get_key(parent_key=password)
            f = fernet.Fernet(passw_key)
            return f.decrypt(self.enc_key)

    def get_content(self, key):
        assert self.content != None
        f = fernet.Fernet(key)
        return f.decrypt(self.content)

    def set_password(self, password: bytes, parent_key: bytes=None, old_pass=None):
        assert parent_key != None or old_pass != None
        key = None
        if parent_key:
            key = self.get_key(parent_key=parent_key)
        elif old_pas:
            key = self.get_key(password=old_pass)
        
        assert key != None
        # this will fail if you have the wrong key
        # to make sure you have the correct key, call get_content
        self.get_content(key)

        password_key = self.get_key(parent_key=password)
        f = fernet.Fernet(password_key)
        self.enc_key = f.encrypt(key)

    def update_content(self, key, content: bytes):
        f = fernet.Fernet(key)

        # this will fail if you have the wrong key
        # and is used so you don't overwrite the content with content encrypted with the wrong key
        f.decrypt(self.content)
        
        self.content = f.encrypt(content)

    def get_child_node(self, path: list[str]):
        if len(path) == 0:
            return self
        for child in self.children:
            if child.name == path[0]:
                return child.get_child_node(path[1:])
        raise Exception("child wasn't found")

    def get_child_key(self, key, path: list[str]):
        if len(path) == 0:
            return key
        for child in self.children:
            if child.name == path[0]:
                child_key = child.get_key(parent_key=key)
                return child.get_child_key(child_key, path[1:])
        raise ChildNotFoundException("child wasn't found")

    def to_json(self):
        json = {
            "name": self.name,
            "uuid": self.uuid,
            "content": self.content,
            "enc_key": self.enc_key,
            "children": []
        }

        for child in self.children:
            json["children"].append(child.to_json())

        return json
    
    def from_json(json: str, parent_key: bytes = None, password: str = None):
        assert parent_key != None or password != None
        name = json["name"]
        uuid = json["uuid"]
        content = json["content"]
        children = json["children"]
        enc_key = json["enc_key"]
        if password and not enc_key:
            raise Exception("password was given but enc_key wasn't")
        if password:
            passw_key = key_from_hash(password_hash, uuid)
            f = fernet.Fernet(passw_key)
            key = f.decrypt(enc_key)
        else:
            key = key_from_hash(parent_key, uuid)
        
        # check if the key is correct
        # this will fail if you have the wrong key
        # to make sure you have the correct key, call get_content
        f = fernet.Fernet(key)
        f.decrypt(content)

        decrypted_children = []
        for child in children:
            decrypted_children.append(Node.from_json(child, parent_key=key))
        
        return Node(key=key, name=name, children=decrypted_children, content=content)

def key_from_hash(password_hash: bytes, salt: bytes):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    return base64.urlsafe_b64encode(kdf.derive(password_hash))
