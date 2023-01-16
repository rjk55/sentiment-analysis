from locust import HttpLocust, TaskSet, task, HttpUser, between

class LoadTest(HttpUser):
    wait_time = between(1, 2)
    
    def on_start(self):
        response = self.client.get("/")
        # print(response.cookies)
        # csrftoken = response.cookies['csrftoken']
        # print(csrftoken)

    @task(5)
    def review(self):
        self.client.post("/", 
            {"url":"http://localhost:8080/currys"},
            headers={"accept": "application/json", "Content-Type": "application/json"}
            )