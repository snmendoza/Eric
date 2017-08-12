Eric
====

Eric: Room Integrated Controller

Requirements
------------

* Kivy 1.10.0. [See installation instructions](https://kivy.org/docs/installation/installation.html).
* Pip packages listed on requirements.txt
* ALSA development headers

Configuration
-------------

This app needs a `config.json` file. Use `config.json.example` for reference.
Up to 6 lights are supported.

Installation on Raspberry Pi
----------------------------

These instructions are for installing Eric on a Raspberry Pi.
The chosen OS is Raspbian Jessie Lite.
Official touch display will be assumed as the input device.

* Download and install Raspbian Jessie Lite. [Download page and instructions](https://www.raspberrypi.org/downloads/raspbian/).
* (Optional) Change keyboard layout.
```
$ sudo dpkg-reconfigure keyboard-configuration
```
* (Optional) [Set up WiFi](https://www.raspberrypi.org/documentation/configuration/wireless/wireless-cli.md).
* (Optional) [Use a static IP address](https://www.modmypi.com/blog/how-to-give-your-raspberry-pi-a-static-ip-address-update).
* (Optional) [Enable SSH](https://www.raspberrypi.org/documentation/remote-access/ssh/).
* Update package index and install dependencies.
```
$ sudo apt-get update; sudo apt-get install git python-setuptools python-pip
```
* Clone app repo.
```
$ git clone https://github.com/stupidusername/Eric.git ~/eric
```
* Install Kivy >= 1.10. [Instructions for Raspberry Pi](https://kivy.org/docs/installation/installation-rpi.html).
* Install app requirements.
```
$ sudo pip install -r ~/eric/requirements.txt
```
* Configure Kivy to use the touch display as user input. [See installation guide of Kivy](https://kivy.org/docs/installation/installation-rpi.html#using-official-rpi-touch-display).
* Configure app by editing ~/eric/config.json. When running the app on a Raspberry Pi the property "audio_mixer" should take the value "PCM".
```
$ cp ~/eric/config.json.example ~/eric/config.json
$ nano config.json
```
