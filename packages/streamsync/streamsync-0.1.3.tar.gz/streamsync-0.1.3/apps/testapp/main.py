import streamsync as ss
from streamsync import session_verifier

print("Hello world! You'll see this message in the log")
print("If you edit the file somewhere else, for example, in VS Code, the code will reload automatically. Including dependencies!")

ss.init_state({
    "message": "Hello",
    "counter": 19,
    "_private": "I like white bread",
    "private": "I still like bologna on white bread now and then",
    "collapsible": "yes",
    "product": 22
})


@session_verifier
def check_session(cookies, headers):
    print("CHECKING SESSION GLGLGLGL")
    # return True # Allow session
    return True  # Deny session


def toggle_collapsible(state):
    if state["collapsible"] == "yes":
        state["collapsible"] = "no"
    else:
        state["collapsible"] = "yes"


def increment(state, session):
    state["counter"] += 1
    print("you got to increment")
    print(repr(session))


def slow_op(payload):
    import time
    time.sleep(5)
    print("It's been five seconds")
    print(repr(payload))


def change_route_vars(state):
    state.set_route_vars({
        "product_id": 35,
        "country": None
    })


def handle_hash_change(state, payload):
    route_vars = payload.get("route_vars")
    if not route_vars:
        return
    state["product"] = route_vars.get("product_id")


def handle_click_a(state):
    from datetime import datetime

    now = datetime.now()
    print(now.hour)
    if now.hour >= 10:
        state.set_page("pink")
    else:
        state.set_page("blue")
