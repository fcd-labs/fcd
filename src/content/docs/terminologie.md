---
title: "Terminologie"
---

Woorden lenen waar de markt ze heeft, alleen toevoegen wat de markt mist. De marktterm per object staat bij [het FCD-model](model.md).

## Full Circle Delivery

| Term | Betekenis |
|---|---|
| Full Circle Delivery (FCD) | De term voor het geheel: de hele cirkel rond, niet alleen continuous delivery. Een way of working, geen framework. Niet software development lifecycle. |
| Cirkel | Intentie → delivery → product → leren → weer intentie. |
| Gebruiker | Wie het product gebruikt. Niet klant: dat is de business. |
| Senang | Op je gemak, tevreden. Nu en later. |
| Perspectief | Een blik op de cirkel, met eigen kaders. |
| Kader | Eén richtinggevende uitspraak. Samen zijn de kaders de guardrails voor AI. Niet standaard (keurslijf), niet afspraak (vrijblijvend). In de code `Principle`. |
| Comply or explain | Je volgt het kader, of je legt uit waarom niet. |
| Afwijking | De explain bij een kader. Een mens keurt hem goed: de eigenaar. In de code `Explanation`. |
| FCD-model | Eén taal: de bouwstenen, per perspectief geplaatst. Niet CD-model. |
| Jouw FCD-model | Waar je staat, waar je heen wilt, welk perspectief aandacht nodig heeft. |
| Declaratief bestand | Jouw FCD-model vastgelegd: wat en waarom, reproduceerbaar. Het levert de platen, niet andersom. |
| FCD-taal | Eén taal voor mens en machine: de woorden en regels van het FCD-model (intent, deelproduct, kader, quality gate), met de woorden die de markt al kent. Het declaratieve bestand (`*.fcd.yaml`, `apiVersion: fcd/v0`) is de FCD-taal voor de machine. |
| Continuous delivery | Een perspectief binnen FCD: er is altijd een werkende weg naar productie. |
| Backlog | Wat het FCD-model vraagt en nog niet is ingevuld. Niet "gaten". |
| FCD-criteria | Betrouwbaar, veilig, volledig, effectief, efficiënt en budget. Voor het product én voor FCD. |

## Van intent tot product

| Term | Betekenis |
|---|---|
| Intent | Wat de gebruiker wil, vanuit de persona: persona en userstory, waarom (objective), meten (key result), gedrag als scenario's. Intent is intent, geen norm. |
| Persona | De gebruiker van het product. |
| Product | Deelproducten vormen samen een product. Het draait op productie. |
| Deelproduct | De eenheid van deployment en van release. Bestaat uit één of meer containers, elk met een eigen lifecycle. Een squad is eigenaar. |
| Container | Hierin draait een service. Gebouwd uit code en libraries. |
| Bouwen, deployen, releasen | Bouwen levert een container, deployen zet een deelproduct op een omgeving, releasen maakt een versie van een deelproduct beschikbaar voor de gebruiker. |
| Squad | Eigenaar van deelproducten. Samenstelling: mensen, mensen en AI-agents, of alleen AI-agents. |
| Contracten | Afspraken tussen deelproducten. Contract first; het schema is onderdeel van het contract. |
| Output | De software. |
| Outcome | Wat het voor de gebruiker oplevert. |

## Eigenaarschap en toetsen

| Term | Betekenis |
|---|---|
| People, process, product | Geldt op elk niveau. Het product van het ene niveau draagt het process van het volgende, tot aan het werkproces van de gebruiker. |
| Werkproces | Het process van de gebruiker. Eigenaar: de gebruiker zelf of de business van de gebruiker. |
| FCD-producten | De producten waarmee squads werken, zoals de pipeline en het dashboard. Draaiende FCD. |
| Eigenaar van | Niet "maken met": wie iets maakt, blijft verantwoordelijk. De tribe is eigenaar van FCD, squads zijn eigenaar van het product. |
| Verifiëren | Werkt het product goed? Gemeten met KPI's, voor de producten en de FCD-producten. Continu. |
| Valideren | Is product gelijk aan intent? Gemeten met de objective en de key results. Continu. |
| Momentopname | De status op een gekozen moment, gegenereerd uit de data. Voor de historie en trendanalyse. |

## Showcases

| Term | Betekenis |
|---|---|
| Showcase | Laat werkend zien hoe het kan. Het opent het gesprek. |
| ShowKitchen | Het product in de showcases: software as a service voor restaurants. |
| Demo, Classic, Ideal | De drie showcases: hetzelfde product, drie manieren van werken. Elke showcase is een paar: fcd-X (de way of working) en sk-X (het product). |
| Productplaat | Wat zit in wat, gegenereerd uit het declaratieve bestand. |
| Full Circle Delivery-plaat | Hoe het product ontstaat en levend blijft, gegenereerd uit het declaratieve bestand. |
