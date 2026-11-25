"""Графики для README. Данные в репозиторий не входят: положите их в data/orders.xlsx.
Запуск из корня репозитория: python scripts/make_figures.py"""
import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
BLUE='#2b6cb0'; LIGHT='#90cdf4'; GREY='#a0aec0'; ORANGE='#dd6b20'
plt.rcParams.update({'font.size':10,'axes.titlesize':12,'axes.titleweight':'bold','axes.spines.top':False,'axes.spines.right':False,
                     'axes.grid':True,'grid.alpha':.25,'axes.axisbelow':True,'legend.frameon':False})
f=lambda x,d=0: f'{x:,.{d}f}'.replace(',',' ').replace('.',',')
import sys; path=sys.argv[1] if len(sys.argv)>1 else 'data/orders.xlsx'
d=pd.read_excel(path)
d=d[(d['Контрибуция']>-60000000)&(d['Среднее время между редакциями']>=0)]
y=d['Результат']; base=y.mean()*100
def bars(ax,s,title,xlabel):
    t=d.groupby(s,observed=True)['Результат'].agg(['mean','size'])
    b=ax.bar(t.index.astype(str),t['mean']*100,color=[BLUE if v*100>=base else ORANGE for v in t['mean']])
    ax.bar_label(b,[f'{f(v*100,0)}%\nn={n}' for v,n in zip(t['mean'],t['size'])],padding=3,fontsize=8.5)
    ax.axhline(base,color='#4a5568',ls='--',lw=1,label=f'в среднем {f(base,0)}%'); ax.legend(loc='upper right',fontsize=8.5)
    ax.set_ylim(0,118); ax.set_title(title); ax.set_xlabel(xlabel); ax.set_ylabel('Доля выполненных заявок, %')
fig,axes=plt.subplots(1,2,figsize=(12,4.2))
bars(axes[0],d['Количество отмен'].clip(upper=6).replace(6,'6+') if False else pd.cut(d['Количество отмен'],[-1,0,1,2,3,5,100],labels=['0','1','2','3','4–5','6+']),'Отмены в истории заявки','Число отмен')
bars(axes[1],pd.cut(d['Время до отправки'],[0,2,5,10,20,100],labels=['до 2','2–5','5–10','10–20','больше 20']),'Время до отправки','Время до отправки')
fig.suptitle('Заявки без отмен выполняются почти всегда, а с отменами и дальним горизонтом — гораздо реже',fontweight='bold')
fig.tight_layout(); fig.savefig('images/fulfillment_drivers.png',dpi=130,bbox_inches='tight'); plt.close()
t=d.groupby(pd.cut(d['Время до отправки'],[0,2,5,10,20,100]),observed=True)['Результат'].agg(['mean','size']); print(t)
# по направлениям
t=d.groupby('Учетное направление')['Результат'].agg(['mean','size']); t=t[t['size']>=40].sort_values('mean')
t.index=[s.split(') ',1)[1] for s in t.index]
fig,ax=plt.subplots(figsize=(8,4.4))
b=ax.barh(t.index,t['mean']*100,color=[BLUE if v*100>=base else ORANGE for v in t['mean']])
ax.bar_label(b,[f'{f(v*100,0)}% (n={n})' for v,n in zip(t['mean'],t['size'])],padding=3,fontsize=9)
ax.axvline(base,color='#4a5568',ls='--',lw=1); ax.set_xlim(0,95); ax.set_xlabel('Доля выполненных заявок, %')
ax.set_title('Хуже всего выполняются досылы из-под ПВ, лучше всего ВРП')
fig.tight_layout(); fig.savefig('images/fulfillment_by_direction.png',dpi=130); plt.close()
