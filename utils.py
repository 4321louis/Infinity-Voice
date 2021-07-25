from datetime import datetime

# prints argument and current date and time
def print_timed(s: str) -> None:
    print("[" + str(datetime.now()) + "]" + s)


