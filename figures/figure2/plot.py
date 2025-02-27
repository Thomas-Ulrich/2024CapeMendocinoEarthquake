import pandas as pd
import numpy as np
import pygmt

class Cpt:
    def __init__(self, cpt):
        cpt = pd.read_csv(cpt, sep='\t', header=None)
        self.cpt_o = cpt.iloc[-3:]
        cpt = cpt[:-3]
        cpt[0] = np.asfarray(cpt[0])
        self.cpt = cpt
    def __call__(self, value):
        if value is None:
            return self.cpt_o.iloc[2, 1]
        idx = np.sum(self.cpt[0] < value) - 1
        if idx < 0:
            return self.cpt_o.iloc[0, 1]
        elif idx + 2 > self.cpt.shape[0]:
            return self.cpt_o.iloc[1, 1]
        else:
            return self.cpt.iloc[idx, 1]
        
        
repeating_cat = pd.read_csv('./repeating_earthquakes.csv')
cat = pd.read_csv('./aftershocks.csv')
cat_on_fault = pd.read_csv('./aftershocks_on_fault.csv')
background = pd.read_csv('./background_seismicity.csv')
mainshock = pd.read_csv('./mainshock.csv')

static_inv = pd.read_csv('./static_inv.csv')
gnss = pd.read_csv('./gnss_data.csv')
static_inv_gnss_syn = pd.read_csv('./static_inv_gnss_syn.csv')
fault_cords = pd.read_csv('./fault_cords.csv')

kinematic_inv = pd.read_csv('./kinematic_inv.csv')
kinematic_inv_gnss_syn = pd.read_csv('./kinematic_inv_gnss_syn.csv')


cpt = Cpt('./slip.cpt')

stf = pd.read_csv('./stf.csv')

region=[-125.3, -123.6, 40, 41]
fig = pygmt.Figure()
pygmt.config(FORMAT_GEO_MAP='ddd.xx', MAP_FRAME_TYPE='plain')

#### panel c #####

fig.coast(
    frame=['lrtb'],
    projection=f"M20",
    region=region,
    shorelines='1p,black',
    land = 'lightgray'
    
)
fig.plot(
    data='./faults.gmt',
    pen="1p,black",
)

fig.plot(
    x=cat.lon,
    y=cat.lat,
    style="c1p",
    fill="black",
)
spec="e60/0.39+f18"
fig.plot(x=fault_cords.lon, y=fault_cords.lat, pen='1,cyan', close=True)
disp = gnss[['id', 'lon', 'lat', 'E', 'N']]
fig.velo(
    data=disp.iloc[:, 1:],
    spec=spec,
    pen="2p,red",
    line=True,
    vector="0.6c+e+gred",
)
fig.velo(
    data=static_inv_gnss_syn[['lon', 'lat', 'E', 'N']],
    spec=spec,
    pen="2p,blue",
    line=True,
    vector="0.4c+e+gblue",
)
fig.velo(
    data=kinematic_inv_gnss_syn[['lon', 'lat', 'E', 'N']],
    spec=spec,
    pen="2p,pink",
    line=True,
    vector="0.4c+e+gpink",
)
size = 0.03
fig.velo(
    data=[[-125.25, 40.87, size, 0]],
    spec=spec,
    pen="2p,blue",
    line=True,
    vector="0.4c+e+gblue",
)
fig.velo(
    data=[[-125.25, 40.84, size, 0]],
    spec=spec,
    pen="2p,pink",
    line=True,
    vector="0.4c+e+gpink",
)
fig.velo(
    data=[[-125.25, 40.9, size, 0]],
    spec=spec,
    pen="2p,red",
    line=True,
    vector="0.6c+e+gred",
)
fig.text(x=-125.25, y=40.9, text='3 cm', font="10p", offset='0.8c/0.5c')
fig.text(x=-125.25, y=40.87, text='Static inversion', font="10p", offset='3.5c/0.0c') 
fig.text(x=-125.25, y=40.84, text='Kinematic inversion', font="10p", offset='3.5c/0.0c') 
fig.text(x=-125.25, y=40.9, text='Data', font="10p", offset='3.5c/0.0c')




fig.basemap(map_scale="n0.1/0.1+w10k+f+u")
fig.text(position='TL', no_clip=True, text='(c)', font='12p,Helvetica,black', offset='-0.8c/0.4c')


