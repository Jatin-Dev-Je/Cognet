from app.core.auth.jwt import create_token, verify_token


def test_jwt_round_trip_contains_user_id() -> None:
	token = create_token("user-123")
	payload = verify_token(token)

	assert payload["user_id"] == "user-123"