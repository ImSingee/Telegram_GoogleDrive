def is_authenticated(user_id):
    # 未授权：返回 False
    # 已授权：返回 credentials
    return False


def save_credential(user_id, credential):
    print(credential)
