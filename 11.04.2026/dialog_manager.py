class DialogState:
    START = "start"
    WAIT_CITY = "wait_city"

user_states = {}

def get_state(user_id):
    if user_id in user_states:
        return user_states[user_id]
    return DialogState.START

def set_state(user_id, state):
    user_states[user_id] = state