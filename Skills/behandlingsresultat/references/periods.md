# Behandlingsresultat Period Types

Behandlingsresultat contains multiple period types representing different aspects of social security coordination.

## Period Type Overview

| Type | Purpose | Interface | Multiple Allowed |
|------|---------|-----------|------------------|
| `Lovvalgsperiode` | Which country's law applies | PeriodeOmLovvalg, AvgiftspliktigPeriode | Yes (but usually 1) |
| `Medlemskapsperiode` | Membership in Norwegian NI | AvgiftspliktigPeriode | Yes |
| `Anmodningsperiode` | Article 16 exception request | PeriodeOmLovvalg | Yes (but usually 1) |
| `Utpekingsperiode` | Provisional designation | PeriodeOmLovvalg | Yes |
| `HelseutgiftDekkesPeriode` | EEA pensioner health coverage | - | No (OneToOne) |

## Common Interfaces

### ErPeriode (Base)
```kotlin
interface ErPeriode {
    fun getFom(): LocalDate
    fun getTom(): LocalDate?
    fun overlapperMedÅr(year: Int): Boolean
}
```

### PeriodeOmLovvalg
Implemented by: Lovvalgsperiode, Anmodningsperiode, Utpekingsperiode
```kotlin
interface PeriodeOmLovvalg : ErPeriode {
    val lovvalgsland: Land_iso2
    val bestemmelse: LovvalgBestemmelse?
    val tilleggsbestemmelse: Tilleggsbestemmelse?
    val innvilgelsesresultat: InnvilgelsesResultat
    val medlemskapstype: Medlemskapstyper
}
```

### AvgiftspliktigPeriode
Implemented by: Lovvalgsperiode, Medlemskapsperiode
```kotlin
interface AvgiftspliktigPeriode : ErPeriode {
    val trygdeavgiftsperioder: Set<Trygdeavgiftsperiode>
    val innvilgelsesresultat: InnvilgelsesResultat
}
```

## Lovvalgsperiode

**Purpose**: Determines which country's social security legislation applies.

**Key attributes**:
```kotlin
@Entity
class Lovvalgsperiode {
    var fom: LocalDate
    var tom: LocalDate?
    var lovvalgsland: Land_iso2          // Country whose law applies
    var bestemmelse: LovvalgBestemmelse? // EU Reg 883/2004 article
    var tilleggsbestemmelse: Tilleggsbestemmelse?
    var innvilgelsesresultat: InnvilgelsesResultat  // INNVILGET, AVSLAATT, OPPHØRT
    var medlemskapstype: Medlemskapstyper  // PLIKTIG, FRIVILLIG, UNNTATT
    var dekning: Trygdedekninger?

    @OneToMany
    var trygdeavgiftsperioder: Set<Trygdeavgiftsperiode>
}
```

**Common bestemmelser (LovvalgBestemmelse)**:
- `ART_11_3_A` - Work in one country
- `ART_11_3_E` - Other persons
- `ART_12_1` - Posted workers
- `ART_13_1` - Work in multiple countries
- `ART_16_1` - Exception agreement

## Medlemskapsperiode

**Purpose**: Membership in Norwegian National Insurance (folketrygden).

**Key attributes**:
```kotlin
@Entity
class Medlemskapsperiode {
    var fom: LocalDate
    var tom: LocalDate?
    var innvilgelsesresultat: InnvilgelsesResultat
    var medlemskapstype: Medlemskapstyper
    var trygdedekning: Trygdedekninger?
    var bestemmelse: Bestemmelse?  // FTRL-specific

    @OneToMany
    var trygdeavgiftsperioder: Set<Trygdeavgiftsperiode>
}
```

## Anmodningsperiode

**Purpose**: Article 16 exception request sent to/received from foreign authority.

**Key attributes**:
```kotlin
@Entity
class Anmodningsperiode {
    var fom: LocalDate
    var tom: LocalDate?
    var lovvalgsland: Land_iso2
    var bestemmelse: LovvalgBestemmelse?
    var innvilgelsesresultat: InnvilgelsesResultat
    var sendtUtland: Boolean  // Sent to foreign authority
    var anmodetAv: String?    // Requesting entity

    @OneToOne
    var anmodningsperiodeSvar: AnmodningsperiodeSvar?  // Response from authority
}
```

## Utpekingsperiode

**Purpose**: Provisional designation of applicable law (EU/EFTA coordination).

**Key attributes**:
```kotlin
@Entity
class Utpekingsperiode {
    var fom: LocalDate
    var tom: LocalDate?
    var lovvalgsland: Land_iso2
    var bestemmelse: LovvalgBestemmelse?
    var innvilgelsesresultat: InnvilgelsesResultat
    var medlemskapstype: Medlemskapstyper
}
```

## Working with Periods

### Adding Periods
```kotlin
// Membership period
val periode = Medlemskapsperiode().apply {
    fom = LocalDate.of(2024, 1, 1)
    tom = LocalDate.of(2024, 12, 31)
    innvilgelsesresultat = InnvilgelsesResultat.INNVILGET
    medlemskapstype = Medlemskapstyper.PLIKTIG
}
behandlingsresultat.addMedlemskapsperiode(periode)
```

### Retrieving Periods
```kotlin
// Single period (throws if multiple)
val lovvalg = resultat.hentLovvalgsperiode()

// Optional (safe)
val lovvalg: Optional<Lovvalgsperiode> = resultat.finnLovvalgsperiode()

// Validated period of any type
val periode: PeriodeOmLovvalg? = resultat.finnValidertPeriodeOmLovvalg()
```

### Clearing Periods
```kotlin
resultat.clearMedlemskapsperioder()
resultat.clearLovvalgsperioder()

// Clear all via service
behandlingsresultatService.tømBehandlingsresultat(resultat)
```

## Debugging

### Find all periods for a result
```sql
-- Lovvalgsperioder
SELECT * FROM lovvalgsperiode WHERE behandlingsresultat_id = :id;

-- Medlemskapsperioder
SELECT * FROM medlemskapsperiode WHERE behandlingsresultat_id = :id;

-- Anmodningsperioder
SELECT * FROM anmodningsperiode WHERE behandlingsresultat_id = :id;

-- Utpekingsperioder
SELECT * FROM utpekingsperiode WHERE behandlingsresultat_id = :id;
```

### Find overlapping periods
```sql
SELECT p1.id, p2.id, p1.fom, p1.tom, p2.fom, p2.tom
FROM lovvalgsperiode p1
JOIN lovvalgsperiode p2 ON p1.behandlingsresultat_id = p2.behandlingsresultat_id
WHERE p1.id < p2.id
AND p1.fom <= COALESCE(p2.tom, DATE '9999-12-31')
AND COALESCE(p1.tom, DATE '9999-12-31') >= p2.fom;
