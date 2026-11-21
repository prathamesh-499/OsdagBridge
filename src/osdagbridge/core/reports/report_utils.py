import re
from osdagbridge.core.reports.styles import FIGURE, SPACING, TYPOGRAPHY

from osdagbridge.core.utils.common import (
    KEY_MP_GD_MEMBER_ID,
    KEY_MP_GD_SELECT_GIRDER,
    KEY_MP_GIRDER_DEPTH,
    KEY_TS_NO_OF_GIRDERS
)

_ROW_END = re.compile(r"(?:\\\\(?:\[[^]]+\])?|\\Report(?:Wide)?TableRowBreak)")


def repeat_longtable_headers(document_tex):
    """Add continuation headers to longtables with a conventional bold header row.

    Chapter builders produce the final LaTeX as strings, including dynamic rows.
    Running this on the assembled document lets the same rule cover both static
    and dynamically-sized tables without duplicating their header definitions.
    Tables that already define longtable head sections are left untouched.
    """
    table_pattern = re.compile(r"\\begin\{longtable\}.*?\\end\{longtable\}", re.DOTALL)

    def _add_head(match):
        table = match.group(0)
        start_space = r"\ReportLongTableStartSpace" + "\n"
        if r"\endfirsthead" in table or r"\endhead" in table:
            return start_space + table

        lines = table.splitlines(keepends=True)
        caption_index = next(
            (i for i, line in enumerate(lines) if r"\caption" in line), None
        )
        if caption_index is None:
            return start_space + table
        if not re.search(r"\\\\(?:\[[^]]+\])?\s*$", lines[caption_index].rstrip()):
            lines[caption_index] = lines[caption_index].rstrip("\n") + r"\\" + "\n"

        # Find every consecutive bold header row. Some report tables have a
        # two-line heading (for example, a grouped braking-load header); copying
        # only the first row produces a malformed continuation header.
        header_index = next(
            (
                i for i in range(caption_index + 1, len(lines))
                if r"\textbf" in lines[i]
                and _ROW_END.search(lines[i])
            ),
            None,
        )
        if header_index is None:
            return start_space + "".join(lines)

        header_end = header_index
        last_header_row = header_index
        for i in range(header_index + 1, len(lines)):
            line = lines[i]
            if r"\textbf" in line and _ROW_END.search(line):
                last_header_row = i
                header_end = i
            elif last_header_row > header_index and (
                r"\hline" in line or r"\cline" in line
            ):
                header_end = i
            elif not line.strip() or r"\cline" in line:
                continue
            elif _ROW_END.search(line):
                # The first non-bold table row is the body. Stop before it.
                break

        if last_header_row == header_index:
            # A single-row header is valid; the loop can still extend its
            # header block over the closing rule below.
            pass
        if header_end < header_index:
            return start_space + table

        header_block = "".join(lines[header_index:header_end + 1])
        # Include the rule immediately below the last header row so the
        # continued table has the same separation from its body.
        if header_end + 1 < len(lines) and r"\hline" in lines[header_end + 1]:
            header_end += 1
            header_block = "".join(lines[header_index:header_end + 1])
        repeated_head = (
            r"\endfirsthead" + "\n"
            + r"\hline" + "\n"
            + header_block
            + r"\endhead" + "\n"
        )
        lines.insert(header_end + 1, repeated_head)
        return start_space + "".join(lines)

    return table_pattern.sub(_add_head, document_tex)


def _tex(value):
    """Escape a Python value for safe LaTeX embedding."""
    s = str(value) if value is not None else ''
    if not s:
        return r''
    # Normalise non-ASCII glyphs from section designations (e.g. "∠ 100 ⅹ 100ⅹ 10")
    # that pdflatex cannot render.
    for uni, ascii_ in [('∠', 'L'), ('ⅹ', 'x'), ('×', 'x')]:
        s = s.replace(uni, ascii_)
    s = s.replace('\\', r'\textbackslash{}')
    for ch, esc in [('&', r'\&'), ('%', r'\%'), ('$', r'\$'), ('#', r'\#'),
                    ('{', r'\{'), ('}', r'\}'),          
                    ('_', r'\_\allowbreak{}'),            
                    ('~', r'\textasciitilde{}'), ('^', r'\^{}')]:
        s = s.replace(ch, esc)
    s = s.replace(':', r':\allowbreak{}')
    return s


