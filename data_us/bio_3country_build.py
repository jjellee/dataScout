import pandas as pd, numpy as np, json, textwrap, re
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import TwoSlopeNorm, LinearSegmentedColormap

FR="/home/inhyuk/Downloads/public/static/alternative/Pretendard-Regular.ttf"; FB="/home/inhyuk/Downloads/public/static/alternative/Pretendard-Bold.ttf"
fm.fontManager.addfont(FR); fm.fontManager.addfont(FB)
FAM = fm.FontProperties(fname=FR).get_name()
plt.rcParams.update({"font.family":FAM,"axes.unicode_minus":False,"pdf.fonttype":42,"axes.spines.top":False,"axes.spines.right":False,
    "axes.edgecolor":"#c8c7c1","axes.labelcolor":"#52514e","xtick.color":"#52514e","ytick.color":"#52514e","grid.color":"#e6e5e0","grid.linewidth":0.6,
    "axes.titlesize":12,"axes.titleweight":"bold","figure.facecolor":"#ffffff"})
TP="#0b0b0b"; TS="#52514e"; TM="#8a8984"
C = {"US":"#2a78d6","JP":"#eb6834","KR":"#1baf7a","KR2":"#4a3aa7","BM":"#9a9a96"}
OUT="bio_3country_2026.pdf"

df = pd.read_csv("close.csv", index_col=0, parse_dates=True).ffill().drop(columns=["1306.T"])
T = json.load(open("tickers.json")); T.pop("1306.T"); T["4579.T"]="JP|라쿠알리아창약"
st = pd.read_csv("stats.csv"); st = st[st.ticker!="1306.T"].copy(); st.loc[st.ticker=="4579.T","name"]="라쿠알리아창약"
mr = pd.read_csv("monthly.csv", index_col=0).drop(columns=["1306.T"])
base_date = df.loc[:"2025-12-31"].index[-1]; last = df.loc[:"2026-08-21"].index[-1]
ytd = df.loc[base_date:last]; norm = ytd/ytd.iloc[0]*100
LAST = last.strftime("%Y-%m-%d")
A4 = (11.69, 8.27)

def header(fig, title, sub=""):
    fig.text(0.04, 0.955, title, fontsize=15, fontweight="bold", color=TP, va="center")
    if sub: fig.text(0.04, 0.925, sub, fontsize=9.5, color=TS, va="center")
    fig.text(0.96, 0.955, f"기준일 {LAST} · 현지통화 종가 · 2025-12-31=100", fontsize=8.5, color=TM, ha="right", va="center")
def footer(fig, n):
    fig.text(0.04, 0.025, "dataScout · 데이터: Yahoo Finance(수정종가) · 지수/ETF: XBI·IBB·NBI·S&P500 / 1621(TOPIX-17 의약품)·Nikkei225 / KODEX바이오·TIGER헬스케어·KOSPI·KOSDAQ", fontsize=7.5, color=TM)
    fig.text(0.96, 0.025, f"{n}", fontsize=8, color=TM, ha="right")
def endlabel(ax, s, text, color, **kw):
    ax.annotate(text, (s.index[-1], s.iloc[-1]), xytext=(4,0), textcoords="offset points", fontsize=8, color=color, va="center", fontweight="bold", **kw)
def fmt(v): return f"{v:+.1f}%"
def endlabels(ax, items, gap):
    """items=[(x, y, text, color)] → 세로 겹침 제거 후 표기"""
    items = sorted(items, key=lambda r: r[1]); ys=[r[1] for r in items]
    for i in range(1,len(ys)):
        if ys[i] < ys[i-1]+gap: ys[i] = ys[i-1]+gap
    for (x,y0,t,c),y in zip(items,ys):
        ax.annotate(t, (x,y0), xytext=(x+pd.Timedelta(days=3), y), textcoords="data", fontsize=8, color=c, va="center", fontweight="bold",
                    arrowprops=dict(arrowstyle="-", color=c, lw=0.5, alpha=0.6, shrinkA=0, shrinkB=2) if abs(y-y0)>gap*0.3 else None)

