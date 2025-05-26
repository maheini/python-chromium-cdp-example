# Python Chromium Chrome DevTools Protocol example

Take screenshots, visit websites, execute JS and more with this basic python script, demonstrating CDP with websocket access.

Please note: This repo is intended for Linux x64 only.

In order to install the required Chromium binaries, you can simply run install.py . You need to install all required apt-packages manually in order to get the binaries working.

### Apt requirements

In order to get chromium running, you'll need various apt packages installed on your system (Debian in this case):
```
sudo apt-get update && sudo apt-get install -y ca-certificates fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libc6 libcairo2 libcups2 libcurl4 libdbus-1-3 libexpat1 libgbm1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libudev1 libvulkan1 libx11-6 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 wget xdg-utils
```