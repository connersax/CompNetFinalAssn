#!/bin/bash

infa=$(iw dev | awk '$1=="Interface"{print $2}')
sudo airmon-ng stop $infa
sudo NetworkManager

exit 0