pdf = PdfPages(OUT); page=[0]
def save(fig):
    page[0]+=1; footer(fig, page[0]); pdf.savefig(fig); plt.close(fig)

# ---------- 1. 표지 ----------
fig = plt.figure(figsize=A4)
fig.text(0.04, 0.90, "미국·일본·한국 바이오주 2026년 주가 흐름 비교분석", fontsize=22, fontweight="bold", color=TP)
fig.text(0.04, 0.855, f"연초(2025-12-31) 대비 {LAST} 현재 · 대표 ETF/지수 + 3국 60개 종목 · 현지통화 기준", fontsize=11, color=TS)
# hero numbers
heroes = [("미국  XBI", "XBI", C["US"], "S&P500 대비", "^GSPC"), ("일본  TOPIX-17 의약품 ETF", "1621.T", C["JP"], "Nikkei225 대비", "^N225"), ("한국  KODEX 바이오", "244580.KS", C["KR"], "KOSPI 대비", "^KS11")]
S = st.set_index("ticker")
for i,(lab,t,col,bl,bt) in enumerate(heroes):
    x = 0.04 + i*0.31
    fig.patches.append(plt.Rectangle((x,0.60),0.29,0.21, transform=fig.transFigure, facecolor="#f6f6f3", edgecolor="none"))
    fig.patches.append(plt.Rectangle((x,0.60),0.006,0.21, transform=fig.transFigure, facecolor=col, edgecolor="none"))
    fig.text(x+0.02, 0.78, lab, fontsize=10.5, color=TS, fontweight="bold")
    fig.text(x+0.02, 0.695, fmt(S.loc[t,"ytd"]), fontsize=30, fontweight="bold", color=TP)
    fig.text(x+0.02, 0.645, f"{bl} {S.loc[t,'ytd']-S.loc[bt,'ytd']:+.1f}%p  ·  벤치마크 {fmt(S.loc[bt,'ytd'])}", fontsize=9, color=TS)
    fig.text(x+0.02, 0.615, f"최대낙폭 {S.loc[t,'mdd']:.1f}%  ·  고점({S.loc[t,'high_date']}) 대비 {S.loc[t,'off_high']:.1f}%", fontsize=9, color=TS)
# table
keys = ["XBI","IBB","^NBI","^GSPC","1621.T","^N225","244580.KS","143860.KS","^KS11","^KQ11"]
ax = fig.add_axes([0.04,0.08,0.92,0.48]); ax.axis("off")
cols = ["구분","지수 / ETF","연초대비","1개월","3개월","최대낙폭","고점대비","연중고점","연중저점"]
rows=[]
for k in keys:
    r=S.loc[k]; rows.append([r.region, r["name"], fmt(r.ytd), fmt(r.m1), fmt(r.m3), f"{r.mdd:.1f}%", f"{r.off_high:.1f}%", r.high_date, r.low_date])
tb = ax.table(cellText=rows, colLabels=cols, loc="upper center", cellLoc="center", colWidths=[0.06,0.30,0.09,0.09,0.09,0.09,0.09,0.09,0.09])
tb.auto_set_font_size(False); tb.set_fontsize(9); tb.scale(1,1.38)
for (r,c),cell in tb.get_celld().items():
    cell.set_edgecolor("#e6e5e0"); cell.set_linewidth(0.6)
    if r==0: cell.set_facecolor("#f0efe9"); cell.get_text().set_fontweight("bold"); cell.get_text().set_color(TS)
    else:
        if c==1: cell.get_text().set_ha("left"); cell.set_text_props(x=0.02)
        if c in (2,3,4):
            v=float(cell.get_text().get_text().rstrip('%')); cell.get_text().set_color("#1a7f3c" if v>0 else "#c0392b" if v<0 else TP)
        if keys[r-1] in ("^GSPC","^N225","^KS11","^KQ11"): cell.set_facecolor("#fafaf8"); cell.get_text().set_color(TM if c in (0,1,7,8) else cell.get_text().get_color())
        elif c==0: cell.get_text().set_color(C[rows[r-1][0]]); cell.get_text().set_fontweight("bold")
