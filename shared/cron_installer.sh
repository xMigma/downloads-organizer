#!/bin/bash
# Librería compartida para instalación/desinstalación de cron jobs
# Uso: source /path/to/shared/cron_installer.sh

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

# Función para descargar archivos (usa curl o wget)
download_file() {
    local url=$1
    local output=$2

    if command -v curl &> /dev/null; then
        curl -sSL "$url" -o "$output"
    elif command -v wget &> /dev/null; then
        wget -q "$url" -O "$output"
    else
        echo "Error: Se necesita curl o wget instalado"
        return 1
    fi
}

# ============================================================================
# FUNCIONES DE CRON
# ============================================================================

# Instala un cron job que se ejecuta al reinicio (@reboot)
# Argumentos:
#   $1 - ID único para identificar el cron job (ej: "file-organizer", "screenshot-organizer")
#   $2 - Comando completo a ejecutar
#   $3 - Archivo de log (opcional)
install_reboot_cron() {
    local cron_id="$1"
    local command="$2"
    local log_file="${3:-}"
    
    if [ -z "$cron_id" ] || [ -z "$command" ]; then
        echo "Error: install_reboot_cron requiere cron_id y command"
        return 1
    fi
    
    # Crear archivo temporal con el crontab actual
    crontab -l 2>/dev/null > /tmp/crontab.tmp || touch /tmp/crontab.tmp
    
    # Eliminar entradas anteriores con el mismo ID
    grep -v "# CRON_ID:$cron_id" /tmp/crontab.tmp > /tmp/crontab.new || touch /tmp/crontab.new
    
    # Construir la línea del cron job
    local cron_line="@reboot $command"
    if [ -n "$log_file" ]; then
        cron_line="$cron_line >> $log_file 2>&1"
    fi
    cron_line="$cron_line # CRON_ID:$cron_id"
    
    # Añadir nueva entrada
    echo "$cron_line" >> /tmp/crontab.new
    
    # Instalar nuevo crontab
    crontab /tmp/crontab.new
    rm -f /tmp/crontab.tmp /tmp/crontab.new
    
    echo "Cron job '$cron_id' instalado correctamente"
    return 0
}

# Elimina un cron job por su ID
# Argumentos:
#   $1 - ID único del cron job
remove_cron_by_id() {
    local cron_id="$1"
    
    if [ -z "$cron_id" ]; then
        echo "Error: remove_cron_by_id requiere cron_id"
        return 1
    fi
    
    if crontab -l 2>/dev/null | grep -q "# CRON_ID:$cron_id"; then
        crontab -l | grep -v "# CRON_ID:$cron_id" | crontab -
        echo "Cron job '$cron_id' eliminado"
        return 0
    else
        echo "No se encontró cron job con ID '$cron_id'"
        return 1
    fi
}

# Verifica si un cron job existe por su ID
# Argumentos:
#   $1 - ID único del cron job
# Retorna: 0 si existe, 1 si no existe
cron_exists() {
    local cron_id="$1"
    crontab -l 2>/dev/null | grep -q "# CRON_ID:$cron_id"
}

# ============================================================================
# FUNCIONES DE INSTALACIÓN DE ARCHIVOS
# ============================================================================

# Copia archivos locales o descarga desde URL
# Argumentos:
#   $1 - Directorio de instalación
#   $2 - Lista de archivos separados por espacio
#   $3 - URL base para descarga (opcional, si no hay archivos locales)
install_files() {
    local install_path="$1"
    local files="$2"
    local base_url="${3:-}"
    
    mkdir -p "$install_path"
    
    local is_local=true
    for file in $files; do
        if [ ! -f "$file" ]; then
            is_local=false
            break
        fi
    done
    
    if $is_local; then
        echo "Detectado repositorio local, usando archivos locales..."
        for file in $files; do
            cp "$file" "$install_path/"
        done
    elif [ -n "$base_url" ]; then
        echo "Descargando archivos desde repositorio remoto..."
        for file in $files; do
            download_file "$base_url/$file" "$install_path/$file"
        done
    else
        echo "Error: No se encontraron archivos locales y no se especificó URL base"
        return 1
    fi
    
    return 0
}

# ============================================================================
# FUNCIONES DE UI
# ============================================================================

# Muestra un banner de instalación
show_install_banner() {
    local title="$1"
    echo "===================================="
    echo "  $title"
    echo "===================================="
    echo ""
}

# Muestra mensaje de instalación completada
show_install_complete() {
    local target_dir="$1"
    local log_file="$2"
    local install_path="$3"
    local run_command="$4"
    
    echo ""
    echo "===================================="
    echo "Instalación completada!"
    echo "===================================="
    echo ""
    echo "Configuración:"
    echo "  - Directorio: $target_dir"
    echo "  - Se ejecutará automáticamente al reiniciar"
    if [ -n "$log_file" ]; then
        echo "  - Logs: $log_file"
    fi
    echo ""
    echo "Comandos útiles:"
    echo "  # Ejecutar ahora:"
    echo "  $run_command"
    echo ""
    if [ -n "$log_file" ]; then
        echo "  # Ver logs:"
        echo "  tail -f $log_file"
        echo ""
    fi
    echo "  # Ver cron jobs instalados:"
    echo "  crontab -l | grep CRON_ID"
    echo ""
}

# Pregunta por un directorio con valor por defecto
# Argumentos:
#   $1 - Prompt a mostrar
#   $2 - Valor por defecto
# Retorna: El directorio seleccionado (echo)
ask_directory() {
    local prompt="$1"
    local default="$2"
    local result
    
    read -p "$prompt [$default]: " result
    result=${result:-$default}
    
    # Expandir ~ de forma segura (sin eval para evitar problemas con caracteres especiales)
    if [[ "$result" == "~"* ]]; then
        result="$HOME${result:1}"
    fi
    
    echo "$result"
}

# Verifica/crea directorio
# Argumentos:
#   $1 - Ruta del directorio
# Retorna: 0 si ok, 1 si cancelado
ensure_directory() {
    local dir="$1"
    
    if [ -d "$dir" ]; then
        return 0
    fi
    
    echo "Advertencia: El directorio '$dir' no existe."
    read -p "¿Crear directorio? (s/N): " create
    if [ "$create" = "s" ] || [ "$create" = "S" ]; then
        mkdir -p "$dir"
        echo "Directorio creado"
        return 0
    else
        read -p "¿Continuar de todos modos? (s/N): " cont
        if [ "$cont" = "s" ] || [ "$cont" = "S" ]; then
            return 0
        fi
        return 1
    fi
}
