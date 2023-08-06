# login.py


from dhuolib.utils.persistence import Persistence
from dhuolib.auth.openid import OpenId


def do_login(username, password) -> None:
    """Authenticates at DHuO Data"""

    openId = OpenId(username, password)
    
    if not openId.is_authenticated():
        raise Exception("Invalid username or password")
    
    persistence = Persistence();
    persistence.save_username(username)
    persistence.save_password(password)
    persistence.save_workspace(openId.get_workspace())

    # click.echo(f"Workspace padrão: {openId.get_workspace()}")
