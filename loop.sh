#!/bin/sh

BASEDIR=$(dirname "$0")
until python "$BASEDIR/main.py"
do
	sleep 1
done
