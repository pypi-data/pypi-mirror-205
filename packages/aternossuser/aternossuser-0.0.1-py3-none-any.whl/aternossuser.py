import requests

class Auth:
    def __init__(self, mail, password):
        self.mail = mail
        self.password = password
        self.auth_token = None
        
    def login(self):
        response = requests.post('https://aternos.org/login/', data={
            'user': self.mail,
            'password': self.password
        })
        if response.status_code == 200 and response.json()['success']:
            self.auth_token = response.cookies.get('ATERNOS_SESSION')
        else:
            raise Exception('Failed to login')
            
class Server:
    def __init__(self, auth: Auth):
        self.auth = auth
        self.server_id = None
        
    def get_status(self):
        response = requests.get('https://aternos.org/ajax/getServer/', cookies={
            'ATERNOS_SESSION': self.auth.auth_token
        })
        return response.json()['status']
    
    def start(self):
        response = requests.get('https://aternos.org/ajax/start/', cookies={
            'ATERNOS_SESSION': self.auth.auth_token
        })
        if response.status_code == 200 and response.json()['success']:
            self.server_id = response.json()['id']
        else:
            raise Exception('Failed to start server')
            
class Files:
    def __init__(self, auth: Auth, server: Server):
        self.auth = auth
        self.server = server
        
    def path(self, path):
        response = requests.get('https://aternos.org/ajax/console/', params={
            'id': self.server.server_id,
            'command': 'cd {}'.format(path)
        }, cookies={
            'ATERNOS_SESSION': self.auth.auth_token
        })
        return response.json()
    
    def console(self, command):
        response = requests.get('https://aternos.org/ajax/console/', params={
            'id': self.server.server_id,
            'command': command
        }, cookies={
            'ATERNOS_SESSION': self.auth.auth_token
        })
        return response.json()
    
    def start(self):
        response = requests.get('https://aternos.org/ajax/start/', cookies={
            'ATERNOS_SESSION': self.auth.auth_token
        })
        if response.status_code == 200 and response.json()['success']:
            self.server.server_id = response.json()['id']
        else:
            raise Exception('Failed to start server')
