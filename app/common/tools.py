from app import User

def get_msg(methods_name, params):
    try:
        msg = by[methods_name](*params)
    except KeyError:
        msg = by['other'](methods_name)

    return msg


def save_user_info():
    User().push(from_wxid, res['account'], res['remark'])