fig.text(0.04, 0.585, "대표 지수·ETF 성과 요약  (회색 행 = 시장 벤치마크)", fontsize=10.5, fontweight="bold", color=TP)
fig.text(0.04, 0.225, "핵심 요약", fontsize=10.5, fontweight="bold", color=TP)
for i,b in enumerate(["미국: 금리 인하·M&A 재개에 8/19 Moderna-Merck mRNA 암백신 3상 성공이 더해져 XBI·IBB 사상 최고치. 6월(+15.9%)·8월(+12.7%) 두 달이 연간 성과의 대부분. 20종목 중 15개 상승, 중앙값 +15.4%.",
                      "일본: 닛케이 +31.1% 강세장 속 제약주는 소외(1621 +6.8%). 오츠카HD·다케다만 신고가, 주가이(-14.2%)·다이이치산쿄(-14.2%)는 기대 선반영 후 실망 매물. 18종목 중앙값 +3.6%.",
                      "한국: 코스피 +64.0% 반도체 쏠림과 7/21 코오롱티슈진·삼천당제약 임상 쇼크(동반 하한가)로 바이오 자금 이탈. 22종목 중 20개 하락, 중앙값 -25.2%. 8월 반등(+12.1%)은 낙폭과대주 중심의 기술적 성격."]):
    for j,x in enumerate(textwrap.wrap(b, 118)): fig.text(0.05 if j==0 else 0.065, 0.192-i*0.045-j*0.019, ("• " if j==0 else "")+x, fontsize=9, color=TP)
save(fig)

# ---------- 2. 정규화 추이: 현지통화 / 달러환산 ----------
fig, axes = plt.subplots(1,2, figsize=A4); fig.subplots_adjust(left=0.05,right=0.95,top=0.86,bottom=0.14,wspace=0.18)
header(fig, "① 바이오 ETF 연초 대비 추이 — 현지통화 vs 달러 환산", "미국 XBI · 일본 1621 · 한국 KODEX바이오/TIGER헬스케어, 점선은 각국 시장 벤치마크")
usd = norm.copy()
usd["1621.T"] = (ytd["1621.T"]/ytd["JPY=X"]); usd["1621.T"]=usd["1621.T"]/usd["1621.T"].iloc[0]*100
for k in ["244580.KS","143860.KS","^KS11","^KQ11"]:
    usd[k]=(ytd[k]/ytd["KRW=X"]); usd[k]=usd[k]/usd[k].iloc[0]*100
usd["^N225"]=(ytd["^N225"]/ytd["JPY=X"]); usd["^N225"]=usd["^N225"]/usd["^N225"].iloc[0]*100
series = [("XBI","미국 XBI",C["US"],"-"),("1621.T","일본 1621 의약품",C["JP"],"-"),("244580.KS","한국 KODEX 바이오",C["KR"],"-"),("143860.KS","한국 TIGER 헬스케어",C["KR2"],"-"),
          ("^GSPC","S&P500",C["US"],":"),("^N225","Nikkei225",C["JP"],":"),("^KS11","KOSPI",C["KR"],":")]
for ax,data,ttl in [(axes[0],norm,"현지통화 기준"),(axes[1],usd,"달러 환산 기준 (USDJPY +1.6%, USDKRW -3.3%)")]:
    for t,lab,col,ls in series:
        s=data[t].dropna(); ax.plot(s.index,s.values,color=col,lw=2 if ls=="-" else 1.3,ls=ls,label=lab,alpha=1 if ls=="-" else 0.8)
        endlabel(ax,s,f"{s.iloc[-1]-100:+.0f}%",col)
    ax.axhline(100,color="#c8c7c1",lw=0.8); ax.grid(axis="y"); ax.set_title(ttl,loc="left"); ax.set_ylabel("2025-12-31 = 100")
    ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m월")); ax.set_xlim(ytd.index[0], ytd.index[-1]+pd.Timedelta(days=14))
h,l=axes[0].get_legend_handles_labels(); fig.legend(h,l,loc="lower center",ncol=7,fontsize=8.5,frameon=False,bbox_to_anchor=(0.5,0.045))
save(fig)

