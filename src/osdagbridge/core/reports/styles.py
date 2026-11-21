"""Single source of truth for OsdagBridge report formatting."""
from types import MappingProxyType
import re

COLORS = MappingProxyType({"accent": "91B014", "pass": "91B014", "fail": "D9534F", "info": "4472C4", "text": "000000", "warning": "FFFF00"})
DOCUMENT = MappingProxyType({"paper": "a4paper", "font_size": "12pt", "geometry": "top=0.85in,bottom=1.05in,left=0.8in,right=0.8in,includeheadfoot,headheight=18pt,footskip=27pt", "line_spacing": "1.15", "table_padding": "6pt", "row_stretch": "1.12", "longtable_pre": "0pt", "longtable_post": "6pt", "rule_width": "0.5pt", "extra_row_height": "0.6pt", "min_table_space": "5", "longtable_start_lines": "14", "header_rule": "1pt", "header_gap": "2pt", "footer_gap": "6pt", "footer_note_raise": "2em"})
TABLE = MappingProxyType({"compact_padding": "3.5pt", "dense_padding": "4pt", "analysis_padding": "3pt", "row_stretch": "1.25", "caption_top": "2pt", "caption_bottom": "2pt"})
SPACING = MappingProxyType({"section": "1em", "medium": "0.8em", "small": "0.4em", "tight": "0.3em", "small_medium": "0.6em", "paragraph": "0.4cm", "half_block": "0.5cm", "block": "0.8cm", "major": "2.2em", "caption_gap": "4pt", "caption_tight": "-0.5em", "caption_after": "0.5em", "figure_before": "-0.5em", "figure_after": "0.5em", "row": "6pt", "row_wide": "8pt", "row_tight": "3pt", "title": "1.5cm", "title_gap": "1.5cm", "logo_gap": "1cm", "title_small": "0.3cm", "cover_title": "2cm", "toc_row": "2pt", "chapter_number_gap": "1em", "executive_chapter_before": "-30pt", "executive_chapter_after": "10pt"})
FIGURE = MappingProxyType({"placement": "H", "float_placement": "htbp", "placeholder_width": r"0.97\textwidth", "summary_width": r"0.9\textwidth", "full_width": r"\textwidth", "chapter_width": r"0.85\textwidth", "chart_width": r"0.88\textwidth", "analysis_width": r"0.75\textwidth", "cell_width": r"0.31\textwidth", "cell_placeholder_width": r"0.95\linewidth", "org_logo_height": "2.2cm", "logo_panel": r"0.6\textwidth", "org_panel": r"0.35\textwidth"})
TYPOGRAPHY = MappingProxyType({"caption": "small", "footnote": "footnotesize", "cover_brand": "Huge", "cover_subtitle": "large", "cover_title": "Large", "chapter_title": "Large", "executive_title": "Large", "toc_title": "Large"})
CHART = MappingProxyType({"ur_size": (8.4, 4.0), "material_size": (7.2, 4.0), "dpi": 160, "accent": "#91B014", "info": "#4472C4", "fail": "#D9534F", "threshold": 1.0, "threshold_color": "red", "grid_alpha": 0.22, "material_grid_alpha": 0.45, "bar_width": 0.62})
HEADER = MappingProxyType({"organization": "Osdag $|$ FOSSEE $|$ Indian Institute of Technology Bombay", "page": r"Page \thepage\ of \pageref{LastPage}", "default_note": r"\footnotesize\textit{* Software default value}"})
TABLE_LAYOUTS = {
    1: '|L{5.5cm}|L{8.5cm}|',
    2: '|L{5.5cm}|p{10.0cm}|',
    3: '|L{2.2cm}|L{1.8cm}|p{3.8cm}|p{3.8cm}|p{3.8cm}|',
    4: '|L{1.8cm}|L{2.3cm}|L{1.8cm}|p{4.8cm}|p{4.8cm}|',
    5: '|L{1.4cm}|p{2.2cm}|p{2.2cm}|p{3.0cm}|p{2.4cm}|p{2.2cm}|',
    6: '|L{2.2cm}|L{2.2cm}|L{3.0cm}|L{2.5cm}|C{1.8cm}|C{1.8cm}|',
    7: '|L{5.5cm}|p{9.5cm}|',
    8: '|L{3.0cm}|C{2.1cm}|C{2.1cm}|C{2.2cm}|C{1.7cm}|C{2.8cm}|',
    9: '|L{7.0cm}|C{5.5cm}|C{2.0cm}|',
    10: '|C{4.0cm}|p{11.0cm}|',
    11: "' + col_spec + '",
    12: '|C{1.0cm}|L{3.8cm}|C{2.6cm}|C{1.8cm}|C{1.8cm}|C{1.8cm}|C{1.8cm}|',
    13: '|\n>{\\centering\\arraybackslash}p{3.1cm}|\n>{\\centering\\arraybackslash}p{1.7cm}|\n>{\\centering\\arraybackslash}p{1.2cm}|\n>{\\centering\\arraybackslash}p{1.3cm}|\n>{\\centering\\arraybackslash}p{1.7cm}|\n>{\\centering\\arraybackslash}p{1.2cm}|\n>{\\centering\\arraybackslash}p{1.3cm}|\n>{\\centering\\arraybackslash}p{1.6cm}|\n>{\\centering\\arraybackslash}p{1.6cm}|',
    14: '|>{\\centering\\arraybackslash}p{5.2cm}|>{\\centering\\arraybackslash}p{5.2cm}|>{\\centering\\arraybackslash}p{5.2cm}|',
    15: '|L{7cm}|p{8.5cm}|',
    16: '|L{4cm}|L{10cm}|',
    17: '|C{2.5cm}|C{3.5cm}|C{3.5cm}|>{\\centering\\arraybackslash}p{4.2cm}|C{1.8cm}|',
    18: '|C{2.5cm}|L{8.0cm}|>{\\centering\\arraybackslash}p{5.0cm}|',
    19: '|C{2.5cm}|L{3cm}|C{3.5cm}|C{2.5cm}|>{\\centering\\arraybackslash}p{4.0cm}|',
    20: '|C{2.5cm}|L{6.5cm}|>{\\arraybackslash}p{6.5cm}|',
    21: '|C{2.5cm}|L{3.5cm}|C{3.5cm}|>{\\centering\\arraybackslash}p{4.2cm}|C{1.8cm}|',
    22: '|C{2.5cm}|L{3.5cm}|C{3.5cm}|>{\\centering\\arraybackslash}p{3.5cm}|C{2.5cm}|',
    23: '|C{2.5cm}|C{3.5cm}|C{3.5cm}|>{\\centering\\arraybackslash}p{3.5cm}|C{2.5cm}|',
    24: '|C{1.6cm}|>{\\centering\\arraybackslash}p{3.6cm}|C{2.4cm}|C{2.0cm}|C{2.1cm}|C{1.7cm}|C{1.5cm}|',
    25: '|L{3.6cm}|C{5.6cm}|>{\\centering\\arraybackslash}p{2.6cm}|L{3.0cm}|',
    26: '|L{3.2cm}|>{\\centering\\arraybackslash}p{4.3cm}|>{\\centering\\arraybackslash}p{4.3cm}|C{2.0cm}|',
    27: '|L{5.3cm}|>{\\arraybackslash}p{7.2cm}|C{2.0cm}|',
    28: '|C{3.0cm}|C{3.5cm}|C{3.0cm}|>{\\centering\\arraybackslash}p{4.2cm}|C{1.8cm}|',
    29: '|L{5.5cm}|C{3.5cm}|>{\\centering\\arraybackslash}p{4.5cm}|C{2cm}|',
    30: '|L{7cm}|>{\\arraybackslash}p{8.5cm}|',
    31: '|L{5.5cm}|>{\\centering\\arraybackslash}p{4.1cm}|>{\\centering\\arraybackslash}p{4.1cm}|C{1.8cm}|',
    32: '|C{2.0cm}|L{2.0cm}|L{2.2cm}|C{2.5cm}|C{2.0cm}|C{2.0cm}|',
    33: '|C{2.2cm}|L{2.2cm}|L{2.5cm}|C{2.5cm}|C{2.5cm}|>{\\centering\\arraybackslash}p{3.6cm}|',
    34: '|C{2.0cm}|L{1.8cm}|C{2.2cm}|C{3.0cm}|C{1.8cm}|C{1.8cm}|C{1.2cm}|C{1.8cm}|',
    35: '|C{3.4cm}|L{4.5cm}|C{2.3cm}|C{2.3cm}|>{\\centering\\arraybackslash}p{1.6cm}|',
    36: '|c|c|p{13cm}|',
}

