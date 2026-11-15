# 📋 Documento de Asignación de Roles y Flujo de Trabajo

**Proyecto:** Adapting Farms with NASA Data (NASA Space Apps 2026)  
**Fecha:** 2026-11-15  
**Equipo:** 6 personas - Juan, Martin, Mati, Enzo, Topo y gualda

---

## 🎯 Resumen de los Nuevos Pasos a Realizar

Según la solicitud del usuario, el proyecto necesita estos 3 pasos críticos para ser usable por agricultores con escasos conocimientos tecnológicos:

1. **📱 Reducción de información con menús desplegables** - Simplificar la UI para agricultores con poca experiencia tecnológica
2. **💰 Quitar porcentajes y cálculos de ganancias** - Remover indicadores % y márgenes de renta del código
3. **🗺️ Separar datos por 3 zonas clave de San Luis (norte, centro, sur)** - Adaptar los datos a regiones específicas de la provincia

---

## 👥 Asignación de Roles por Integrante

Basado en el seguimiento del proyecto y las guías existentes, aquí asigno las responsabilidades:

### **Juan** - Líder de UI/Experiencia de Configuración
**Qué ha venido haciendo:** Ha estado a cargo del `Sidebar`, `ConfigForm` y `MapSelector` - la configuración inicial del lote.
**Nuevas responsabilidades:**
- Implementar menús desplegables (`<select>` o componentes custom) en lugar de selects complejos y pills de botones en `ConfigForm.jsx`
- Simplificar el formulario de regulación de agua a un solo menú desplegable [Solo lluvia / Con riego]
- Rediseñar las prioridades para usar menús en lugar de checkboxes multiples
- Asegurar que el flujo de configuración siga siendo funcional con el nuevo diseño simplificado
- **Archivos a modificar:** `Front/src/components/config/ConfigForm.jsx`, `Front/src/components/config/Sidebar.jsx`

### **Martin** - Especialista en Datos y Visualización
**Qué ha venido haciendo:** Ha trabajado con los datos mock (`mockData.js`), las estrategias de rotación y la visualización de resultados.
**Nuevas responsabilidades:**
- Remover todos los cálculos de porcentaje y márgenes de ganancia del `MOCK_SIMULATION_RESULT` en `mockData.js`
- Eliminar campos `margin`, `soilHealthScore %`, y métricas con % en las estrategias
- Reemplazar por descripciones en lenguaje simple (ej. "Mejor infiltración" en lugar de "+35% infiltración")
- **Archivos a modificar:** `Front/src/data/mockData.js`

### **Mati** - Experto en Datos Agrícolas y Zonificación
**Qué ha venido trabajando:** Ha estado trabajando con la guía del equipo de datos, `crops.yaml` y los indicadores climáticos.
**Nuevas responsabilidades:**
- Definir las 3 zonas clave de San Luis con características particulares:
  - **Norte:** Mayores precipitaciones, patrón de heladas diferente, cultivos más tolerantes a agua
  - **Centro:** Condiciones promedio de la provincia, rotaciones mixtas
  - **Sur:** Zona más áridá, menor lluvia, mayor estrés hídrico, cultivos resistentes a sequía
- Crear o adaptar `data/crops.yaml` para cada zona (3 versiones: norte, centro, sur)
- Asegurar que los rasgos de cultivo estén adaptados a las condiciones de cada zona
- **Archivos a crear/modificar:** `data/crops.yaml` (estructura por zonas), datos climáticos por zona

### **Enzo** - Integrador Backend-Frontend
**Qué ha venido haciendo:** Ha trabajado con la estructura del backend (FastAPI) y cómo conectar con el frontend.
**Nuevas responsabilidades:**
- Actualizar los schemas Pydantic en `backend/app/schemas.py` para que trabajen con la nueva estructura de datos (sin porcentajes, con zonas)
- Ajustar el motor de puntuación `engine.py` para que use los nuevos datos de cultivos por zona
- Asegurar que los endpoints API respondan con la nueva estructura (sin campos de ganancia/%)
- Conectar el nuevo `crops.yaml` por zona con el backend
- **Archivos a modificar:** `Backend/src/app/schemas.py`, `Backend/src/app/scoring/engine.py`

