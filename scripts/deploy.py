import os
import config

os.system(f"curl -X POST \"{config.deploy_url}\"")