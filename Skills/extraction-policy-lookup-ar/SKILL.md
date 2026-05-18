---
name: extraction-policy-lookup-ar
description: Consulta sistemas internos de Libra para obtener el documento de póliza a partir de datos del asegurado o del vehículo
status: stub — integración técnica pendiente de definición con Juan Mazzochi
---

# Consulta de Póliza en Sistemas Internos (Policy Lookup AR)

Recupera el documento de póliza desde los sistemas internos de Libra Seguros usando los datos identificatorios disponibles: número de póliza, dominio del vehículo, datos del asegurado o tomador.

Este skill es una capa de integración — no analiza la póliza. El análisis lo hace `extraction-policy-summary-ar` sobre el documento que este skill devuelve.

## Contexto

- **Agente:** Mike (Extraction Agent)
- **Se activa cuando:** `poliza_path = null` y hay datos identificatorios disponibles en el output de `extraction-claim-summary-ar`
- **Output:** path al documento de póliza recuperado (para pasar a `extraction-policy-summary-ar`), o `null` con motivo si no se encuentra

## Campos de búsqueda (orden de prioridad)

1. `numero_poliza` — el más directo; extraído de la demanda por `extraction-claim-summary-ar`
2. `vehiculo.dominio` — dominio del vehículo asegurado (ej: AQX769)
3. `asegurado.dni` o `asegurado.cuit` — datos del tomador/asegurado
4. `asegurado.nombre` + `vehiculo.marca_modelo` — búsqueda combinada como fallback

## Input

```json
{
  "numero_poliza": "string | null",
  "vehiculo": {
    "dominio": "string | null",
    "marca": "string | null",
    "modelo": "string | null"
  },
  "asegurado": {
    "nombre": "string | null",
    "dni": "string | null",
    "cuit": "string | null"
  },
  "fecha_siniestro": "ISO date — para verificar vigencia de la póliza a esa fecha"
}
```

## Output

```json
{
  "found": true | false,
  "poliza_path": "ruta al documento recuperado | null",
  "numero_poliza": "string | null",
  "vigente_a_fecha_siniestro": true | false | null,
  "motivo_no_encontrado": "string | null",
  "confidence": "high | medium | low"
}
```

## TODO — Integración técnica (pendiente con Juan Mazzochi)

Los siguientes puntos deben definirse antes de implementar este skill:

- [ ] ¿Sistema de origen? (API REST / base de datos directa / sistema de gestión de pólizas)
- [ ] ¿Endpoint o query? (URL, método, autenticación)
- [ ] ¿Formato de respuesta del sistema? (JSON / XML / PDF / otro)
- [ ] ¿Credenciales de acceso? (API key / OAuth / usuario-contraseña)
- [ ] ¿El sistema devuelve el documento de póliza completo o solo datos estructurados?
- [ ] ¿Qué hacer si hay múltiples pólizas para el mismo vehículo/asegurado? (tomar la vigente a la fecha del siniestro)
- [ ] ¿El sistema tiene entorno de staging para pruebas?

Ver: `docs/policy-lookup-integration.md`

## Reglas

- Si `found = false`: no bloquear el pipeline. Continuar con `policy_summary = null` y marcar como pendiente en la entrega al abogado.
- Si `vigente_a_fecha_siniestro = false`: marcar como señal de atención crítica y escalar a Ali antes de continuar. Posible defensa de falta de cobertura por póliza no vigente al momento del siniestro.
- Si `found = true` pero `confidence = low` (ej: match solo por nombre sin DNI): registrar ambigüedad y marcar para revisión humana.
