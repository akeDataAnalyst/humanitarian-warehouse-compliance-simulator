# Humanitarian Warehouse Compliance & Training Simulator

Interactive training and self-audit tool for humanitarian warehousing staff.

This project simulates realistic warehouse scenarios and compliance checks to help field teams practice standards, identify risks, and receive actionable corrective guidance.


## Key Features

- Realistic crisis warehouse scenarios (South Sudan floods, Yemen access blocks, Ethiopia nutrition surge, etc.)   
- Training Mode (learn best practices) vs Audit Mode (realistic assessment)  
- Compliance score (0–100%), risk level classification, and prioritized findings  
- Recommended corrective actions with practical steps  
- Downloadable session report (JSON)  

## Results from Sample Simulation (South Sudan Flood Scenario)

**Compliance Score**: 50.0%  
**Risk Level**: High Risk  
**Top Findings & Actions** (prioritized):

- FIFO/FEFO system visibly implemented → No (weight 18)  
  → Immediately address. Review and update SOPs. Implement FIFO/FEFO system.

- Warehouse is secure → Partial (weight 15)  
  → Immediately address. Review and update SOPs.

- Updated stock ledger / bin cards → Partial (weight 15)  
  → Immediately address. Review and update SOPs. Conduct full stock count.

- Adequate ventilation and protection from weather → No (weight 12)  
  → Immediately address. Review and update SOPs.

- Fire extinguishers present and serviced → Partial (weight 10)  
  → Immediately address. Review and update SOPs.

## Tech Stack

- **Python** 3.9+  
- **Streamlit** – interactive dashboard  
- **Pandas** – data handling  
- **Plotly**   



Interactive training & compliance audit simulator for humanitarian warehousing — built to support global WIM standardization, capacity building, risk identification, and audit readiness.
humanitarian-warehouse-compliance-simulator