# ---------- 3. 상대강도 + 드로다운 ----------
fig, axes = plt.subplots(1,2, figsize=A4); fig.subplots_adjust(left=0.05,right=0.95,top=0.86,bottom=0.10,wspace=0.18)
header(fig, "② 시장 대비 상대강도와 연중 낙폭", "좌: 바이오 ETF ÷ 시장지수 (100 초과 = 시장 대비 초과수익) · 우: 연중 고점 대비 낙폭(Drawdown)")
ax=axes[0]; rs_items=[]
for t,b,lab,col in [("XBI","^GSPC","XBI / S&P500",C["US"]),("1621.T","^N225","1621 / Nikkei225",C["JP"]),("244580.KS","^KS11","KODEX바이오 / KOSPI",C["KR"]),("244580.KS","^KQ11","KODEX바이오 / KOSDAQ",C["KR2"])]:
    s=(norm[t]/norm[b]*100).dropna(); ax.plot(s.index,s.values,color=col,lw=2,label=lab); rs_items.append((s.index[-1],s.iloc[-1],f"{s.iloc[-1]:.0f}",col))
endlabels(ax, rs_items, 3.5)
ax.axhline(100,color="#c8c7c1",lw=0.8); ax.grid(axis="y"); ax.set_title("벤치마크 대비 상대강도",loc="left"); ax.legend(fontsize=8,frameon=False,loc="lower left")
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m월")); ax.set_xlim(ytd.index[0], ytd.index[-1]+pd.Timedelta(days=14))
ax=axes[1]
for t,lab,col in [("XBI","미국 XBI",C["US"]),("1621.T","일본 1621",C["JP"]),("244580.KS","한국 KODEX 바이오",C["KR"]),("143860.KS","한국 TIGER 헬스케어",C["KR2"])]:
    s=ytd[t].dropna(); dd=(s/s.cummax()-1)*100; ax.plot(dd.index,dd.values,color=col,lw=2,label=lab); ax.fill_between(dd.index,dd.values,0,color=col,alpha=0.06)
    endlabel(ax,dd,f"{dd.iloc[-1]:.0f}%",col)
ax.grid(axis="y"); ax.set_title("연중 고점 대비 낙폭 (%)",loc="left"); ax.legend(fontsize=8,frameon=False,loc="lower left")
ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m월")); ax.set_xlim(ytd.index[0], ytd.index[-1]+pd.Timedelta(days=14))
save(fig)

# ---------- 4. 월별 수익률 히트맵 ----------
fig = plt.figure(figsize=A4); header(fig, "③ 월별 수익률 (%) — 어느 달이 성과를 갈랐나", "6월·8월 미국 급등 / 2월 일본 급등 후 4개월 연속 하락 / 한국 5~7월 3개월 연속 급락")
order = ["XBI","IBB","^NBI","^GSPC","1621.T","^N225","244580.KS","143860.KS","^KS11","^KQ11"]
H = mr[order].T; H.index=[S.loc[k,"name"] for k in order]
ax = fig.add_axes([0.22,0.12,0.72,0.72])
cmap = LinearSegmentedColormap.from_list("div",["#c0392b","#f4f4f1","#1a7f3c"])
vmax = 25
im = ax.imshow(H.values, cmap=cmap, norm=TwoSlopeNorm(vcenter=0,vmin=-vmax,vmax=vmax), aspect="auto")
ax.set_xticks(range(H.shape[1])); ax.set_xticklabels([c[5:]+"월" for c in H.columns]); ax.set_yticks(range(H.shape[0])); ax.set_yticklabels(H.index, fontsize=9.5)
for i in range(H.shape[0]):
    for j in range(H.shape[1]):
        v=H.values[i,j]; ax.text(j,i,f"{v:+.1f}",ha="center",va="center",fontsize=9,color="white" if abs(v)>14 else TP, fontweight="bold" if abs(v)>=10 else "normal")
