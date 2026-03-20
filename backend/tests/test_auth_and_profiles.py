def get_auth_header(client, phone: str = "01000000000", role: str = "patient") -> dict[str, str]:
    send_resp = client.post("/v1/auth/send-otp", json={"phone": phone})
    assert send_resp.status_code == 200

    verify_resp = client.post(
        "/v1/auth/verify-otp",
        json={
            "phone": phone,
            "otp_code": "123456",
            "full_name": "Test User",
            "role": role,
        },
    )
    assert verify_resp.status_code == 200
    token = verify_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_auth_me(client):
    headers = get_auth_header(client)
    me_resp = client.get("/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["phone"] == "01000000000"


def test_create_profile_authenticated_patient(client):
    headers = get_auth_header(client, phone="01000000001")

    create_resp = client.post(
        "/v1/profiles",
        headers=headers,
        json={
            "full_name": "Patient Child",
            "relation": "child",
            "chronic_conditions": ["asthma"],
        },
    )
    assert create_resp.status_code == 200

    list_resp = client.get("/v1/profiles", headers=headers)
    assert list_resp.status_code == 200
    profiles = list_resp.json()
    assert len(profiles) >= 1
    assert profiles[0]["relation"] in {"self", "father", "mother", "child", "other"}
