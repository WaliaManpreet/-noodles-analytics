# Noodles Crypto Analytics Platform

Dashboard screenshot: docs/screenshots/executive-dashboard.png

## Project Overview

Production-ready currency analytics platform processing 1M+ rows of
market data daily using Python, MySQL, and Power BI.

Key Features:
- Automated Python ETL pipeline (5-min runtime)
- Star schema data warehouse design
- Interactive Power BI dashboards
- Comprehensive data quality validation
- Scheduled daily refresh

## Architecture

json Files → Python ETL → MySQL (noodles_dw) → Power BI Dashboards

Architecture diagram (YOU CREATE in Task 9 §1):
docs/architecture-diagram.png

## Technology Stack

| Layer | Technology |
| ETL | Python 3.9, pandas, SQLAlchemy |
| Data Warehouse | MySQL 8.x |
| Visualization | Power BI Desktop, DAX |

## Project Structure

noodles-analytics/
├── 05_data_warehouse_design.ipynb
├── 06_powerbi_prep.ipynb
├── reports/          (Tasks 7–8 .pbix files)
├── docs/             ← YOU CREATE in Task 9
│   ├── architecture-diagram.png    ← §1
│   ├── data-dictionary.xlsx        ← §2
│   ├── technical-runbook.md        ← §3
│   ├── user-guide.md               ← §4
│   └── demo-presentation.pptx      ← §5
└── README.md

## Data Model

Dimensions: DimCurrency, DimDate, DimPlatform
Facts: FactSocialEngagement

Data dictionary (YOU CREATE in Task 9 §2):
docs/data-dictionary.xlsx

## Key Insights

- Bitcoin Dominance: 45% of total market capitalization
- Volume Leaders: Top 20 currencies = 90% of trading volume
- Social Correlation: Engagement predicts 30% of price movements
- Volatility: Average daily price change of ±8%

## Achievements

- Processed 1M+ rows of currency data
- Built automated ETL pipeline
- Delivered interactive Power BI dashboards
- Referential integrity in star schema

## Documentation  (files YOU CREATE — not pre-built reference links)

- Technical Runbook  →  docs/technical-runbook.md       (Task 9 §3)
- User Guide         →  docs/user-guide.md              (Task 9 §4)
- Architecture       →  docs/architecture-diagram.png   (Task 9 §1)
- Data Dictionary    →  docs/data-dictionary.xlsx       (Task 9 §2)

## Demo

Demo video URL: (https://www.youtube.com/watch?v=dXpkRmNdtpI)
Presentation (YOU CREATE in Task 9 §5): docs/demo-presentation.pptx

## Contact

Manpreet Walia | manpreetwalia.2014@gmail.com
Optional — markdown link syntax for GitHub README only (after files exist in repo):

[Architecture Diagram](docs/architecture-diagram.png)
[Data Dictionary](docs/data-dictionary.xlsx)
[Technical Runbook](docs/technical-runbook.md)
[User Guide](docs/user-guide.md)
[Presentation slides](docs/demo-presentation.pptx)
Do not expect the paths above to open from this task page — verify links only on your GitHub repository after push.

Related docs from earlier tasks (different paths — optional cross-links):

Task 5: data_warehouse_schema.md (schema export, not the architecture PNG)
Task 8: reports/executive-dashboard-guide.md, reports/dax-measures-reference.md
Create Final Checklist

Create docs/final-checklist.md:
# Final Project Checklist

## Code & Scripts

- [ ] All Python scripts execute without errors
- [ ] `pip install` dependencies documented in task1.md / task6.md
- [ ] SQL scripts create schema successfully
- [ ] ETL pipeline runs end-to-end
- [ ] Validation scripts pass all checks

## Data Quality

- [ ] 99%+ data quality score
- [ ] No orphaned facts
- [ ] Referential integrity maintained
- [ ] SCD Type 2 working correctly
- [ ] Reject files handled properly

## Power BI

- [ ] Dashboards load in < 5 seconds
- [ ] All visuals display data
- [ ] Cross-filtering works
- [ ] Drill-through configured
- [ ] Bookmarks functional
- [ ] Published to Power BI Service
- [ ] Scheduled refresh configured

## Documentation

- [ ] README.md complete with screenshots
- [ ] Technical runbook written
- [ ] User guide for stakeholders
- [ ] Data dictionary created
- [ ] Architecture diagram included
- [ ] All code commented

## Presentation

- [ ] Demo presentation (10 slides)
- [ ] Demo video recorded (10 min)
- [ ] Key insights documented
- [ ] Performance benchmarks included


## Submission Package
- [ ] docs/architecture-diagram.png
- [ ] docs/data-dictionary.xlsx
- [ ] docs/technical-runbook.md
- [ ] docs/user-guide.md
- [ ] docs/demo-presentation.pptx
- [ ] Demo video uploaded


## GitHub Verification
- [ ] All docs open correctly in GitHub
- [ ] README.md links verified
- [ ] Screenshots visible in repo


## Environment Setup
- [ ] Python virtual environment created
- [ ] requirements.txt included
- [ ] MySQL schema export included


## Portfolio

- [ ] GitHub repository public
- [ ] Professional README
- [ ] Screenshots added
- [ ] Demo video uploaded
- [ ] LinkedIn post drafted
