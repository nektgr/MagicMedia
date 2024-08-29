import grpc.experimental.gevent as grpc_gevent
import gevent
import grpc
import random
from locust import User, task, between
from proto import rpc_create_vacancy_pb2, rpc_update_vacancy_pb2, vacancy_service_pb2, rpc_signin_user_pb2
import proto.auth_service_pb2_grpc as auth_service_pb2_grpc
import proto.vacancy_service_pb2_grpc as vacancy_service_pb2_grpc
import time

grpc_gevent.init_gevent()

class VacancyGrpcUser(User):
    wait_time = between(1, 1)
    
    users = [
        {"email": "giseb50863@biowey.com", "password": "Test_1"},
        {"email": "yarkiyirtu@gufum.com", "password": "Test_2"},
        {"email": "fokkucidra@gufum.com", "password": "Test_3"},
    ]

    def on_start(self):
        self.channel = grpc.insecure_channel('vacancies.cyrextech.net:7823')
        self.auth_client = auth_service_pb2_grpc.AuthServiceStub(self.channel)
        self.vacancy_client = vacancy_service_pb2_grpc.VacancyServiceStub(self.channel)
        self.login()
        gevent.spawn(self.background_fetch_loop)

    def login(self):
        user = random.choice(self.users)
        email = user["email"]
        password = user["password"]
        credentials = rpc_signin_user_pb2.SignInUserInput(email=email, password=password)
        response = self.auth_client.SignInUser(credentials)
        self.access_token = response.access_token
        print(f"Logged in with {email}")

    @task
    def create_update_fetch_delete_vacancy(self):
        start_time = time.time()
        try:
            create_request = rpc_create_vacancy_pb2.CreateVacancyRequest(
                Title="Test Vacancy 21312",
                Description="A test vacancy",
                Division="DEVELOPMENT",
                Country="Test Country"
            )
            created_vacancy = self.vacancy_client.CreateVacancy(create_request)
            vacancy_id = created_vacancy.vacancy.Id

            update_request = rpc_update_vacancy_pb2.UpdateVacancyRequest(
                Id=vacancy_id,
                Title="Updated Test Vacancy"
            )
            self.vacancy_client.UpdateVacancy(update_request)

            fetch_request = vacancy_service_pb2.VacancyRequest(Id=vacancy_id)
            fetched_vacancy = self.vacancy_client.GetVacancy(fetch_request)

            delete_request = vacancy_service_pb2.VacancyRequest(Id=vacancy_id)
            self.vacancy_client.DeleteVacancy(delete_request)

            self.environment.events.request.fire(
                request_type="gRPC",
                name="create_update_fetch_delete_vacancy",
                response_time=(time.time() - start_time) * 1000,
                response_length=len(str(fetched_vacancy)),
            )
        except grpc.RpcError as e:
            self.environment.events.request.fire(
                request_type="gRPC",
                name="create_update_fetch_delete_vacancy",
                response_time=(time.time() - start_time) * 1000,
                response_length=0,
                exception=e,
            )
            print(f"gRPC error during task execution: {e}")
        
        gevent.sleep(30)

    def background_fetch_loop(self):
        while True:
            self.background_fetch()
            gevent.sleep(45)

    def background_fetch(self):
        start_time = time.time()
        try:
            fetch_request = vacancy_service_pb2.GetVacanciesRequest(page=1, limit=10)
            response_stream = self.vacancy_client.GetVacancies(fetch_request)

            for vacancy in response_stream:
                print(f"Vacancy ID: {vacancy.Id}")

            self.environment.events.request.fire(
                request_type="gRPC",
                name="background_fetch",
                response_time=(time.time() - start_time) * 1000,
                response_length=0,
            )
        except grpc.RpcError as e:
            self.environment.events.request.fire(
                request_type="gRPC",
                name="background_fetch",
                response_time=(time.time() - start_time) * 1000,
                response_length=0,
                exception=e,
            )
