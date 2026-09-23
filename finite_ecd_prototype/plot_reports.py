#!/usr/bin/env python3
"""Generate simple SVG plots from benchmark summary JSON files."""
from __future__ import annotations
import argparse, json
from pathlib import Path


def load_cases(path):
    data = json.loads(Path(path).read_text())
    return [c["summary"] for c in data.get("cases", []) if isinstance(c.get("summary"), dict)]


def svg_scatter(cases, xkey, ykey, title):
    W,H,ML,MB = 720,420,70,55
    xs=[c[xkey] for c in cases if c.get(xkey) is not None and c.get(ykey) is not None]
    ys=[c[ykey] for c in cases if c.get(xkey) is not None and c.get(ykey) is not None]
    if not xs or not ys: return "<svg xmlns='http://www.w3.org/2000/svg'><text x='10' y='20'>no data</text></svg>"
    xmin,xmax=min(xs),max(xs); ymin,ymax=min(ys),max(ys)
    if xmin==xmax: xmax=xmin+1
    if ymin==ymax: ymax=ymin+1
    def X(x): return ML+(x-xmin)/(xmax-xmin)*(W-ML-30)
    def Y(y): return H-MB-(y-ymin)/(ymax-ymin)*(H-40-MB)
    parts=[f"<svg xmlns='http://www.w3.org/2000/svg' width='{W}' height='{H}' viewBox='0 0 {W} {H}'>",
           "<rect width='100%' height='100%' fill='white'/>",
           f"<text x='{W/2}' y='24' text-anchor='middle' font-family='sans-serif' font-size='18'>{title}</text>",
           f"<line x1='{ML}' y1='{H-MB}' x2='{W-30}' y2='{H-MB}' stroke='black'/>",
           f"<line x1='{ML}' y1='40' x2='{ML}' y2='{H-MB}' stroke='black'/>",
           f"<text x='{W/2}' y='{H-12}' text-anchor='middle' font-family='sans-serif'>{xkey}</text>",
           f"<text transform='translate(16 {H/2}) rotate(-90)' text-anchor='middle' font-family='sans-serif'>{ykey}</text>"]
    for c in cases:
        if c.get(xkey) is None or c.get(ykey) is None: continue
        label=Path(c.get('instance','')).name.replace('_instance.json','')
        parts.append(f"<circle cx='{X(c[xkey]):.2f}' cy='{Y(c[ykey]):.2f}' r='5' fill='#2563eb'/>")
        parts.append(f"<text x='{X(c[xkey])+7:.2f}' y='{Y(c[ykey])-7:.2f}' font-size='10' font-family='sans-serif'>{label}</text>")
    parts.append(f"<text x='{ML}' y='{H-MB+18}' font-size='10' font-family='sans-serif'>{xmin}</text>")
    parts.append(f"<text x='{W-45}' y='{H-MB+18}' font-size='10' font-family='sans-serif'>{xmax}</text>")
    parts.append(f"<text x='{ML-45}' y='{H-MB}' font-size='10' font-family='sans-serif'>{ymin:.3g}</text>")
    parts.append(f"<text x='{ML-45}' y='45' font-size='10' font-family='sans-serif'>{ymax:.3g}</text>")
    parts.append("</svg>")
    return "\n".join(parts)


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('sweep'); ap.add_argument('--outdir', default='reports')
    args=ap.parse_args(); out=Path(args.outdir); out.mkdir(exist_ok=True)
    cases=load_cases(args.sweep)
    (out/'certificate_size_vs_width.svg').write_text(svg_scatter(cases,'weighted_width','certificate_bytes','Certificate size vs weighted width'))
    (out/'verify_time_vs_certificate_size.svg').write_text(svg_scatter(cases,'certificate_bytes','certificate_verify_seconds','Verification time vs certificate size'))
    print(json.dumps({"status":"COMPLETE","plots":[str(out/'certificate_size_vs_width.svg'),str(out/'verify_time_vs_certificate_size.svg')]}, indent=2))

if __name__=='__main__': main()
