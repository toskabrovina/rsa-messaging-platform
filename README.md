# RSA Messaging Platform

## Përshkrimi i Projektit

RSA Messaging Platform është një aplikacion komunikimi client-server i zhvilluar në Python, i cili përdor RSA encryption për komunikim të sigurt ndërmjet klientëve.

Qëllimi i projektit është demonstrimi i komunikimit të sigurt përmes enkriptimit të mesazheve duke përdorur RSA public-key cryptography.

Aplikacioni lejon shumë klientë të lidhen në server, të shkëmbejnë mesazhe të enkriptuara dhe të komunikojnë në mënyrë të sigurt përmes TCP sockets.

---

## Karakteristikat

- Gjenerimi i RSA public/private keys
- Shkëmbim i sigurt i public keys
- Enkriptim dhe dekriptim i mesazheve
- Komunikim multi-client
- Arkitekturë client-server
- Broadcast i mesazheve
- Sistem usernames
- Komunikim i sigurt

---

## Struktura e Projektit

```text
rsa-messaging-platform/
│
├── server.py
├── client.py
├── rsa_utils.py
├── config.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Përshkrimi i File-ve

### server.py
Menaxhon:
- Lidhjen e klientëve
- Broadcast të mesazheve
- Komunikimin e sigurt
- Menaxhimin e përdoruesve

### client.py
Menaxhon:
- Lidhjen me serverin
- Dërgimin e mesazheve të enkriptuara
- Pranimin dhe dekriptimin e mesazheve

### rsa_utils.py
Përmban funksionet RSA:
- Gjenerimin e çelësave
- Enkriptimin
- Dekriptimin
- Serializimin e public keys
- Llogaritjen e kufirit praktik të plaintext për RSA OAEP (`get_max_plaintext_size`)

### config.py
Përmban konfigurimet:
- Host address
- Port
- Buffer size
- Utility helpers për validim dhe info të konfigurimit

### requirements.txt
Përmban bibliotekat e nevojshme Python.

### .gitignore
Parandalon ngarkimin e file-ve të panevojshme në GitHub.

---

## Teknologjitë e Përdorura

- Python 3
- Socket Programming
- RSA Encryption
- TCP/IP Networking
- Cryptography Library
- Multithreading

---

## Instalimi i Varësive

Ekzekuto komandën:

```bash
pip install -r requirements.txt
```

---

## Si të Ekzekutohet Projekti

### Hapi 1 — Startimi i Serverit

Ekzekuto:

```bash
python server.py
```

Shembull:

```text
[SERVER STARTED] 127.0.0.1:5555
```

---

### Hapi 2 — Startimi i Client-it

Hape terminal tjetër dhe ekzekuto:

```bash
python client.py
```

Vendos username:

```text
Enter your username: Vesa
```

Lidhja e suksesshme:

```text
🔐 Secure connection established!
```

---

### Hapi 3 — Lidhja e Klientëve të Tjerë

Në terminale të tjera ekzekuto:

```bash
python client.py
```

---

## Si Funksionon Projekti

1. Serveri gjeneron RSA keys.
2. Client-i gjeneron RSA keys.
3. Bëhet shkëmbimi i public keys.
4. Mesazhet enkriptohen para dërgimit.
5. Mesazhet dekriptohen nga pranuesi.
6. Serveri bën broadcast të mesazheve tek klientët e lidhur.

---

## Shembull i Komunikimit

### Client 1

```text
Enter your username: Vesa
Hello everyone
```

### Client 2

```text
Vesa: Hello everyone
```

### Server

```text
[CONNECTED] Vesa
Vesa: Hello everyone
```

---

## Koncepti i Sigurisë

Ky projekt përdor RSA asymmetric encryption:
- Public keys përdoren për enkriptim.
- Private keys përdoren për dekriptim.
- Mesazhet nuk mund të lexohen pa private key përkatës.

---

## Kufizime të Njohura

- RSA-2048 me OAEP ka kufi praktik për madhësinë e mesazhit (afërsisht nën 190 bytes për një enkriptim).
- Ky projekt është i orientuar për demonstrim/arsim dhe rrjet lokal të besuar.
- Nëse serveri mbyllet, klientët shkëputen dhe duhet të rilidhen manualisht.

---

## Troubleshooting (Zgjidhje të Shpejta)

- **Connection refused:** Verifiko që `server.py` po ekzekutohet dhe porta `5555` nuk është e zënë.
- **Failed to decrypt message:** Mund të ketë pasur ndërprerje lidhjeje ose payload i pavlefshëm.
- **Mesazhi nuk dërgohet:** Shkurto mesazhin dhe provo përsëri (RSA ka limit madhësie).
- **Shkëputje e papritur:** Rinis klientin dhe rilidhu me serverin.

---

## Autorët
Toska Brovina,
Ubejd Shahini,
Vesa Braina,
Valon Hajredini
