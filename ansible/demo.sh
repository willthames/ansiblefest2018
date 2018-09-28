#!/usr/bin/env ash

set -eu

if [ $# -lt 1 ] ; then
  echo "$0 line-number"
  exit
fi

line=$(sed "$1!d" demo.txt)
echo $line
