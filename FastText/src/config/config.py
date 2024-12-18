import os
from dotenv import load_dotenv

load_dotenv()

HF_HOME = os.getenv('HF_HOME')
if not HF_HOME:
    raise EnvironmentError("HF_HOME not set")