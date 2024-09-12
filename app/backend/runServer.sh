# Script to activate venv and run server
python3 -m venv venv
source venv/bin/activate
# wait for venv to activate
sleep 1
uvicorn main:app --reload