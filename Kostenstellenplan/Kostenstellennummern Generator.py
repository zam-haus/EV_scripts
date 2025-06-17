#!/usr/bin/env python3

s = """23	/010101	Gebäude Betrieb – Abgaben – Erbzins
23	/010102	Gebäude Betrieb – Abgaben – Grundsteuer
23	/010103	Gebäude Betrieb – Abgaben – Straßenreinigung
23	/010104	Gebäude Betrieb – Abgaben – Schmutzwasser
23	/010105	Gebäude Betrieb – Abgaben – Rundfunkbeitrag
23	/010106	Gebäude Betrieb – Abgaben – Niederschlagswasser
23	/010199	Gebäude Betrieb – Abgaben – Sammel
23	/010201	Gebäude Betrieb – Versicherung – Gebäudeversicherung
23	/010202	Gebäude Betrieb – Versicherung – PV-Versicherung
23	/010299	Gebäude Betrieb – Versicherung – Sammel
23	/010301	Gebäude Betrieb – Müllentsorgung – Restmüll
23	/010302	Gebäude Betrieb – Müllentsorgung – Sperrmüll
23	/010303	Gebäude Betrieb – Müllentsorgung – Sondermüll
23	/010399	Gebäude Betrieb – Müllentsorgung – Sammel
23	/010401	Gebäude Betrieb – Betriebsmittel (Energie, Wasser) – Strom
23	/010402	Gebäude Betrieb – Betriebsmittel (Energie, Wasser) – Gas
23	/010403	Gebäude Betrieb – Betriebsmittel (Energie, Wasser) – Wasser
23	/010499	Gebäude Betrieb – Betriebsmittel (Energie, Wasser) – Sammel
23	/010501	Gebäude Betrieb – Verbrauchsmaterial – Sanitär
23	/010502	Gebäude Betrieb – Verbrauchsmaterial – Erstehilfe Aussstattung
23	/010503	Gebäude Betrieb – Verbrauchsmaterial – Licht
23	/010504	Gebäude Betrieb – Verbrauchsmaterial – Reinigungsmittel
23	/010599	Gebäude Betrieb – Verbrauchsmaterial – Sammel
23	/010601	Gebäude Betrieb – wiederkehrende Kosten (z.B. Wartung) – Aufzüge
23	/010602	Gebäude Betrieb – wiederkehrende Kosten (z.B. Wartung) – Brandschutzeinrichtung
23	/010603	Gebäude Betrieb – wiederkehrende Kosten (z.B. Wartung) – Elektrische Geräte (VDE)
23	/010604	Gebäude Betrieb – wiederkehrende Kosten (z.B. Wartung) – Rolltore
23	/010605	Gebäude Betrieb – wiederkehrende Kosten (z.B. Wartung) – PV
23	/010606	Gebäude Betrieb – wiederkehrende Kosten (z.B. Wartung) – Heizung
23	/010699	Gebäude Betrieb – wiederkehrende Kosten (z.B. Wartung) – Sammel
23	/010701	Gebäude Betrieb – Reinigung – Gebäudereinigung
23	/010702	Gebäude Betrieb – Reinigung – Winterdienst
23	/010799	Gebäude Betrieb – Reinigung – Sammel
23	/010801	Gebäude Betrieb – Reparaturen – am Haus
23	/010802	Gebäude Betrieb – Reparaturen – Haustechnik
23	/010803	Gebäude Betrieb – Reparaturen – Mobiliar
23	/010805	Gebäude Betrieb – Reparaturen – IT
23	/010899	Gebäude Betrieb – Reparaturen – Sammel
23	/0199	Gebäude Betrieb – Sammel
23	/020101	Personal – Angestellte ZAM ges. – Gehalt und Lohnnebenkosten
23	/020103	Personal – Angestellte ZAM ges. – Reisekosten
23	/020104	Personal – Angestellte ZAM ges. – Fortbildungskosten
23	/020105	Personal – Angestellte ZAM ges. – Betriebsmittel
23	/020199	Personal – Angestellte ZAM ges. – Sammel
23	/020201	Personal – Betreuung Werkstätten
23	/020401	Personal – Betreuung Programm
23	/020501	Personal – Betreuung Ehrenamt
23	/020601	Personal – Dienstleistungen & Honorare
23	/0299	Personal – Sammel
23	/030101	Werkstätten – Holz – Anschaffungen
23	/030102	Werkstätten – Holz – Wartung
23	/030103	Werkstätten – Holz – Betriebsmittel
23	/030104	Werkstätten – Holz – Material
23	/030105	Werkstätten – Holz – Reinigung und Entsorgung
23	/030106	Werkstätten – Holz – Angebote
23	/030199	Werkstätten – Holz – Sammel
23	/030201	Werkstätten – Metall – Anschaffungen
23	/030202	Werkstätten – Metall – Wartung
23	/030203	Werkstätten – Metall – Betriebsmittel
23	/030204	Werkstätten – Metall – Material
23	/030205	Werkstätten – Metall – Reinigung und Entsorgung
23	/030206	Werkstätten – Metall – Angebote
23	/030299	Werkstätten – Metall – Sammel
23	/030301	Werkstätten – Elektronik – Anschaffungen
23	/030302	Werkstätten – Elektronik – Wartung
23	/030303	Werkstätten – Elektronik – Betriebsmittel
23	/030304	Werkstätten – Elektronik – Material
23	/030305	Werkstätten – Elektronik – Reinigung und Entsorgung
23	/030306	Werkstätten – Elektronik – Angebote
23	/030399	Werkstätten – Elektronik – Sammel
23	/030401	Werkstätten – Prototypen – Anschaffungen
23	/030402	Werkstätten – Prototypen – Wartung
23	/030403	Werkstätten – Prototypen – Betriebsmittel
23	/030404	Werkstätten – Prototypen – Material
23	/030405	Werkstätten – Prototypen – Reinigung und Entsorgung
23	/030406	Werkstätten – Prototypen – Angebote
23	/030499	Werkstätten – Prototypen – Sammel
23	/030501	Werkstätten – Chemie – Anschaffungen
23	/030502	Werkstätten – Chemie – Wartung
23	/030503	Werkstätten – Chemie – Betriebsmittel
23	/030504	Werkstätten – Chemie – Material
23	/030505	Werkstätten – Chemie – Reinigung und Entsorgung
23	/030506	Werkstätten – Chemie – Angebote
23	/030599	Werkstätten – Chemie – Sammel
23	/030601	Werkstätten – Textil – Anschaffungen
23	/030602	Werkstätten – Textil – Wartung
23	/030603	Werkstätten – Textil – Betriebsmittel
23	/030604	Werkstätten – Textil – Material
23	/030605	Werkstätten – Textil – Reinigung und Entsorgung
23	/030606	Werkstätten – Textil – Angebote
23	/030699	Werkstätten – Textil – Sammel
23	/030701	Werkstätten – Druck – Anschaffungen
23	/030702	Werkstätten – Druck – Wartung
23	/030703	Werkstätten – Druck – Betriebsmittel
23	/030704	Werkstätten – Druck – Material
23	/030705	Werkstätten – Druck – Reinigung und Entsorgung
23	/030706	Werkstätten – Druck – Angebote
23	/030799	Werkstätten – Druck – Sammel
23	/030801	Werkstätten – Farben – Anschaffungen
23	/030802	Werkstätten – Farben – Wartung
23	/030803	Werkstätten – Farben – Betriebsmittel
23	/030804	Werkstätten – Farben – Material
23	/030805	Werkstätten – Farben – Reinigung und Entsorgung
23	/030806	Werkstätten – Farben – Angebote
23	/030899	Werkstätten – Farben – Sammel
23	/030901	Werkstätten – Ausprobier – Anschaffungen
23	/030902	Werkstätten – Ausprobier – Wartung
23	/030903	Werkstätten – Ausprobier – Betriebsmittel
23	/030904	Werkstätten – Ausprobier – Material
23	/030905	Werkstätten – Ausprobier – Reinigung und Entsorgung
23	/030906	Werkstätten – Ausprobier – Angebote
23	/030999	Werkstätten – Ausprobier – Sammel
23	/031001	Werkstätten – Bio – Anschaffungen
23	/031002	Werkstätten – Bio – Wartung
23	/031003	Werkstätten – Bio – Betriebsmittel
23	/031004	Werkstätten – Bio – Material
23	/031005	Werkstätten – Bio – Reinigung und Entsorgung
23	/031006	Werkstätten – Bio – Angebote
23	/030099	Werkstätten – Bio – Sammel
23	/0399	Werkstätten – Sammel
23	/040101	Gemeinschaftsbereiche – Raumgestaltung – Pflanzen
23	/040102	Gemeinschaftsbereiche – Raumgestaltung – Athmosphärisches
23	/040199	Gemeinschaftsbereiche – Raumgestaltung – Sammel
23	/040201	Gemeinschaftsbereiche – Leitsystem & Orientierung
23	/040301	Gemeinschaftsbereiche – Akustik
23	/040401	Gemeinschaftsbereiche – Mobiliar
23	/040501	Gemeinschaftsbereiche – Technik
23	/040601	Gemeinschaftsbereiche – Küche
23	/040701	Gemeinschaftsbereiche – Kinder
2	/040801	Gemeinschaftsbereiche – Co-Working
2	/0499	Gemeinschaftsbereiche – Sammel
2	/050101	Programm & Entwicklung – Kommunikation – Webseite
2	/050102	Programm & Entwicklung – Kommunikation – Drucksachen
2	/050103	Programm & Entwicklung – Kommunikation – Newsletter
2	/050104	Programm & Entwicklung – Kommunikation – Social Media
2	/050105	Programm & Entwicklung – Kommunikation – Pressekontakt
2	/050199	Programm & Entwicklung – Kommunikation – Sammel
2	/050201	Programm & Entwicklung – Fortbildung – Reisen
2	/050202	Programm & Entwicklung – Fortbildung – Messen
2	/050203	Programm & Entwicklung – Fortbildung – Konferenzen
2	/050204	Programm & Entwicklung – Fortbildung – Eintritte
2	/050299	Programm & Entwicklung – Fortbildung – Sammel
2	/050301	Programm & Entwicklung – Bewerbung um Gelder – Spendeneinwerbung
2	/050302	Programm & Entwicklung – Bewerbung um Gelder – Drittmittelprojekte
2	/050399	Programm & Entwicklung – Bewerbung um Gelder – Sammel
2	/050401	Programm & Entwicklung – Ehrenamtspflege – Bewerbung
2	/050402	Programm & Entwicklung – Ehrenamtspflege – Betreuung
2	/050403	Programm & Entwicklung – Ehrenamtspflege – Verpflegung
2	/050404	Programm & Entwicklung – Ehrenamtspflege – Veranstaltungen
2	/050499	Programm & Entwicklung – Ehrenamtspflege – Sammel
2	/050501	Programm & Entwicklung – Programmaktivitäten – PCS Veranstaltungen
2	/050599	Programm & Entwicklung – Programmaktivitäten – Sammel
2	/0599	Programm & Entwicklung – Sammel
2	/060101	Projekte – Gebäudeinstandsetzung – Baumaterial
2	/060102	Projekte – Gebäudeinstandsetzung – Elektronisches Zugangssystem
2	/060103	Projekte – Gebäudeinstandsetzung – Elektrik Nord Werkstätten
2	/060104	Projekte – Gebäudeinstandsetzung – Reparatur PV
2	/060105	Projekte – Gebäudeinstandsetzung – Erfassung Betriebsmittel
2	/060106	Projekte – Gebäudeinstandsetzung – IT
2	/060107	Projekte – Gebäudeinstandsetzung – Lüftung Prototypen
2	/060199	Projekte – Gebäudeinstandsetzung – Sammel
12	/060201	Projekte – PCS – Projektbüro
12	/060202	Projekte – PCS – Resumée
2	/060203	Projekte – PCS – Call for Ideas
12	/060299	Projekte – PCS – Sammel
2	/060301	Projekte – UMBAU 2022-2024
2	/060501	Projekte – BBSR OE-Geld
12	/060601	Projekte – Teilhabefonds
2	/060701	Projekte – VULCA Seminar 2024
12	/0699	Projekte – Sammel
12	/070101	Verein – Verwaltung – Software und Lizenzen
12	/070102	Verein – Verwaltung – Hardware
12	/070103	Verein – Verwaltung – Porto
2	/070104	Verein – Verwaltung – Telekommunikation und Internet
12	/070199	Verein – Verwaltung – Sammel
12	/070201	Verein – Beratungsleistungen – Steuerberatung
12	/070202	Verein – Beratungsleistungen – Rechtsberatung
12	/070203	Verein – Beratungsleistungen – Organisationsentwicklung
12	/070204	Verein – Beratungsleistungen – Arbeitssicherheit
123	/070299	Verein – Beratungsleistungen – Sammel
2	/070301	Verein – Verbandsmitgliedschaften
23	/070401	Verein – Versicherungen
23	/070501	Verein – Bewertung Externer
2	/0799	Verein – Sammel
2	/080101	Einnahmen – Städtische Förderung – UMBAU Stadt
2	/080102	Einnahmen – Städtische Förderung – AUFBAU-GF Stadt
2	/080103	Einnahmen – Städtische Förderung – AUFBAU Stadt
2	/080104	Einnahmen – Städtische Förderung – BETRIEB Stadt
2	/080105	Einnahmen – Städtische Förderung – FOLGEN Erbbaurecht
23	/080106	Einnahmen – Städtische Förderung – UNERWARTETES Stadt
2	/080107	Einnahmen – Städtische Förderung – PCS Stadt
23	/080199	Einnahmen – Städtische Förderung – Sammel
23	/080201	Einnahmen – Werkstätten – Materialverkauf
23	/080202	Einnahmen – Werkstätten – Nutzungsgebühren
23	/080203	Einnahmen – Werkstätten – Teilnahmegebühren
23	/080204	Einnahmen – Werkstätten – Vermietung
23	/080299	Einnahmen – Werkstätten – Sammel
23	/080301	Einnahmen – Co-Working – Arbeitsplatzvermietung
23	/080399	Einnahmen – Co-Working – Sammel
2	/080401	Einnahmen – Gastro – Getränkeverkauf
2	/080499	Einnahmen – Gastro – Sammel
2	/080501	Einnahmen – Veranstaltungen – Raumvermietungen
1	/080502	Einnahmen – Veranstaltungen – Eintritte
1	/080599	Einnahmen – Veranstaltungen – Sammel
12	/080601	Einnahmen – Verein – Mitgliedsbeiträge
1	/080602	Einnahmen – Verein – Spenden
12	/080699	Einnahmen – Verein – Sammel
1	/080701	Einnahmen – Teilhabefonds
2	/080801	Einnahmen – PCS Bund
3	/080901	Einnahmen – PV-Einspeisung
123	/089901	Einnahmen – Sammel
9	/090101	Sonstiges – Durchlaufende Posten
9	/090201	Sonstiges – Interne Umbuchungen"""

