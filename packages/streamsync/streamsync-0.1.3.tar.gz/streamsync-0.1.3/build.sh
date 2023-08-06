#!/bin/bash

set -e

cd ./tests
pytest
cd ..

cd ./ui
npm run build
cd ..


rm -rf ./src/streamsync/app_templates/*

cp -r ./apps/default ./src/streamsync/app_templates
cp -r ./apps/hello ./src/streamsync/app_templates

rm -f ./dist/*

python -m build