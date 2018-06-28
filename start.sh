#!/bin/sh
export FLASK_APP=reggie/
pip install -e .
python app.py
