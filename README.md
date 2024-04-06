# Simutrans Dataweb
(2020 - now)<br>
Simutrans Dataweb was created with the idea to have a better way of storing and analyzing population data from Simutrans maps. Initially thought of as a Flask-based web interface but that part hasn't been done yet.

This "app" uses the following structure for the population data, it has 2 different `csv`-file and 1 `.env`-file per map (for example with a map called A):
- a file to save all the population data entries
```
  data/A/populationdata.csv

  example
  ----------
  uid,セーブ,日付,都市uid,人口
  0,1,郡野元年01月04日,-1,0
  ----------
  uid    - id of the entry
  セーブ  - save number
  日付    - in-game date of the entry
  都市uid - id of the city the entry belongs to
  人口    - actual population value of the entry
```
- a file to save the town data
```
  data/A/towndata.csv

  example
  ----------
  uid,都市名,都道府県名,区,市名,人口,開始セーブ,中止セーブ,計画された人口
  0,豊島,中原都,1,中原,1000,2,20,40000
  ----------
  uid           - id of the entry
  都市名        - name of the entry/town
  都道府県名     - name of the province or similar subdivision
  区            - is this entry a subdivision of a bigger city
  市名          - if this is a subdivision of a bigger city, the name of the bigger city
  人口          - actual population value of the entry
  開始セーブ     - starting save number of this entry
  中止セーブ     - last save number of this entry
  計画された人口 - planned population of this entry
```
- an environment file to save environment variables (currently only made with Japanese and Latin alphabet using languages, English version of the labels can be added separated with `/`) 
```
  data/A/.env
  example
  ----------
  lang=DE
  name=ZweiVolk
  subdivision=Countries

  example
  ----------
  start_period=1920
  name_period=郡野
  lang=JP
  name=郡野国/Korino
  subdivision=都道府県/Prefectures

  lan          - language expected for the map
  name_period  - name of a possible period used for the map
  start_period - start of this period
  name         - name of the map
  subdivision  - name of the subdivisions of the map (think countries/states/provinces etc)
  ```

Then there are some files to interact/add to these csv "databases" for each one a specific map "database" is first chosen:
- A file to add population data (`add_population.py`) where new date is given and then the population data for each town is given;
- A test file to look up the subdivision of a town (`test.py`);
- A file to plot the population of the top 10 towns on the chosen map & the total/subdivisions population (`plot.png`);
- A file to find some interesting data about the chosen map (`interesting_info.py`) it prints out the save number, current ingame date, amount of towns, check if there exist towns with big changes since previous save, total population, population per province subdivision, top 10 most populous cities (added towns that are a subdivision to their parent city), populations of cities and their town subdivisions, towns per province subdivision
