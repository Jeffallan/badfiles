#! /bin/bash

ME=`whoami`

mkdir test
cd test
# makes random files

for n in {1..100}; do
    dd if=/dev/urandom of=file$( printf %03d "$n" ).bin bs=1 count=$(( RANDOM + 1024 ))
done
#zips files together
for n in {1..10}; do
    zip -r zip$(printf %02d "$n").zip $(ls | grep .bin | sort -R | head)
done

wget -U "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0" -nd -r --level=1  --wait=1 -e robots=off -A jpg,jpeg -H https://www.shutterstock.com/search/cute+cat

for n in {1..10}; do
    zip -r img$(printf %02d "$n").zip $(ls | grep .jpg | sort -R | head)
done

echo ".zip" >> not_zip.txt
echo ".zip" >> not_zip.zip

cp not_zip.txt not_zip.zip

tar -cvf not_zip.txt.tar not_zip.txt

#make zip with symlink
ln -s /etc/passwd etcpass.sh
zip --symlinks sym1.zip etcpass.sh

#make zip with setuid 4
touch uid.sh
chmod 4755 uid.sh
zip uid.zip uid.sh

#make zip with setgid 2
touch gid.sh
chmod 2755 gid.sh
zip gid.zip gid.sh

#sticky bit 1
touch sticky.sh
chmod 1755 sticky.sh
zip sticky.zip sticky.sh

#TODO make with combination of sym, uid and gid?

touch uid_sticky.sh
chmod 5755 uid_sticky.sh
zip uid_sticky.zip uid_sticky.sh

touch gid_sticky.sh
chmod 6755 gid_sticky.sh
zip gid_sticky.zip gid_sticky.sh

touch uid_gid_sticky.sh
chmod 7755 uid_gid_sticky.sh
zip uid_gid_sticky.zip uid_gid_sticky.sh

touch uid_gid.sh
chmod 6755 uid_gid.sh
zip uid_gid.zip uid_gid.sh

#zip lowest perms
touch lowest.sh
chmod 1500 lowest.sh
zip lowest_perms.zip lowest.sh

#zip highest perms
touch highest.sh
chmod 7777 highest.sh
zip highest_perms.zip highest.sh


#make zip slip
touch "../../slip"
zip zipslip.zip ../../slip
rm ../../slip

#make zip bomb
wget https://raw.githubusercontent.com/damianrusinek/zip-bomb/master/zip-bomb.py
python3 zip-bomb.py flat 2048 flat-bomb.zip
python3 zip-bomb.py nested 2048 nested-bomb.zip


chmod 777 ./file001.bin
tar -cvf exe.tar ./file001.bin

mkdir tar_dir
cp ./file001.bin ./tar_dir/file001.bin
tar -cvf tar_dir.tar tar_dir

tar -cvf abs.tar file002.bin

##make Tarfiles
sudo su --session-command "touch root.sh; \
                           tar -cvf  root_group.tar ./root.sh; \
                           sudo chown $ME root_group.tar; \
                           tar -cvf root_own.tar ./root.sh; \
                           sudo chgrp $ME root_own.tar"
