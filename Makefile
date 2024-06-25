.DEFAULT_GOAL := default

run_api:
	uvicorn project_waste.api.fast:app --reload
