#!/bin/bash
echo "Installing & linking optilibre service"
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
ln -s "$SCRIPT_DIR/systemd/opti_libre.service" /etc/systemd/system/
ln -s "$SCRIPT_DIR/systemd/opti_libre.timer" /etc/systemd/system/
cd "$SCRIPT_DIR" || exit
python3 -m venv venv
source venv/bin/activate
pip install -r "$SCRIPT_DIR/requirements.txt"
echo "optilibre installed."
echo "To enable the service, enter:"
echo "systemctl enable --now opti_libre"
