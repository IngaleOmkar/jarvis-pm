import library.api

def login(username, password):
    if username and password:
        session = library.api.login(username, password)
        if session == False:
            # show a popup saying invalid username/password and render login again
            return {'error': 'Invalid username or password'}
        elif isinstance(session, library.api.usersession):
            return {'session': session}
        else:
            return {'error': 'Unknown error'}
    elif not username or not password:
        return {'error': 'Username or password not provided'}
    else:
        return {'error': 'Unknown error'}

def register(username, password):
    if username and password:
        session = library.api.createNewAccount(username, password)
        if session == False:
            return {'error': 'Username already exists'}
        elif isinstance(session, library.api.usersession):
            return {'session': session}
        else:
            return {'error': 'Unknown error'}
    elif not username or not password:
        return {'error': 'Username or password not provided'}
    else:
        return {'error': 'Unknown error'}