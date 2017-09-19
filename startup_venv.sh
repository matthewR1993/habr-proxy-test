#!/bin/bash
source ENV/bin/activate
gunicorn -w 4 -b 0.0.0.0:8080 server:app
