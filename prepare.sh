#!/usr/bin/env bash

echo "# demo" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin git@github.com:ichux/demo.git
git push -u origin master