indices = [0, 0, 0]
categories = [None, None, None]
line = categories
for l in s.split("\n")+["\t\t"]:
    oldline = line
    line = l.split("\t")
    change = []

    for i in range(3):
        if line[i] != categories[i]:
            change.append(i)
            indices[i] += 1
            for j in range(i+1,3):
                indices[j] = 0
            categories[i] = line[i]

    if 1 in change and oldline[2] != "":
        print("{:02}\t{}".format(indices[0], oldline[0]),
              "{:02}\t{}".format(indices[1]-1, oldline[1]),
              99, "Sammel", sep="\t")
    if 0 in change:
        print("{:02}\t{}".format(indices[0]-1, oldline[0]), 99, "Sammel", sep="\t")

    if line[0] != "":
        print(*["{:02}\t{}".format(indices[i], line[i]) for i in range(len(line)) if line[i]], sep="\t")\

# Generate Sammel entries
#   for i in range(3):
#       if line[i] != categories[i]:
#           change.append(i)
#           indices[i] += 1
#           for j in range(i+1,3):
#               indices[j] = 0
#           categories[i] = line[i]
#   
#   #if 1 in change and len(oldline) == 3:
#   #    print("{:02}\t{}".format(indices[0]-1, oldline[0]),
#   #          "{:02}\t{}".format(indices[1]-1, oldline[1]),
#   #          99, "Sammel", sep="\t")
#   #if 0 in change:
#   #    print("{:02}\t{}".format(indices[0]-1, oldline[0]), 99, "Sammel", sep="\t")
    