def executive_summary_table_spec(column_count):
    count = max(1, int(column_count))
    label_width = 3.0
    available_width = 16.7
    member_width = round(max(1.5, (available_width - label_width) / count), 1)
    return (
        f"|C{{{label_width}cm}}|"
        + "|".join([f"C{{{member_width}cm}}"] * count)
        + "|"
    )


def _layout_name(number):
    result = ""
    while number:
        number, remainder = divmod(number - 1, 26)
        result = chr(65 + remainder) + result
    return result

def build_document_preamble(project_name, job_number, report_date, report_version):
    """Build the document preamble and report-wide visual macros."""
    d = DOCUMENT
    s = SPACING
    f = FIGURE
    template = r'''\documentclass[@@FONT@@,@@PAPER@@]{report}
\usepackage[@@PAPER@@,@@GEOMETRY@@]{geometry}
\usepackage[utf8]{inputenc}
\usepackage{graphicx,amsmath,amssymb,booktabs,array,tabularx,float,fancyhdr}
\usepackage[hidelinks]{hyperref}\usepackage{xcolor}\usepackage{setspace}\usepackage{enumitem}\usepackage{caption}\usepackage{subcaption}\usepackage[longtable]{multirow}\usepackage{colortbl}\usepackage{longtable}\usepackage{titlesec}\usepackage{titletoc}\usepackage{lastpage}\usepackage{makecell}\usepackage{etoolbox}\usepackage{needspace}
\captionsetup{labelfont=bf,justification=raggedright,singlelinecheck=false,format=plain}
\DeclareUnicodeCharacter{2264}{\ensuremath{\leq}}\DeclareUnicodeCharacter{00B0}{\ensuremath{^\circ}}\DeclareUnicodeCharacter{2013}{--}\DeclareUnicodeCharacter{2014}{---}\DeclareUnicodeCharacter{00B2}{\ensuremath{^2}}
\numberwithin{table}{chapter}\numberwithin{figure}{chapter}
\setlength{\LTleft}{\fill}\setlength{\LTright}{\fill}\setlength{\tabcolsep}{@@PADDING@@}\renewcommand{\arraystretch}{@@STRETCH@@}\setlength{\LTpre}{@@LTPRE@@}\setlength{\LTpost}{@@LTPOST@@}\setlength{\arrayrulewidth}{@@RULE@@}\setlength{\extrarowheight}{@@EXTRA@@}\setlength{\headheight}{18pt}\setlength{\footskip}{27pt}
\BeforeBeginEnvironment{table}{\needspace{@@MINSPACE@@\baselineskip}}
\definecolor{osdagGreen}{HTML}{@@ACCENT@@}\definecolor{reportPass}{HTML}{@@PASS@@}\definecolor{reportFail}{HTML}{@@FAIL@@}\definecolor{reportInfo}{HTML}{@@INFO@@}\definecolor{reportText}{HTML}{@@TEXT@@}\definecolor{reportWarning}{HTML}{@@WARNING@@}
\newcommand{\ReportPass}[1]{\textcolor{reportPass}{#1}}\newcommand{\ReportFail}[1]{\textcolor{reportFail}{#1}}\newcommand{\ReportInfo}[1]{\textcolor{reportInfo}{#1}}\newcommand{\ReportAccent}[1]{\textcolor{osdagGreen}{#1}}\newcommand{\ReportText}[1]{\textcolor{reportText}{#1}}
\newcolumntype{L}[1]{>{\raggedright\arraybackslash}p{#1}}\newcolumntype{C}[1]{>{\centering\arraybackslash}p{#1}}\newcolumntype{R}[1]{>{\raggedleft\arraybackslash}p{#1}}
\newcommand{\ReportSectionSpace}{\vspace{@@SECTION@@}}\newcommand{\ReportMediumSpace}{\vspace{@@MEDIUM@@}}\newcommand{\ReportSmallSpace}{\vspace{@@SMALL@@}}\newcommand{\ReportTightSpace}{\vspace{@@TIGHT@@}}\newcommand{\ReportSmallMediumSpace}{\vspace{@@SMALLMEDIUM@@}}\newcommand{\ReportParagraphSpace}{\vspace{@@PARAGRAPH@@}}\newcommand{\ReportHalfBlockSpace}{\vspace{@@HALFBLOCK@@}}\newcommand{\ReportBlockSpace}{\vspace{@@BLOCK@@}}\newcommand{\ReportMajorSpace}{\vspace{@@MAJOR@@}}\newcommand{\ReportCaptionGap}{\vspace{@@CAPGAP@@}}\newcommand{\ReportCaptionTightSpace}{\vspace{@@CAPTIGHT@@}}\newcommand{\ReportCaptionAfterSpace}{\vspace{@@CAPAFTER@@}}\newcommand{\ReportTOCRowSpace}{\vspace{@@TOCROW@@}}\newcommand{\ReportTitlePageSpace}{\vspace*{@@TITLE@@}}\newcommand{\ReportTitlePageGap}{@@TITLEGAP@@}\newcommand{\ReportLogoGap}{@@LOGOGAP@@}\newcommand{\ReportTitleSmallGap}{@@TITLESMALL@@}\newcommand{\ReportCoverTitleSpace}{\vspace{@@COVERTITLE@@}}\newcommand{\ReportTableRowBreak}{\\[@@ROW@@]}\newcommand{\ReportWideTableRowBreak}{\\[@@ROWWIDE@@]}\newcommand{\ReportTightTableRowBreak}{\\[@@ROWTIGHT@@]}
\newcommand{\ReportCompactTablePadding}{\setlength{\tabcolsep}{@@COMPACT@@}}\newcommand{\ReportDenseTablePadding}{\setlength{\tabcolsep}{@@DENSE@@}}\newcommand{\ReportAnalysisTablePadding}{\setlength{\tabcolsep}{@@ANALYSIS@@}}\newcommand{\ReportTallTableRows}{\renewcommand{\arraystretch}{@@TALL@@}}\newcommand{\ReportCaptionSize}{\@@CAPSIZE@@}\newcommand{\ReportFootnoteSize}{\@@FOOTSIZE@@}\newcommand{\ReportCaptionTopSpace}{\setlength{\abovecaptionskip}{@@CAPTOP@@}}\newcommand{\ReportCaptionBottomSpace}{\setlength{\belowcaptionskip}{@@CAPBOTTOM@@}}\newcommand{\ReportLeftAlignedLongTable}{\setlength{\LTleft}{0pt}\setlength{\LTright}{\fill}}\newcommand{\ReportLongTableStartSpace}{\Needspace{@@LONGTABLESPACE@@\baselineskip}}\newcommand{\ReportTablePageBreak}{\clearpage}
\newcommand{\ReportFigurePlacement}{@@PLACE@@}\newcommand{\ReportFloatPlacement}{@@FLOAT@@}\newcommand{\ReportPlaceholderWidth}{@@PHWIDTH@@}\newcommand{\ReportChapterFigureWidth}{@@CHWIDTH@@}\newcommand{\ReportChartWidth}{@@CHARTWIDTH@@}\newcommand{\ReportAnalysisFigureWidth}{@@ANALYSISWIDTH@@}\newcommand{\ReportCellPlaceholderWidth}{@@CELLPLACEHOLDER@@}\newcommand{\ReportCellWidth}{@@CELLWIDTH@@}\newcommand{\ReportOrgLogoHeight}{@@ORGLOGO@@}\newcommand{\ReportLogoPanelWidth}{@@LOGOPANEL@@}\newcommand{\ReportOrganizationPanelWidth}{@@ORGPANEL@@}\newcommand{\ReportCoverBrand}[1]{\Huge\textbf{#1}}\newcommand{\ReportCoverSubtitle}[1]{\large #1}\newcommand{\ReportCoverTitle}[1]{\Large #1}
\newcommand{\ReportExecutiveTitle}{\centering\@@EXECUTIVE@@\bfseries Executive Summary\par}\newcommand{\ReportChapterTitleFormat}{\titleformat{\chapter}[block]{\normalfont\@@CHAPTER@@\bfseries\centering}{\thechapter}{@@CHAPTERGAP@@}{}}\newcommand{\ReportStandardChapterSpacing}{\titlespacing*{\chapter}{0pt}{0pt}{10pt}}\newcommand{\ReportExecutiveChapterSpacing}{\titlespacing*{\chapter}{0pt}{@@EXECPRE@@}{@@EXECAFT@@}}\newcommand{\ReportTOCTitleFormat}{\centering\@@TOCTITLE@@\bfseries}
\setstretch{@@LINE@@}
\newbool{hasSDonPage}\boolfalse{hasSDonPage}
\fancypagestyle{main}{\fancyhf{}\fancyhead[L]{@@PROJECT@@ $|$ @@JOB@@}\fancyhead[R]{@@DATE@@ $|$ @@VERSION@@}\fancyfoot[L]{@@ORG@@}\fancyfoot[C]{\raisebox{@@FOOTRAISE@@}[0pt][0pt]{\ifbool{hasSDonPage}{\ReportText{@@DEFAULTNOTE@@}}{}}}\fancyfoot[R]{@@PAGE@@}\renewcommand{\headrule}{\color{osdagGreen}\hrule width\headwidth height @@HEADRULE@@\vspace{@@HEADGAP@@}}\renewcommand{\footrule}{\color{osdagGreen}\hrule width\headwidth height @@HEADRULE@@\vspace{@@FOOTRULEGAP@@}}}
\fancypagestyle{plain}{\fancyhf{}\fancyhead[L]{@@PROJECT@@ $|$ @@JOB@@}\fancyhead[R]{@@DATE@@ $|$ @@VERSION@@}\fancyfoot[L]{@@ORG@@}\fancyfoot[C]{\raisebox{@@FOOTRAISE@@}[0pt][0pt]{\ifbool{hasSDonPage}{\ReportText{@@DEFAULTNOTE@@}}{}}}\fancyfoot[R]{@@PAGE@@}\renewcommand{\headrule}{\color{osdagGreen}\hrule width\headwidth height @@HEADRULE@@\vspace{@@HEADGAP@@}}\renewcommand{\footrule}{\color{osdagGreen}\hrule width\headwidth height @@HEADRULE@@\vspace{@@FOOTRULEGAP@@}}}
\fancypagestyle{firstpage}{\fancyhf{}\renewcommand{\headrulewidth}{0pt}\fancyfoot[L]{@@ORG@@}\fancyfoot[R]{@@PAGE@@}\renewcommand{\footrule}{\color{osdagGreen}\hrule width\headwidth height @@HEADRULE@@\vspace{@@FOOTRULEGAP@@}}}\pagestyle{main}
\newcommand{\placeholder}[1]{\textit{\textless #1\textgreater}}\newcommand{\todo}[1]{\colorbox{reportWarning}{TODO: #1}}\newcommand{\sdstar}{\textsuperscript{*}}\newcommand{\markSD}{\global\booltrue{hasSDonPage}}\renewcommand{\sdstar}{\textsuperscript{*}\markSD{}}\AddToHook{shipout/before}{\global\boolfalse{hasSDonPage}}
\title{\Huge\textbf{OsdagBridge} \\ \large Open Source Software for Steel Girder Bridge Design \\ \vspace{2cm} \Large Design Report}\author{}\date{}
@@TABLE_LAYOUT_MACROS@@\begin{document}
'''
    values = {"FONT":d["font_size"],"PAPER":d["paper"],"GEOMETRY":d["geometry"],"PADDING":d["table_padding"],"STRETCH":d["row_stretch"],"LTPRE":d["longtable_pre"],"LTPOST":d["longtable_post"],"RULE":d["rule_width"],"EXTRA":d["extra_row_height"],"MINSPACE":d["min_table_space"],"LONGTABLESPACE":d["longtable_start_lines"],"ACCENT":COLORS["accent"],"PASS":COLORS["pass"],"FAIL":COLORS["fail"],"INFO":COLORS["info"],"TEXT":COLORS["text"],"WARNING":COLORS["warning"],"SECTION":s["section"],"MEDIUM":s["medium"],"SMALL":s["small"],"TIGHT":s["tight"],"SMALLMEDIUM":s["small_medium"],"PARAGRAPH":s["paragraph"],"HALFBLOCK":s["half_block"],"BLOCK":s["block"],"MAJOR":s["major"],"CAPGAP":s["caption_gap"],"CAPTIGHT":s["caption_tight"],"CAPAFTER":s["caption_after"],"TOCROW":s["toc_row"],"TITLE":s["title"],"TITLEGAP":s["title_gap"],"LOGOGAP":s["logo_gap"],"TITLESMALL":s["title_small"],"COVERTITLE":s["cover_title"],"ROW":s["row"],"ROWWIDE":s["row_wide"],"ROWTIGHT":s["row_tight"],"COMPACT":TABLE["compact_padding"],"DENSE":TABLE["dense_padding"],"ANALYSIS":TABLE["analysis_padding"],"TALL":TABLE["row_stretch"],"CAPTOP":TABLE["caption_top"],"CAPBOTTOM":TABLE["caption_bottom"],"CAPSIZE":TYPOGRAPHY["caption"],"FOOTSIZE":TYPOGRAPHY["footnote"],"EXECUTIVE":TYPOGRAPHY["executive_title"],"CHAPTER":TYPOGRAPHY["chapter_title"],"TOCTITLE":TYPOGRAPHY["toc_title"],"CHAPTERGAP":SPACING["chapter_number_gap"],"EXECPRE":SPACING["executive_chapter_before"],"EXECAFT":SPACING["executive_chapter_after"],"PLACE":f["placement"],"FLOAT":f["float_placement"],"PHWIDTH":f["placeholder_width"],"CHWIDTH":f["chapter_width"],"CHARTWIDTH":f["chart_width"],"ANALYSISWIDTH":f["analysis_width"],"CELLPLACEHOLDER":f["cell_placeholder_width"],"CELLWIDTH":f["cell_width"],"ORGLOGO":f["org_logo_height"],"LOGOPANEL":f["logo_panel"],"ORGPANEL":f["org_panel"],"LINE":d["line_spacing"],"PROJECT":project_name,"JOB":job_number,"DATE":report_date,"VERSION":report_version,"ORG":HEADER["organization"],"PAGE":HEADER["page"],"HEADRULE":d["header_rule"],"HEADGAP":d["header_gap"],"FOOTRAISE":d["footer_note_raise"],"FOOTRULEGAP":d["footer_gap"],"DEFAULTNOTE":HEADER["default_note"]}
    for key, value in values.items():
        template = template.replace(f"@@{key}@@", str(value))
    return template.replace("@@TABLE_LAYOUT_MACROS@@", "")


