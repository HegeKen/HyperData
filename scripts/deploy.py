import os
import config
import time

os.system(f"curl -X POST \"{config.deploy_url}\"")