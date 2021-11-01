import requests
import threading
import time
from random import randint, choice

from .random_dict import dict_creator

local_ip ="::1"
service_domain = "http://localhost/api/"
rate_limit_bucket_time=61


def test_post_single_request_without_body():
    response = requests.post(service_domain,)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == {"ip": local_ip}


def test_post_single_request():

    simple_body = {
        "name": "test_post_single_request",
        "age": 22,
        "number": 18.5,
        "frends": ["ali", "peyman"],
        "job": {"MP": "backend",
                "FL": "python.."}
    }
    expected_body = {**simple_body, **{"ip": local_ip}}

    response = requests.post(service_domain, json=simple_body)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == expected_body


def test_post_bad_data():
    bad_data = """`1234567890-=/*-.qwertyuiop[]\\ \t \n \r 
    asdfghjkl;'zxcvbnm,./~!@#$%^&*()_+QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?
    !٬٫﷼٪×،*)(ـ+۱۲۳۴۵۶۷۸۹۰-=ضصثقفغ غعهخحجچ\شسیبلاتنمکگظطزرذدپو./ًٌٍَُِّْ][}{|ؤئيإأآة»«:؛كٓژٰ‌ٔء><؟}])
    """

    simple_body = {"bad_data": bad_data}
    expected_body = {**simple_body, **{"ip": local_ip}}
    response = requests.post(service_domain, json=simple_body)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == expected_body


def test_post_long_body():
    simple_body = {"long_valid_data": (104000 * "1234567890")}
    expected_body = {**simple_body, **{"ip": local_ip}}
    response = requests.post(service_domain, json=simple_body)

    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert response.json() == expected_body

    simple_body = {"long_unvalid_data": (105000 * "1234567890")}
    response = requests.post(service_domain, json=simple_body)

    assert response.status_code == 413


def test_post_synchronicity_random_body_request():
    
    time.sleep(rate_limit_bucket_time)
    tread_number = 100
    run_treads = 2


    def send_request(courent_run_treads):
        frends=[["ali", "peyman", "saman", "ali","farhad"],
                ["sajad", "mohammad","sara"],
                ["sahar", "peyman"]]
        jobs=[
                {"freelance":"backend"},
                {"home":"frontend"},
                {"freelance":"frontend"},
                {"office":"backend"},
                {"office":"mobile"},
                {"office":"frontend"},
                ] 

        
        names = [
                "saman", "ali", "mohammad", "sara", "farhad",
                "somaye", "zeynab", "faeze", "sina", "mohammadali",
                "amir", "amirali", "amirreza", "jac", "omid", "peyman", 
                "pejman", "poria", "sahar", "shr","nastaran", "pari",
                ]
        
        simple_body = {
            "name": choice(names),
            "age": randint(1,50),
            "number": randint(1,40)/2,
            "frends": choice(frends),
            "job": choice(jobs)
        }

        expected_body = {**simple_body, **{"ip": local_ip}}
        response = requests.post(service_domain, json=simple_body)

        if courent_run_treads == 0:
            assert response.status_code == 200
            assert response.headers["Content-Type"] == "application/json"
            assert response.json() == expected_body
        else:
            assert response.status_code == 429
    
    for courent_run_treads in range(run_treads):
        threads = []

        for _ in range(tread_number):
            tr = threading.Thread(target=send_request, args=[courent_run_treads])
            threads.append(tr)
            tr.start()

        for _, thread in enumerate(threads):
            thread.join()


def test_post_synchronicity_random_deep_body_request():

    time.sleep(rate_limit_bucket_time)

    def send_request():
        simple_body = dict_creator()

        expected_body = {**simple_body, **{"ip": local_ip}}
        response = requests.post(service_domain, json=simple_body)

        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/json"
        assert response.json() == expected_body

    tread_number = 100
    run_treads = 1

    for _ in range(run_treads):
        threads = []

        for _ in range(tread_number):
            tr = threading.Thread(target=send_request)
            threads.append(tr)
            tr.start()

        for _, thread in enumerate(threads):
            thread.join()


