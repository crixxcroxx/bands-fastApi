run:
	uvicorn main:app --reload

migrate:
	alembic upgrade head