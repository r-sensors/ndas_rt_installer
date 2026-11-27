cd "$(dirname "$0")"
install_dir="/var/lib/cloud9/ndas_rt"
backup_dir="/var/lib/cloud9/ndas_rt_backups/"
username="debian"
echo "Install dir: "${install_dir}

function remove_all_but_settings {
    for f in ${install_dir}/*; do
        if [[ ${f##*/} != "settings" ]]; then
            echo "Removing "$f
            rm -r $f
        fi
    done
}

function keep_settings {
    while true; do
    read -p "Keep old settings? (y/n)?" yn
        case $yn in
            [Yy]* )
                remove_all_but_settings
                break;;
            [Nn]* )
                rm /root/ndas_rt/firewall-rules
                rm -r ${install_dir}
                mkdir ${install_dir}
                break;;
            * ) echo "Please answer yes or no.";;
        esac
    done
}

function make_backup {
    while true
        do
            read -p "Directory ndas_rt exists, make backup (y/n)?" yn
                case $yn in
                    [Yy]* )
                        backup_name=${backup_dir}/$(date +'%Y-%m-%d_%H-%M-%S')".zip"
                        if [ ! -d "$backup_dir" ];
                            then mkdir ${backup_dir};
                            chown ${username} ${backup_dir}
                        fi
                        zip -r ${backup_name} ${install_dir}
                        chown ${username} ${backup_name}
                        echo "Created "${backup_name}
                        break;;
                    [Nn]* ) break;;
                    * ) echo "Please answer yes or no.";;
                esac
        done
}

function install_modules {
    for f in $install_dir/sw_modules/*; do
        if [ -d "$f" ]; then
            module_installer=$f/install.sh
            echo $module_installer
            bash $module_installer
        fi
    done
}


#backup previous installation and move settings if nesessary
if [ -d "$install_dir" ]; then
    make_backup
    keep_settings
else
    mkdir ${install_dir}
fi
#copy new files and
if [ -d "../ndas_rt" ]; then
    cp -r ../ndas_rt/* ${install_dir}
elif [ -d "../ndas_rt_src" ]; then
    cp -r ../ndas_rt_src/* ${install_dir}
else
    echo "There is not ndas_rt directory. Need to use 'git clone --recurse-submodules'"
fi

bash ${install_dir}/system_manager/install.sh
install_modules
chown -R ${username} ${install_dir}
chgrp -R ${username} ${install_dir}
echo "Done!"
