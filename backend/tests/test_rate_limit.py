from app.middleware.rate_limit import is_allowed


def test_rate_limit_blocks_after_limit() -> None:
	user_id = "rate-limit-user"

	for _ in range(20):
		assert is_allowed(user_id, limit=20, window_seconds=60)

	assert is_allowed(user_id, limit=20, window_seconds=60) is False