---
title: "Showcases"
---

Een werkende showcase opent het gesprek. Je ziet hoe het kan werken en waar wijzigingen nodig zijn.

Drie showcases, met hetzelfde product en dezelfde intent, op drie manieren van werken:

| Showcase | Wat het laat zien | Status |
|---|---|---|
| [Demo](demo.md) | De kleinste way of working die de hele cirkel rond gaat. AI als versneller. | werkend |
| [Classic](classic.md) | Zoals het vaak gaat: alle deelproducten gaan samen naar productie. | placeholder |
| [Ideal](ideal.md) | Zoals het kan: een deelproduct gaat los naar productie. | placeholder |

Omdat product en intent gelijk blijven, vergelijk je alleen de manier van werken.

## ShowKitchen

Het product in elke showcase is ShowKitchen: software as a service voor restaurants, van een leverancier. Een open keuken, waar de gast ziet hoe er gekookt wordt.

Elke showcase is een eigen [FCD](/fcd/jouw-fcd/): **FCD-‹naam›**, met de configuratie in de repo **fcd-‹naam›**. Het product ShowKitchen is in elke showcase hetzelfde: één repository per deelproduct, zoals **sk-bestellen**. Pipeline en Dashboard zijn ook voor elke showcase hetzelfde: [fcd-pipeline](https://github.com/fcd-labs/fcd-pipeline) en [fcd-dashboard](https://github.com/fcd-labs/fcd-dashboard).

## Uit het declaratieve bestand

Elke showcase is vastgelegd in declaratieve bestanden. De platen worden daaruit gegenereerd. Het declaratieve bestand levert de plaat, niet andersom.

Wat het FCD-model vraagt en nog niet is ingevuld, staat op de plaat als backlog. Met de schakelaar zie je de plaat met en zonder backlog.

De bestanden en de generatoren staan in de repository [fcd-labs/fcd](https://github.com/fcd-labs/fcd): `fcd/` en `generators/`.
