# NHL Puck Management Score — 2025-26 Season

A data-driven composite puck management score for every NHL skater in the 2025-26 regular season. Built using public NHL API play-by-play data and MoneyPuck skater statistics.

## Methodology

Three distinct metrics are combined into a single composite score:

1. **Giveaway Rate per 60** — how often a player turns the puck over per 60 minutes of 5on5 ice time
2. **Giveaway Above Expected** — how dangerous those turnovers were relative to what was expected given the situation (zone, coordinates, period)
3. **Defensive Zone Giveaway Rate** — dzone giveaways per dzone shift start, adjusted for zone deployment

Each metric is MAD z-scored within position groups (forwards and defensemen separately) and confidence weighted based on 5on5 ice time before being combined into a composite score.

## Data Sources

- **NHL API** — play-by-play data for all 1,312 regular season games (free, no authentication required)
- **MoneyPuck** — season level skater statistics (moneypuck.com)

## How to Run

1. Clone the repo
2. Create the conda environment:
```bash
conda env create -f environment.yml
conda activate nhl-puck-mgmt
```
3. Pull the NHL API data:
```bash
python src/data/fetch.py
```
4. Process the raw data:
```bash
python src/data/process.py
```
5. Run the notebooks in order:
   - `01_eda.ipynb`
   - `02_model.ipynb`
   - `03_scoring.ipynb`
   - `04_visualizations.ipynb`

## Key Findings

- Top puck managers tend to be defensive specialists and two-way forwards
- Elite offensive players (McDavid, MacKinnon) rank lower due to higher usage and more aggressive puck carrying style
- Ottawa, Vegas and Montreal rank highest at the team level

## Project Structure
nhl-puck-management/

├── data/

│   ├── raw/          # raw NHL API JSON (not committed)

│   └── processed/    # clean CSVs

├── notebooks/        # analysis notebooks

├── src/              # Python scripts

│   ├── data/         # fetch and process scripts

├── outputs/          # charts and visualizations

├── environment.yml

└── README.md


## Credits

- MoneyPuck data used under non-commercial license — please credit [MoneyPuck.com](https://moneypuck.com)
- NHL API data is publicly available

## Author

Zaki Aslam | [LinkedIn](https://www.linkedin.com/in/zaki-aslam-20b7162bb/)
