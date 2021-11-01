import requests

service_domain = "http://localhost:8000"
rate_limit_ip = 20


def test_ip_day_limit():
    for ip in range(1, 41):
        response = requests.post(service_domain, json={"username": "test"}, headers={
                                 "X-Forwarded-For": f"127.0.1.{ip}"})

        if ip <= rate_limit_ip:
            assert response.status_code == 200
            assert response.headers["Content-Type"] == "application/json"
        else:
            assert response.status_code == 429
