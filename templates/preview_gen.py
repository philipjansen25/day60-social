import re, html, json, sys
REPO='/home/user/day60-social'; WK='2026-11/wk46'
src=open(f'{REPO}/{WK}/posts.md').read()
posts={}
for m in re.finditer(r"^### ((?:LI|IG|FB)\d) · (.*?)\n(.*?)```\n(.*?)```", src, re.S|re.M):
    pid, head, meta, copy = m.groups()
    posts[pid]={'head':head,'meta':meta,'copy':copy.strip()}
sched=[]
for l in src.split('\n'):
    c=[x.strip() for x in l.split('|')]
    if len(c)>8 and re.match(r'^(LI|IG|FB)\d$',c[1]): sched.append(dict(id=c[1],day=c[2],time=c[3],plat=c[4],fmt=c[5],asset=c[6],batch=c[7],pin=c[8].replace('**','')))
def assets_for(a):
    a=a.replace('–','-')
    m=re.match(r'(p\d+_[a-z_]+?)_1-(\d+)\.png',a)
    if m: return [f'{m.group(1)}_{i}.png' for i in range(1,int(m.group(2))+1)]
    if a.endswith('.pdf'): return [f'p06_three_touches_{i}.png' for i in range(1,7)]
    return [a]
def esc(t): return html.escape(t, quote=False)
def fmt_copy(t):
    t=esc(t)
    t=re.sub(r'(https://getday60\.com/\S+)', r'<span class="lnk">\1</span>', t)
    t=re.sub(r'(?<![\w&])(#\w+)', r'<span class="tag">\1</span>', t)
    return t.replace('\n','<br>')
def media(files, plat):
    if files[0].endswith('.mp4'):
        return f'<div class="media vid"><video src="assets/{files[0]}" controls muted playsinline preload="metadata"></video></div>'
    if len(files)>1:
        imgs=''.join(f'<img src="assets/{f}" alt="slide {i+1}" loading="lazy">' for i,f in enumerate(files))
        return f'<div class="media car"><div class="track">{imgs}</div><div class="hint">{len(files)} slides · swipe</div></div>'
    return f'<div class="media"><img src="assets/{files[0]}" alt="" loading="lazy"></div>'
def meta_lines(meta):
    out=[]
    for l in meta.strip().split('\n'):
        l=l.strip()
        if l.startswith('- '):
            k,_,v=l[2:].partition(':')
            if k in ('Tags','Link','Alt text','Alt text (per slide)','Document','Recording'):
                out.append(f'<div class="ml"><b>{esc(k)}</b> {esc(v.strip())}</div>')
    return ''.join(out)
PL={'LinkedIn':('li','Philip Jansen','Founder, Day60 · personal profile'),'Instagram':('ig','getday60',''),'Facebook':('fb','Day60','Page')}
cards_by_day={}
used=set()
for s in sched:
    p=posts[s['id']]; cls,name,sub=PL[s['plat']]
    files=assets_for(s['asset'])
    for f in files: used.add(f)
    if s['asset'].endswith('.pdf'): used.add('p06_three_touches_linkedin.pdf')
    pin=f'<span class="pin">{esc(s["pin"])}</span>' if s['pin'] else ''
    head=f'<div class="ph {cls}"><div class="av">{"P" if cls=="li" else "D"}</div><div><div class="pn">{esc(name)}</div><div class="ps">{esc(sub) if sub else esc(s["time"]+" CT")}</div></div><div class="pl">{esc(s["plat"])}</div></div>'
    if cls=='ig':
        body=head+media(files,cls)+f'<div class="cap"><b>getday60</b> {fmt_copy(p["copy"])}</div>'
    else:
        body=head+f'<div class="cap">{fmt_copy(p["copy"])}</div>'+media(files,cls)
    card=(f'<article class="post {cls}" id="{s["id"]}"><div class="chip"><span class="id">{s["id"]}</span>{esc(s["time"])} CT · {esc(s["fmt"])} · Batch {s["batch"]}{pin}</div>'
          f'<div class="frame">{body}</div><details><summary>Specs</summary><div class="ml"><b>Assets</b> {esc(", ".join(files))}</div>{meta_lines(p["meta"])}</details></article>')
    cards_by_day.setdefault(s['day'],[]).append(card)
days=''.join(f'<section class="day"><h2>{esc(d)}</h2><div class="grid">{"".join(c)}</div></section>' for d,c in cards_by_day.items())
# extra sections from posts.md
def section(title):
    m=re.search(r'^## '+re.escape(title)+r'.*?\n(.*?)(?=^## |\Z)', src, re.S|re.M); return m.group(1) if m else ''
def md_table(t):
    rows=[[c.strip() for c in l.strip().strip('|').split('|')] for l in t.strip().split('\n') if l.strip().startswith('|')]
    rows=[r for r in rows if not set(''.join(r))<=set('- ')]
    h=''.join(f'<th>{esc(c)}</th>' for c in rows[0])
    b=''.join('<tr>'+''.join(f'<td>{esc(c).replace("**","")}</td>' for c in r)+'</tr>' for r in rows[1:])
    return f'<div class="tw"><table><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>'
def md_list(t):
    items=[l.strip()[2:] if l.strip().startswith('- ') else re.sub(r'^\d+\.\s*','',l.strip()) for l in t.strip().split('\n') if re.match(r'^\s*(-|\d+\.)\s',l)]
    return '<ul>'+''.join('<li>'+re.sub(r'\*\*(.*?)\*\*',r'<b>\1</b>',esc(i))+'</li>' for i in items)+'</ul>'
bios=md_table(section('Profile bio lines'))
script_sec=section('Saturday filming')
script=f'<p>{esc(script_sec.strip().split(chr(10))[0])}</p>'+md_table(script_sec)
pins=md_list(section('Pinned and featured'))
qs=md_list(section('Open questions for HQ'))
angle=re.search(r'\*\*Angle:\*\* (.*)', src).group(1); angle=angle[0].upper()+angle[1:]
sched_tbl=md_table('\n'.join(l for l in section('Schedule at a glance').split('\n') if l.startswith('|')))
html_out=open('/tmp/claude-0/-home-user-day60-social/b6710d43-4ef8-534c-b45e-cef5489411c2/scratchpad/preview/tpl.html').read()
html_out=html_out.replace('{{ANGLE}}',esc(angle).replace('&quot;','"')).replace('{{DAYS}}',days).replace('{{SCHED}}',sched_tbl).replace('{{PINS}}',pins).replace('{{BIOS}}',bios).replace('{{SCRIPT}}',script).replace('{{QS}}',qs)
open('/tmp/claude-0/-home-user-day60-social/b6710d43-4ef8-534c-b45e-cef5489411c2/scratchpad/preview/day60-social-w46.html','w').write(html_out)
files={f'assets/{f}': f'{REPO}/{WK}/{f}' for f in sorted(used)}
json.dump(files, open('/tmp/claude-0/-home-user-day60-social/b6710d43-4ef8-534c-b45e-cef5489411c2/scratchpad/preview/files.json','w'), indent=0)
print(len(posts),'posts',len(sched),'sched',len(files),'files')
