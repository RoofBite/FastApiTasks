run-app:
	@docker-compose -f docker-compose-app-local.yml up --force-recreate --build
run-tests:
	@docker-compose -f docker-compose-tests-local.yml up --force-recreate --build
