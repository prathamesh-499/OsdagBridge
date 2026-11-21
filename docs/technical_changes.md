# OsdagBridge report generator: technical changes

## Changes

1. **Repeated table headers.** Longtables repeat their complete header blocks on continuation pages. A shared start-space macro is emitted before each longtable, and Table 3.3 starts on a new page to keep its caption with its header. **Files:** `report_utils.py`, `report_generator.py`, `styles.py`.

2. **Layout and footer spacing.** Central page geometry and footer spacing, table row spacing/padding, caption spacing, figure widths, and table-start thresholds reduce footer collisions and caption/header splits. **Files:** `styles.py`, `report_generator.py`, `report_utils.py`, `chap1.py`–`chap8.py`, `executive_summary.py`.

3. **Load and geometry tables.** Chapter 3 separates vehicle live loads, associated vehicle loads, and footpath loads; vehicle rows follow UI selections. Total Load values are read from the stored vehicle-total-load values in the report output payload (with input payload fallback), not recalculated. Missing footpath is explicit, and unavailable braking/centrifugal values are not fabricated. **Files:** `chap3.py`, `report_generator.py`, `styles.py`, `report_utils.py`.

4. **Section 5.5 UR chart.** Matplotlib generates the girder, deck, cross-bracing, and end-diaphragm summary chart with a dashed UR=1.0 threshold. Missing values omit bars and receive a note. The End Diaphragm chart/table source mismatch is documented under Known limitations. **Files:** `chap5.py`, `chart_renderer.py`, `styles.py`.

5. **Chapter 7 material charts.** Charts show available steel tonnage and concrete/reinforcement quantities. After restoring the BOQ generator to `dev`, missing aggregate cross-bracing or End Diaphragm weights are omitted and identified in the steel chart note. The Figure 7.2 caption describes the reported quantities without claiming a particular reinforcement source. **Files:** `chap7.py`, `chart_renderer.py`, `styles.py`.

6. **Central style module.** `styles.py` is the source for `DOCUMENT` page settings, `COLORS`, `TYPOGRAPHY`, `SPACING`, `TABLE`, `FIGURE`, `CHART`, `HEADER`, `TABLE_LAYOUTS`, and shared LaTeX preamble/TOC builders. Chapter generators consume these values through imports and macros. **Files:** `styles.py`, `report_generator.py`, `report_utils.py`, `executive_summary.py`, `chap1.py`–`chap8.py`, `chart_renderer.py`.

## Files changed under the report generator

`src/osdagbridge/core/reports/chap1.py`–`chap8.py`, `chart_renderer.py`, `executive_summary.py`, `report_generator.py`, `report_utils.py`, and `styles.py`.

Matplotlib is already declared in `environment.yml` and `pyproject.toml`; it is not listed in `requirements.txt`. No dependency was added.


## Known limitations

- Braking load remains “N/A”: the existing IRC 6 helper is unsafe for one- or two-lane cases and is not tied to the selected vehicle checkboxes.
- Centrifugal force is not calculated because curve radius and design speed are not provided.
- The displayed footpath pressure of 4.905 kN/m² comes from the existing default of 500 kg/m².
- Table 5.29’s End Diaphragm rows read from cross-bracing results. The Section 5.5 chart searches `end_diaphragm_design_results` for recognized `Member.efficiency` / `Optimum.UR` fields; for Run B it finds none and shows “No design data,” while the table shows 0.76 (moment) and 0.29 (shear). These sources are not reconciled here.
- The full report build has a pre-existing multiply-defined `sec:assumptions` label warning.
- The report grew from approximately 64 pages to approximately 73 pages, as observed in the regenerated PDF.