def expand_table_layouts(document_tex):
    """Replace layout aliases with valid literal LaTeX column specifications."""
    keys = [c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if c not in "LCR"] + [c for c in "abcdefghijklmnopqrstuvwxyz" if c not in "lcrpmb"] + list("0123456789")
    lookup = {keys[index]: layout for index, layout in enumerate(TABLE_LAYOUTS.values())}
    pattern = re.compile(r"(\\begin\{(?:longtable|tabular)\}\{)\\([A-Za-z0-9])(\})")
    return pattern.sub(lambda match: match.group(1) + lookup.get(match.group(2), match.group(2)) + match.group(3), document_tex)


def build_toc_section():
    return r'''\ReportChapterTitleFormat
\ReportStandardChapterSpacing
\setcounter{tocdepth}{2}
\titlecontents{chapter}[1.5em]{\normalfont\ReportTOCRowSpace}{\contentslabel{1.5em}}{\hspace*{-1.5em}}{\hfill\contentspage}
\titlecontents{section}[3.8em]{\normalfont}{\contentslabel{2.3em}}{\hspace*{-2.3em}}{\hfill\contentspage}
\titlecontents{subsection}[7.0em]{\normalfont}{\contentslabel{3.2em}}{\hspace*{-3.2em}}{\hfill\contentspage}
\newpage\renewcommand{\contentsname}{\ReportTOCTitleFormat Table of Contents}\tableofcontents'''
