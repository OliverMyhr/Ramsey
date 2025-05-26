Describes the notebooks directory

# Kjøring av .py-filer

## Drought

I drought.ipynb kjøres alt av .py-filer for å rense filtered1_data.csv, samt både statistisk og prediktiv analyse av Drought, og diverse visualiseringer.

### Dannelse av csv-filer

I andre rute (under imports) i drought.ipynb får man valget om å danne en ny csv-fil. Merk at dersom man velger å lage en ny fil vil dette ta en stund, da over 2.2 millioner linjer håndteres. Et forhåndsbestemt, tilfeldig sett med FIPS-koder (1001, 1003, 1005) har blitt valgt som eksempel, og da den opprinnelige fila inneholder værdata for 16 år i USA, vil bare en FIPS kode gi over 6000 linjer. I dette prosjektet fokuserer man da i hovedsak på omtrent 18 000 linjer (tre FIPS koder). Et unntak er visualiseringen av kartet over hele USA med værdata (temperatur), der man åpenbart har tatt utgangspunkt i alle FIPS koder. I tillegg vil det lages en csv-fil med kun temperatur data, og en for nedbør data. Disse to brukes i visualiseringsdelen lenger nede i .ipynb-filen.


## Frost

### frost_data_collection_notebooks.ipynb
I denne filen kjøres alt av resultater fra tilhørende py fil: frost_data_collection.py

### frost_data_analysis_notebooks.ipynb
I denne filen kjøres alt av resultater fra tilhørende py fil: frost_data_analysis.py

### frost_pred_analysis_notebooks.ipynb
I denne filen kjøres alt av resultater fra tilhørende py fil: frost_pred_analysis.py

### frost_to_json_visual.ipynb
I denne filen kjøres alt av resultater fra tilhørende py fil: frost_to_json_visual.py