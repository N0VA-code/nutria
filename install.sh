#!/bin/bash -e

echo "* * * * * * * * * * * * * * * * * * * * * *"
echo "  osp_team_project installer"
echo "  "

if [ $(which apt-get) ]; then
    echo "[+] installing dependences"
    sudo apt-get -y install python python3-pip default-jre
else
    echo "[!] you'll need to install ubuntu or dependences by yourself"
fi

pip install --upgrade pip
pip install --upgrade -r requirements.txt

if [[ "$(uname)" == "Linux" ]]; then
    wget "https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.12.1-linux-x86_64.tar.gz"
    tar xvzf "elasticsearch-7.12.1-linux-x86_64.tar.gz"
else
    echo "[!] you'll need to install linux or get a elasticsearch yourself"
fi

echo "[+] all dependences are installed"

echo " "
echo "* * * * * * * * * * * * * * * * * * * * * *"
echo "  Thanks for installing our program"
echo "  7-team @ OSP class"

read -p "[-] do you want to run the program now? (y/n) : " input
if [[ "$input" = "y" || "$input" = "Y" ]]; then
    echo "[+] Running the program now"
    # service script here
    ./run_app.sh
fi
