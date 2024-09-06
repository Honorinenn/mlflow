import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import networkx as nx
import matplotlib.pyplot as plt
import heapq
import random
 
class FlightGraph:
    def __init__(self):
        self.flightGraph = nx.DiGraph()
        self.flight = []  # Placeholder for flight data
        self.flightMap = {}  # Placeholder for city-to-index mapping
 
    def Dijkstra(self, source, destination):
        # Convert NetworkX graph to adjacency list format
        adjacency_list = {node: [(neighbor, data['weight']) for neighbor, data in self.flightGraph[node].items()] for node in self.flightGraph.nodes()}
 
        pq = []
        dist = {node: float('inf') for node in adjacency_list}
        vis = set()
        parent = {}
 
        dist[source] = 0
        heapq.heappush(pq, (0, source))
 
        while pq:
            currw, currv = heapq.heappop(pq)
            if currv in vis:
                continue
            vis.add(currv)
 
            for nextv, nextw in adjacency_list[currv]:
                if nextv not in vis:
                    newWeight = currw + nextw
                    if newWeight < dist[nextv]:
                        dist[nextv] = newWeight
                        parent[nextv] = currv
                        heapq.heappush(pq, (newWeight, nextv))
 
        # Construct the shortest path
        pathTaken = []
        if dist[destination] == float('inf'):
            return pathTaken
 
        i = destination
        while i != source:
            pathTaken.append(i)
            i = parent.get(i, source)
        pathTaken.append(source)
        pathTaken.reverse()
 
        return pathTaken
 
    def buildGraph(self):
        # Example flight data and map for 10 cities
        cities = ['Manhattan', 'Philadelphia', 'Ames', 'Dallas', 'San Antonio', 'Phoenix', 'Los Angeles', 'San Diego', 'Bend', 'Seattle', ]
        self.flightMap = {city: i for i, city in enumerate(cities)}
 
        # Add edges between cities with random distances
        for i in range(10):
            for j in range(i + 1, 10):
                distance = random.randint(5, 20)  # Random distance between 5 and 20
                self.flightGraph.add_edge(i, j, weight=distance, flight=f'Flight{i}{j}', probability=random.uniform(0, 1))
                self.flightGraph.add_edge(j, i, weight=distance, flight=f'Flight{j}{i}', probability=random.uniform(0, 1))
 
    def drawGraph(self):
        # Draw the graph using matplotlib
        plt.figure(figsize=(12, 8))
        pos = nx.spring_layout(self.flightGraph)
        weights = nx.get_edge_attributes(self.flightGraph, 'weight')
        labels = {i: city for city, i in self.flightMap.items()}
 
        nx.draw(self.flightGraph, pos, with_labels=False, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
        nx.draw_networkx_labels(self.flightGraph, pos, labels=labels, font_size=12, font_weight='bold')
        nx.draw_networkx_edge_labels(self.flightGraph, pos, edge_labels=weights)
        plt.title("Flight Graph")
        plt.show()
 
# Example usage:
graph = FlightGraph()
graph.buildGraph()
graph.drawGraph()
 
# Running Dijkstra's algorithm
source_index = 0  # Starting from 'New York'
destination_index = 9  # Ending at 'San Jose'
shortest_path = graph.Dijkstra(source_index, destination_index)
 
# Map back to city names for readability
city_names = [city for city, index in graph.flightMap.items()]
shortest_path_names = [city_names[i] for i in shortest_path]
 
print("Shortest path from Manhattan to Ames:", shortest_path_names)
