In generale, Windows non è un ambiente ideale per lo sviluppo. Si consiglia di utilizzare o una partizione con ubuntu, o una macchina virtuale in ambiente linux. In ogni caso, qui ci sono delle informazioni su come installare codice su OS Windows 10.

## 1) Installazione python

1.1) Windows 10 può installarlo automaticamente. Alternativamente, si puà scaricare da qui:

    https://www.python.org/downloads/

Python è necessario per buona aprte di quanto segue.

## 2) Installazione pip / conda

2.1) Scaricare pip da:

    https://bootstrap.pypa.io/get-pip.py

Se si apre come pagina, si può scaricare direttamente.

2.2) Scaricare l'eseguibile di anaconda da:

    https://www.anaconda.com/products/individual#windows

e lanciarlo

    
## 3) Installazione git

Si scarica e esegue da qui:

    https://git-scm.com/download/win

## 4) installazione jupyter

Due opzioni: da prompt dei comandi o da anaconda

4.1) Aprire prompt di comandi come amministratore, poi

    python3 -m pip install jupyter

si può lanciare con 

    jupyter notebook

Nota: talvolta l'html potrebbe avere alcuni problemi in delle versioni di windows, copiare il secondo intdirizzo indicato (con http://localhost:8888/...)

4.2) Lanciare anaconda navigator, jupyter dovrebbe essere sulla prima pagina.

## 5) Installazione root

Si può installare solo tramite binaries, seguendo le istruzioni qui:

    https://root.cern/install/


## 6) Installazione macchina virtuale

Si può scaricare da qui:

    https://www.virtualbox.org/wiki/Downloads

In particolare la versione per windows:

    https://download.virtualbox.org/virtualbox/6.1.26/VirtualBox-6.1.26-145957-Win.exe
