# !/bin/bash
# This script automatically install deb packages, python packages, prepare system, install ndasrt app and run it
function print_green {
    echo -e "\e[32m$1\e[0m"
}
print_green "Welcome to NDAS-RT installer!"
print_green "Downloading ndas_rt"
if git clone https://github.com/r-sensors/ndas_rt.git; then
    echo "The repository has been uploaded successfully"
else
    echo "Cannot download repo!"
    exit 1
fi
print_green "Starting installation of debian packages"
dpkg -i --skip-same-version deb_packages/*.deb ;
print_green "Starting installation of python packages"
python3 -m pip install --system python37_packages/* ;
print_green "Preparing system"
bash system_files/prepare.sh;
print_green "Starting eeprom writer"
sudo -u debian python3 utils/eeprom/write_v2.py;
print_green "Starting installation of NDAS-RT software"
bash scripts/install_software.sh ;
print_green "Starting installation and running of NDAS-RT service"
bash services/install_services.sh enable;
