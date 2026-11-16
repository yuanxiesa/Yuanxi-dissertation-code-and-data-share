"""Render CSV assessments as individually cropped PNG cards.

Run: python3 scripts/generate_assessment_cards.py
Use --all for every CSV row, or repeat --doi to select publications.
Requires pdflatex (TeX Live) and pdftoppm (Poppler) on PATH.
"""
import argparse
import ast
import csv
import hashlib
import html
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
DEMO_DOIS = ['10.1002/chir.23189', '10.1002/mrc.5234', '10.1002/mrc.4130',
             '10.1002/anie.201706532', '10.1007/s12272-020-01277-4']
DIAGRAMS = {'Aware': 'AwareOfProblem Defeat Diagram.png',
            'Review': 'Review Defeat Diagram.png', 'IntroOnly': 'IntroOnly Defeat Diagrm.png'}


def escape(text):
    mapping = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$',
               '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}',
               '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}
    return ''.join(mapping.get(c, c) for c in text)


def message_tex(text):
    # Preserve CSV wording; render its Markdown bold spans as bold text.
    return ''.join(r'\textbf{' + escape(part) + '}' if i % 2 else escape(part)
                   for i, part in enumerate(text.split('**')))


def read_rows(path):
    with path.open(encoding='utf-8-sig', newline='') as stream:
        return list(csv.DictReader(stream))


def card_tex(row, metadata):
    messages = ast.literal_eval(row['message'])
    if not isinstance(messages, list) or not messages or not all(isinstance(m, str) for m in messages):
        raise ValueError(f"Invalid message list for {row['DOI']}")
    if row['verdict'] not in ('at risk', 'not at risk'):
        raise ValueError(f"Invalid verdict for {row['DOI']}")
    surname = metadata['Author'].split(';')[0].split(',')[0].strip()
    author = surname + (' et al.' if ';' in metadata['Author'] else '')
    publication_label = f"{author} ({metadata['Publication Year'].strip()})"
    messages = [m.replace('Publication ' + row['tag'] + ' (DOI:',
                          'Publication ' + publication_label + ' (DOI:')
                for m in messages]
    title = html.unescape(re.sub(r'<[^>]+>', '', metadata['Title']))
    images = [ROOT / 'img' / name for flag, name in DIAGRAMS.items() if row[flag] == 'y']
    if images:
        visualization = '\n\\par\\vspace{6pt}\n'.join(
            r'\includegraphics[width=\linewidth]{\detokenize{' + str(p) + '}}' for p in images)
    else:
        visualization = r'''\vspace{20pt}\colorbox{wash}{\begin{minipage}{0.85\linewidth}
\centering\vspace{14pt}No identified defeater\par\vspace{12pt}
$\mathrm{Cite}(y,x)\Rightarrow\mathrm{UP}(x,y)$\par\vspace{12pt}
Default inference remains defeasible.\vspace{14pt}\end{minipage}}'''
    return r'''\documentclass[11pt]{article}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx,amsmath,xcolor,newtxtext,newtxmath,ragged2e}
\usepackage[active,tightpage]{preview}
\setlength{\PreviewBorder}{4pt}
\definecolor{ink}{HTML}{243746}\definecolor{wash}{HTML}{F2F5F7}
\setlength{\parindent}{0pt}\setlength{\parskip}{7pt}\setlength{\fboxsep}{14pt}
\begin{document}\begin{preview}
\fcolorbox{ink}{white}{\begin{minipage}{6.7in}
{\Large\bfseries Assessment Card}\par
\textbf{''' + escape(author) + '}\\par\n\\textit{' + escape(title) + r'''}\par
{\small DOI: ''' + escape(row['DOI']) + r'''}\par
\vspace{8pt}{\color{ink}\hrule}\vspace{12pt}
\begin{minipage}[t]{0.46\linewidth}\vspace{0pt}\RaggedRight
\textbf{Justifications}\par
''' + '\n\\par\\vspace{\\baselineskip}\n'.join(message_tex(m) for m in messages) + r'''
\end{minipage}\hfill
\begin{minipage}[t]{0.49\linewidth}\vspace{0pt}
\textbf{Reasoning Visualization}\par
''' + visualization + r'''
\end{minipage}\par\vspace{16pt}{\color{ink}\hrule}\vspace{9pt}
{\large\bfseries Verdict: ''' + escape(row['verdict']) + r'''}
\end{minipage}}
\end{preview}\end{document}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--csv', type=Path, default=ROOT / 'results/chpt6-results.csv')
    parser.add_argument('--metadata', type=Path, default=ROOT / 'data/DOI-10-13012-b2idb-4610831_v3/Willoughby2014_286citing_publications.csv')
    parser.add_argument('--output-dir', type=Path, default=ROOT / 'output/assessment-cards')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--all', action='store_true')
    group.add_argument('--doi', action='append')
    parser.add_argument('--dpi', type=int, default=200)
    args = parser.parse_args()
    for tool in ('pdflatex', 'pdftoppm'):
        if not shutil.which(tool):
            parser.error(f'{tool} is required on PATH')
    if args.dpi < 72:
        parser.error('--dpi must be at least 72')
    rows = {r['DOI'].strip().lower(): r for r in read_rows(args.csv)}
    metadata = {r['DOI'].strip().lower(): r for r in read_rows(args.metadata)}
    selected = list(rows) if args.all else [d.strip().lower() for d in (args.doi or DEMO_DOIS)]
    missing = [d for d in selected if d not in rows or d not in metadata]
    if missing:
        parser.error('Missing assessments or metadata: ' + ', '.join(missing))
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = []
    for doi in selected:
        row = rows[doi]
        stem = re.sub(r'[^a-zA-Z0-9.-]+', '_', doi) + '_' + hashlib.sha256(doi.encode()).hexdigest()[:8]
        output = args.output_dir / stem
        source = card_tex(row, metadata[doi])
        output.with_name(output.name + '.tex').write_text(source, encoding='utf-8')
        with tempfile.TemporaryDirectory(prefix='assessment-card-') as directory:
            work = Path(directory)
            (work / 'card.tex').write_text(source, encoding='utf-8')
            result = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', 'card.tex'], cwd=work, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(f'LaTeX failed for {doi}:\n{result.stdout[-4000:]}')
            subprocess.run(['pdftoppm', '-png', '-singlefile', '-r', str(args.dpi), str(work / 'card.pdf'), str(output.resolve())], check=True, capture_output=True)
        manifest.append({'DOI': doi, 'verdict': row['verdict'], 'png': output.name + '.png'})
        print(output.with_name(output.name + '.png'))
    with (args.output_dir / 'manifest.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=['DOI', 'verdict', 'png'])
        writer.writeheader()
        writer.writerows(manifest)


if __name__ == '__main__':
    main()
