# Organizador de Descargas

Script de Python que organiza automáticamente los archivos de tu carpeta de Descargas en subcarpetas según su tipo (imágenes, documentos, videos, etc.).

## Características

- Organiza archivos por extensión en carpetas predefinidas
- Se ejecuta automáticamente al iniciar el sistema (con cron)
- Configuración sencilla
- Sin dependencias externas
- Logs de actividad

## Instalación

```bash
curl -sSL https://raw.githubusercontent.com/xMigma/downloads-organizer/main/install.sh | bash
```

O si prefieres revisar el script primero:

```bash
curl -sSL https://raw.githubusercontent.com/xMigma/downloads-organizer/main/install.sh -o install.sh
chmod +x install.sh
./install.sh
```

El instalador te preguntará qué directorio organizar y lo configurará todo automáticamente.

### Ejecución manual

Para probar el script sin reiniciar:

```bash
# Usar el directorio por defecto (~/Downloads)
python3 main.py

# Especificar un directorio
python3 main.py ~/Descargas
```

### Ver logs

Los logs se guardan en `organizer.log`:

```bash
tail -f organizer.log
```

## Configuración

**Cambiar el directorio configurado:**

Si ya instalaste el script y quieres cambiar el directorio:

```bash
./uninstall.sh  # Elimina la configuración anterior
./install.sh    # Instala con el nuevo directorio
```

## Categorías de archivos

El script organiza los archivos en estas carpetas:

- **images**: jpg, jpeg, png, gif, bmp, svg, webp, etc.
- **videos**: mp4, avi, mkv, mov, wmv, flv, etc.
- **audios**: mp3, wav, flac, aac, ogg, m4a, etc.
- **documents**: pdf, doc, docx, txt, odt, etc.
- **compressed**: zip, rar, 7z, tar, gz, etc.
- **executables**: exe, msi, deb, rpm, appimage, etc.
- **code**: py, js, java, cpp, html, css, etc.
- **others**: cualquier otro tipo de archivo

Puedes personalizar estas categorías editando [extensions.py](extensions.py).

## Desinstalación

```bash
curl -sSL https://raw.githubusercontent.com/xMigma/downloads-organizer/main/uninstall.sh | bash
```

O si instalaste desde el repositorio:

```bash
./uninstall.sh
```

O manualmente:

```bash
crontab -l | grep -v 'file-organizer' | crontab -
rm -rf ~/.local/bin/file-organizer
```

Esto eliminará el cron job y los archivos instalados. Los archivos organizados permanecerán en su lugar.

## Estructura del proyecto

```
.
├── main.py              # Script principal
├── file_organizer.py    # Lógica de organización
├── extensions.py        # Definición de categorías y extensiones
├── install.sh           # Instalador
├── uninstall.sh         # Desinstalador
└── README.md            # Documentación
```

## Requisitos

- Python 3.8 o superior
- Linux/Unix con cron
- No requiere dependencias externas

## Solución de problemas

### El script no se ejecuta al reiniciar

Verifica que el cron job esté instalado:
```bash
crontab -l | grep file-organizer
```

Verifica que cron esté corriendo:
```bash
systemctl status cron
```

### Permisos denegados

Asegúrate de que tienes permisos de escritura en la carpeta a organizar:
```bash
ls -ld ~/Downloads
```

### Ver errores en los logs

```bash
tail -f organizer.log
```

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.
