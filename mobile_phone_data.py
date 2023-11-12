import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

path = r"C:\Users\lisa2\Desktop\Tilo\Hackathon\InveniumData\TT Festival_Invenium\CSV Files\Gastein\Red Bull Play Streets 10_02_2023\Red Bull PlayStreets - 2023-02-10 (16 - 24h) - Visitors During the Day.csv"
df1 = pd.read_csv(path)

p2 = r"C:\Users\lisa2\Desktop\Tilo\Hackathon\InveniumData\TT Festival_Invenium\CSV Files\Gastein\Red Bull Play Streets 10_02_2023\Red Bull PlayStreets - 2023-02-10 (16 - 24h) - Stay Duration Distribution.csv"
df2 = pd.read_csv(p2)



# plotly fig setup
fig = make_subplots(rows=1,
                    cols=2,
                    subplot_titles=('Visitors during the day',  'Stay duration of visitors'))

# traces
fig.add_trace(
    go.Scatter(x=df1["Time"], y=df1["Visitors"]),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(x=df2["Stay duration (minutes)"], y=df2["Visitors"]),
    row=1, col=2
)

# edit axis labels
fig['layout']['xaxis']['title']='Time'
fig['layout']['xaxis2']['title']='Stay duration (minutes)'
fig['layout']['yaxis']['title']='Visitors'
fig['layout']['yaxis2']['title']='Visitors'

fig.update_layout(
    showlegend=False,
    title=dict(text="Red Bull PlayStreets - 2023-02-10", font=dict(size=50), x=0.5),

    #title_text="Event"
)

# plot it
fig.show()