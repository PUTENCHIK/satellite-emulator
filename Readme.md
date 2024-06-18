# Технологическая(проектно-технологическая) практика
### АВТОРЫ <br /> Шорников Даниил <br /> Олифиренко Максим <br /> Антипин Демид
## Main.py
### Функция по получения zip с данными о определенной дате
```python
def get_data(date: str):
    try:
        gotten_date = datetime.date.fromisoformat(date)
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")

    if gotten_date > datetime.date.today() - datetime.timedelta(days=1):
        raise Exception(f"Gotten date must be early then today")

    link = f"https://api.simurg.space/datafiles/map_files?date={date}"
    file_name = f"archives/{date}.zip"
    with open(file_name, "wb") as f:
        print(f"Downloading {file_name}")
        response = requests.get(link, stream=True)
        total_length = response.headers.get('content-length')

        if response.json()['detail'] == "Map files not foud":
            raise Exception(f"Sorry but storage doesn't save archive for date {date}")

        if total_length is None:
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(50 * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()
```
### Функция с запуском download_archive.sh
```python
def unzip(date: str):
    print("unzip func")
    subprocess.call(f"./scripts/download_archive.sh {date}", shell=True)
```
### Функция с запуском create_interval_folders.sh
```python
def separate_files(date: str):
    subprocess.call(f"./scripts/create_interval_folders.sh {TIME_INTERVAL}", shell=True)
```
## Download_archive.sh
### Temporary directory for .crx files and archives
```bash
if [ -d temporary ]; then
	rm -r temporary
fi
mkdir temporary;
```
### Unzipping main archive 
```bash
archive="archives/$1.zip";
unzip $archive -d temporary/;
```
### Unzipping gz achives
```bash
for filename in temporary/*.crx.gz; do
	gunzip $filename;
done
```
### Creating directory files/ and special directory for date archive
```bash
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
```
