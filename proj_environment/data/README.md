Describes the data directory and datasets

# Datasett

## filtered1_data.csv

Denne csv-filen blir dannet i notebooken drought.ipynb gjennom kode fra droughtEKTE.py (les mer under notebooks). Her har man valgt ut tre FIPS-koder som vil si ulike områder i USA, der FIPS kodene her alle representerer fylker i Alabama (Autauga, Baldwin og Barbour fylker).

## filtered1_data_cleaned.csv

Denne csv-filen er en slags modifikasjon av den foregående. Her har drought_clean.py blitt tatt i bruk for å erstatte "outliers" for hver kolonne (bortsett fra score, date og fips). Her brukes også standardavvik og gjennomsnitt i prosessen.

### Kolonnenavn

- fips: områder (fylker) i USA
- date: dato for måling av diverse værdata
- PRECTOT: total nedbør per dag
- PS: lufttrykk ved overflaten
- QV2M: luftfuktighet ved en høyde på 2 meter
- T2M: lufttemperatur (2 meter)
- T2MDEW: kondenspunkt (2 meter)
- T2MWET: våttemperatur (2 meter)
- T2M_MAX: maksimum temperatur (2 meter)
- T2M_MIN: minimum temperatur (2 meter)
- T2M_RANGE: temperaturvariasjon
- TS: overflatetemperatur
- WS10M: vindhastighet (10 meter)
- WS10M_MAX: maksimum vindhastighet (10 meter)
- WS10M_MIN: minimum vindhastighet (10 meter)
- WS10M_RANGE: variasjon i vindhastighet (10 meter)
- WS50M: vindhastighet (50 meter)
- WS50M_MAX: maksimum vindhastighet (50 meter)
- WS50M_MIN: minimum vindhastighet (50 meter)
- WS50M_RANGE: variasjon i vindhastighet (50 meter)
- score: en slags poengsum for å avgjøre brukbarhet (ukentlig)

## initial_data.json