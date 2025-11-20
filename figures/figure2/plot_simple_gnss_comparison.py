import pandas as pd
import numpy as np
import pygmt

class Cpt:
    def __init__(self, cpt):
        cpt = pd.read_csv(cpt, sep='\t', header=None)
        self.cpt_o = cpt.iloc[-3:]
        cpt = cpt[:-3]
        cpt[0] = np.array(cpt[0]).astype(float)
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

cat = pd.read_csv('./aftershocks.csv')
cat['time'] = pd.to_datetime(cat['time'])
cat = cat[cat.time > pd.to_datetime('2024-12-05T18:44:21')]


cat_on_fault = pd.read_csv('./aftershocks_on_fault.csv')
cat_on_fault['time'] = pd.to_datetime(cat_on_fault['time'])
cat_on_fault = cat_on_fault[cat_on_fault.time > pd.to_datetime('2024-12-05T18:44:21')]


repeating_cat = pd.read_csv('./repeating_earthquakes.csv')
background = pd.read_csv('./background_seismicity.csv')
mainshock = pd.read_csv('./mainshock.csv')

static_inv = pd.read_csv('./static_inv.csv')
gnss = pd.read_csv('./gnss_data.csv')
#static_inv_gnss_syn = pd.read_csv('./static_inv_gnss_syn.csv')
static_inv_gnss_syn = pd.read_csv('gnss_data_preferred_DR.csv')
fault_cords = pd.read_csv('./fault_cords.csv')

kinematic_inv = pd.read_csv('./kinematic_inv.csv')
kinematic_inv_gnss_syn = pd.read_csv('./kinematic_inv_gnss_syn.csv')


cpt = Cpt('./slip.cpt')

stf = pd.read_csv('./stf.csv')

back_projection = pd.read_csv('../figure1/back_projection.csv')

span_2024={'lon':[-125.247, -124.490], 'lat':[40.383, 40.303]}


plot_kinematic = True
plot_seismicity  = False


region=[-125.3, -123.6, 40, 41]
fig = pygmt.Figure()
pygmt.config(FORMAT_GEO_MAP='ddd.xx', MAP_FRAME_TYPE='plain')

#### panel c #####

fig.coast(
    frame=['lrtb'],
    projection=f"M20",
    region=region,
    shorelines='1p,black',
    land = 'lightgray',
    water='lightblue'

)
fig.plot(
    data='./faults.gmt',
    pen="1p,black",
)

if plot_seismicity:
    cc = 100
    fig.plot(
        x=background.lon,
        y=background.lat,
        style="c0.05c",
        fill=f'{cc}/{cc}/{cc}',
    )
    fig.plot(
        x=repeating_cat.lon,
        y=repeating_cat.lat,
        style="c0.1c",
        fill='red',
    )
    fig.plot(
        x=cat.lon,
        y=cat.lat,
        style="c0.07c",
        fill="cyan",
    )

spec="e60/0.39+f18"


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
if plot_kinematic:
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
if plot_kinematic:
    fig.velo(
        data=[[-125.25, 40.84, size, 0]],
        spec=spec,
        pen="2p,pink",
        line=True,
        vector="0.4c+e+gpink",
    )
    fig.text(x=-125.25, y=40.84, text='Kinematic inversion', font="10p", offset='3.5c/0.0c')

fig.velo(
    data=[[-125.25, 40.9, size, 0]],
    spec=spec,
    pen="2p,red",
    line=True,
    vector="0.6c+e+gred",
)

fig.text(x=-125.25, y=40.9, text='3 cm', font="10p", offset='0.8c/0.5c')
fig.text(x=-125.25, y=40.87, text='Dynamic rupture model', font="10p", offset='3.8c/0.0c')
fig.text(x=-125.25, y=40.9, text='Data', font="10p", offset='2.35c/0.0c')

fig.plot(x=span_2024["lon"], y=span_2024["lat"], pen = "10p,black@50%")


fig.basemap(map_scale="n0.07/0.81+w10k+f+u")
fig.text(position='TL', no_clip=True, text='(c)', font='12p,Helvetica,black', offset='-0.8c/0.4c')



fn = './fig_gnss_comparison.pdf'
fig.savefig(fn)
print(f"done writing {fn}")
