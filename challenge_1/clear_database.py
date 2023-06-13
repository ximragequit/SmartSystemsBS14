import time
os.system ("sudo docker compose -f database/postgres-compose.yaml down")

time.sleep(10)

os.system ("sudo docker compose -f database/postgres-compose.yaml up -d")
