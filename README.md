## Install the pre-requisites:

```
poetry install
```

## Run our script

Run our Pillow example, where we flip an image upside down:

```
poetry run python src/run_pillow_example.py
```

Run our pydicom example, where we decompress and save a DICOM file:

```
poetry run python src/run_pydicom_example.py image
poetry run python src/run_pydicom_example.py video
```

## Dockerised version

video:

```
docker build -t leak . && docker run -it --rm --name=video -m 512m -e FILE=video leak
```

image:

```
docker build -t leak . && docker run -it --rm --name=image -m 512m -e FILE=image leak
```
