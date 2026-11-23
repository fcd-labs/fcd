---
title: "Hoe Demo is gemaakt"
---

Deze showcase is gemaakt door een product owner, een chat en een AI-squad. Het antwoord op het experiment: één intent en één beschrijving van een deelproduct zijn genoeg, mits het harnas er staat.

## Kennis in het model

AI heeft FCD niet bedacht. Het FCD-model bundelt vakkennis over kwaliteit, testen, audit, releasen en continuous delivery: de kaders, de quality gates, comply or explain, één bron. Die kennis vormt het harnas. AI hielp het model uit te werken en de showcase te bouwen.

## Eén intent

Het begon met één zin: als gast wil ik uit een menu kiezen, zodat mijn bestelling bij keuken, bar en kassa terechtkomt. En met één vraag: is één intent, met een beschrijving van het deelproduct, genoeg voor een AI-squad?

## Twee sporen tegelijk

Het model en de showcase groeiden parallel. Het model gaf de showcase richting; de showcase liet zien waar het model nog niet klopte. Het model groeide eerst in gesprekken in de chat; de showcase volgde in negen dagen. Alles in vrije tijd, naast ander werk.

## Drie rollen

| Rol | Wie | Wat |
|---|---|---|
| Product owner | sim007 | Het wat en waarom, de besluiten, de Goedkeuring |
| Denkpartner | Claude in de chat | Het model, de FCD-taal, de site en de platen; de opdrachten voor Claude Code |
| AI-squad | Claude Code | ShowKitchen, de Pipeline en het Dashboard; eerst een voorstel, dan pushen |

## Ook een cirkel

Een intent werd in de chat een opdracht. Claude Code maakte een plan, de product owner koos, en Claude Code bouwde, testte en meldde terug. Met die terugmelding werd de site bijgewerkt. Wat geleerd werd, werd de volgende intent.

## Wat schuurde, en wat het opleverde

- **De site liep achter op de showcase.** Daaruit kwam één bron: de configuratie staat in fcd en gaat naar de showcase, niet andersom.
- **Woorden doen ertoe.** Procesplaat werd Full Circle Delivery-plaat, proces werd delivery, en de FCD-taal kreeg een naam.
- **De AI vond een tegenspraak in de kaders:** een afwijking op een kader waarbij explain niet mocht. Nu controleert de generator dat zelf.
- **Het harnas is niet af.** Wat ontbreekt, is backlog: een keuze, geen gat.

## Het antwoord

Ja, mits het harnas er staat. Wat de AI-squad maakte, ging door dezelfde stappen en quality gates, en de besluiten bleven bij de product owner. AI needs delivery. Delivery needs AI.

## Het bewijs

De intent: [mvp0-fcd-demo.md](https://github.com/fcd-labs/fcd-demo/blob/main/docs/mvp0-fcd-demo.md). Stand 23 november 2026:

| Repository | Commits | Met de AI-squad als co-auteur |
|---|---|---|
| [sk-bestellen](https://github.com/fcd-labs/sk-bestellen/commits/main) | 34 | 29 |
| [fcd-pipeline](https://github.com/fcd-labs/fcd-pipeline/commits/main) | 53 | 42 |
| [fcd-dashboard](https://github.com/fcd-labs/fcd-dashboard/commits/main) | 56 | 50 |
| [fcd-demo](https://github.com/fcd-labs/fcd-demo/commits/main) | 59 | 46 |
| **Totaal** | **202** | **167** |

Kijk zelf: de regel "Co-Authored-By" in een commit laat zien dat de AI-squad meeschreef.
