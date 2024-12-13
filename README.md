**CRUD de Gestión y Manejo de inventario de un Hospital**

Este es un proyecto web desarrollado en **Python** utilizando el framework **Flask**. Permite gestionar un CRUD (Crear, Leer, Actualizar y Eliminar) pacientes
para que con esa data gestionar inventario y revisar diferentes reportes del mismo. Aparte esta realizado un CRUD de usuarios que pueden ingresar al Sistema.

**Roles:**

  **-Administrador**
  
  - Nombre: Ricardo 
  
  - Correo: rick03093@gmail.com
  
  - Contraseña: Piojo2016
    
  - Con este rol administramos tanto pacientes como usuarios (Validación de Correos - Dominios conocidos)
  
  **-Inventario**
  
  - Nombre: inventario
  
  - Correo: inventario@gmail.com
    
  - Contraseña: Piojo2018
    
  - En este rol se permite realziar los distintos reportes de Inventario


## Características principales
- Autenticación y gestión de usuarios.
- CRUD para pacientes(Diferentes datos y modelos de tablas referirse a la carpeta Models y ver las relaciones que hay para todos los modelos).
- Gestión de inventario.
- Conexión a base de datos mediante SQLAlchemy (configurable para Railway o local).

## Requisitos previos
Asegúrate de tener instalados los siguientes requisitos:
- **Python 3.8+**
- Gestor de paquetes **pip**
- MySQL (local o una instancia en Railway) {En el archivo main.py hay como conectarse a una instancia local o a un servicio deploy como Railway}


## Configuración inicial para correr el proyecto localmente
1. **Clonar el repositorio**:
   En la terminal bash:
   
       -git clone <URL_DEL_REPOSITORIO>
       
       -cd <NOMBRE_DEL_PROYECTO>
   
3. **Crear un entorno virtual**:
   
   En la terminal bash:
   
       -python -m venv venv
     
       -En Windows: venv\Scripts\Activate.ps1
    
5. **Instalar las dependencias**:

   En la terminal bash:
   
       -pip install -r requirements.txt
   
7. **Configura las variables de entorno**:
   
   Crear un archivo ".env" en el directorio raíz con la siguiente estructura, ajustando los valores según la  base de datos:

       -DB_USER=tu_usuario
       -DB_PASSWORD=tu_contraseña
       -DB_HOST=tu_host
       -DB_PORT=puerto_mysql
       -DB_NAME=nombre_de_la_base_de_datos
   

9. **Inicializar la base de datos**:
    
   Ejecutar el archivo "main.py" para verificar la conexión a la base de datos y realizar la configuración inicial.
   
   En la terminal bash:
   
       -python main.py
   

**Estructura del proyecto**
El proyecto está organizado de la siguiente forma:

controllers/

    auth_controller.py       # Controlador de autenticación
    dashboard_controller.py  # Controlador del panel de control
    main_controller.py       # Controlador principal
    patients_controller.py   # CRUD de pacientes
    inventory_controller.py  # Gestión de inventario

    
models/

    users_model.py           # Modelo para usuarios
    role_model.py           # Modelo para roles de los usuarios en el sistema
    patients_model.py        # Modelo para pacientes del hospital
    enfermedad_model.py        # Modelo para enfermedades
    patientenfermedad_model.py   # Modelo para unir los paceintes con las enfermedades de la base de datos
    medicine_model.py           # Modelo para registrar las medicinas manejadas en el hospital
    consumos_model.py           # Modelo para registrar consumos de medicinas por pacientes
    
    
static/

    # Archivos estáticos (CSS, JS) de algunas plantillas html
    
    
templates/

    # Plantillas HTML para las vistas de los resportes y los CRUD usuario y pacientes
    
    
main.py                     # Punto de entrada principal


requirements.txt            # Dependencias del proyecto


**Uso**
1. Inicializar la aplicación:
   En la terminal bash:
     -python main.py
   
2. Acceder a la aplicación en tu navegador en [http://127.0.0.1:5000](http://127.0.0.1:5000).
   
## Notas adicionales:
**Base de datos local**: Descomentar las líneas correspondientes en main.py para usar una base de datos local.

  **-Administrador**
  
  - Nombre: Ricardo 
  
  - Correo: rick03093@gmail.com
  
  - Contraseña: Piojo2016
    
  - Con este rol administramos tanto pacientes como usuarios (Validación de Correos - Dominios conocidos)
  
  **-Inventario**
  
  - Nombre: inventario
  
  - Correo: inventario@gmail.com
    
  - Contraseña: Piojo2018
    
  - En este rol se permite realziar los distintos reportes de Inventario


