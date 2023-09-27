import logging

import asyncio

import main

def load_env(filename="settings.env"):
    import os
    with open(filename) as f:
        env = [s.split("=") for s in f.readlines()]
    for key, value in env:
        os.environ[key.strip()] = value.strip()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    load_env()
    asyncio.run(main.run_bot())


