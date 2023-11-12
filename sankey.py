import plotly.graph_objects as go

fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = ["Tourism Technology Festival", "The Keep Eco Rooms", "❌ no accommodation", "Hostel One", "7 Burgers"],
      color = "blue"
    ),
    link = dict(
      source = [0, 0, 0, 1, 3], # indices correspond to labels, eg A1, A2, A1, B1, ...
      target = [1, 2, 3, 4, 4],
      value = [4, 80, 40, 4, 7]
  ))])

fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)
fig.show()