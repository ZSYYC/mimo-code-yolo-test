#! /bin/bash
sudo systemctl stop bbfs_hfs_jiance
sleep 1
sudo systemctl stop ce_bao_deng_jiance
sleep 1
sudo systemctl stop xiao_chong_ti_jiance
sleep 1
sudo systemctl start bbfs_hfs_jiance
sleep 2
sudo systemctl start ce_bao_deng_jiance
sleep 2
sudo systemctl start xiao_chong_ti_jiance
# sudo systemctl restart 
# sudo systemctl start ce_bao_deng_xiaochong