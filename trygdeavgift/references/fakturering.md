# Fakturering (Invoicing)

## Overview

Fakturering handles the creation and management of invoices for trygdeavgift,
integrating with `faktureringskomponenten` which in turn manages OEBS.

## Architecture

```
Melosys-API
    │
    ▼
┌─────────────────────┐
│ Saksflyt Step       │
│ OpprettFakturaserie │
└─────────┬───────────┘
          │ REST
          ▼
┌─────────────────────┐
│ Fakturerings-       │
│ komponenten         │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│      OEBS           │
│ (Invoice System)    │
└─────────────────────┘
```

## Faktureringskomponenten Integration

### Location
`integrasjon/src/main/kotlin/.../faktureringskomponenten/`

### Key DTOs

```kotlin
FakturaserieDto {
    fakturaserieReferanse: String?  // Returned by create
    fodselsnummer: String
    fakturaGjelder: String
    referanseBruker: String
    referanseNAV: String
    perioder: List<FakturaseriePeriodeDto>
    fakturaMottaker: FakturaMottakerDto
    startdato: LocalDate
    sluttdato: LocalDate?
    // ...
}

FakturaseriePeriodeDto {
    startDato: LocalDate
    sluttDato: LocalDate
    enhetsprisPerManed: BigDecimal
    beskrivelse: String
}

FakturaMottakerDto {
    ident: String         // fnr or orgnr
    kontaktperson: String?
    // ...
}
```

### Operations

| Method | Description |
|--------|-------------|
| `opprettFakturaserie()` | Create new invoice series |
| `kansellerFakturaserie()` | Cancel existing series |
| `oppdaterFakturaMottaker()` | Update recipient |
| `hentFakturaserie()` | Get series details |
| `beregnTotalBeloep()` | Calculate total amount |

## Saksflyt Steps

### OPPRETT_FAKTURASERIE
Location: `saksflyt/src/main/kotlin/.../steg/fakturering/OpprettFakturaserie.kt`

**When called:**
- IVERKSETT_VEDTAK_FTRL flow
- IVERKSETT_VEDTAK_EOS flow
- IVERKSETT_VEDTAK_TRYGDEAVTALE flow

**Actions:**
1. Check if behandling already has fakturaserieReferanse
2. If exists and periods changed: kanseller old, create new
3. Build FakturaserieDto from trygdeavgiftsperioder
4. Call faktureringskomponenten.opprettFakturaserie()
5. Store fakturaserieReferanse on behandlingsresultat

### KANSELLER_FAKTURASERIE
Location: `saksflyt/src/main/kotlin/.../steg/fakturering/KansellerFakturaserie.kt`

**When called:**
- Annullering of membership
- Opphør of membership
- Period changes requiring new faktura

**Actions:**
1. Get existing fakturaserieReferanse
2. Call faktureringskomponenten.kansellerFakturaserie()
3. Store new referanse if returned

### SEND_FAKTURA_AARSAVREGNING
Location: `saksflyt/src/main/kotlin/.../steg/arsavregning/SendFakturaÅrsavregning.kt`

**When called:**
- IVERKSETT_VEDTAK_AARSAVREGNING flow

**Actions:**
1. Calculate difference from previous year
2. Create årsavregning faktura
3. Handle both positive (invoice) and negative (refund) amounts

### OPPDATER_FAKTURAMOTTAKER
Location: `saksflyt/src/main/kotlin/.../steg/fakturering/OppdaterFakturamottaker.kt`

**When called:**
- OPPDATER_FAKTURAMOTTAKER process type
- When fullmektig changes

## Betalingsvalg (Payment Choice)

```kotlin
enum class Betalingstype {
    FAKTURA,      // Invoice to mottaker
    KONTONUMMER   // Direct bank transfer (pensjonister)
}
```

Stored on `Fagsak.betalingsvalg` and affects whether faktura is created.

## Fakturamottaker

### Determination Logic
`TrygdeavgiftMottakerService.finnFakturamottaker()`:

1. Check if arbeidsgiver is fullmektig
2. Check fagsak.fullmektig
3. Default to bruker (person)

### Types
- **Person**: Invoice to the member
- **Arbeidsgiver**: Invoice to employer (fullmektig)
- **Fullmektig**: Invoice to designated representative

## Manglende Innbetaling (Unpaid Invoice)

### Kafka Consumer
Location: `service/src/main/kotlin/.../avgift/ManglendeFakturabetalingConsumer.kt`

**Flow:**
1. OEBS sends Kafka message about unpaid invoice
2. Consumer receives message
3. Creates OPPRETT_NY_BEHANDLING_MANGLENDE_INNBETALING prosess
4. Oppgave created for saksbehandler

### Message Processing
```kotlin
@KafkaListener(topics = ["melosys.manglende-fakturabetaling"])
fun handleMessage(message: ManglendeFakturabetalingDto) {
    // Find behandling by fakturaserieReferanse
    // Create new behandling
    // Create oppgave
}
```

## Event Listener

### FaktureringEventListener
Location: `service/src/main/kotlin/.../avgift/fakturering/FaktureringEventListener.kt`

Listens for behandling events to trigger fakturering updates:
- Status changes
- Period changes
- Mottaker changes

## Debugging

### Check Faktura Status
```bash
# Via faktureringskomponenten API (in test/local)
curl "http://localhost:8083/api/v1/fakturaserie/{referanse}"
```

### SQL Queries
```sql
-- All fakturaseriereferanser for case
SELECT br.fakturaserie_referanse, b.type, b.status, b.registrert_dato
FROM behandlingsresultat br
JOIN behandling b ON br.behandling_id = b.id
WHERE b.fagsak_id = :fagsakId
AND br.fakturaserie_referanse IS NOT NULL;

-- Find behandling for faktura
SELECT b.*, f.saksnummer
FROM behandling b
JOIN fagsak f ON b.fagsak_id = f.id
JOIN behandlingsresultat br ON br.behandling_id = b.id
WHERE br.fakturaserie_referanse = :referanse;
```

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No fakturaserieReferanse | Step not executed | Check prosessinstans for OPPRETT_FAKTURASERIE |
| Wrong mottaker | Fullmektig logic | Check fagsak.fullmektig, arbeidsgiver settings |
| Duplicate invoices | Multiple vedtak | Check for concurrent prosessinstanser |
| Amount mismatch | Period calculation | Verify trygdeavgiftsperioder match invoice |

## Related Confluence Pages

- [Samhandling Melosys og OEBS](https://confluence.adeo.no/spaces/TEESSI/pages/478274543)
- [Nye prosesser saksbehandling og fakturering](https://confluence.adeo.no/spaces/TEESSI/pages/432217812)
