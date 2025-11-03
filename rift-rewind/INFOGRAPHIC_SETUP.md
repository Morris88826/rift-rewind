# Infographic Page Setup Guide

The infographic page displays performance metrics using an interactive radar chart. To get it working, you need to install Chart.js.

## Installation

Run the following command in your project root:

```bash
npm install chart.js
```

## Features

The infographic page includes:

1. **Radar Chart** - Shows normalized performance metrics:
   - KDA (Kill/Death/Assist ratio)
   - CS Score (Creep Score)
   - Gold Efficiency
   - Damage Output
   - Kill Participation

2. **Filter Options**:
   - Filter by Lane (Mid, Support, ADC, Top, Jungle, or All Lanes)
   - Filter by Champion (Ahri, Lux, Zed, or All Champions)
   - Filter by Game Mode (Ranked, Unranked, ARAM, or All Modes)

3. **Statistics Summary** - Quick stats showing:
   - Matches Analyzed (based on filters)
   - Win Rate (%)
   - Average KDA
   - Average CS

4. **Detailed Statistics Table** - Breakdown by champion/lane/mode showing:
   - Win Rate percentage
   - Average K/D/A
   - Average CS
   - Number of games played

## How the Radar Chart Works

The radar chart displays five normalized metrics (0-100 scale):

- **KDA**: Your average Kill/Death/Assist ratio
- **CS Score**: Your average creep score (normalized to max 350)
- **Gold Efficiency**: Your average gold earned (normalized to max 20,000)
- **Damage Output**: Your average damage (normalized to max 25,000)
- **Kill Participation**: Your average kill participation percentage

The chart updates dynamically when you change the filters.

## Adding Real Data

To integrate with real match data:

1. Replace the `matchData` array in `InfographicView.vue` with data from your API
2. Ensure each match object includes these fields:
   ```javascript
   {
     champion: 'ChampionName',
     lane: 'LaneRole',
     mode: 'GameMode',
     kills: number,
     deaths: number,
     assists: number,
     cs: number,
     gold: number,
     damage: number,
     participation: number (0-100)
   }
   ```

## Chart.js Documentation

For more information about Chart.js and customization options, visit:
https://www.chartjs.org/docs/latest/

## Troubleshooting

If you see "Chart.js not loaded" warning:
- Make sure you've installed Chart.js: `npm install chart.js`
- Restart your dev server after installation
- The chart should appear after the page loads

## Customization

To modify the radar chart styling:

1. **Colors** - Change the `borderColor` and `backgroundColor` in the `datasets` array
2. **Labels** - Modify the metrics in the `radarData` computed property
3. **Scale** - Adjust the `max` value in the scales configuration
4. **Animation** - See Chart.js documentation for animation options

## Sample Data

The infographic comes with sample data for these champions:
- Ahri (Mid)
- Lux (Support)
- Zed (Mid)

With data across three game modes:
- Ranked
- Unranked
- ARAM
