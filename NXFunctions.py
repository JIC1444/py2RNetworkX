import pandas as pd
import csv
import numpy as np
from IPython.display import display
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt

#HAVE EDITED THE PHYLUM16STEXT FILE AS COULDN'T GET THE COLUMN NAME LOCATIONS
def CreateNXGraph(df_location, phyla, about_location, y_axis, y_axis_label ,save_location, gtype):
  df = pd.read_csv(df_location, sep=" ", names = None) 
  for idx, row in enumerate(df["Location"]): 
    df["Location"][idx] = (df["Location"][idx])[:3]
    
  for location in sorted(set(df["Location"])): 
    df_temp = df.loc[df["Location"] == location]
    filter = df["Location"].str.contains(location)
    df = df[~filter]
    df_temp.iloc[:,1:] = (df_temp.iloc[:,1:].astype(int)).sum()
    df_temp = df_temp.drop_duplicates()
    df = pd.concat([df, df_temp])
    
  df_about = pd.read_csv(about_location, sep = " ")
  tail = (df_about.drop(["site", "sample.code" ,"location" ,"siteID" ,"replicate" ,"precipitation", "temperature"], axis = 1))
  tail = tail.drop_duplicates()
  df = pd.concat([df, tail], axis=1)
  if y_axis == "elevation":
    df.insert(6, "elevation", [815, 436, 589, 1213, 700, 1087, 476, 779, 1133, 1208, 780, 474], True)


  location_coordinates = list(zip(df["T.grid"], df[y_axis]))

  def CalculateWeightedPosition(dataframe, node_phylum, coordinate_list:tuple, frequency_list): 
    total_freq = float(dataframe[node_phylum].sum(axis = 0))
    sum_ = (0.0,0.0)
    for idx, value in enumerate(coordinate_list):
      constant = frequency_list[idx]
      if constant != 0:
        sum_ = tuple(map(sum,zip(sum_,([constant*x for x in value]))))
    weighted_coordinates_x = sum_[0]/total_freq
    weighted_coordinates_y = float(sum_[1]/total_freq)
    weighted_coordinates = (weighted_coordinates_x,weighted_coordinates_y)
    return weighted_coordinates
  
  G = nx.Graph() 
  pos = {}
  edge_labels = {}
  colour_map = []
  for _, row in df.iterrows():
    G.add_node(row["Location"])
    pos[row["Location"]] = np.array([row["T.grid"], row[y_axis]])
    colour_map.append("green")
  
  df = df.reset_index()

  for idx, phylum in enumerate(phyla):
    node_coords = CalculateWeightedPosition(df, phylum, location_coordinates, list(df[phylum]))
    G.add_node(phylum)
    colour_map.append("black")
    pos[phylum] = np.array(node_coords)
    largest_connection = max(df[phylum])
    for _,row in df.iterrows():
      if row[phylum] != 0:
        if row[phylum] == largest_connection:
          G.add_edge(phylum, row["Location"], color = "blue") 
        else:
          G.add_edge(phylum, row["Location"], color = (0.871, 0.871, 0.871)) 
        #edge_labels[df.loc[idx].at["Location"]] = largest_connection
        #edge_labels = {(phylum, df.loc[idx].at["Location"]): str(G.edges[phylum, df.loc[idx].at["Location"]])}
        #WEIGHT INSTEAD COULD BE PROPORTION OF BACTERIA AT SITE

  figure, ax = plt.subplots()
  ax.set_facecolor((0.98, 0.98, 0.92))
  colors = [G[u][v]['color'] for u,v in G.edges]
  nx.draw(G,pos, ax = ax, node_color = colour_map, edge_color = colors, with_labels = True)

  #nx.draw_networkx_edge_labels(G,pos=pos, edge_labels=edge_labels, font_size=10, font_color="blue")
  ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
  limits=plt.axis('on')
  plt.grid(True)
  plt.xlabel("Temperature (˚C)")
  plt.ylabel(y_axis_label)
  ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

  #plt.figure(figsize = (50,50))
  #nx.draw_networkx_nodes(G, pos=pos, node_color=colour_map)
  edge_visuals = {"width": 0.5, "alpha": 0.5, "edge_color":"black"}
  #nx.draw_networkx_edge_labels(G, pos, edge_labels = edge_labels, font_color = "blue")
  arc_rad = 0.25
  #edges = nx.draw_networkx_edges(G, pos=pos)
  plt.show()

  #fig.savefig("2.png", bbox_inches='tight',pad_inches=0)
