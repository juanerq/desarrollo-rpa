# Prueba tecnica RPA (DATA)
## Sobre el proyecto

Siguiendo las [instrucciones](https://ordinary-increase-e87.notion.site/RPA-DATA-2da37f1d8e3b46bcbece442ca238678c) proporcionadas, se implementó el servicio dentro de un contenedor Docker. La elección de esta herramienta se fundamentó en su facilidad de despliegue y ejecución, lo que optimiza el proceso y asegura una mayor eficiencia en la gestión del servicio.

La finalidad de este servicio es ejecutarse diariamente en el horario establecido, con el propósito de verificar los usuarios que posean tres o más órdenes en estado "returned" o "cancelled" en el mes configurado.


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

    | Columna                | Tipo              | Descripción                                        |
    |------------------------|-------------------|----------------------------------------------------|
    | shipping_id            | ObjectId          | Id de envio                                        |
    | shipping_date          | datetime          | Fecha de envio                                     |
    | shipping_status        | string            | Estado admitidas: returned - cancelled - completed |
    | order_vendor_dbname    | ObjectId          | Relación del usuario                               |

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
  - `EMAIL` correo que hará el envio de los mensajes
  - `EMAIL_PASS` contraseña de aplicación en google, pasos para generarla
    - Ingresar en tu cuenta de Gmail a `Gestionar tu cuenta de Google`
    - Buscar `Contraseñas de aplicaciones`
    - En el campo `App name` ingresar el nombre deseado de la llave
    - Click en `Crear`
    - Copiar la llave y pegar en este campo
  - `EXECUTE_TIME` hora de ejecución diaria en formato militar
  - `TEST_MAIL` Correo al que se simulará el envío de correos a los usuarios
  - `MONITOR_IN_MONTH` Mes en que se hará el monitoreo, formato año-mes, por defecto es el mes actual
  - `MONGO_URL` Leer explicación para configurar la URL de conexion que esta en el .env.example
  
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

Al ejecutar el servicio
- Si existe el archivo `shipments-data.csv` en la carpeta `files` se eliminaran las colecciones (users, shippings) y se poblará la base de datos con el archivo CSV.
- Se realizará el monitoreo a la hora configurada.

### Recrear contenedor del servicio

```bash
docker compose up my-service -d --build
```

### Detener ejecución del servicio

```bash
docker compose down
```

### Ver logs del servicio

```bash
docker compose logs -f my-service
```