🚀 ECHOME – Time Capsule Secure Message Delivery System

ECHOME is a secure, blockchain-backed, asynchronous time-based message storage and delivery platform. Users upload encrypted files or messages and set a future release time. The system handles secure storage, verification, and automated delivery upon maturity.

📌 Table of Contents

Overview

Features

System Architecture

Technology Stack

Security Model

Database Schema

Setup & Installation

Docker Deployment

Environment Variables

Celery & Redis Configuration

Blockchain Integration

Troubleshooting

License

Author

🧠 Overview

ECHOME allows users to store "Time Capsules" that strictly unlock in the future.

The Workflow:

Upload: User uploads a file/message and selects a release date.

Process: The file is temporarily stored, then a Celery worker encrypts and uploads it to IPFS/S3.

Lock: The unlock timestamp and verification hash are stored on the Ethereum blockchain via Smart Contract.

Wait: The system holds the decryption keys securely.

Release: Celery Beat checks for expired capsules every minute.

Notify: Upon maturity, the system retrieves the file, validates integrity against the blockchain, and emails the user.

⭐ Features

Encrypted Storage: AES-256 encryption for all files.

Time-Lock: Strict server-side and blockchain-side timestamp validation.

Async Processing: Heavy lifting (uploads, encryption) handled by Celery workers to keep the API fast.

Blockchain Verification: Uses Ethereum (Sepolia/Testnet) to prove time-capsule integrity.

Scalable Queue: Powered by Redis (Upstash) with TLS security.

Robust Backend: Built on Django 4.2 with PostgreSQL.

Containerized: Fully Dockerized for easy deployment.

🏗 System Architecture

flowchart TD
    %% Definitions
    classDef client fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef core fill:#fff9c4,stroke:#fbc02d,stroke-width:2px;
    classDef db fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef async fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px;
    classDef ext fill:#eceff1,stroke:#455a64,stroke-width:2px,stroke-dasharray: 5 5;

    %% Nodes
    Client([👤 Client / Frontend]):::client
    
    subgraph Core_System ["🧠 Core System"]
        Django[Django API]:::core
        DB[(PostgreSQL)]:::db
    end
    
    subgraph Async_Layer ["⚡ Async Processing"]
        Redis{Redis Queue}:::async
        Worker[[Celery Worker]]:::async
        Beat((Celery Beat)):::async
    end
    
    subgraph External_Services ["🌐 External Services"]
        Storage[IPFS / S3 Bucket]:::ext
        Chain[Blockchain / Smart Contract]:::ext
    end

    %% Flows
    Client -->|1. Upload File| Django
    Django -->|2. Store Metadata| DB
    Django -->|3. Dispatch Task| Redis
    
    Beat -->|Cron: Check Expiry| Redis
    Redis -->|Consume Task| Worker
    
    Worker -->|4. Encrypt & Upload| Storage
    Worker -->|5. Verify Hash| Chain
    Worker -.->|Update Status| DB


ASCII View

      +-----------------+
      |  User / Client  |
      +--------+--------+
               | 1. POST /upload
               v
    +-----------------------+       +------------------+
    |      Django API       | ----> |   PostgreSQL DB  |
    +----------+------------+       +------------------+
               |
               | 2. Task.delay()
               v
    +-----------------------+
    |    Redis (Broker)     | <----+
    +----------+------------+      |
               |                   |
               | 3. Pop Task       | 6. Schedule (Cron)
               v                   |
    +-----------------------+      |
    |     Celery Worker     |      |
    +----------+------------+      |
               |                   |
    +----------+----------+        |
    | 4. Upload           | 5. Sign|
    v                     v        |
+----------+      +-----------+    |
| IPFS/S3  |      | Blockchain|    |
+----------+      +-----------+    |
                                   |
    +-----------------------+      |
    |      Celery Beat      | -----+
    +-----------------------+


🧩 Technology Stack

Component

Technology

Description

Backend

Django 4.2

Python Web Framework

Queue Broker

Redis

Hosted on Upstash (TLS enabled)

Async Tasks

Celery 5.x

Distributed Task Queue

Scheduler

Celery Beat

Periodic task scheduler (Cron)

Database

PostgreSQL

Relational Database

Blockchain

Web3.py