for s in ax.spines.values(): s.set_visible(False)
ax.tick_params(length=0)
for y in [3.5,5.5]: ax.axhline(y,color="white",lw=3)
for i,(k,col) in enumerate([("미국",C["US"]),("일본",C["JP"]),("한국",C["KR"])]):
    ys=[(0,3),(4,5),(6,9)][i]; ax.text(-0.6, (ys[0]+ys[1])/2, k, ha="right", va="center", fontsize=10, color=col, fontweight="bold", transform=ax.transData)
ax.text(0, -0.9, "연초대비 →", fontsize=8, color=TM)
for i,k in enumerate(order): ax.text(H.shape[1]-0.4, i, fmt(S.loc[k,"ytd"]), va="center", fontsize=9, color="#1a7f3c" if S.loc[k,"ytd"]>0 else "#c0392b", fontweight="bold")
ax.set_xlim(-0.5, H.shape[1]+0.3)
save(fig)

# ---------- 5. 종목별 YTD 바 ----------
fig, axes = plt.subplots(1,3, figsize=A4); fig.subplots_adjust(left=0.10,right=0.97,top=0.86,bottom=0.08,wspace=0.55)
header(fig, "④ 종목별 연초 대비 수익률 — 3국 주요 바이오·제약 60종목", "숫자 = 연초대비 %, 괄호 = 연중 고점 대비 % · 회색 막대 = 마이너스 · 미국 Moderna는 +130%에서 절단")
for ax,reg,col,ttl in zip(axes,["US","JP","KR"],[C["US"],C["JP"],C["KR"]],["미국 (20)","일본 (18)","한국 (22)"]):
    d = st[(st.region==reg)&~st.ticker.str.startswith("^")&~st.ticker.isin(["XBI","IBB","1621.T","244580.KS","143860.KS"])].sort_values("ytd")
    y=np.arange(len(d)); vals=d.ytd.values; CAP=130
    ax.barh(y, np.minimum(vals,CAP), color=[col if v>=0 else "#b9b8b2" for v in vals], height=0.68)
    for yi,v in enumerate(vals):
        if v>CAP: ax.plot([CAP-6,CAP-2],[yi-0.45,yi+0.45],color="white",lw=2.5); ax.plot([CAP-9,CAP-5],[yi-0.45,yi+0.45],color="white",lw=2.5)
    ax.set_yticks(y); ax.set_yticklabels(d.name, fontsize=8.2); ax.axvline(0,color="#8a8984",lw=0.8); ax.grid(axis="x")
    for yi,(v,oh) in enumerate(zip(vals,d.off_high.values)):
        ax.text((min(v,CAP)+2) if v>=0 else 2, yi, f"{v:+.0f}% ({oh:.0f})", va="center", ha="left", fontsize=7.2, color=TS)
    lo,hi=min(vals.min(),0),min(max(vals.max(),0),CAP); ax.set_xlim(lo-8, hi+55)
    ax.set_title(f"{ttl}  중앙값 {np.median(vals):+.1f}%  ·  상승 {int((vals>0).sum())} / 하락 {int((vals<0).sum())}", loc="left", fontsize=10)
save(fig)

