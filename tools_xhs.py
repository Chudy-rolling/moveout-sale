# Generates Xiaohongshu cover + list images from items.json
import json,sys,html,os,subprocess
repo=os.path.dirname(os.path.abspath(__file__)); out=sys.argv[1]
d=json.load(open(os.path.join(repo,'items.json'))); shop=d['shop']
RANK={"在售":0,"已预订":1,"已售出":2}
items=sorted([i for i in d['items'] if i['status'] in RANK],key=lambda i:(RANK[i['status']],i['code']))
on=[i for i in items if i['status']!='已售出']
e=html.escape
src=lambda p:'file://'+os.path.join(repo,p)
FONT="'Noto Sans CJK SC',sans-serif"; SERIF="'Noto Serif CJK SC',serif"
base=f"""<style>*{{box-sizing:border-box;margin:0}}body{{width:1080px;font-family:{FONT};color:#18241d;background:#fff}}
.tag{{position:absolute;top:22px;left:22px;background:#d85f35;color:#fff;font-weight:700;font-size:44px;padding:6px 22px 6px 44px;border-radius:6px 18px 18px 6px}}
.tag:before{{content:"";position:absolute;left:16px;top:50%;width:14px;height:14px;margin-top:-7px;border-radius:50%;background:#fff}}</style>"""
# cover
picks=[c for c in ['A10','A02','A07','A08'] if any(i['code']==c and i['status']!='已售出' for i in items)]
picks=(picks+[i['code'] for i in on if i['code'] not in picks and i['photos']])[:4]
cells=''.join(f'<div style="position:relative;border-radius:24px;overflow:hidden;background:#eef4ee"><img src="{src(it["photos"][0])}" style="width:100%;height:100%;object-fit:cover;display:block"><span class="tag">${it["price"]}</span></div>' for c in picks for it in [next(x for x in items if x['code']==c)])
lo=min(i['price'] for i in on)
cover=f"""<html><head><meta charset=utf-8>{base}</head><body style="height:1440px;background:#1d4a33;color:#f1f7f2;padding:70px 60px">
<div style="font-size:34px;opacity:.85;letter-spacing:2px">Jersey City · Journal Square 自提</div>
<div style="font-family:{SERIF};font-weight:700;font-size:112px;line-height:1.08;margin-top:22px">毕业回国<br>JSQ 出闲置二手</div>
<div style="display:flex;gap:16px;margin-top:30px;align-items:center"><span style="background:#d85f35;color:#fff;font-size:44px;font-weight:700;padding:8px 26px;border-radius:999px">${lo} 起</span><span style="font-size:40px">植物 · 花架 · 园艺好物</span></div>
<div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:400px 400px;gap:20px;margin-top:48px">{cells}</div>
</body></html>"""
# list
rows=''
for i in items:
    sold=i['status']=='已售出'
    ph=f'<img src="{src(i["photos"][0])}" style="width:220px;height:220px;object-fit:cover;border-radius:18px;display:block;{"filter:grayscale(1);opacity:.5" if sold else ""}">' if i['photos'] else '<div style="width:220px;height:220px;border-radius:18px;background:#eef4ee"></div>'
    badge='<span style="background:#d9ead9;color:#1f5130;font-size:28px;padding:4px 16px;border-radius:999px">已售出</span>' if sold else ('<span style="background:#fbe3c8;color:#7a3e05;font-size:28px;padding:4px 16px;border-radius:999px">已预订</span>' if i['status']=='已预订' else '')
    rows+=f"""<div style="display:flex;gap:34px;align-items:center;padding:28px 0;border-bottom:2px solid #e3ebe4;{"opacity:.6" if sold else ""}">{ph}
<div style="flex:1;display:grid;gap:10px"><div style="display:flex;gap:14px;align-items:center"><span style="background:#1d4a33;color:#fff;font-size:28px;padding:2px 14px;border-radius:8px">{e(i['code'])}</span>{badge}</div>
<div style="font-size:42px;font-weight:700;line-height:1.25;{"text-decoration:line-through" if sold else ""}">{e(i['name'])}</div>
<div style="font-size:30px;color:#5d6b62;line-height:1.4">{e(i['condition'] or '')}{' · ' if i['condition'] and i['note'] else ''}{e(i['note'][:34]+('…' if len(i['note'])>34 else ''))}</div></div>
<div style="font-size:60px;font-weight:700;color:#d85f35;white-space:nowrap;{"text-decoration:line-through" if sold else ""}">${i['price']}</div></div>"""
lst=f"""<html><head><meta charset=utf-8>{base}</head><body>
<div style="background:#1d4a33;color:#f1f7f2;padding:60px 60px 50px"><div style="font-family:{SERIF};font-weight:700;font-size:80px">清仓清单</div>
<div style="font-size:34px;margin-top:14px;opacity:.9">在售 {len(on)} 件 · 已出 {len(items)-len(on)} 件 · Journal Square PATH 附近自提</div></div>
<div style="padding:10px 60px 30px">{rows}</div>
<div style="padding:34px 60px 60px;font-size:32px;color:#5d6b62;line-height:1.6">想要哪件，私信报编号就好<br>{e(shop['pickup'])}</div></body></html>"""
for name,h in [('cover',cover),('list',lst)]:
    open(os.path.join(out,name+'.html'),'w').write(h)
print('ok',picks,len(items))
