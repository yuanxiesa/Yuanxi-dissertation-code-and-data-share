from pathlib import Path
cases=[
('Awareness of the code glitch','Liu et al. (2020)','Stereochemical revision of xylogranatin F by GIAO and DU8+ NMR calculations','10.1002/chir.23189',
'The bibliography annotation records a citation to Neupane et al. (2019) or Willoughby et al. (2020). Review status and introduction-only citations are not positively annotated.',
'The citation provides a defeasible reason to infer that the authors were aware of the code glitch. This awareness undercuts the inference from citing the WJH protocol to unreliability propagating from it to this publication, $r_{1a}$.',
'Not at risk','This publication is judged not at risk on the basis of evidence suggesting awareness of the glitch. Further evidence may warrant revising this judgment.',
['AwareOfProblem Defeat Diagram.png']),
('Review status','Jonas et al. (2022)','Prediction of chemical shift in NMR: A review','10.1002/mrc.5234',
'At least one of Scopus and Web of Science identifies this publication as a review. Awareness and introduction-only citations are not positively annotated.',
'Review articles generally discuss existing research rather than execute the WJH protocol. Review status therefore provides a reason to undercut the inference from citing the protocol to using it in research, $r_{2a}$.',
'Not at risk','This publication is judged not at risk on the basis of its review status. The judgment may be revised if additional evidence indicates relevant use of the protocol.',
['Review Defeat Diagram.png']),
('Introduction-only citations','Lomas (2014)',r'$^1$H NMR spectra of alcohols and diols in chloroform: DFT/GIAO calculation of chemical shifts','10.1002/mrc.4130',
'All citations to the WJH protocol are annotated as appearing in the introduction. Awareness and review status are not positively annotated.',
'The location of the citations suggests that the protocol serves as background information. This provides a defeasible reason to undercut the inference from citation to use, $r_{2a}$. Citation text indicating actual use could defeat this reason, as in the counterexamples discussed in the chapter.',
'Not at risk','This publication is judged not at risk on the basis of citation location. Evidence of actual use in the citation contexts may warrant revising this judgment.',
['IntroOnly Defeat Diagrm.png']),
('No identified defeater','Matsuo et al. (2017)','Structural Revision and Biomimetic Synthesis of Goupiolone B','10.1002/anie.201706532',
'None of the three indicators---awareness, review status, and introduction-only citations---is positive in the annotated data.',
'Neither the publication metadata, bibliography, nor section headings provide an identified reason to defeat the inference from citation to unreliability propagation, $r_{1a}$. The default inference therefore remains undefeated by the evidence checked in this prototype.',
'Still at risk','This publication is judged to remain at risk of unreliability propagation. The judgment is defeasible: additional evidence, including citation-context content, may warrant revising it.',[]),
('Multiple justifications','Kim et al. (2020)','Structure elucidation of small organic molecules by contemporary computational chemistry methods','10.1007/s12272-020-01277-4',
'The bibliography annotation records a citation to the glitch report or the addendum, and at least one database identifies the publication as a review. Introduction-only citations are not positively annotated.',
'\\textbf{1. Awareness.} The citation supports a defeasible inference of awareness of the glitch, undercutting the inference from citation to UP, $r_{1a}$.\n\n\\textbf{2. Review status.} Review status supplies a separate reason to undercut the inference from citation to use, $r_{2a}$. Both justifications are retained.',
'Not at risk','This publication is judged not at risk for two distinct reasons. Retaining both explanations makes the grounds explicit; it does not assign a higher confidence score.',
['AwareOfProblem Defeat Diagram.png','Review Defeat Diagram.png'])]
import ast, csv, json, re
nb=json.load(open('scripts/prototype-chpt6.ipynb'))
templates={}
for cell in nb['cells']:
 for node in ast.parse(''.join(cell['source'])).body:
  if isinstance(node,ast.Assign) and isinstance(node.value,ast.Constant):
   for target in node.targets:
    if isinstance(target,ast.Name) and target.id.startswith('template_'):templates[target.id]=node.value.value
