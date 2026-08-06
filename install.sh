# !/bin/bash
cd "$(dirname "$0")"
echo "Welcome to NDAS-RT installer!"

options=(
            "Install debian packages"
            "Install python packages"
            "Prepare system"
            "Install NDAS-RT software"
            "Install and run NDAS-RT service"
            "Stop and uninstall NDAS-RT service"
            "Quit"
    )

select opt in "${options[@]}"; do
    case $opt in
        "Install debian packages")
            dpkg -i --skip-same-version deb_packages/*.deb ;;
         "Install python packages")
            python3 -m pip install --system python37_packages/* ;;
        "Prepare system")
            bash system_files/prepare.sh ;;
        "Install NDAS-RT software")
            bash scripts/install_software.sh ;;
        "Install and run NDAS-RT service")
            bash services/install_services.sh enable;;
        "Stop and uninstall NDAS-RT service")
            bash services/install_services.sh disable;;
        "Quit")
            exit ;;
        *) echo "invalid option $REPLY" ;;
    esac
done
