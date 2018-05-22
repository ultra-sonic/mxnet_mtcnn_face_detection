#!/bin/bash
find /data_100G/Linus_Timelapse/processed -name "*.jpg" -mtime +10 -exec rm -rf {} \;
