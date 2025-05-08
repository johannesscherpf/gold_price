# Data Mining



## Nächste Schritte


## GitLab
- Projektstruktur im GitLab anlegen:
    - Branches anlegen
    - requirements.txt
    - gitignore
    - usw.
    --> ich bin da nicht so gut drin, kennt ihr euch besser aus?

## Datenbeschaffung
- Daten einlesen
    - Goldpreis API von Alpha Vantage
    - Nachteil: Man kann nur 25x pro Tag abrufen. Die habe ich heute schon ausgeschöpft. Wir sollten in Zukunft   evtl. als csv zwischenspeichern.
    - Yahoo Finance API für weitere Variablen
    - weitere Datenquellen?

## Data Understanding
- wir sollten die Daten überprüfen
 --> nach Ausreißern schauen (Maximale und Minimale Werte)
    --> Graphisch mit Boxplot/Histogramm
 --> auf Vollständigkeit testen (für jeden Tag ein Wert)
- evtl. Abgleich einzelner Datenpunkte mit den "echten" Werten

- dann können wir ein paar Visualisierungen machen
    --> z.B. Goldpreisentwicklung über die Zeit
    --> Scatterplot mit Goldpreis/Ölpreis
    --> wir können uns weitere Sachen überlegen

## Datenintegration
    - wir sollten uns darauf einigen, wie weit wir in die Vergangenheit schauen wollen. Ich würde ab 01.01. 2020 vorschlagen. Die API von Alpha Vantage geht bis 2019 aber in 2019 waren einige seltsame Werte drinnen.
    - wir können darauf achten, dass wir pro Tag immer einen Wert haben
    - wir können die unterschiedlichen Variablen dann in einen gesamten Datensatz integrieren


## Weiteres Vorgehen
- für das weitere Vorgehen können wir dann vielleicht in ein paar Wochen weiter überlegen