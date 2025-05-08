# Seguimiento de Tareas - Proyecto RRHH LL

Este documento rastrea el progreso de las tareas de desarrollo para el proyecto RRHH LL, siguiendo el plan y los principios definidos.

## Fase 1: Inicialización y Planificación
- [x] Ingestar contexto del proyecto (documentos proporcionados).
- [x] Descomponer el proyecto en tareas.
- [x] Crear archivo `seguimiento_tareas.md`.

## Fase 2: Configuración del Entorno
- [x] Inicializar repositorio Git.
- [x] Configurar ramas Git-flow (`develop`, `version`, `main`).

## Fase 3: Desarrollo Iterativo de Features (Frontend-First para F1, F2, F4)

### Feature 1: Gestión de Personal (CRUD)
- [x] **Frontend (Mobile):** Implementar UI y lógica para CRUD de Personal.
- [x] **Frontend (Web):** Implementar UI y lógica para CRUD de Personal (Basic tests passed, more tests needed).
- [x] **Frontend (Web):** Escribir pruebas completas para la funcionalidad CRUD de Personal.
- [ ] **Backend:** Implementar API y lógica para CRUD de Personal (Model, Controller, Service, Repository).
- [ ] **Backend:** Implementar migraciones de base de datos para tabla de Personal.

### Feature 2: Registro Diario de Trabajo con Imágenes
- [ ] **Frontend (Mobile):** Implementar UI y lógica para registro de trabajo, incluyendo captura y carga de imágenes.
- [ ] **Frontend (Mobile):** Implementar lógica de offline capability para registro de trabajo.
- [ ] **Frontend (Mobile):** Implementar lógica de geofencing para validación de ubicación.
- [ ] **Backend:** Implementar API y lógica para registro de trabajo.
- [ ] **Backend:** Implementar lógica para manejo y almacenamiento de imágenes (integración S3).
- [ ] **Backend:** Implementar migraciones de base de datos para tabla de Registros de Trabajo.

### Feature 4: Panel de Control del Empleador (Web)
- [ ] **Frontend (Web):** Implementar diseño y estructura del Panel de Control.
- [ ] **Frontend (Web):** Implementar visualización de datos clave (KPIs) en el Panel de Control.
- [ ] **Frontend (Web):** Implementar funcionalidades de filtrado y visualización de registros.

### Feature 3: Cálculo de Pago Semanal
- [ ] **Backend:** Diseñar e implementar Motor de Cálculo de Pago configurable.
- [ ] **Backend:** Implementar lógica para generación automática de períodos de pago semanal.
- [ ] **Backend:** Implementar API para acceso a datos de cálculo de pago.
- [ ] **Backend:** Implementar migraciones de base de datos para tablas relacionadas con cálculo de pago.

## Tareas Transversales
- [ ] Implementar Autenticación (JWT).
- [ ] Implementar Autorización (Role-Based).
- [ ] Configurar variables de entorno.
- [ ] Implementar manejo de tareas asíncronas (colas/workers).
- [ ] Implementar seguridad (encriptación, sanitización).
- [ ] Implementar estrategia de testing (Unit, Integration, E2E).
- [ ] Configurar CI/CD (placeholder).
- [ ] Configurar monitoreo y logging (placeholder).

## Futuras Features (Según documentos)
- [ ] Gestión Avanzada de Tareas.
- [ ] Gestión de Materiales (Solicitud/Aprobación inicial).
- [ ] Módulo de Reportes Personalizados Avanzado.
- [ ] Módulo de Fichaje / Reloj Digital con Validación Fotográfica.
- [ ] Módulo de Anticipos y Descuentos.
