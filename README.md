## Habrhabr proxy 

Tested for python 3.5, linux ubuntu.

Run tests:
```sh
python3 -m unittest discover
```

Start with virtualenv:
```sh
# activate virtualenv and run:
pip3 install -r requirements.txt 
gunicorn -w 4 -b 0.0.0.0:8080 server:app
```
or
```sh
./startup_venv.sh
```

Start with docker container:
```sh
sudo docker build -t habr-proxy .
sudo docker run --name habr-proxy -p 8080:8080 -it habr-proxy:latest
```
or
```
./startup_docker.sh
```

Start, stop container:
```sh
sudo docker start habr-proxy
sudo docker stop habr-proxy
```

### Check it out on http://localhost:8080

For example:

http://localhost:8080/company/yandex/blog/258673/

http://localhost:8080/users/Milfgard/
