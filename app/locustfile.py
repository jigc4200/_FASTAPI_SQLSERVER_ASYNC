from locust import HttpUser, task, between
import random

class FastAPIUser(HttpUser):
    host = "http://127.0.0.1:8000"  # Especifica la URL base de tu servidor FastAPI
    wait_time = between(1, 2.5)  # Tiempo de espera entre tareas

    @task
    def get_consolidated_data(self):
        user_id = random.randint(1000, 10000)  # Genera un user_id aleatorio entre 1000 y 10000
        self.client.get(f"/consolidated-data/{user_id}")

   