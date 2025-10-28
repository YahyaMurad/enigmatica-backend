from fastapi import Depends

# temporary stand-in for authentication
def get_current_user_id() -> int:
    # later, decode JWT and return user.id
    return 1  # mock user for now
