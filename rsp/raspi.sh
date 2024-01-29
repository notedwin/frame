#!/bin/bash

# No need to setup WIFI using script, use rpi imager!
# On a RPI 4 use https://www.raspberrypi.com/tutorials/how-to-use-a-raspberry-pi-in-kiosk-mode/

KIOSK_URL = "http://notedwin.com/"

sudo apt-get install --no-install-recommends unclutter -y

cat <<EOF >> ~/kiosk.sh
#!/bin/sh
xset -dpms     # disable DPMS (Energy Star) features.
xset s off     # disable screen saver
xset s noblank # don't blank the video device
chromium-browser --app="https://192.168.0.122:5000" --kiosk  --user-data-dir=/home/notedwin/chrome --noerrdialogs --disable-session-crashed-bubble --disable-infobars --check-for-update-interval=604800 --disable-pinch --autoplay-policy=no-user-gesture-required --disable-web-security --disable-popup-blocking --no-margins --enable-features=OverlayScrollbar
EOF

chmod +x ~/kiosk.sh
sudo su -
cat <<EOF >> /etc/xdg/lxsession/LXDE-pi/autostart
# @lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi

@/home/notedwin/kiosk.sh
EOF


sudo apt install git tmux vim -y

rm -rf LCD-show
git clone https://github.com/goodtft/LCD-show.git
chmod -R 755 LCD-show
cd LCD-show/
sudo ./LCD35-show 90


# resources:
# https://desertbot.io/blog/raspberry-pi-touchscreen-kiosk-setup



