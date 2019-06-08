# setup.sh
echo "Making virtual environment for python, make sure you have some form of python3-venv installed and then click enter"
read temp1
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
echo "Make sure you have postgresql installed"
echo "'brew install postgresql' on MacOS"
echo "the package is libpq-dev on linux, click enter when done"
read temp2
pip install -r requirements.txt
