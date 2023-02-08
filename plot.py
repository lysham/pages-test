import os
import plotly.express as px

fig = px.scatter(x=range(10), y=range(10))
filename = os.path.join("pxplot.html")
fig.write_html(filename)