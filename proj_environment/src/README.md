Explains the source code structure

# .py-filer

## Drought

### drought_clean.py

Denne .py-filen tar del i starten av prosjektet. Den brukes i all hovedsak til å erstatte "outliers" i kolonnene (bortsett fra fips, score og date som ikke er målte verdier), og den leter etter irrelevante, urealistiske temperaturverdier. Merk at dette kun er en type test, man kunne laget mange fler slike tester, men det er veldig mange målvariabler i csv-filen som brukes og det ville tatt lang tid å lage slike tester for samtlige kolonner.

### drought_pred_analysis.py

Denne filen tilhører oppgave 6 av prosjektet. Her tas det bruk av sk learn for å lage en lineær regresjonsmodell, og før det settes trenings- og test-sett opp for å forberede. For regresjon har det her blitt valgt scatterplot for å vise den lineære funksjonen tydelig satt opp mot de målte verdiene. Man ser klart og tydelig at en lineær modell ikke stemmer særlig godt med punktene (for det meste) med scatterplotten er likevel en veldig tydelig måte å vise prediksjon kontra virkleighet. Videre brukes også regplot som i denne sammenhengen strengt tatt blir samme type visualisering som vanlig sccatterplot, men valgte å beholde den likevel. Så bruktes i tillegg lineplot, og den er fordelaktig på med tanke på at faktisk vs. predikert verdi settes opp mot hverandre, og man ser tydelig hvor den ene varierer mer enn den andre. Et lie minus er at med så mange punkter kan det se uoversiktlig ut, men alt i alt er det en solid visualisering.

### drought_stat_analysis.py



### drought_visual.py



### droughtEKTE.py



## Frost data
