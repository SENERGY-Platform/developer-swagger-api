#!/bin/bash
FLASK_APP=./server.py flask db init &
FLASK_APP=./server.py flask db migrate &
FLASK_APP=./server.py flask db upgrade &

