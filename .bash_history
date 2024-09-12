sudo apt update
sudo apt upgrade -y
sudo apt install samba samba-common-bin -y
sudo nano /etc/samba/smb.conf
sudo smbpasswd -a pi
sudo /etc/init.d/smbd restart
sudo raspi-config
