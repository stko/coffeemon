
##### To install CoffeeMon, get a virgin raspian lite image from raspberry.org
# tested on raspian stretch
#  boot it, start the install script with
#    bash <(curl -s http://mywebsite.com:8080/install.sh)
# and spent some hours with your friends or family. When you are back,
# the installation should be done

echo "The CoffeeMon Installer starts"
cd

sudo apt-get update --assume-yes
sudo apt-get install --assume-yes \
joe \
nano \
python3-pip \
usbmount \
lighttpd php-common php-cgi php

## begin unisonfs overlay file system (http://blog.pi3g.com/2014/04/make-raspbian-system-read-only/)

### Do we need to disable swap?? actual not..

# dphys-swapfile swapoff
# dphys-swapfile uninstall
# update-rc.d dphys-swapfile disable

sudo apt-get  --assume-yes install unionfs-fuse


# Create mount script

cat << 'EOF' | sudo tee /usr/local/bin/mount_unionfs
#!/bin/sh
DIR=$1
ROOT_MOUNT=$(awk '$2=="/" {print substr($4,1,2)}' < /etc/fstab)
if [ $ROOT_MOUNT = "rw" ]
then
	/bin/mount --bind ${DIR}_org ${DIR}
else
	/bin/mount -t tmpfs ramdisk ${DIR}_rw
	/usr/bin/unionfs-fuse -o cow,allow_other,suid,dev,nonempty ${DIR}_rw=RW:${DIR}_org=RO ${DIR}
fi
EOF

# make it executable:

sudo chmod +x /usr/local/bin/mount_unionfs
 ## see the directory renaming at the end of this installation script

## end unisonfs overlay file system

# set webbrowser rights
sudo groupadd www-data
sudo usermod -G www-data -a pi
sudo chown -R www-data:www-data /var/www/html
sudo chmod -R 775 /var/www/html

# add php to lighttpd
sudo lighty-enable-mod fastcgi
sudo lighty-enable-mod fastcgi-php
sudo service lighttpd force-reload


# Read-Only Image instructions thankfully copied from https://kofler.info/raspbian-lite-fuer-den-read-only-betrieb/

# remove packs which do need writable partitions
sudo apt-get remove --purge --assume-yes cron logrotate triggerhappy dphys-swapfile fake-hwclock samba-common
sudo apt-get autoremove --purge --assume-yes


wget  https://github.com/stko/coffeemon/archive/master.zip -O coffeemon.zip && unzip coffeemon.zip
mv coffeemon-master coffeemon
sudo cp -r coffeemon/www/* /var/www/html
sudo mkdir /etc/coffeemon
sudo cp coffeemon/scripts/cmsettings_sample.cfg /etc/coffeemon/settings.ini

wget  https://github.com/tatobari/hx711py/archive/master.zip -O hx711py.zip && unzip hx711py.zip
cp hx711py-master/hx711.py coffeemon/scripts

chmod a+x /home/pi/coffeemon/scripts/*.sh


# automatically connect to a CoffeeMon hotspot, if around
#wpa_passphrase "CoffeeMon" "oobdoobd" | sudo tee -a /etc/wpa_supplicant/wpa_supplicant.conf > /dev/null


# start to make the system readonly
#sudo rm -rf /var/lib/dhcp/ /var/spool /var/lock
#sudo ln -s /tmp /var/lib/dhcp
#sudo ln -s /tmp /var/spool
#sudo ln -s /tmp /var/lock
#if [ -f /etc/resolv.conf ]; then
#	sudo mv /etc/resolv.conf /tmp/resolv.conf
#fi
#sudo ln -s /tmp/resolv.conf /etc/resolv.conf

# add the temporary directories to the mountlist
cat << 'MOUNT' | sudo tee /etc/fstab
proc            /proc           proc    defaults          0       0
/dev/mmcblk0p1  /boot           vfat    ro,defaults          0       2
/dev/mmcblk0p2  /               ext4    ro,defaults,noatime  0       1
# a swapfile is not a swap partition, no line here
#   use  dphys-swapfile swap[on|off]  for that
##tmpfs	/var/log	tmpfs	nodev,nosuid	0	0
##tmpfs	/var/tmp	tmpfs	nodev,nosuid	0	0
tmpfs	/tmp	tmpfs	nodev,nosuid	0	0
#/dev/sda1       /media/usb0     vfat    ro,defaults,nofail,x-systemd.device-timeout=1   0       0


mount_unionfs   /etc            fuse    defaults          0       0
mount_unionfs   /var            fuse    defaults          0       0


MOUNT

#add boot options
echo -n " fastboot noswap" | sudo tee --append /boot/cmdline



# setting up the systemd services
# very helpful source : http://patrakov.blogspot.de/2011/01/writing-systemd-service-files.html

cat << 'EOF' | sudo tee  /etc/systemd/system/cmannounce.service
[Unit]
Description=Triggers announces device on redirect server, if settings file exists
ConditionFileNotEmpty=/etc/coffeemon/settings.ini
Wants=network.target

[Service]
ExecStart=/home/pi/coffeemon/scripts/announceDevice.sh /etc/coffeemon/settings.ini
Restart=on-failure

[Install]
WantedBy=default.target
EOF


cat << 'EOF' | sudo tee  /etc/systemd/system/coffeemon.service
[Unit]
Description=CoffeeMon Main Server
Wants=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/coffeemon/scripts/coffeemon.py --host 0.0.0.0 --config /etc/coffeemon/settings.ini
Restart=always

[Install]
WantedBy=default.target

EOF


sudo systemctl enable cmannounce 
sudo systemctl enable coffeemon

echo "Your actual config"
sudo nano /etc/coffeemon/settings.ini



#Prepare unisonfs  directories
sudo cp -al /etc /etc_org
sudo mv /var /var_org
sudo mkdir /etc_rw
sudo mkdir /var /var_rw


#PS3='Please take your choice: '
#options=("show config" "edit config" "Quit")
#select opt in "${options[@]}"
#	do
#		case $opt in
#			"show config")
#				more /etc/coffeemon/settings.ini
#
#			;;
#			"edit config")
#				sudo nano /etc/coffeemon/settings.ini
#
#			;;
#			"Quit")
#				break
#			;;
#			*) echo invalid option;;
#		esac
#	done

cat << 'EOF'
Installation finished

SSH is enabled and the default password for the 'pi' user has not been changed.
This is a security risk - please login as the 'pi' user and type 'passwd' to set a new password."

Also this is the best chance now if you want to do some own modifications,
as with the next reboot the image will be write protected

if done, end this session with
 
     sudo halt

and your CoffeeMon all-in-one is ready to use

have fun :-)

the CoffeeMon team
EOF

sync
sync
sync

