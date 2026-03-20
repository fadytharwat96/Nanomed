def get_auth_header(client, phone: str, role: str) -> dict[str, str]:
    send_resp = client.post("/v1/auth/send-otp", json={"phone": phone})
    assert send_resp.status_code == 200

    verify_resp = client.post(
        "/v1/auth/verify-otp",
        json={
            "phone": phone,
            "otp_code": "123456",
            "full_name": "Lifecycle User",
            "role": role,
        },
    )
    assert verify_resp.status_code == 200
    token = verify_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_nurse_request_lifecycle(client):
    patient_headers = get_auth_header(client, phone="01000000009", role="patient")

    profile_resp = client.post(
        "/v1/profiles",
        headers=patient_headers,
        json={"full_name": "Case Owner", "relation": "self", "chronic_conditions": []},
    )
    assert profile_resp.status_code == 200
    profile_id = profile_resp.json()["id"]

    request_resp = client.post(
        "/v1/requests",
        headers=patient_headers,
        json={
            "profile_id": profile_id,
            "service_type": "blood_draw",
            "address_text": "Cairo",
            "lat": 30.0400,
            "lng": 31.2300,
            "notes": "urgent",
        },
    )
    assert request_resp.status_code == 200
    payload = request_resp.json()
    assert payload["status"] == "assigned"
    request_id = payload["id"]

    nurse_headers = get_auth_header(client, phone="01111111111", role="nurse")

    arrive_resp = client.post(f"/v1/nurse/requests/{request_id}/arrive", headers=nurse_headers)
    assert arrive_resp.status_code == 200
    assert arrive_resp.json()["status"] == "arrived"

    start_resp = client.post(f"/v1/nurse/requests/{request_id}/start", headers=nurse_headers)
    assert start_resp.status_code == 200
    assert start_resp.json()["status"] == "in_progress"

    complete_resp = client.post(f"/v1/nurse/requests/{request_id}/complete", headers=nurse_headers)
    assert complete_resp.status_code == 200
    assert complete_resp.json()["status"] == "completed"
