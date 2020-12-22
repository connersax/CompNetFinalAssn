#!/bin/bash

infa=$(iw dev | awk '$1=="Interface"{print $2}')
sudo airmon-ng check kill
sudo airmon-ng start $infa

exit 0
