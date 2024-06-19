#!/bin/bash

# Temporary directory for .crx files and archives
if [ -d temporary ]; then
	rm -r temporary
fi
mkdir  temporary;

# Unzipping main archive 
archive="archives/$1.zip";
unzip $archive -d temporary/;

# Unzipping gz achives
for filename in temporary/*.crx.gz; do
	gunzip $filename;
done

# Creating directory files/ and special directory for date archive
if ! [ -d files ]; then
	mkdir files;
fi

for filename in temporary/*.crx; do
	station=$(echo $filename | sed 's|temporary/\([^_]*\)_.*|\1|')
	if ! [ -d files/$station ]; then
        	mkdir files/$station;
	fi
	new_name=${filename::-4}.'rnx';
	sudo ./CRX2RNX $filename;
	mv $new_name files/$station/$1.rnx;
done

rm -r temporary;
