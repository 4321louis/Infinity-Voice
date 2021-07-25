from datetime import datetime

# prints argument and current date and time
def timestamp(s: str) -> None:
    print("[" + str(datetime.now()) + "]" + s)


