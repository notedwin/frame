# Inky Frame

A smol project using raspberry pi zero to use an e-ink display as a photo frame.

<div style="height: 250px; display: flex; flex-direction: row;">
    <img src="./img/2.jpeg" style="height: 250px;">
    <img src="./img/1.jpeg" style="height: 250px;">
</div>

## Hardware

- Raspberry Pi Zero 2W
- [Pimoroni Inky e-ink Display](https://shop.pimoroni.com/products/inky-impression-7-3?variant=40512683376723)
- Soldering Iron
- header pins

## Software Setup

> Requires ansible on your local machine

Flash an SD card with Raspian using [RPI imager](https://www.raspberrypi.com/software/) to take advantage of autosetup for wifi, and ssh keys.

On your local machine, run:

```bash
./deploy.sh
```

Connect to the pi and run:

```bash
# manual steps: uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# optional steps for my setup:
# install beszel agent
```

### Inspiration

[hitherdither](https://github.com/hbldh/hitherdither?tab=readme-ov-file#id4)

[frameos](https://github.com/FrameOS/frameos/)
