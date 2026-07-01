#!/bin/bash
cd /home/yaoteam/yaoteam/yyc/mmdet_dino || exit
umask 002

/home/yaoteam/anaconda3/envs/mmdet_dino/bin/python \
	    /home/yaoteam/yaoteam/yyc/mmdet_dino/cebaodeng_server.py \
	        2>&1 | tee -a /home/yaoteam/yaoteam/yyc/mmdet_dino/cebaodeng_server.log

