# deploy process on server
deploy() {
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    touch .hushlogin
    sudo apt-get update
    sudo apt install zsh neovim -y
    sudo raspi-config nonint do_spi 0
    sudo raspi-config nonint do_i2c 0
    grep -q "^dtoverlay=spi0-0cs" /boot/firmware/config.txt || echo "dtoverlay=spi0-0cs" | sudo tee -a /boot/firmware/config.txt
    # for beszel
    grep -q "^cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1" /boot/firmware/cmdline.txt || echo "cgroup_enable=cpuset cgroup_enable=memory cgroup_memory=1" | sudo tee -a /boot/firmware/cmdline.txt
    sudo reboot
}

docker build -t gitea.notedwin.com/notedwin/frame:0.0.1 . --platform=linux/arm64
docker push gitea.notedwin.com/notedwin/frame:0.0.1
ssh notedwin@192.168.0.81 "sudo docker ps -aq --filter "name=inky_frame" | xargs -r sudo docker rm -f"
ssh notedwin@192.168.0.81 "sudo docker run -d --name inky_frame --privileged --restart unless-stopped --pull always -v /home/notedwin/images:/app/images gitea.notedwin.com/notedwin/frame:0.0.1"