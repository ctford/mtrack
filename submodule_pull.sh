#!/bin/sh
cd mtrack_project
for dir in `find . -maxdepth 1 -type d`
do
  echo $dir
  (cd $dir && git pull)
done