### **Topo** - Tester de Usabilidad y Validación
**Qué ha venido haciendo:** Ha participado en la coordinación general y revisión de integraciones.
**Nuevas responsabilabilities:**
- Probar la nueva interfaz simplificada con el objetivo de validar que agricultores con escasos conocimientos tecnológicos puedan usarla
- Verificar que los menús desplegables funcionen correctamente
- Confirmar que se hayan removido correctamente los porcentajes y cálculos de ganancia
- Validar que las 3 zonas de San Luis devuelvan información adecuada
- Reportar usabilidad y sugerencias de mejora
- **Tareas adicionales:** Diseñar/tests básicos, validar flujo completo

### **gualda** - Documentador y Coordinador General
**Qué ha venido haciendo:** Ha estado a cargo de las guías del equipo, documentación del proyecto y plan de trabajo paralelo.
**Nuevas responsabilabilidades:**
- Actualizar este documento (`contexto/roles_y_flujo_trabajo.md`) con el progreso de cada integrante
- Mantener actualizadas las guías de cada equipo (`guia_equipo_backend.md`, `guia_equipo_frontend.md`, `guia_equipo_datos.md`)
- Coordinar las reuniones de seguimiento y el flujo de trabajo
- Documentar los cambios realizados para la demo final
- **Archivos a actualizar:** Todos los documentos de contexto, especialmente los de guía por equipo

---

## 📊 Orden de Trabajo: Paso a Paso vs Simultáneo

### 🔄 Enfoque Recomendado: Híbrido (Principalmente Simultáneo con Dependencias Claras)

Dado que son 6 personas y el tiempo es limitado (1 día), el trabajo debe realizarse principalmente en **simultáneo**, pero con las siguientes dependencias:

#### **Fase 1: Trabajo Paralelo (Horas 1-3)**
Todos los equipos pueden trabajar en sus áreas asignadas al mismo tiempo:
- **Juan:** Implementa menús desplegables en ConfigForm/Sidebar
- **Martin:** Remueve porcentajes de mockData.js
- **Mati:** Define zonas Norte/Centro/Sur y adapta crops.yaml
- **Enzo:** Actualiza schemas y engine del backend para nueva estructura
- **Topo:** Empieza a probar versiones preliminares
- **gualda:** Documenta avances y coordina

**Orden crítico:** El trabajo de **Mati (zonas y crops.yaml)** debe completarse mínimamente para que **Enzo** pueda conectar el backend correctamente. Lo demás se puede hacer en paralelo.

#### **Fase 2: Integración y Testing (Horas 3-5)**
- Una vez que Juan termine los menús desplegables y Martin haya remueve los porcentajes
- Enzo integra los cambios del backend con los del frontend
- Topo testa el flujo completo con agricultores simulados
- gualda documenta todo el proceso

#### **Fase 3: Ajustes Finales (Horas 5-6)**
- Refinamientos menores en UI basados en pruebas de Topo
- Verificación de que todo el flujo funcione end-to-end
- Preparación del material para la demo

### 🛑 Puntos de Cuidado (No Bloquear el Trabajo)

1. **Mock data primero:** El backend (Enzo) debe poder trabajar con datos mock que tengan la nueva estructura (sin porcentajes, con zonas) desde temprano - esto permite que Juan y Martin avancen en sus cambios sin esperar datos reales.

2. **Zonas mínimas viables:** Mati debe definir al menos los rasgos esenciales por zona (no necesita ser perfecto desde el inicio). Enzo puede usar datos mock genéricos mientras Mati termina la zona completa.

3. **Remover porcentajes es independiente:** El trabajo de Martin para quitar porcentajes no bloquea a los demás - se puede hacer en paralelo y después integrar.

4. **Menús desplegables:** El trabajo de Juan en la UI no bloquea al backend - los selects pueden mantenerse como fallback mientras se implementan los menús nuevos.

---

## 📅 Cronograma Sugerido (6 Horas)

