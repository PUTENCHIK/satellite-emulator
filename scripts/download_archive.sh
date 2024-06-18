#!/bin/bash

# Temporary directory for .crx files and archives
if [ -d temporary ]; then
	rm -r temporary
fi
mkdir temporary;

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

if ! [ -d files/$1 ]; then
	mkdir files/$1;
fi

for filename in temporary/*.crx; do
	new_name=${filename::-4}.'rnx';
	./CRX2RNX $filename;
	mv $new_name files/$1/;
done

rm -r temporary;
