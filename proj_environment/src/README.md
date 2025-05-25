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

## Frost data
