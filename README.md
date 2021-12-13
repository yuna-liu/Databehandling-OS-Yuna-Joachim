
# Databehandlingsprojekt: OS - Yuna & Joachim

---
## Goal of this project

The **goal** of this [project][projectlink] is to:
- work in a group
- use python to clean and filter the data
- make dashboard to visualize the historical data 
for 120 years Olympic Games from [Kaggle][kagglelink]

[projectlink]: https://github.com/yuna-liu/Databehandling-OS-Yuna-Joachim/blob/main/Projekt_OS.pdf

[kagglelink]: https://www.kaggle.com/heesoo37/120-years-of-olympic-history-athletes-and-results

---

## Our final dashboard app
This project is a coorperation between Yuna Liu, and Joachim Wiegert.

The final **dashboard** App of this project could be found **[here][dashboardlink]** in Heroku:

[dashboardlink]: https://dashboard-yuna-joachim.herokuapp.com/

---

## File structures:

### A explosive data analysis over the whole dataset:
- Uppgifter 0 sovled we seperately in files: Q0_J.ipynb and Q0_Y.ipynb

### Data analysis of canada
- Uppgifter 1 solved we in file: Q1_J.ipynb and Q1_Y_hash.ipynb

### Sport statistics
- Uppgifter 2 solved we in file: Q2_Y.ipynb

### Files to create Dashboard
- Canada statistics dashboard: Q3_J_dashboard.py
- Sport statistics dashboard: Q3_Y_dashboard_world.py
- Sidebar dashboard of both candada and sport statistics: Q3_dashboard_main.py

### Functions/modules constructed for this project
- analyze_functions.py, which is a module with defined function count_medals for arbitrary attributes
- get_iso.ipynb, which documented how we get the corresponding noc to iso code for each country
- load_data.py, which is a module with defined class to look into data, and check missing data etc.

### Data and figures
- data folder included the original data and data we generated
- Visualiseringar folder included collected all figures in uppgiter 1 and 2.


---
## Discussion board

Joachim: Jag testar om pull och push fungerar. Syns detta online sen så fungerar det :)

Yuna: I add raw datasets in data folder, och a OOP(with name: load_data) to get data from local, show data structure, and describe missing data etc. The cleaned datasete will locate automatically to data_clean folder. I create a Q0 file to solve the question 0. Date: 2021-11-08

2021-11-08 - J: Created a pipenv here, uploaded my pipfile also.

### Dashboard-idéer:

- En tidsplot, med en slider för att välja år

- En plot med något annat, som åldersfördelning, sporter etc på x-axeln

- En ruta som visar lite olika siffror, max-min-värden(?), antal medaljer av olika slag

TODO:

### Anteckningar inför presentation:

- Visa dashboard, vad visar vi, ett par intressanta saker man kan se i det vi presenterar.

- Visa koderna, hur vi har tänkt, visa "count medals"-funktionen

- Hur har arbetet gått? Mycket distans, Joachim sjuk halva tiden, problem med två olika Python-versioner, följande problem med gir-merge, git bash blev räddningen!

Kod och video ska lämnas in på fredag, 19/11

### Anteckningar till presentationen

Joachim tar Q1

- Q1-frågorna

- Någon extra statistik

- Någon bit från koden

Yuna tar Q2

- Q2-frågorna

- Någon extra statistik

- Någon bit från koden







