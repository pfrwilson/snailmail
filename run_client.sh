if [ -d ./venv ]; then
python -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
else
source venv/bin/activate
fi 
export PYTHONPATH=$(pwd)
python client/clientmain.py