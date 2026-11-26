"""Regenerate the three diagram template PNGs and their editable TeX sources."""
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def diagram_tex(kind):
    awareness = kind == 'awareness'
    index = {'awareness': '1', 'review': '2', 'introduction-only': '3'}[kind]
    premise = {'awareness': r'\mathrm{AwareOfProblem}(y,x)',
               'review': r'\mathrm{Review}(y)',
               'introduction-only': r'\mathrm{IntroOnly}(y,x)'}[kind]
    target = '1a' if awareness else '2a'
    top = rf'u_{index}(y,x):\quad {premise}\Rightarrow\neg r_{{{target}}}(y,x)'
    if awareness:
        nodes = r'''
\node[claim] (cite) at (0,0) {$\mathrm{Cite}(y,x)$};
\node[claim] (up) at (10,0) {$\mathrm{UP}(x,y)$};
\draw[flow] (cite.east) -- node[below=5pt] {$r_{1a}(y,x)$} (up.west);
\coordinate (attack) at (5,0.22);
\node[rules] at (5,-2.35) {$r_{1a}(y,x):\quad\mathrm{Cite}(y,x)\Rightarrow\mathrm{UP}(x,y)$};
'''
    else:
        nodes = r'''
\node[claim] (cite) at (0,0) {$\mathrm{Cite}(y,x)$};
\node[claim] (use) at (5,0) {$\mathrm{Use}(y,x)$};
\node[claim] (up) at (10,0) {$\mathrm{UP}(x,y)$};
\draw[flow] (cite.east) -- node[below=5pt] {$r_{2a}(y,x)$} (use.west);
\draw[flow] (use.east) -- node[below=5pt] {$r_{2b}(y,x)$} (up.west);
\coordinate (attack) at (2.5,0.22);
\node[rules] at (5,-2.65) {$\begin{aligned}
r_{2a}(y,x):\quad &\mathrm{Cite}(y,x)\Rightarrow\mathrm{Use}(y,x)\\[8pt]
r_{2b}(y,x):\quad &\mathrm{Use}(y,x)\Rightarrow\mathrm{UP}(x,y)
\end{aligned}$};
'''
    attack_x = '5' if awareness else '2.5'
    return r'''\documentclass[border=12pt]{standalone}
\usepackage{amsmath,newtxtext,newtxmath,tikz}
\usetikzlibrary{arrows.meta}
\definecolor{attackred}{HTML}{B71919}
\begin{document}
\begin{tikzpicture}[
font=\Large,
claim/.style={draw=black,line width=1.2pt,rounded corners=9pt,minimum width=3.1cm,minimum height=1.35cm,fill=white},
rules/.style={draw=black!60,line width=1pt,rounded corners=8pt,fill=black!5,inner sep=14pt},
flow/.style={-{Stealth[length=9pt,width=9pt]},line width=1.4pt}]
''' + nodes + rf'''
\node[draw=attackred,line width=1.2pt,rounded corners=9pt,fill=red!9,inner sep=14pt] (defeater) at (5,3.25) {{${top}$}};
\draw[attackred,line width=1.5pt,{{Bar[width=15pt]}}-] (attack) -- (attack |- defeater.south);
\node[text=attackred,anchor=west,font=\Large\itshape] at ({attack_x},1.55) {{undercuts}};
\end{{tikzpicture}}
\end{{document}}
'''


def main():
    names = {'awareness': 'AwareOfProblem Defeat Diagram',
             'review': 'Review Defeat Diagram',
             'introduction-only': 'IntroOnly Defeat Diagrm'}
    sources = ROOT / 'img' / 'diagram-sources'
    sources.mkdir(exist_ok=True)
    for kind, name in names.items():
        source = diagram_tex(kind)
        (sources / f'{kind}.tex').write_text(source)
        with tempfile.TemporaryDirectory(prefix='reasoning-diagram-') as directory:
            work = Path(directory)
            (work / 'diagram.tex').write_text(source)
            result = subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                                     'diagram.tex'], cwd=work, capture_output=True, text=True)
            if result.returncode:
                raise RuntimeError(result.stdout[-4000:])
            output = ROOT / 'img' / name
            subprocess.run(['pdftoppm', '-png', '-singlefile', '-r', '200',
                            str(work / 'diagram.pdf'), str(output)], check=True,
                           capture_output=True)
            print(output.with_suffix('.png'))


if __name__ == '__main__':
    main()
