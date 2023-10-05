from pyvis.network import Network
import networkx as nx
import streamlit.components.v1 as components
import streamlit as st

class GraphRenderer:
	def __init__(self,width=500,height=1000):
		self.width=width
		self.height=height

	def draw_graph(self,triplets):
		with st.spinner("Rendering Graph...."):
			G = nx.DiGraph()
			for triplet in triplets:
				subject_entity = triplet["subject_entity"]
				relation_type = triplet["relation_type"]
				target_entity = triplet["target_entity"]
				G.add_node(subject_entity, size=20, color='#3924f2', font_weight='bold')
				if ',' in target_entity:
					G.add_node(relation_type)
					G.add_edge(subject_entity, relation_type)
					
					target_entities = target_entity.split(',')
					for entity in target_entities:
					    G.add_node(entity)
					    G.add_edge(relation_type, entity)
				elif 'and' in target_entity.split(' '):
					G.add_node(relation_type)
					G.add_edge(subject_entity, relation_type)
					
					target_entities = target_entity.split('and')
					for entity in target_entities:
					    G.add_node(entity)
					    G.add_edge(relation_type, entity)
				elif 'or' in target_entity.split(' '):
					G.add_node(relation_type)
					G.add_edge(subject_entity, relation_type)
					
					target_entities = target_entity.split('or')
					for entity in target_entities:
					    G.add_node(entity)
					    G.add_edge(relation_type, entity)
				else:
					G.add_node(target_entity)
					G.add_edge(subject_entity, target_entity,label=relation_type,arrow='to')
			net = Network(notebook=True,directed=True)
			net.from_nx(G)
			net.show("file.html")
			HtmlFile = open("file.html", 'r', encoding='utf-8')
			source_code = HtmlFile.read() 
			components.html(source_code,height=self.height)
