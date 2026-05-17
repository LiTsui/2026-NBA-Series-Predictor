# NBA Series Predictor for the 2026 Playoffs

> **Update: May 11, 2026** <br>
Parsed matchup history, standings, and team ratings data <br/>
Replaced invalid values in the original data sets <br/>
Created data comparisons based on matchups

> **Update: May 13, 2026** <br>
Overhauled the team statistics comparison system based on existing playoff series data <br>
Partitioned datasets into training, validation, and testing data for model training

> **Update: May 14, 2026** <br>
Created the first iteration of the neural network <br>
Achieved an average 70% accuracy on validation data

> **Update: May 15, 2026** <br>
Implemented helper functions to find dropout and neuron counts <br>
Achieved an average 90% accuracy on testing data <br>

> **Update: May 16, 2026** <br>
Implemented the system to simulate each round of the 2026 NBA Playoffs

---

### **Project Overview**  
The NBA Series Predictor uses historical playoff game data and regular season team statistics to create matchup features and train a model capable of predicting which team will win the 2025-2026 playoffs. The model will only use playoff data starting from 1996 since 1996 was the start of the "play by play era"; an era in which real-time statistics are measured game by game. 

The data has been partitioned into three datasets for model training. 
- The training dataset will use matchups from 1996 - 2019
- The validation dataset will use matchups from 2020 - 2022
- The testing dataset will use matchups from 2023 - 2025

---

### **NBA Terminology**
The matchups for the NBA Playoffs are of a best of 7 format (the first round was a best of 5 until 2002). The games played to win a best of 7 are called a series. Therefore winning one game does not mean winning the series entirely. 

- **Seeds:** The rank of each team within their conference based on total wins during the regular season 
- **Western Conference:** Consists of teams west of the Mississippi River and the Memphis Grizzlies 
- **Eastern Conference:** Consists of teams east of the Mississippi River but not the Memphis Grizzlies 
- **Play-In Tournament:** 4 teams from each conference compete against each other within their conference for the 7th and 8th seeds. The model will not predict the outcomes for this
- **First Round:** The top 8 teams from each conference compete in a best of 7 (best of 5 until 2002) series for a spot in the Conference Semi-Finals
- **Conference Semi-Finals:** The second round of the NBA Playoffs. 4 teams from each conference compete in a best of 7 series for a spot in the Conference Finals 
- **Conference Finals:** The third round of the NBA Playoffs. 2 teams from each conference compete in a best of 7 series for a spot in the NBA Finals. 
- **NBA Finals:** The fourth and final round of the NBA Playoffs. 1 team from each conference compete in a best of 7 series for the NBA Championship and the Larry O’Brien Trophy

The league's teams have changed several times until 2014 so playoff data from 1996 to 2014 may feature teams that do not exist anymore or have relocated. A recent example of this would be the Seattle Supersonics becoming the Oklahoma City Thunder. These are the teams currently in the NBA:

#### **Western Conference Teams**
- Dallas Mavericks
- Denver Nuggets
- Golden State Warriors
- Houston Rockets
- Los Angeles Clippers
- Los Angeles Lakers
- Memphis Grizzlies
- Minnesota Timberwolves 
- New Orleans Pelicans
- Oklahoma City Thunder
- Phoenix Suns
- Portland Trail Blazers
- Sacramento Kings
- San Antonio Spurs
- Utah Jazz

#### **Eastern Conference Teams**
- Atlanta Hawks 
- Boston Celtics
- Brooklyn Nets
- Charlotte Hornets
- Chicago Bulls
- Cleveland Cavaliers
- Detroit Pistons 
- Indiana Pacers
- Miami Heat 
- Milwaukee Bucks
- New York Knicks
- Orlando Magic
- Philadelphia 76ers
- Toronto Raptors
- Washington Wizards 

---

### **Machine Learning Terminology**

---

### **Phase 1: Parsing data from the NBA API**

API stands for "Application Programming Interface." It is the online database that stores information regarding the NBA's teams and their playoff statistics.

---

### **Phase 2: Model Creation**

---

### **Phase 3: Model Training and Validation Tuning**

---

### **Phase 4: Model Testing**

---

### **Phase 5: Predicting the 2026 NBA Playoffs**

---

### **Unaccounted Factors**
Injuries are an integral part of the NBA Playoffs and therefore a player’s individual impact is important to consider when predicting the outcome of a playoff series. However, due to the scale of this project, it is not plausible to assess every player’s impact on their team. It is also not plausible to predict which players would be injured. 

There are also instances where certain players may overperform or underperform during the playoffs compared to their regular season statistics.  A few examples would be Jimmy Butler while playing for the Miami Heat or James Harden.

---

### **Extras**
The raw and processed data have already been parsed for ease. If there is any corruption involved with the data, run `load_data.py`. Then run `clean_data.py`. Then `matchup_features.py`.

It is also possible to predict playoff series several years from now once future data becomes available. If you want to do so, change the upper bound of the for loops in the main functions of `clean_data.py`, `load_data.py`, and `matchup_features.py`. Then run the files in that order.

