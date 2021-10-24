Linux è il sistema operativos su cui è consigliato iniziare. Esistono diverse distribuzioni possibili:

* Red Hat Enterprise è utilizzato in genere lato aziendale.
* Scientific Linux è usato al Cern, è una versione di Red Hat sponsorizzata dal Fermilab. E' stabile e lunga vita media, oltre alla disponibilità di librerie.
* Ubuntu è la più user friendly, facile da scaricare e usare, per cui ha una community piuttosto vasta. Non è ottimale, specie con le librerie grafiche.

Le istruzioni saranno per ubuntu

## 1) Installazione sistema operativo - esempio con Ubuntu 20.04 LTS

Si parte dall'istallazione di un file immagine (*iso*) qui:

    https://www.ubuntu-it.org/download

Il suggerimento è di scegliere una distribuzione Long Term Support (LTS) piuttosto che una di sviluppo (senza LTS nel nome).

Di seguito assumeremo la 20.04.3

Per installarlo ci sono due modi:

1.1) Far partire una iso da uno strumento esterno e realizzare una partizione. Consigliato se sapete quello che state facendo e volete impiegare parte del vostro spazio sul pc in maniera permanente.

Istruzioni:

    Scaricare la iso dal sito su una penna. 
    Ubuntu 20.04 può essere pesante, ordine 3 GB, quindi occhio alla connessione.

    Riavviare il computer, e, nel bios settare il boot di modo che dia priorità alla penna. 
    Il modo di aprire il bios varia da macchina a macchina, tipicamente consiste nel premere 
    un pulsante durante il caricamento di Windows (ad es. F2). Questo di solito compare tra le scritte durante l'avvio.

1.2) Realizzare una macchina virtuale e installare il sistema operativo lì. Questo in genere ha difficoltà e rischi piuttosto bassi, quindi consigliato a meno che non vogliate lavorare su linux per la maggior parte del vostro tempo.

Istruzioni:

    Scarivcare virtualbox da qui: https://www.virtualbox.org/wiki/Downloads 
    per la piattaforma ospite (ad es. Windows).
    
    Una volta avviato, creare una nuova macchina tramite file -> nuova macchina, 
    con settings Linux , Ubuntu-32 (64 a seconda dell'architettura), e nome macchina riconoscibile.
    
    Aperta la macchina, avviarla e caricare il file iso scaricato in precedenza. 
    Partirà l'installazione e il sistema operativo di conseguenza.


## 2) Python3

Con la versione di linux 20.04 python3 è automaticamente installato

## 3) pip/conda

3.1) Installare pip:
    
    sudo apt-get install pip

3.2) Istruzioni per Anaconda:
    
    Andare su https://docs.conda.io/projects/conda/en/latest/user-guide/install/linux.html 
    seguire il link per scaricare l'installer https://www.anaconda.com/products/individual
 
Eseguire:
    
    sudo bash Anaconda-latest-Linux-x86_64.sh

Nota: può essere necessario aggiungere conda al path. 
Assumendo che anaconda sia installato in /home/myusername/anaconda3    

    PATH=$PATH:~/anaconda3/bin

## 4) git

    sudo apt-get install git
    
## 5) jupyter

## 6) root

Seguire le istruzioni trovate qui:

    https://root.cern/install

6.1) installare via binaries:
    
Scaricare i binaries qui:
    
    https://root.cern/install/#download-a-pre-compiled-binary-distribution

Eseguire:

    wget https://root.cern/download/root_v6.24.02.Linux-ubuntu20-x86_64-gcc9.3.tar.gz
    tar -xzvf root_v6.24.02.Linux-ubuntu20-x86_64-gcc9.3.tar.gz
    source root/bin/thisroot.sh # also available: thisroot.{csh,fish,bat}

6.2) Se c'è conda installato

Seguire la procedura qui :
    
    https://root.cern/install/#conda
   
Eseguire:

    conda config --set channel_priority strict
    conda create -c conda-forge --name rootenv root 
    conda activate rootenv
    
Nota bene: conda qui creerà un ambiente in cui root funziona. La versione suggerita 
        
