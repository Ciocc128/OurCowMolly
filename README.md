# 🥛 OurCowMolly

OurCowMolly è un progetto backend sviluppato come **Minimum Viable Product (MVP)** con l’obiettivo di simulare la gestione digitale di un piccolo negozio locale (es. un lattaio), permettendo la **creazione, gestione e tracciamento degli ordini** in modo semplice e strutturato.

Il progetto nasce con una forte finalità **formativa**: migliorare le competenze in **backend development**, **system design** e **API design**, adottando buone pratiche realistiche ma mantenendo la complessità sotto controllo.

---

## 🎯 Obiettivo del progetto

Costruire un backend che:

- gestisca **prodotti**, **clienti** e **ordini**
- implementi **logica di business reale** (stock, stati ordine, prezzi)
- esponga **API REST** chiare e testabili
- sia facilmente estendibile verso:
  - una dashboard web
  - un’interazione tramite chatbot (LLM)

---

## 🚀 MVP — Cosa include

### 📦 Products
- CRUD completo per i prodotti
- Gestione dello stock (`in_stock`)
- Prezzo con tipo numerico preciso (`Numeric / Decimal`)

### 👤 Customers
- CRUD completo per i clienti
- Associazione cliente → ordini

### 🧾 Orders
- Creazione ordini con più prodotti (`OrderItem`)
- Salvataggio del **prezzo unitario snapshot** (`unit_price`)
- Calcolo e persistenza del `total_price`
- Stati dell’ordine:
  - `PENDING`
  - `CONFIRMED`
  - `DELIVERED`
  - `CANCELLED`
- Regole di business:
  - lo stock viene scalato **solo alla conferma** (`CONFIRMED`)
  - transizioni di stato controllate
  - errori gestiti con eccezioni custom (`NotFoundError`, `BadRequestError`)

---

## 🏗️ Architettura

Struttura modulare:

```
.
├── core/          # config, database, utils
├── products/      # models, schemas, service, routers
├── customers/     # models, schemas, service, routers
├── orders/        # models, schemas, service, routers
├── main.py
└── requirements.txt
```

Principi adottati:
- separazione tra **router** (HTTP layer) e **service** (business logic)
- ORM con **SQLAlchemy**
- validazione e serializzazione con **Pydantic schemas**
- logging strutturato
- codice **sincrono** (scelta intenzionale per semplicità MVP)

---

## 🛠️ Stack Tecnologico

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite (database locale per MVP)
- Pydantic
- Uvicorn

---

## ▶️ Avvio del progetto

1) Crea e attiva un virtual environment

2) Installa le dipendenze:

```bash
pip install -r requirements.txt
```

3) Avvia il server:

```bash
uvicorn main:app --reload
```

4) Apri la documentazione interattiva:

- http://127.0.0.1:8000/docs

---

## 🔮 Sviluppi futuri (post-MVP)

- Interazione tramite **chatbot (LLM)** per creare ordini in linguaggio naturale
- Dashboard web per il lattaio
- Autenticazione e ruoli
- Migrazione a database persistente (es. PostgreSQL)
- Migrations con Alembic
- Possibile uso di WebSocket per aggiornamenti realtime

---

## 📌 Note finali

Questo progetto è pensato come **base solida e didattica**, non come prodotto enterprise.
Le scelte architetturali privilegiano chiarezza, leggibilità ed estendibilità.
