Explains the source code structure

# .py-filer

## Drought

### drought_clean.py

Denne .py-filen tar del i starten av prosjektet. Den brukes i all hovedsak til å erstatte "outliers" i kolonnene (bortsett fra fips, score og date som ikke er målte verdier), og den leter etter irrelevante, urealistiske temperaturverdier. Merk at dette kun er en type test, man kunne laget mange fler slike tester, men det er veldig mange målvariabler i csv-filen som brukes og det ville tatt lang tid å lage slike tester for samtlige kolonner.

### drought_pred_analysis.py

Denne filen tilhører oppgave 6 av prosjektet. Her tas det bruk av sk learn for å lage en lineær regresjonsmodell, og før det settes trenings- og test-sett opp for å forberede. For regresjon har det her blitt valgt scatterplot for å vise den lineære funksjonen tydelig satt opp mot de målte verdiene. Man ser klart og tydelig at en lineær modell ikke stemmer særlig godt med punktene (for det meste) med scatterplotten er likevel en veldig tydelig måte å vise prediksjon kontra virkleighet. Videre brukes også regplot som i denne sammenhengen strengt tatt blir samme type visualisering som vanlig sccatterplot, men valgte å beholde den likevel. Så bruktes i tillegg linjeplot, og den er fordelaktig på med tanke på at faktisk vs. predikert verdi settes opp mot hverandre, og man ser tydelig hvor den ene varierer mer enn den andre. Et lite minus er at med så mange punkter kan det se uoversiktlig ut, men alt i alt er det en solid visualisering. Til sist ble et søylediagram visualisert, og det ble litt det samme som linjeplottet, men muligens litt mindre uoversiktlig siden søylene ble smeltet sammen.

### drought_stat_analysis.py

Denne filen tilhører oppgave 4, dataanalyse. Her blir korrelasjonsverdier og p-verdi brukt for å si noe om korrelasjonen mellom variabler. Videre blir disse framstilt i drought.ipynb med søylediagram og et spider chart. Særlig spider chartet viser tydelig korrelasjonen mellom variabler, der man for eksempel ser at T2M samsvarer med T2M_MIN og T2M_MAX, noe som gir mening.

### drought_visual.py

Her kan Oliver skrive

### droughtEKTE.py

Dette er .py-filen som danner filtered1_data.csv. Her plukkes tre FIPS koder ut som begrenser antallet rader, og her finnes også funksjoner som danner grunnlaget for visualisering, det vil si at en csv-fil lages med for eksempel T2M for alle FIPS koder (hele USA), som muliggjør temperaturkartet i drought.ipynb. Annen viktig info er at en zip-fil lastes ned via URL, som så brukes i new_file()-funksjonen for å lage ny fil. Merk: dersom navnet er det samme på den nye csv-filen som den som allerede finnes i data, vil den gamle erstattes med den nye.


## Frost

### frost_data_collection.py
Denne filen henter data fra frostAPI. Flere av funksjonene er hjelpefunksjoner som bidrar til forståelse av datafilen for videre behandling. Videre er det flere funksjoner for rensing og klargjøring av data. Hovedresultatet fra denne filen er funksjonen final_data() som er en renset datafil, men den tar ikke hensyn til outliers, dette blir fikset i frost_data_analysis.py filen. 

### frost_data_analysis.py
En py fil som bygger videre på frost_data_collection.py. Denne filen inneholder en funksjon remove_outliers() som gir en forbedret versjon av final_data(). I tillegg er det flere funksjoner tilknyttet ulike former for analyse og litt plotting. Det er definert funksjoner for korrelasjonsanalyse, median, gjennomsnitt, standardavvik, outliers og noe mer. 

### frost_pred_analysis.py
Denne bygger videre på remove_outliers funksjonen fra frost_data_analysis.py. remove_outliers() er en forbedret versjon av final_data() og gir en klargjort datafil. Numpy blir essensielt i denne pyfilen. I denne py filen blir det hentet ut data fra hver mulige måned. Månedene får indekser 0, 1, 2, ..., n-te måned i noen av funksjonene slik at det blir enklere å sette opp matriseligningen som gir en prediksjon. Det blir benyttet minste kvadraters metode til å finne koeffisienter a og b slik at en prediksjon p_1(x) er gitt ved ax+b. x = {0, 1, 2, ..., n} siden det blir månedsindeksen. Hvis data tilhørende hver måned er gitt som b_vektor = {b_1, b_2, ... , b_n}, blir ligningssystemet seende noe slikt ut: for x = 0: b = b_1, x = 1: a + b = b_2, x = 2: 2a + b = b_2 osv. for de andre x-verdiene. Ligningssystemets venstre side gir matrisen A. Deretter løses A_T * A * x_hat = A_T * b_vector for x_hat der x_hat = (a, b). Resultatet a, b er resultatet av regresjonen og brukes videre til ulike plot som visualiserer ulike sammenhenger med regresjonsmodellen.

### frost_to_json_function.py
Dette er en funksjon sender data fra API til en json fil.

### frost_to_json_main.py
Det er denne py filen at frost_to_json funksjonen brukes til å sende rådata til en json fil og ferdigbehandlet data til en json fil. 