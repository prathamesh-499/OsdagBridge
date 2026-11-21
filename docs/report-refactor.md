# OsdagBridge report refactor

## Summary

The report generator now uses a shared style module to define page geometry, typography, colors, table spacing, figure widths, chart colors, and header/footer styling. Chapter generators emit shared LaTeX macros for repeated formatting and use named table-layout aliases that are expanded at the end of report assembly.

Multi-page tables repeat their complete header block. The live-load chapter reports vehicles and related loads in separate tables, includes the selected custom vehicles, and reports an explicit no-footpath row when no footpath is selected. The report source does not invent braking, centrifugal, or footpath values when they are unavailable.

Section 5.5 and Chapter 7 charts are generated programmatically through `chart_renderer.py` and embedded as figures. UR charts use a dashed threshold at 1.0; material charts show steel tonnage and concrete volume with reinforcement weight.

Page geometry and footer spacing were adjusted, and Table 3.3 starts on a fresh page to prevent a continuation header from appearing before its caption. Longtable start spacing is inserted before each environment so page breaks keep the caption with its first header. Table row spacing, cell padding, caption gaps, and figure sizing are configurable from the shared style definitions.

## Main files

- `src/osdagbridge/core/reports/styles.py` defines style constants, LaTeX style macros, table layouts, document preamble, TOC styling, and table-layout expansion.
- `src/osdagbridge/core/reports/report_generator.py` uses the shared preamble and TOC builders and expands style aliases after chapter assembly.
- `src/osdagbridge/core/reports/report_utils.py` adds continuation heads for assembled longtables and uses shared figure dimensions and typography.
- `src/osdagbridge/core/reports/chap1.py` through `chap8.py` and `executive_summary.py` use shared spacing, table, and figure macros.
- `src/osdagbridge/core/reports/chart_renderer.py` centralizes chart dimensions, colors, and UR threshold styling.
- `src/osdagbridge/core/reports/chap3.py` builds separate live vehicle, associated vehicle load, and footpath tables from existing input and analysis values.

## PDF review

`Report_Before.pdf` is the saved Run B report. `Report_After.pdf` was rebuilt from its saved LaTeX source and embedded images using the new report preamble and the table continuation/page-break fixes. The saved design data includes both-side footpath selection and its reported pressure. A live desktop design session was not available, so this validates rendering against the saved report data rather than a fresh design calculation.

The after PDF was compiled with pdfLaTeX and visually reviewed at the live-load, G4 check, and software-default footer pages. It contains 73 physical pages; the numbered report pages end at 72 because the title page is unnumbered. The build retains a pre-existing multiply-defined `sec:assumptions` label warning.
