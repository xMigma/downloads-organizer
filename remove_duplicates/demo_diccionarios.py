# PASO 1: Agrupar por TAMAÑO (filtro rápido)
files_by_size = {
    5242880: ["foto_playa.jpg", "foto_playa(1).jpg", "paisaje.jpg"],
    10485760: ["video.mp4", "video_backup.mp4"],
    2097152: ["cancion.mp3"],  # ← Solo 1 archivo, se descarta
    8388608: ["documento.pdf", "factura.pdf", "manual.pdf"],
}

# PASO 2: Agrupar por HASH MD5 (confirma duplicados)
hash_duplicates = {
    "a1b2c3d4...": ["foto_playa.jpg", "foto_playa(1).jpg"],  # ← DUPLICADOS
    "x9y8z7w6...": ["paisaje.jpg"],                          # ← Único
    "m3n4o5p6...": ["video.mp4", "video_backup.mp4"],        # ← DUPLICADOS
    "q7r8s9t0...": ["documento.pdf"],                        # ← Único
    "j1k2l3m4...": ["factura.pdf", "manual.pdf"],            # ← DUPLICADOS
}
