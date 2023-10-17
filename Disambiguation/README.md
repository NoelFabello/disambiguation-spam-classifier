# Creación del entorno virtual
## Serán necesarios los siguientes paquetes para completar las dependencias:

>sudo apt install python3.11-dev libcairo2-dev libgirepository1.0-dev python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-webkit2-4.0

## Será necesario descargar una serie de archivos de nltk:

### Para ello en una terminal dentro del entorno virtual:
>$ python

### y en la consola de Python:
> import nltk
> nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords'); nltk.download('averaged_perceptron_tagger')

# Datasets
El comprimido mails.zip del directorio Datasets/ contiene los correos electrónicos que se utilzaron para crear el Dataset utilizado en el proyecto

# Ficheros en models/ y outputs/
Son ficheros de ejemplo para trabajar con ellos en la aplicación