# ---------- 6. 종목별 정규화 추이 (주도/낙오 강조) ----------
fig, axes = plt.subplots(1,3, figsize=A4); fig.subplots_adjust(left=0.05,right=0.97,top=0.86,bottom=0.10,wspace=0.25)
header(fig, "⑤ 종목별 주가 추이 — 주도주·낙오주 강조", "회색 = 전체 종목, 색선 = 연초대비 상위 3 / 진회색 = 하위 3 / 검정 점선 = 대표 ETF (극단치 Moderna·온콜리스는 범위 밖)")
for ax,reg,col,ttl in zip(axes,["US","JP","KR"],[C["US"],C["JP"],C["KR"]],["미국","일본","한국"]):
    d = st[(st.region==reg)&~st.ticker.str.startswith("^")&~st.ticker.isin(["XBI","IBB","1621.T","244580.KS","143860.KS"])].sort_values("ytd",ascending=False)
    for t in d.ticker: ax.plot(norm.index, norm[t], color="#d9d8d2", lw=0.8)
    top = [t for t in d.ticker if t not in ("MRNA","4588.T")][:3]; bot=list(d.ticker[-3:]); items=[]
    shades=[col,"#7aa9e0" if reg=="US" else "#f3a07e" if reg=="JP" else "#6fcfa8", "#b5cdea" if reg=="US" else "#f8c8b2" if reg=="JP" else "#b2e5cf"]
    for t,c in zip(top,shades):
        s=norm[t]; ax.plot(s.index,s.values,color=c,lw=2); items.append((s.index[-1],s.iloc[-1],f"{S.loc[t,'name']} {s.iloc[-1]-100:+.0f}%",c))
    for t,c in zip(bot,["#3b3b39","#6a6a66","#9a9a96"]):
        s=norm[t]; ax.plot(s.index,s.values,color=c,lw=1.8); items.append((s.index[-1],s.iloc[-1],f"{S.loc[t,'name']} {s.iloc[-1]-100:+.0f}%",c))
    e=norm[{"US":"XBI","JP":"1621.T","KR":"244580.KS"}[reg]]; ax.plot(e.index,e.values,color=TP,lw=1.4,ls="--"); items.append((e.index[-1],e.iloc[-1],f"ETF {e.iloc[-1]-100:+.0f}%",TP))
    endlabels(ax, items, {"US":5.5,"JP":6.5,"KR":5.0}[reg])
    if reg=="US": ax.text(0.02,0.96,"Moderna +392% (8/19 하루 +177%) — 범위 밖, 강조 제외",transform=ax.transAxes,fontsize=8,color=TS,va="top")
    if reg=="JP": ax.text(0.02,0.96,"온콜리스바이오 +144% — 범위 밖, 강조 제외",transform=ax.transAxes,fontsize=8,color=TS,va="top")
    ax.axhline(100,color="#c8c7c1",lw=0.8); ax.grid(axis="y"); ax.set_title(ttl,loc="left")
    ax.set_ylim({"US":(40,165),"JP":(35,160),"KR":(15,140)}[reg]); ax.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m월"))
    ax.set_xlim(ytd.index[0], ytd.index[-1]+pd.Timedelta(days=60))
save(fig)

# ---------- 7+. 해설 ----------
txt = open("narrative.txt").read().strip()
blocks = re.split(r"\n(?=\[\d\.)", txt)
lines=[]  # (kind, text)
for b in blocks:
    for ln in b.split("\n"):
        ln=ln.rstrip()
        if not ln: continue
        if re.match(r"\[\d\.", ln): lines.append(("h", ln.strip("[]")))
        elif ln.startswith("- "):
            w=textwrap.wrap(ln[2:], 86)
            for i,x in enumerate(w): lines.append(("b" if i==0 else "bc", x))
        else:
            for x in textwrap.wrap(ln, 92): lines.append(("p", x))
    lines.append(("sp",""))
LH=0.027; y0=0.885; ymin=0.07
i=0; pn=0
while i < len(lines):
    fig=plt.figure(figsize=A4); pn+=1
    header(fig, "⑥ 비교분석 해설" + (f" ({pn})" if pn>1 else ""), "수치는 앞 페이지 데이터(현지통화·연초대비) 기준 · 배경 사실은 2026-08 보도 참조")
    y=y0
    while i < len(lines) and y > ymin:
        k,t=lines[i]
        if k=="h":
            if y < ymin+LH*3: break
            y-=LH*0.4; fig.text(0.05,y,t,fontsize=12,fontweight="bold",color=TP); y-=LH*1.25
        elif k=="p": fig.text(0.05,y,t,fontsize=9.8,color=TP); y-=LH
        elif k=="b": fig.text(0.06,y,"•",fontsize=9.8,color=TS); fig.text(0.075,y,t,fontsize=9.8,color=TP); y-=LH
        elif k=="bc": fig.text(0.075,y,t,fontsize=9.8,color=TP); y-=LH
        else: y-=LH*0.5
        i+=1
    save(fig)

