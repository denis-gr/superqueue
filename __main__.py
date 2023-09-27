def load_env(filename="settings.env"):
    import os
    with open(filename) as f:
        env = [s.split() for s in f.readlines()]
    for key, value in env:
        os.environ[key] = value


if __file__ == "__main__":
    load_env()

