
# Databehandlingsprojekt: OS - Yuna & Joachim

This [project][projectlink] is to make dashboard to visualize the historical data for 120 years Olympic Games from [Kaggle][link]

[projectlink]: https://github.com/yuna-liu/Databehandling-OS-Yuna-Joachim/blob/main/Projekt_OS.pdf

[link]: 

The final App could be found in [Heroku][link]:

[link]: https://dashboard-yuna-joachim.herokuapp.com/


---

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

### short explanations of the files:
- Uppgifter 0 sovled we seperately in files: Q0_J.ipynb and Q0_Y.ipynb
- Uppgifter 1 solved we in file: Q1_J.ipynb and Q1_Y_hash.ipynb
- Uppgifter 2 solved we in file: Q2_Y.ipynb
- Uppgifter 3 solved we in three dashboards:
- Canada statistics dashboard solved in Q3_J_dashboard.py
- Sport statistics dashboard solved in Q3_Y_dashboard_world.py
- Sidebar dashboard solved we in Q3_dashboard_main.py
- analyze_functions.py is a module with defined function count_medals for arbitrary attributes
- get_iso.ipynb documented how we get the corresponding noc to iso code for each country
- load_data.py is a module with defined class to look into data, and check missing data etc.
- data folder included the original data and data we generated
- Visualiseringar folder included collected all figures in uppgiter 1 and 2.






