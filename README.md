# Vaistinių kainų analizė

## Tikslas
Šio projekto tikslas – išanalizuoti akcijines prekes trijose Lietuvos internetinėse vaistinėse:

- Camelia 
- Gintarinė vaistinė
- Mano vaistinė

## Naudotos technologijos

- **Web scraping**: Scrapy
- **Duomenų bazė**: MySQL
- **Duomenų apdorojimas**: SQL + Pandas
- **Vizualizacija**: Matplotlib, Seaborn

Scrapy → MySQL (raw duomenys)
→ SQL (valymas ir transformacijos)
→ Pandas (analizė)
→ Vizualizacijos

## Projekto struktūra

pharmacy-price-analysis/

├── scrapers/ # Scrapy spideriai ir pipeline

├── database/ # schema.sql, views.sq
├── analysis/ # SQL užklausos per Python
├── visualizations/ # Matplotlib, Seaborn vizualizacijos
├── visualizations charts/ # sugeneruoti grafikai
├── docs/insights.md # analizės išvados
├── requirements.txt
└── README.md

## Duomenų apdorojimas

Atliekami šie pagrindiniai veiksmai:

- suvienodinamos kategorijos tarp skirtingų vaistinių
- išskiriami ir standartizuojami nuolaidų modeliai:
  - `direct_percent`
  - `bulk_min_qty`
  - `buy_x_get_y`
- apskaičiuojama `final_price_equivalent`
- pašalinami netinkami arba nepilni duomenys

## Analizės kryptys

- kainų palyginimas tarp vaistinių ir kategorijų
- nuolaidų tipų pasiskirstymas
- brandų kainų palyginimas
- kainų diapazonų analizė

## Pagrindinės įžvalgos

Pilna analizė pateikta `docs/insights.md`

## Pastabos

- pilni scraped duomenys nėra viešinami
- projektas skirtas edukaciniams ir analitiniams tikslams

