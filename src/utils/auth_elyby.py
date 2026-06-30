from pathlib import Path

USER_SETTINGS = ''
LAUNCHER_SETTINGS = ''
DEBUG = False

class Auth_elyby():
    def __init__(self):
        self.settings_path = Path(f'{os.getcwd()}/src/data/{USER_SETTINGS}.json')

    def create_account(self,username:str):
        full_username = f"OfflinePlayer:{username}"
        uuid = hashlib.md5(full_username).digest()
        # Set version to 3 (MD5 name-based)
        md5_hash = bytearray(md5_hash)
        md5_hash[6] = (md5_hash[6] & 0x0f) | 0x30  # Version 3
        md5_hash[8] = (md5_hash[8] & 0x3f) | 0x80  # Variant 10
        
        # Format sebagai UUID string
        uuid_hex = md5_hash.hex()
        uuid_formatted = f'{uuid_hex[:8]}-{uuid_hex[8:12]}-{uuid_hex[12:16]}-{uuid_hex[16:20]}-{uuid_hex[20:]}'

        data = {
            "auth_type": "elyby",
            "username": username,
            "uuid": uuid_formatted,
            "access_token": "",
      }

        with open(self.settings_path,mode='w',encoding='UTF-8') as f:
            json.dump(data,f,ensure_ascii=False,allow_nan=False,indent=4)
            print('account succesfuly created.')
    
    
    def load_account(self):
        with open(self.settings_path,mode='r',encoding='UTF-8') as f:
            json.load(f) if self.settings_path else "file hilang, silahkan buat baru lagi."
        
    def update_acces_token(self,token:str):
        user_data = self.load_account()
        with open(self.settings_path,mode='r',encoding='UTF-8') as f:
            user_data['access_token'] = token
            json.dump(user_data,f,ensure_ascii=False,allow_nan=False,indent=4)


        

if __name__ == "__main__":
    Auth_elyby()