# ---------- 마지막: 주석/출처 ----------
fig=plt.figure(figsize=A4); header(fig,"부록 — 데이터·방법론·참고 보도")
notes = """[데이터]
- 가격: Yahoo Finance 수정종가(배당·분할 반영), 2025-12-31 종가를 100으로 정규화. 한국·일본은 2026-08-21, 미국은 2026-08-21 종가 기준.
- 대표 지수/ETF: 미국 XBI(S&P Biotech, 동일가중·중소형 편중)·IBB(Nasdaq Biotech, 시총가중)·NBI / 일본 NEXT FUNDS TOPIX-17 의약품 ETF(1621) / 한국 KODEX 바이오(244580, 코스닥 신약개발 비중 높음)·TIGER 헬스케어(143860).
- 벤치마크: S&P500, Nikkei225, KOSPI, KOSDAQ. TOPIX ETF(1306)는 2026-03-31 분할이 데이터에 미반영돼 제외.
- 종목 60개: 미국 20(LLY·AMGN·GILD·VRTX·REGN·BIIB·ALNY·MRNA·INSM·NTRA·EXEL·UTHR·SRPT·ARGX·BMRN·INCY·CRSP·IONS·NBIX·VKTX), 일본 18(다케다·다이이치산쿄·주가이·에자이·시오노기·오츠카·아스텔라스·오노·펩티드림·JCR·넥세라·GNI·산바이오·스미토모·교와기린·라쿠알리아·온콜리스·헬리오스), 한국 22(삼성바이오로직스·셀트리온·알테오젠·SK바이오팜·유한양행·HLB·휴젤·리가켐·코오롱티슈진·에이비엘바이오·SK바이오사이언스·한미약품·삼천당제약·클래시스·파마리서치·녹십자·종근당·대웅·디앤디파마텍·보로노이·오스코텍·셀리드).
- 달러 환산: USDJPY·USDKRW(Yahoo) 일별 환율로 나눈 뒤 재정규화.

[지표 정의]
- 1개월/3개월: 기준일 30일/91일 전 마지막 종가 대비. 최대낙폭(MDD): 연초 이후 고점 대비 최대 하락률. 고점대비: 연중 최고 종가 대비 현재.

[참고 보도 (2026년)]
- Forbes 8/19 "Moderna shares skyrocket toward best day ever on cancer drug trial" / Seeking Alpha "Biotech stocks hit post-pandemic high on Moderna trial win" / Benzinga "Biotech is booming, but these 2 stocks missed the memo"
- Mizuho "Can the Comeback Continue? 2026 Biotech Outlook" / ING "Pharma M&A set to accelerate in 2026" / BioPharma Dive "Alnylam plunges as earnings deliver one-two punch" (7/30)
- 니혼게이자이신문 4/27 "주가이제약 주가 한때 15.7% 하락 — 1~3월 증익에도 전망에 아쉬움" / 카부초(株帳) "주가이제약 호실적 대폭락의 정체 — 기대치 갭과 오르포글리프론 대기 구조"
- 머니투데이 7/21 "코오롱티슈진·삼천당제약 하한가…코스닥 개미 곡소리" / 인베스트조선 7/22 "코오롱티슈진 임상 쇼크에 1200억 CB 투자자 손실구간" / 매일신문 7/22 "코스닥 힘 못 쓰니 제약·바이오주도 무너졌다" / 데일리팜 "K-바이오, 잇단 악재에 주가 급락…투자심리 냉각"

[유의]
- 본 자료는 공개 가격 데이터와 보도를 정리한 것으로 투자 권유가 아닙니다. 종목 선정은 시가총액·관심도 기준의 임의 표본이며 업종 전체를 대표하지 않습니다."""
y=0.88
for ln in notes.split("\n"):
    if not ln: y-=0.012; continue
    if ln.startswith("["): fig.text(0.05,y,ln.strip("[]"),fontsize=11,fontweight="bold",color=TP); y-=0.03; continue
    for x in textwrap.wrap(ln, 118): fig.text(0.05,y,x,fontsize=8.6,color=TP if not ln.startswith("- ") else TS); y-=0.021
save(fig)
pdf.close(); print("pages", page[0])
