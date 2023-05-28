import jwt
    
SECRET_WORD = "calculator"


def vaildate(cur, **kwargs):
    params = kwargs['params']
    if not (params.get('username') or params.get('token')):
        return "Username and token shouldn't be empty", 0
    user_id = cur.execute("SELECT id FROM users WHERE username = (?)", (params['username'],)).fetchone()
    if user_id is None:
        return "User doesn't exists", 0

    user_id = user_id[0]
    saved_jqt_token = cur.execute("SELECT session_token FROM session WHERE user_id = (?)", (user_id,)).fetchone()

    if saved_jqt_token:
        saved_jqt_token = saved_jqt_token[0]
        try:
            decoded_token = jwt.decode(saved_jqt_token, SECRET_WORD, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return "Token expired", 0
        except:
            return "Internal error", 0

    if int(decoded_token["user_id"]) != user_id:
        # Token was stolen, delete token from db
        cur.execute("DELETE FROM session WHERE user_id = (?)", (int(decoded_token["user_id"]),))
        return "Stolen token", 0

    return "", user_id