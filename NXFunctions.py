import pandas as pd
import csv
import numpy as np
import networkx as nx
import plotly.graph_objects as go
import matplotlib.pyplot as plt

def createGraph(df_location, phyla, about_location, save_location, gtype):
  df = pd.read_csv(df_location, sep=" ", names = None) 
  df = df.reset_index()
  df = df.rename(columns={"index": "Location"})

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

  location_coordinates = list(zip(df["T.grid"], df["P.grid"]))

  def CalculateWeightedPosition(dataframe, node_phylum, coordinate_list:tuple, frequency_list): 
    total_freq = float(dataframe[node_phylum].sum(axis = 0))
    sum_ = (0.0,0.0)
    for idx, value in enumerate(coordinate_list):
      constant = frequency_list[idx]
      if constant != 0:
        sum_ = tuple(map(sum,zip(sum_,([constant*x for x in value]))))
    weighted_coordinates_x = float
    weighted_coordinates_y = float
    weighted_coordinates_x = sum_[0]/total_freq
    weighted_coordinates_y = float(sum_[1]/total_freq)
    weighted_coordinates = (weighted_coordinates_x,weighted_coordinates_y)
    return weighted_coordinates
  
  G = nx.Graph() 
  pos = {}
  colour_map = []
  for _, row in df.iterrows():
    G.add_node(row["Location"])
    pos[row["Location"]] = np.array([row["T.grid"], row["P.grid"]])
    colour_map.append("lightgreen")
  
  df = df.reset_index()

  for idx, phylum in enumerate(phyla):
    node_coords = CalculateWeightedPosition(df, phylum, location_coordinates, list(df[phylum]))
    G.add_node(phylum)
    colour_map.append("grey")
    pos[phylum] = np.array(node_coords)
    largest_connection = max(df[phylum])
    for _,row in df.iterrows():
      if row[phylum] != 0:
        if row[phylum] == largest_connection:
          G.add_edge(phylum, row["Location"], color = "red") 
        else:
          G.add_edge(phylum, row["Location"], color = (0.871, 0.871, 0.871)) 


  figure, ax = plt.subplots()
  print(G.edges)
  colors = [G[u][v]["color"] for u,v in G.edges]
  nx.draw(G, pos, ax = ax, 
          node_color = colour_map,
          font_color = "black", 
          edge_color = colors, 
          with_labels = True)
  
  
  plt.xlabel("Temperature (˚C)", fontsize = 17)
  plt.ylabel("Precipitation (mm)",  fontsize = 17)


  ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
  limits=plt.axis("on")
  ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
  plt.show()

  #fig.savefig("2.png", bbox_inches='tight',pad_inches=0)
