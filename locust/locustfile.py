from locust import HttpUser, task


class QuickstartUser(HttpUser):
    host = '127.0.0.1:8000'

    def on_start(self):

        response = self.client.post('/api/v1/login/', data={
            "email": "mohamadimahdieh70@gmail.com",
            "password": "1234!@#$"
        }).json()
        self.client.headers = {
            'Authorization':f"Basic {response.get('toke',None)}"
        }

    @task
    def todo_list(self):
        self.client.get("/Todo/api/v1/Todo/")


