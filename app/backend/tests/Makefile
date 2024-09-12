# run_unit_tests:
# 	pytest -m "not integration_test and not end2end_test"

run_unit_tests:
	python delete_db.py
	pytest -m "not integration_test and not end2end_test" -vv

run_integration_tests:
	python delete_db.py 
	python populate_test_db.py
	pytest -m "integration_test" -vv

# before running end2end tests, you need to set the environment variable ENVIRONMENT=test
# and run the server in a separate terminal
w_run_end2end_tests:
	pytest -m end2end_test -vv & \
	taskkill /F /IM uvicorn.exe && \
	python delete_db.py end2end 

l_run_end2end_tests:
	pytest -m end2end_test -vv ; pkill uvicorn && python delete_db.py end2end