base=Path('data/DOI-10-13012-b2idb-4610831_v3')
meta={r['DOI'].strip().lower():r for r in csv.DictReader(open(base/'Willoughby2014_286citing_publications.csv',encoding='utf-8-sig'))}
annotations={r['DOI'].strip().lower():r for r in csv.DictReader(open(base/'Willoughby2014_citation_contexts.csv',encoding='utf-8-sig'))}
def texescape(t):
 return ''.join({'&':r'\&','%':r'\%','$':r'\$','#':r'\#','_':r'\_','{':r'\{','}':r'\}'}.get(c,c) for c in t)
saved={r['DOI']:r for r in csv.DictReader(open('results/chpt6-results.csv',encoding='utf-8-sig'))}
def messages(doi):
 out=[]
 for message in ast.literal_eval(saved[doi]['message']):
  text=texescape(message)
  text=re.sub(r'\*\*(.*?)\*\*',lambda m:r'\textbf{'+m.group(1)+'}',text)
  out.append(text)
 return '\n\n'.join(out)
head=r''' \documentclass[11pt]{article}
\usepackage[letterpaper,margin=0.7in]{geometry}
\usepackage{graphicx,amsmath,xcolor,hyperref}
\usepackage[T1]{fontenc}
\usepackage{newtxtext,newtxmath}
\definecolor{ink}{HTML}{243746}
\definecolor{wash}{HTML}{F2F5F7}
\hypersetup{colorlinks=true,urlcolor=ink}
\setlength{\parindent}{0pt}
\setlength{\parskip}{7pt}
\setlength{\fboxsep}{14pt}
\newcommand{\field}[1]{\par\vspace{5pt}{\color{ink}\bfseries #1}\par}
\begin{document}
'''
pages=[]
for i,(label,author,title,doi,evidence,reason,verdict,conclusion,imgs) in enumerate(cases,1):
 pic=''
 if imgs:
  for im in imgs:
   width=r'\linewidth' if len(imgs)==1 else r'0.91\linewidth'
   pic+=r'\includegraphics[width='+width+']{img/'+im+'}\\[5pt]\n'
  pic=pic.replace('\\n','\n')
  pic+=r'{\footnotesize Red marks the undercutting defeater. '
  if 'AwareOfProblem Defeat Diagram.png' in imgs:pic+=r'\textit{AwareOfProblem} in the image corresponds to \textit{AwareOfIssue} in the chapter. '
  pic+='}'
 else:
  pic=r'''\vspace{30pt}\colorbox{wash}{\begin{minipage}{0.86\linewidth}\centering\vspace{16pt}No identified defeater\par\vspace{12pt}$\mathrm{Cite}(y,x)\Rightarrow\mathrm{UP}(x,y)$\par\vspace{12pt}Default inference remains defeasible.\vspace{16pt}\end{minipage}}'''
 reason=messages(doi)
 pic=pic.replace(r'\[5pt]',r'\\[5pt]')
 pic=pic.split(r'{\footnotesize Red marks')[0]
 page=r'''{\small\color{ink}CHAPTER 6 \quad COMPUTATIONAL PIPELINES}\par\vspace{12pt}
\fcolorbox{ink}{white}{\begin{minipage}{\dimexpr\linewidth-2\fboxsep-2\fboxrule\relax}
{\Large\bfseries Assessment Card}\par
\textbf{'''+author+r'''}\par\textit{'''+title+r'''}\par
{\small DOI: \nolinkurl{'''+doi+r'''}}\par
\vspace{8pt}{\color{ink}\hrule}\vspace{12pt}
\begin{minipage}[t]{0.46\linewidth}\vspace{0pt}
\field{Justifications}
'''+reason+r'''
\end{minipage}\hfill
\begin{minipage}[t]{0.49\linewidth}\vspace{0pt}
\field{Reasoning visualization}
'''+pic+r'''

\end{minipage}
\par\vspace{16pt}{\color{ink}\hrule}\vspace{9pt}
{\large\bfseries Final verdict: '''+saved[doi]['verdict']+r'''}\par

\end{minipage}}
\par\vspace{10pt}{\footnotesize Based on the annotated dataset and Chapter 6 prototype. Justifications and verdicts reproduce the saved Chapter 6 CSV results.}
'''
 pages.append(page)
Path('output/pdf/computational-pipeline-examples.tex').write_text(head+'\n\\newpage\n'.join(pages)+'\n\\end{document}\n')
