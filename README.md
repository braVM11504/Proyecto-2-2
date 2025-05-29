# INFORME DE PROYECTO: SISTEMA DE PARQUEADEROS

# Resumen 
Este proyecto implementa un sistema de control y monitoreo de parqueaderos utilizando Python y PyQt5. Se integran funcionalidades como el registro de usuarios, autenticación con credenciales, generación de códigos QR personalizados y visualización de espacios disponibles mediante una cámara IP. El sistema permite una asignación automática de espacios, evitando repeticiones y manteniendo una interfaz gráfica intuitiva y funcional.

# 1. FUNCIONALIDADES PRINCIPALES DEL PROGRAMA
- Registro y autenticación de usuarios mediante una interfaz gráfica (PyQt5).
- Validación de credenciales a través de un servidor con `parking_client`.
- Generación y envío automático de códigos QR al correo del usuario.
- Asignación dinámica de puestos de parqueo según disponibilidad y rol.
- Visualización del puesto asignado en pantalla.
- Integración de cámara IP para mostrar el estado visual en tiempo real del parqueadero.
- Restricción de tamaño de ventana para mejorar la experiencia de usuario.
- Verificación de campos vacíos y manejo de errores en la conexión servidor-cliente.


# 2. ARCHIVOS DEL PROYECTO

- {interfaz}(): Interfaz gráfica diseñada en Qt Designer.
- {parking_client}(): Módulo cliente que se comunica con el servidor.
- {qrscan}(): Hilo que escanea el codigo QR 
- {parking_server}(): Servidor del programa 
- {users}(): Modulo de las funciones necesarias para el corecto funcionamiento del codigo


# 3. RESULTADOS Y ESTADO ACTUAL
El sistema está funcional y ha sido probado exitosamente en múltiples escenarios. Se logró una integración estable entre la interfaz gráfica, el servidor de validación. Los códigos QR se generan y envían correctamente, y los puestos de parqueo se asignan sin repetición. El sistema puede ser extendido fácilmente para incluir más roles, mejorar el análisis de imagen o integrarse a sistemas de acceso físico automatizado.
