import time
import os


os.system ("sudo docker compose -f /Workshop/challenge_1/database/postgres-compose.yaml down")

time.sleep(5)

os.system ("sudo docker compose -f /Workshop/challenge_1/database/postgres-compose.yaml up -d")