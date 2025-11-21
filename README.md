# Penugasan-Backend-Open-Recruitment-2025

# Database nabil_db
# Membuat database pada postgresql
CREATE DATABASE nabil_db;

# Kemudian membuat table mahasiswa
CREATE TABLE public.mahasiswa (
	nim varchar NOT NULL,
	"name" varchar NOT NULL,
	email varchar NULL,
	status int2 DEFAULT 0 NULL,
	CONSTRAINT mahasiswa_pk PRIMARY KEY (nim)
);

# Cara instalasi source code 
# 1. Install python 3.1.3
# 2. Install Flask (pip install flask)
# 3. Install JWT (pip install Flask-JWT-Extended)
# 4. Install Psycopg2 (pip install psycopg2)

# Konfigurasi File appconfig.ini
[Server]
ServerIP = 127.0.0.1 # Alamat IP Address http server
ServerPort = 8080 # Alamat port http server
JWT_USER =   nabilX # Digunakan untuk user JWT
JWT_PASS = nabil1234 # Digunakan untuk password JWT
JWT_KEY = nabil-super-secret-key # Isi dengan key untuk JWT

[Database]
Type = PostgreSQL # Jenis database yang digunakan
Host = localhost # Alamat host/IP Address database
Name = nabil_db # Nama database yang digunakan
Port = 5432 # Port database
User = postgres # User untuk mengakses database
Password = #dev0p5@xxi # Password untuk mengakses database

# Cara Menggunakan RestfulAPI
# Mengambil Token JWT
Endpoint = 127.0.0.1:8080/api/login_jwt
http method = [POST]
Content-Type = application/json
# Body Raw Data
{
  "username": "nabil",
  "password": "nabil1234"
}
# Result
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc2Mzc0MDEyOCwianRpIjoiMmExMTljMDQtMmQ5ZC00MmE5LWFjYTQtNGQ2ODJkN2VlN2VjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6Im5hYmlsIiwibmJmIjoxNzYzNzQwMTI4LCJjc3JmIjoiMjU4NDVjYjUtZTYxYi00NDI3LWE1NzktZjczMDg3OWYzZTU4IiwiZXhwIjoxNzYzNzQxMDI4fQ.a9V-pFfU0qjQP0xRjQdWSmTsJfMO28sUDUyv13HZRow"
}

# Check Token JWT
Endpoint = 127.0.0.1:8080/api/check_jwt
http method = [GET]
Content-Type = application/json
Authorization = Bearer [token jwt]
# Result
{
    "logged_in_as": "nabil"
}

# List Mahasiswa
Endpoint = 127.0.0.1:8080/api/list_mahasiswa
http method = [GET]
Content-Type = application/json
Authorization = Bearer [token jwt]
# Result
[
    {
        "email": "nabil@ugm.com",
        "name": "Andi Nabil Safaraz",
        "nim": "0101010101",
        "status": 1
    },
    {
        "email": "yasmin@dsada",
        "name": "Yasmin",
        "nim": "2222222222",
        "status": 1
    }
]

# Data Mahasiswa
Endpoint = 127.0.0.1:8080/api/data_mahasiswa
http method = [GET]
Content-Type = application/json
Authorization = Bearer [token jwt]
form-data = nim
# Result
[
    {
        "email": "nabil@ugm.com",
        "name": "Andi Nabil Safaraz",
        "nim": "0101010101",
        "status": 1
    }
]

# Create Mahasiswa
Endpoint = 127.0.0.1:8080/api/create_mahasiswa
http method = [GET]
Content-Type = application/json
Authorization = Bearer [token jwt]
raw = {
  "nim": "2222222222",
  "name": "Yasmin",
  "email": "yasmin@dsada"
}
# Result
{
    "message": "Data mahasiswa berhasil ditambahkan.",
    "name": "yasmin@dsada",
    "nim": "2222222222",
    "status": "Sukses"
}

# Update Mahasiswa
Endpoint = 127.0.0.1:8080/api/update_mahasiswa
http method = [GET]
Content-Type = application/json
Authorization = Bearer [token jwt]
raw = {
  "nim": "1111111111",
  "name": "Altamis",
  "email": "altasmis@xxxxx.com",
   "status": 1
}
# Result
{
    "message": "Data mahasiswa berhasil diubah.",
    "name": 1,
    "nim": "1111111111",
    "status": "Sukses"
}

# Remove Mahasiswa
Endpoint = 127.0.0.1:8080/api/remove_mahasiswa
http method = [GET]
Content-Type = application/json
Authorization = Bearer [token jwt]
form-data = nim
# Result 
{
    "message": "Data mahasiswa berhasil dihapus.",
    "nim": "1111111111",
    "status": "Sukses"
}