| Tiempo | Actividad | Responsable(s) |
|--------|-----------|----------------|
| **0:00 - 0:30** | Kickoff: Revisar este documento, aclarar dudas, definir dudas | Todo el equipo |
| **0:30 - 2:30** | **Trabajo paralelo Fase 1:**<br>- Juan: menús desplegables UI<br>- Martin: quitar % de mockData<br>- Mati: definir zonas + crops.yaml<br>- Enzo: actualizar schemas/backend<br>- Topo: empezar pruebas preliminares<br>- gualda: documentar inicio | Juan, Martin, Mati, Enzo, Topo, gualda |
| **2:30 - 3:30** | **Checkpoint integración:**<br>- Reunión corta (15 min) para verificar que schemas, mockData y UI estén alineados<br>- Ajustes menores si es necesario | Enzo (lidera), con presencia opcional de los demás |
| **3:30 - 5:00** | **Trabajo paralelo Fase 2:**<br>- Juan: completar y refinar menús desplegables<br>- Martin: verificar que % estén removidos totalmente<br>- Mati: terminar definición de zonas y validar crops.yaml<br>- Enzo: integrar backend con nuevo esquema<br>- Topo: testing completo flujo end-to-end<br>- gualda: actualizar documentación | Todos |
| **5:00 - 5:45** | **Testing con usuario simulado:**<br>- Topo prueba con "agricultor inexperto"<br>- Feedback sobre usabilidad de menús, simplicidad | Topo + Juan (ajustes UI) |
| **5:45 - 6:00** | **Cierre y próximos pasos:**<br>- gualda resume avances en documento<br>- Definir qué falta para la demo<br>- Planificar ajustes finales | Todo el equipo / gualda |

---

## 📁 Estructura de Archivos a Modificar/Crear

### Archivos que Juan modificará:
- `Front/src/components/config/ConfigForm.jsx` - Menús desplegables en lugar de selects/pills
- `Front/src/components/config/Sidebar.jsx` - Simplificar configuración

### Archivos que Martin modificará:
- `Front/src/data/mockData.js` - Remover `margin`, `soilHealthScore %`, métricas con %

### Archivos que Mati creará/modificará:
- `data/crops.yaml` - Nueva estructura con 3 zonas (norte, centro, sur)
- Datos climáticos/adaptados por zona

### Archivos que Enzo modificará:
- `Backend/src/app/schemas.py` - Ajustar para nueva estructura sin porcentajes
- `Backend/src/app/scoring/engine.py` - Usar nuevos datos de cultivos por zona

### Archivos compartidos/validados:
- `Front/src/data/mockData.js` - Mock data actualizada (validado por Martin y Enzo)
- `contexto/roles_y_flujo_trabajo.md` - Este documento (actualizado por gualda)

---

## ✅ Checklist de Validación Final

Antes de considerar los pasos completados, verificar:

- [ ] Menús desplegables funcionan en la UI de configuración
- [ ] No hay ningún campo de porcentaje (%) en las estrategias de rotación mostradas
- [ ] No hay cálculos de ganancias/renta en la interfaz
- [ ] Las 3 zonas de San Luis (norte, centro, sur) tienen datos de cultivos definidos
- [ ] El backend puede recibir y procesar solicitudes con la nueva estructura
- [ ] Un agricultor simulado puede completar una configuración y ver estrategias sin confusiones técnicas
- [ ] Todos los endpoints API responden correctamente con el nuevo formato
- [ ] Documentación actualizada en todos los archivos de contexto

---

## 💡 Consejos para el Éxito

1. **Commits frecuentes:** Cada quien hace commits a su área cada 1-2 horas para mantener `main` corriendo (como dice la guía)
2. **Comunicación constante:** Usar el canal de comunicación del equipo para dudas rápidas
3. **Mock data primero:** Los cambios de Juan y Martin deben ser testeables con mock data inmediatamente
4. **Zona mínima viable:** Mati puede empezar con rasgos generales por zona y ir refinando
5. **Demo con usuario real (simulado):** Los últimos 45 minutos deben probarse con alguien que no conozca la tecnología

---

**¿Están todos de acuerdo con esta asignación de roles y este flujo de trabajo?**  
Quedo a la espera de confirmaciones o ajustes por parte del equipo antes de comenzar la ejecución.