@echo off
setlocal EnableExtensions EnableDelayedExpansion
title Tesalia Motoclub - App

cd /d "%~dp0"

set "LOG=%~dp0abrir_app.log"
> "%LOG%" echo ====== abrir_app.bat (%date% %time%) ======

where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: No se encontro "python" en el PATH.
  echo Instala Python y marca "Add python.exe to PATH", o abre desde una terminal donde python funcione.
  echo.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo Creando entorno virtual...
  python -m venv .venv >> "%LOG%" 2>&1
  if errorlevel 1 goto :error
)

set "PY=%~dp0.venv\Scripts\python.exe"

echo Instalando dependencias...
"%PY%" -m pip install -r requirements.txt >> "%LOG%" 2>&1
if errorlevel 1 goto :error

set PGSSLMODE=require

if not exist ".env" (
  echo.
  echo ERROR: No existe el archivo .env en esta carpeta.
  echo Crea/edita .env y agrega SUPABASE_DB_URL=postgresql://...
  echo.
  pause
  exit /b 1
)

set "SUPABASE_DB_URL="
for /f "usebackq tokens=1* delims==" %%A in (`findstr /b "SUPABASE_DB_URL=" ".env"`) do set "SUPABASE_DB_URL=%%B"
if "%SUPABASE_DB_URL%"=="" (
  echo.
  echo ERROR: SUPABASE_DB_URL esta vacio en el archivo .env
  echo Abre .env y pega tu connection string Postgres de Supabase.
  echo.
  pause
  exit /b 1
)

echo Migrando base de datos...
set "FIXED_0002=0"
set "FIXED_0003=0"

:migrate_try
"%PY%" manage.py migrate --fake-initial >> "%LOG%" 2>&1
if errorlevel 1 (
  if "%FIXED_0002%"=="0" (
    findstr /i /c:"DuplicateColumn" "%LOG%" | findstr /i /c:"cover_photo_url" >nul
    if not errorlevel 1 (
      echo Detectado: cover_photo_url ya existe. Marcando migracion club.0002 como aplicada... >> "%LOG%"
      "%PY%" manage.py migrate club 0002_profile_cover_bio --fake >> "%LOG%" 2>&1
      if errorlevel 1 goto :error
      set "FIXED_0002=1"
      goto :migrate_try
    )
  )
  if "%FIXED_0003%"=="0" (
    findstr /i /c:"DuplicateColumn" "%LOG%" | findstr /i /c:"profile_photo_file" >nul
    if not errorlevel 1 (
      echo Detectado: profile_photo_file ya existe. Marcando migracion club.0003 como aplicada... >> "%LOG%"
      "%PY%" manage.py migrate club 0003_profile_upload_fields --fake >> "%LOG%" 2>&1
      if errorlevel 1 goto :error
      set "FIXED_0003=1"
      goto :migrate_try
    )
    findstr /i /c:"DuplicateColumn" "%LOG%" | findstr /i /c:"cover_photo_file" >nul
    if not errorlevel 1 (
      echo Detectado: cover_photo_file ya existe. Marcando migracion club.0003 como aplicada... >> "%LOG%"
      "%PY%" manage.py migrate club 0003_profile_upload_fields --fake >> "%LOG%" 2>&1
      if errorlevel 1 goto :error
      set "FIXED_0003=1"
      goto :migrate_try
    )
  )
  goto :error
)

echo Verificando conexion a la base de datos...
"%PY%" manage.py shell -c "from django.db import connection; s=connection.settings_dict; print('DB_ENGINE=',s.get('ENGINE')); print('DB_HOST=',s.get('HOST')); print('DB_NAME=',s.get('NAME'))" >> "%LOG%" 2>&1
if errorlevel 1 goto :error

echo Abriendo navegador...
start "" "http://127.0.0.1:8000/"

echo Iniciando servidor Django...
"%PY%" manage.py runserver 127.0.0.1:8000 >> "%LOG%" 2>&1

echo.
echo Servidor detenido.
pause
exit /b 0

:error
echo.
echo ERROR: El .bat fallo. Copia este mensaje y te lo arreglo.
echo Revisa el archivo: %LOG%
echo.
pause
exit /b 1
