# Prueba tecnica RPA (DATA)
## Sobre el proyecto

Con base a estas [instrucciones](https://ordinary-increase-e87.notion.site/RPA-DATA-2da37f1d8e3b46bcbece442ca238678c) se realizo el servicio el cual se ejecuta en un contenedor de Docker, se elegio esta herramienta por su faciliad de despliegue y ejecución

### Curiosidades
- **Patrones de diseño**
  - **Hexagonal**

    El uso de esta arquitectura busca proporcionar una mayor escalabilidad para realizar cambios en el software, minimizando las dependencias hacia paquetes de terceros. La organización de carpetas se encarga de estructurar de manera clara la lógica de negocio, facilitando así la comprensión y el mantenimiento del código.

  - **Observador**
  
    Se aplicó para lograr flexibilidad en las notificaciones, permitiendo la integración con diversas herramientas (correos electrónicos, mensajes SMS, bases de datos, etc), al cumplirse ciertos criterios.

- **Colecciones db**
  - **users**

    | Columna       | Tipo           | Descripción                           |
    |---------------|----------------|---------------------------------------|
    | user_id       | ObjectId       | ID del usuario                        |
    | username      | string         | Nombre de usuario                     |
    | email         | string         | Correo                                |
    | phone_number  | string         | Número de telefono                    |

  - **shippings**

    | Columna                | Tipo              | Descripción                            |
    |------------------------|-------------------|----------------------------------------|
    | shipping_id            | ObjectId          | Id de envio                            |
    | shipping_date          | datetime          | Fecha de envio                         |
    | shipping_status        | string            | Estado admitidas: returned - cancelled |
    | order_vendor_dbname    | ObjectId          | Relación del usuario                   |

  - **logs_sent_messages**

    | Columna       | Tipo           | Descripción                           |
    |---------------|----------------|---------------------------------------|
    | user_id       | ObjectId       | ID del usuario                        |
    | shippings     | list[ObjectId] | IDs de envíos                         |
    | date          | datetime       | Fecha de envío del mensaje            |



## Pasos a seguir

### 1. Clonar repositorio 

```bash
git clone https://github.com/juanerq/desarrollo-rpa.git
```

### 2. Archivo de datos (csv)

- Copiar archivo CSV en la carpeta "files".
- Renombrar el archivo con el nombre `shipments-data.csv`.

### 3. Configurar variables de entorno
- Basarse en el archivo `.env.example`
- Llenar estos campos
  - `EMAIL` correo donde van a llegar los mensajes
  - `EMAIL_PASS` contraseña de aplicación en google, pasos para generarla
    - Gestionar tu cuenta de Google
    - Buscar `Contraseñas de aplicaciones`
    - En el campo `App name` ingresar el nombre deseado de la llave
    - Click en `Crear`
    - Copiar la llave y pegar en este campo
  - `EXECUTE_TIME` hora de ejecución diaria en formato militar
  - `TEST_MAIL` Correo al que se simulará el envío de correos a los usuarios
  
<br/>

> En la terminal posicionarse donde se aloja el proyecto clonado

### 4. Desplegar base de datos Mongo (local)

```bash
docker compose up mongo-db -d
```

### 5. Ejecutar servicio

```bash
docker compose up my-service -d
```

Al ejecutar el servicio, se poblará la base de datos con el archivo CSV y se realizará el monitoreo a la hora configurada.

### Detener ejecución del servicio

```bash
docker compose down
```

### Ver logs del servicio

```bash
docker compose logs -f my-service
```