def _render_value(source_dict, key, unit=""):
    val = source_dict.get(key)
    if val in ("", None):
        return ""
    return _tex(val) + unit


def get_girder_entries(input_dict):
    """
    Retrieve all girder labels and member IDs from backend keys.

    Usage Example:
    --------------------------
    girder_entries = get_girder_entries(bridge.input_dict)
    
    # 1. Fallback handling (if backend hasn't populated keys yet)
    if not girder_entries:
        n = int(bridge.input_dict.get(KEY_TS_NO_OF_GIRDERS, 1))
        girder_entries = [(f"Girder {i}", f"M1") for i in range(1, n + 1)]
        
    # 2. Get total number of girders safely
    n_girders = len(girder_entries)
    
    # 3. Iterate over the girders to build table rows
    for lbl, mid in girder_entries:
        # lbl will be e.g., "G1", mid will be e.g., "G1M1"
        # Access girder specific keys dynamically:
        # val = input_dict.get(f"{KEY_MP_GIRDER_DEPTH}.{lbl}.{mid}")
        pass

    Returns:
        List[Tuple[str, str]]
    """
    n = int(input_dict.get(KEY_TS_NO_OF_GIRDERS, 0))

    entries = []

    for i in range(1, n + 1):
        entries.append(
            (
                input_dict.get(f"{KEY_MP_GD_SELECT_GIRDER}.G{i}", ""),
                input_dict.get(f"{KEY_MP_GD_MEMBER_ID}.G{i}.M1", ""),
            )
        )

    return entries


def _fig_or_placeholder(path, caption, width=FIGURE["summary_width"]):
    """Embed figure if path is provided (file already copied to assets), else show placeholder box.
    path is the relative path as pdflatex will see it (e.g. 'assets/plan.png').
    """
    if path:
        p = path.replace('\\', '/')
        return (r'\begin{figure}[H]' + '\n'
                r'\centering' + '\n'
                r'\includegraphics[width=' + width + ']{' + p + '}\n'
                r'\caption*{' + caption + '}\n'
                r'\end{figure}')
    return (r'\begin{figure}[H]' + '\n'
            r'\centering' + '\n'
            r'\fbox{\parbox{' + FIGURE["placeholder_width"] + '}{' + '\n'
            r'\textit{[ PLACEHOLDER: ' + caption + r' ]}' + '\n'
            r'}}' + '\n'
            r'\caption*{' + caption + '}\n'
            r'\end{figure}')

def _fig_embed(path, caption, width=FIGURE["full_width"], height=None):
    """Embed a real figure when path is provided (already copied); otherwise use an fbox placeholder."""
    if path:
        p = path.replace('\\', '/')
        opts = 'width=' + width
        if height:
            opts += ',height=' + height + ',keepaspectratio'
        return (r'\begin{figure}[H]' + '\n'
                r'\vspace{' + SPACING["figure_before"] + '}\n'
                r'\centering' + '\n'
                r'\includegraphics[' + opts + ']{' + p + '}\n'
                r'\vspace{' + SPACING["figure_after"] + '}\n'
                r'\caption*{' + '\\' + TYPOGRAPHY["caption"] + ' ' + caption + '}\n'
                r'\vspace{' + SPACING["figure_before"] + '}\n'
                r'\end{figure}')
    # fbox placeholder — matches template exactly
    return (r'\noindent\fbox{\parbox{' + FIGURE["placeholder_width"] + '}{' + '\n'
            r'\textit{[ PLACEHOLDER: ' + caption + r' ]}' + '\n'
            r'}}')


