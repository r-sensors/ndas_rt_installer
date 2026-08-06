echo "Mounting SD card and creating /archive directory"

options=("Format to FAT32" "Format to ExFAT" "Format to EXT4" "Mount only")
    
select opt in "${options[@]}"; do
    case $opt in 
        "Format to FAT32")
            umount -l -f /dev/mmcblk0p1
            rm -r /media/sdcard
            mkdir /media/sdcard
            mkfs.vfat -F 32 /dev/mmcblk0p1
            mount -o rw,users,umask=000,exec /dev/mmcblk0p1 /media/sdcard
            break  ;;
        "Format to ExFAT")
            umount -l -f /dev/mmcblk0p1
            rm -r /media/sdcard
            mkdir /media/sdcard
            mkfs.exfat /dev/mmcblk0p1
            mount -o rw,users,umask=000,exec /dev/mmcblk0p1 /media/sdcard
            break ;;
        "Format to EXT4")
            umount -l -f /dev/mmcblk0p1
            rm -r /media/sdcard
            mkdir /media/sdcard
            mkfs.ext4 /dev/mmcblk0p1
            mount /dev/mmcblk0p1 /media/sdcard
            break ;;
        "Mount only")
            mkdir /media/sdcard
            mount -o rw,users,umask=000,exec /dev/mmcblk0p1 /media/sdcard
            break ;;
        *) echo "invalid option $REPLY" ;;
    esac
done

mkdir /media/sdcard/logs /media/sdcard/archive /media/sdcard/sl_buffer
chmod 777 /media/sdcard/logs /media/sdcard/archive /media/sdcard/sl_buffer
chown debian /media/sdcard/logs /media/sdcard/archive /media/sdcard/sl_buffer
#create symbolic link to sdcard
ln -s /media/sdcard /var/lib/cloud9
echo "Done!"