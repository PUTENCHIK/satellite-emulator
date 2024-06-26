#!/bin/bash


me=$(basename "$0");

scripts/logger.sh "$me" 'info' "Called $me script"

# Temporary directory for .crx files and archives
if [ -d temporary ]; then
	scripts/logger.sh "$me" 'warning' 'Removed old directory temporary\/'
	rm -rf temporary
fi
mkdir temporary;

# Unzipping main archive 
archive="archives/$1.zip";
scripts/logger.sh "$me" 'debug' "Unpacking main archive $(basename $archive)"
unzip $archive -d temporary/;

# Unzipping gz achives
for filename in temporary/*.crx.gz; do
	scripts/logger.sh "$me" 'debug' "Unpacking $(basename $filename)"
	gunzip $filename;
done

# Creating directory files/ if not exists
if ! [ -d files ]; then
	mkdir files;
fi

for filename in temporary/*.crx; do
	# Separating name of station from crx file's name
	station=$(echo $filename | sed 's|temporary/\([^_]*\)_.*|\1|')
	if ! [ -d files/$station ]; then
		# Creating directory for station if not exists
        	mkdir files/$station;
	fi
	new_name=${filename::-4}.'rnx';
	scripts/logger.sh "$me" 'debug' "Converting station's file: $(basename $filename)";
	sudo ./CRX2RNX $filename;
	# Moving converted RINEX file from temporary directory to files/{dtation name}/{date of file} 
	mv -f $new_name files/$station/$1.rnx;
done

rm -r temporary;
