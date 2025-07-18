# Death-clock

An interactive death clock built with Tkinter. Enter your personal details to estimate the remaining time you have left to live.

## Features
- Countdown timer with detailed statistics
- Progress bar showing percentage of life lived
- Optional age prediction using the [agify.io](https://agify.io) API
- Menu with About dialog and exit option

## Requirements
- Python 3.x
- `requests` for API access
- `tkcalendar` (optional, enables date picker)

Install dependencies with:

```bash
pip install requests tkcalendar
```

## Usage
Run the application with:

```bash
python dethclock.py
```

Fill in your name, date of birth, gender and country. Enable *Use Age Prediction API* to retrieve a predicted lifespan from the agify.io service for additional analysis.