### panel b #####
fig.shift_origin(yshift='16c')
fig.basemap(projection='X18.7c/7c', region=[9.7, 98.5, -28., 0], frame=['WbNr', 'xa10f5', 'ya5+lalong dip [km]'])
dist_dip = 0
for along_dip in range(10):
    dist_stk = 9.7
    for  along_stk in range(24):
        subfault = kinematic_inv.iloc[along_dip * 24 + along_stk]
        r = dist_stk
        l = dist_stk + 3.7
        t = dist_dip
        b = dist_dip  - 2.85
        fig.plot(x=[r, l, l, r], y=np.array([t, t, b, b]), pen='0.5p,gray', close=True, fill=cpt(subfault.slip * 1e-2))
        dist_stk += 3.7
    dist_dip -= 2.8
cc = 100
fig.plot(x = background.along_stk_disloc, y=-background.depth, style='c0.05c', fill=f'{cc}/{cc}/{cc}')
fig.plot(x = cat_on_fault.along_stk_disloc, y=-cat_on_fault.depth, style='c0.05c', fill='cyan')
fig.plot(x = repeating_cat.along_stk_disloc, y=-repeating_cat.depth, style='c0.1c', fill='red')
fig.plot(x = mainshock.along_stk_disloc, y=-mainshock.depth, style='a0.5c', fill='yellow', pen='0.5p,black')
fig.text(position='TL', no_clip=True, text='(b)', font='12p,Helvetica,black', offset='-0.8c/0.5c')
with pygmt.config(FONT_LABEL='24p,Helvetica,black', FONT_ANNOT_PRIMARY='24p,Helvetica,black'):
    fig.colorbar(frame=['xa1f0.5+lSlip [m]', 'ya0.5'], position='g102/-3.5+w4c/0.3c', cmap='slip.cpt')
    
### panel b inset ###
fig.shift_origin(yshift='0.0c', xshift='0.0c')
with pygmt.config(FONT_LABEL='8p,Helvetica-Bold,black', FONT_ANNOT_PRIMARY='8p,Helvetica-Bold,black'):
    fig.basemap(projection='X4c/3c', region=[0.0001, 20.9999, 0.001, 5], frame=['tblr+gwhite'])
fig.plot(x=stf.time, y=stf.Moment_Rate / 1e18, pen='0.3p,black', close=True, fill='gray')
with pygmt.config(FONT_LABEL='6p,Helvetica-Bold,black', FONT_ANNOT_PRIMARY='6p,Helvetica-Bold,black', MAP_FRAME_TYPE='inside'):
    fig.basemap(projection='X4c/3c', region=[0.0001, 39.999, 0.001, 5], frame=['lNbE', 'xa10f5+ltime [s]', 'ya1+lMoment Rate [Nm @[10^{18}@[]'])


### panel a #####
fig.shift_origin(yshift='8.0c')
fig.basemap(projection='X18.7c/7c', region=[0, 100, -20, 0], frame=['WNbr', 'xa10f5+lalong strike [km]', 'ya5+lalong dip [km]'])
for i, row in static_inv.iterrows():
    fig.plot(x=[row.r, row.l, row.l, row.r], y=-np.array([row.t, row.t, row.b, row.b]), pen='0.5p,gray', close=True, fill=cpt(row.slip))
cc = 100
fig.plot(x = background.along_stk_disloc, y=-background.depth, style='c0.05c', fill=f'{cc}/{cc}/{cc}', label='background seismicity')
fig.plot(x = cat_on_fault.along_stk_disloc, y=-cat_on_fault.depth, style='c0.05c', fill='cyan', label='aftershocks')
fig.plot(x = repeating_cat.along_stk_disloc, y=-repeating_cat.depth, style='c0.1c', fill='red', label='repeating earthquakes')
fig.plot(x = mainshock.along_stk_disloc, y=-mainshock.depth, style='a0.5c', fill='yellow', pen='0.5p,black')



fig.text(position='TL', no_clip=True, text='(a)', font='12p,Helvetica,black', offset='-0.8c/0.5c')
fig.legend(position='n0.01/0.01', box='+ggray')



fig.savefig('./figure2.pdf')