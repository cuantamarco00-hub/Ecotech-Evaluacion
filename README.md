EcoTech Solutions – Evaluación N°3 

Sistema de consola en Python para EcoTech Solutions: gestión de empleados, departamentos,
proyectos y horas, con **inicio de sesión por roles** y consulta de **tipo de cambio desde una API externa**
(los datos se guardan en la BD local, hay historial y un respaldo si la API falla).

- Cómo ejecutarlo

1. Instalar dependencias: `pip install -r requirements.txt`
2. Encender MySQL en XAMPP y revisar los datos del archivo `.env` (`DB_ENGINE=sqlite` usa SQLite sin XAMPP).
3. **Solo la primera vez después de esta versión** (cambiaron las tablas), desde la carpeta `src`:
 python -m persistencia.crear_bd reiniciar
4. Ejecutar desde la carpeta `src`: `python main.py`

Al iniciar, el programa crea las tablas y las cuentas base si faltan (se puede repetir sin duplicar
datos ni reiniciar cuentas). Los datos de prueba completos se cargan desde el menú del administrador
(opción 1) o por terminal con `python -m persistencia.semilla_bd`.

| Usuario | Rol | Contraseña de prueba |
|---|---|---|
| `admin` | administrador | `Admin1234` |
| `funcionario` | funcionario | `Func1234` |

Las contraseñas se pueden cambiar con `ADMIN_PASSWORD` y `FUNCIONARIO_PASSWORD` en el `.env`.

## Organización del código (cada archivo, una responsabilidad)

| Carpeta | Qué hace |
|---|---|
| `src/menu.py`, `Menu_usuarios.py`, `menu_indicadores.py` | Menús: piden datos y muestran resultados. No tocan la BD. |
| `src/Servicios/` | Reglas del sistema: comprueban permisos (`permisos.py`), coordinan API, guardado y respaldo (`indicadores.py`). |
| `src/dominio/` | Clases con validaciones: `Empleado`, `Departamento`, `Proyecto`, `RegistroTiempo`, `Usuario`, `Indicador`. |
| `src/persistencia/` | DAO: único lugar donde se escribe SQL (siempre con parámetros). |

Recorrido de la API: **menú → servicio → `api_dolar` (consulta) → `DeserializadorIndicador` (JSON → `Indicador` validado) → `IndicadorDAO` (inserta o actualiza)**.

## ¿Qué puede hacer cada rol?

| | Administrador | Funcionario |
|---|---|---|
| Empleados y sus cuentas | CRUD y crear cuentas | – |
| Departamentos y gerente | CRUD y asignar gerente | – |
| Proyectos y asignaciones | CRUD y asignar/quitar empleados | Ver solo los suyos |
| Registros de tiempo | CRUD con validaciones | Registrar y ver solo los suyos, en proyectos asignados |
| Perfil | Ver y editar el suyo | Ver y editar el suyo (nombre, teléfono, correo) |
| Indicadores (API) e historial local | Sí | Sí |

El funcionario se identifica desde la sesión: nunca se le pide el ID de otra persona.
Cada servicio llama a `exigir_sesion()` o `exigir_admin()` **antes** de ejecutar.

## Seguridad aplicada

- Contraseñas guardadas solo con **hash bcrypt** (con sal); la cuenta está vinculada a un empleado.
- Validación de usuario/clave vacíos, largo, caracteres y 72 bytes máx. de bcrypt.
- Mensaje genérico en el login ("Usuario o contraseña incorrectos"): no se revela si el usuario existe.
- Consultas SQL parametrizadas; moneda de la API validada contra una lista de monedas admitidas.
- Errores de conexión/BD y de la API **sin detalles internos** (no se muestran rutas, SQL ni datos del `.env`).
- La API tiene timeout, reintentos y se valida el código HTTP; si falla, el programa continúa con el respaldo local.
- 3 intentos de login fallidos cierran el programa. Datos sensibles y claves de prueba en el `.env` (no se suben al repositorio).

## Guía para la demostración (evaluación)

1. **Preparar:** `python -m persistencia.crear_bd` y `python -m persistencia.semilla_bd` (dos roles + datos relacionados).
2. **Permisos:** entrar como `admin` y como `funcionario`; el funcionario no ve el menú de administración (y si se
   llamara a un servicio de admin, responde "Acción solo para administrador").
3. **Datos propios:** como funcionario ver perfil, proyectos asignados y registrar horas.
4. **API:** Indicadores → 1 (elegir moneda) → se muestran valor, unidad, fecha y origen.
5. **Conservar:** consultar dos veces el mismo día (sigue 1 fila); cerrar el programa, volver a entrar y ver el historial (opción 2).
6. **Falla:** desconectar internet y consultar: se muestra el último dato con origen "BD local". Con una moneda sin historial, informa y vuelve al menú.
7. **Explicar:** responsabilidades de cada carpeta y la mejora de seguridad con IA (abajo).

## Uso de IA y ajustes de seguridad

Usé Claude (Anthropic) como apoyo para revisar y ordenar el código. No usé lo que generó sin analizarlo; lo que cambió y por qué:

- **Verificación de roles (`permisos.py`):** el código comparaba `"administrador"` con `"Administrador"`, así que
  la comprobación de admin nunca coincidía. Se unificaron los roles en `Usuario.ROL_ADMIN` / `ROL_FUNCIONARIO` y
  se usan en todos los servicios. *Decisión:* usar constantes en un solo lugar en vez de textos repetidos.
- **Login (`Autenticacion.autenticar`):** imprimía "No se encontró la cuenta para el usuario: X", lo que permite
  descubrir qué usuarios existen. Se eliminó y se devuelve siempre el mismo mensaje.
- **Mensajes de error:** `ConnectionError` incluía el detalle del error de MySQL y `ejecutar_seguro` mostraba el
  error inesperado completo. Ahora se muestran mensajes genéricos.
- **Clases antiguas `SistemaDeAutenticacion` / `SeguridadDatos`:** usan SHA-256 sin sal; se **descartaron** para el
  login y se usa bcrypt (`Autenticacion.py`). Quedan solo como parte del UML.
- **Descartado/adaptado de lo sugerido:** el SQL `ON CONFLICT ... DO UPDATE` de la presentación solo funciona en SQLite, y el
  proyecto también usa MySQL; lo reemplacé por "buscar → insertar o actualizar" en `IndicadorDAO.guardar`, que funciona en ambos.