Interaction with Ethereum Nodes

Server

Gunicorn

WSGI HTTP Server

Container

Docker

Application containerization

OS

Alpine Linux

Base image for containers

🔐 Security Model

Data Encryption: Files are encrypted before storage. Decryption keys are stored separately from the file data.

Transport Security: Redis connections use rediss:// (TLS) to ensure queue data is safe over the wire.

Blockchain Integrity: A hash of the original file is stored on-chain. If the file is tampered with during storage, the hash won't match upon retrieval.

Input Sanitization: Strict file type and size validation within Django.

🗃 Database Schema

Model: Capsule

Field

Type

Description

id

UUID

Primary Key

user

ForeignKey

Owner of the capsule

cid

CharField

IPFS Content ID or S3 Key

file_ext

CharField

Original file extension

decryption_pass

CharField

Encrypted password for the file

unlock_time

DateTime

When the capsule opens (UTC)

status

Enum

pending, uploaded, released

tx_hash

CharField

Blockchain transaction hash

💻 Setup & Installation (Local)

Prerequisites

Python 3.10+

PostgreSQL

Redis (Local or Upstash URL)

1. Clone the Repository

git clone [https://github.com/kgpro/ECHOME.git](https://github.com/kgpro/ECHOME.git)
cd ECHOME


2. Virtual Environment

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


3. Install Dependencies

pip install -r requirements.txt


Note: If using Python 3.13+, ensure you are using psycopg3 or psycopg[binary] instead of psycopg2.

4. Database Setup

Ensure PostgreSQL is running and create a DB named echome.

python manage.py migrate
python manage.py createsuperuser


5. Run Server

python manage.py runserver


🐳 Docker Deployment

The project is optimized for Docker.

1. Build and Run

docker-compose up --build -d


This starts:

Web: Gunicorn serving the Django App (Port 8000)

Worker: Celery worker for processing uploads

Beat: Celery scheduler for checking unlock times

2. View Logs

docker-compose logs -f


🌍 Environment Variables

Create a .env file in the root directory:

# Django Settings
DJANGO_SECRET_KEY=change_me_to_something_secure
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,[YOUR_IP]

# Database (PostgreSQL)
POSTGRES_DB=echome
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis / Celery (Upstash)
# Note: Upstash only supports DB 0. Include ssl_cert_reqs for TLS.
REDIS_URL=rediss://default:PASSWORD@HOST:6379
CELERY_BROKER_URL=${REDIS_URL}/0?ssl_cert_reqs=CERT_NONE
CELERY_RESULT_BACKEND=${REDIS_URL}/0?ssl_cert_reqs=CERT_NONE

# Blockchain
WEB3_PROVIDER_URL=[https://sepolia.infura.io/v3/YOUR_KEY](https://sepolia.infura.io/v3/YOUR_KEY)
WALLET_PRIVATE_KEY=your_private_key
CONTRACT_ADDRESS=0x...


⚙️ Celery & Redis Configuration

Running Workers Manually

If not using Docker, you must run these in separate terminal windows:

Worker (Processes tasks):

celery -A ECHOME worker --loglevel=info


Beat (Schedules tasks):

celery -A ECHOME beat --loglevel=info


Important Upstash Note

Upstash Redis instances only support Database 0. Ensure your CELERY_BROKER_URL ends in /0.

🔗 Blockchain Integration

ECHOME uses Web3.py to interact with the Ethereum network (Sepolia Testnet recommended).

Upload: When a capsule is created, a hash is sent to the smart contract.

Verification: When a capsule is unlocked, the system reads from the contract to verify the timestamp and integrity.

⚠️ Common Errors & Fixes

Error

Reason

Fix

ERR max number of dbs is 1

Upstash limitation

Ensure Redis URL ends in /0.

Symbol not found: _PQbackendPID

psycopg2 vs Python 3.13

Upgrade to psycopg[binary] or use Python 3.11.

SIGSEGV in Worker

RAM issues

Reduce worker_concurrency or increase RAM.

Celery Windows Crash

billiard library issue

Use WSL2 or Docker (Celery is unstable on raw Windows).

📜 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this software.

👨‍💻 Author

Kamlesh Gujrati Backend Developer | Blockchain | AI | Django
