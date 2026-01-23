#!/bin/bash
set -e

echo "===================================="
echo "  Instalador de Organizador de Descargas"
echo "===================================="
echo ""

# Detectar directorio de instalación
if [ -n "$INSTALL_DIR" ]; then
    INSTALL_PATH="$INSTALL_DIR"
else
    INSTALL_PATH="$HOME/.local/bin/file-organizer"
fi

# Crear directorio si no existe
mkdir -p "$INSTALL_PATH"

# Función para descargar archivos
download_file() {
    local url=$1
    local output=$2

    if command -v curl &> /dev/null; then
        curl -sSL "$url" -o "$output"
    elif command -v wget &> /dev/null; then
        wget -q "$url" -O "$output"
    else
        echo "Error: Se necesita curl o wget instalado"
        exit 1
    fi
}

# Determinar si estamos instalando desde repo local o remoto
if [ -f "main.py" ] && [ -f "file_organizer.py" ] && [ -f "extensions.py" ]; then
    echo "Detectado repositorio local, usando archivos locales..."
    cp main.py "$INSTALL_PATH/main.py"
    cp file_organizer.py "$INSTALL_PATH/file_organizer.py"
    cp extensions.py "$INSTALL_PATH/extensions.py"
else
    echo "Descargando archivos desde GitHub..."
    BASE_URL="https://raw.githubusercontent.com/xMigma/downloads-organizer/main"

    download_file "$BASE_URL/main.py" "$INSTALL_PATH/main.py"
    download_file "$BASE_URL/file_organizer.py" "$INSTALL_PATH/file_organizer.py"
    download_file "$BASE_URL/extensions.py" "$INSTALL_PATH/extensions.py"
fi

chmod +x "$INSTALL_PATH/main.py"

echo "Archivos instalados en: $INSTALL_PATH"
echo ""

# Preguntar directorio a organizar
DEFAULT_DIR="$HOME/Downloads"
if [ ! -d "$DEFAULT_DIR" ]; then
    DEFAULT_DIR="$HOME/Descargas"
fi

read -p "Que directorio quieres organizar? [$DEFAULT_DIR]: " TARGET_DIR
TARGET_DIR=${TARGET_DIR:-$DEFAULT_DIR}
TARGET_DIR=$(eval echo "$TARGET_DIR")

# Verificar si el directorio existe
if [ ! -d "$TARGET_DIR" ]; then
    echo "Advertencia: El directorio '$TARGET_DIR' no existe."
    read -p "Crear directorio? (s/N): " CREATE_DIR
    if [ "$CREATE_DIR" = "s" ] || [ "$CREATE_DIR" = "S" ]; then
        mkdir -p "$TARGET_DIR"
        echo "Directorio creado"
    else
        read -p "Continuar de todos modos? (s/N): " CONTINUE
        if [ "$CONTINUE" != "s" ] && [ "$CONTINUE" != "S" ]; then
            echo "Instalacion cancelada."
            exit 1
        fi
    fi
fi

# Configurar cron job
echo ""
echo "Configurando cron job para ejecutar al inicio..."

# Crear archivo temporal con el crontab actual
crontab -l 2>/dev/null > /tmp/crontab.tmp || touch /tmp/crontab.tmp

# Eliminar entradas anteriores del organizador
grep -v "$INSTALL_PATH/main.py" /tmp/crontab.tmp > /tmp/crontab.new || touch /tmp/crontab.new

# Añadir nueva entrada
LOG_FILE="$INSTALL_PATH/organizer.log"
echo "@reboot python3 $INSTALL_PATH/main.py \"$TARGET_DIR\" >> $LOG_FILE 2>&1" >> /tmp/crontab.new

# Instalar nuevo crontab
crontab /tmp/crontab.new
rm /tmp/crontab.tmp /tmp/crontab.new

echo "Cron job configurado correctamente"
echo ""
echo "===================================="
echo "Instalacion completada!"
echo "===================================="
echo ""
echo "Configuracion:"
echo "  - Directorio: $TARGET_DIR"
echo "  - Se ejecutara automaticamente al reiniciar"
echo "  - Logs: $LOG_FILE"
echo ""
echo "Comandos utiles:"
echo "  # Ejecutar ahora:"
echo "  python3 $INSTALL_PATH/main.py \"$TARGET_DIR\""
echo ""
echo "  # Ver logs:"
echo "  tail -f $LOG_FILE"
echo ""
echo "  # Ver cron job:"
echo "  crontab -l | grep file-organizer"
echo ""
echo "  # Desinstalar:"
echo "  crontab -l | grep -v '$INSTALL_PATH/main.py' | crontab -"
echo "  rm -rf $INSTALL_PATH"
echo ""
