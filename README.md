`sudo add-apt-repository ppa:deadsnakes/ppa`  

`sudo apt install -y virtualenv`  
`sudo apt install -y python3 python3-dev python3-pip`  
`sudo apt install -y python3-setuptools python3-wheel`  

`virtualenv -p /usr/bin/python3 .env`  
`source .env/bin/activate`  
`pip install -r requirements.txt`  
`python run.py`
