Linux è il sistema operativos su cui è consigliato iniziare. Esistono diverse distribuzioni possibili:

* Scientific Linux è usato al Cern perché è stabile e lunga vita media, oltre alla disponibilità di librerie.
* Red Hat più dal lato aziendale.
* Ubuntu è la più user friendly.

Le istruzioni saranno per ubuntu

## 1) Installazione sistema operativo - esempio con Ubuntu 20.04 LTS

Si parte dall'istallazione di un file immagine (*iso*) qui:

    https://www.ubuntu-it.org/download

Il suggerimento è di scegliere una distribuzione Long Term Support (LTS) piuttosto che una di sviluppo (senza LTS nel nome).

Di seguito assumeremo la 20.04.3

Per installarlo ci sono due modi:

1.1) Far partire una iso da uno strumento esterno e realizzare una partizione. Consigliato se sapete quello che state facendo e volete impiegare parte del vostro spazio sul pc in maniera permanente.

Istruzioni:

    Scaricare la iso dal sito su una penna. Ubuntu 20.04 può essere pesante, ordine 3 GB, quindi occhio alla connessione.

    Riavviare il computer, e, nel bios settare il boot di modo che dia priorità alla penna. Il modo di aprire il bios varia da macchina a macchina, tipicamente consiste nel premere un pulsante durante il caricamento di Windows (ad es. F2). Questo di solito compare tra le scritte durante l'avvio.

1.2) Realizzare una macchina virtuale e installare il sistema operativo lì. Questo in genere ha difficoltà e rischi piuttosto bassi, quindi consigliato a meno che non vogliate lavorare su linux per la maggior parte del vostro tempo.

Istruzioni:

    Scarivcare virtualbox da qui: https://www.virtualbox.org/wiki/Downloads per la piattaforma ospite (ad es. Windows).
    
    Una volta avviato, creare una nuova macchina tramite file -> nuova macchina, con settings Linux , Ubuntu-32 (64 a seconda dell'architettura), e nome macchina riconoscibile.
    
    Aperta la macchina, avviarla e caricare il file iso scaricato in precedenza. Partirà l'installazione e il sistema operativo di conseguenza.


## 2) Python3

## 3) pip/conda

## 4) git

## 5) jupyter

## 6) root
