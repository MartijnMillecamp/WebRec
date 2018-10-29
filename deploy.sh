#!/bin/bash
docker rm imagerun
docker build -t imagebuild .
docker run -d -p 4000:80 imagebuild
