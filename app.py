import streamlit as st
import google.generativeai as genai
import networkx as nx
import plotly.graph_objects as go
import plotly.express as px
import json
import re
import os
from typing import List, Dict, Tuple
import pandas as pd

# Configure page
st.set_page_config(
    page_title="AI Knowledge Graph Generator",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

class KnowledgeGraphGenerator:
    def __init__(self, api_key: str):
        """Initialize the knowledge graph generator with Gemini API."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash-preview-04-17')
        
    def create_extraction_prompt(self, text: str) -> str:
        """Create a prompt for entity and relationship extraction."""
        prompt = f"""
        Analyze the following text and extract entities and relationships. Return the result as a valid JSON object with the following structure:
        
        {{
            "entities": [
                {{"name": "entity_name", "type": "entity_type", "description": "brief_description"}}
            ],
            "relationships": [
                {{"source": "entity1", "target": "entity2", "relationship": "relationship_type", "description": "relationship_description"}}
            ]
        }}
        
        Guidelines:
        - Extract people, organizations, locations, concepts, events, and other significant entities
        - Identify meaningful relationships between entities (works_for, located_in, part_of, leads_to, causes, etc.)
        - Use clear, consistent entity names
        - Provide brief but informative descriptions
        - Focus on the most important entities and relationships
        - Ensure all entities mentioned in relationships are also listed in the entities array
        
        Text to analyze:
        {text}
        
        Return only the JSON object, no additional text.
        """
        return prompt
    
    def extract_entities_relationships(self, text: str) -> Dict:
        """Extract entities and relationships using Gemini."""
        try:
            prompt = self.create_extraction_prompt(text)
            response = self.model.generate_content(prompt)
            
            # Clean the response to extract JSON
            response_text = response.text.strip()
            
            # Try to find JSON in the response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
            else:
                # If no JSON found, try to parse the entire response
                return json.loads(response_text)
                
        except json.JSONDecodeError as e:
            st.error(f"Error parsing AI response: {e}")
            return {"entities": [], "relationships": []}
        except Exception as e:
            st.error(f"Error calling Gemini API: {e}")
            return {"entities": [], "relationships": []}
    
    def create_graph(self, extracted_data: Dict) -> nx.Graph:
        """Create a NetworkX graph from extracted entities and relationships."""
        G = nx.Graph()
        
        # Add nodes (entities)
        for entity in extracted_data.get("entities", []):
            G.add_node(
                entity["name"],
                type=entity.get("type", "unknown"),
                description=entity.get("description", "")
            )
        
        # Add edges (relationships)
        for rel in extracted_data.get("relationships", []):
            source = rel.get("source", "")
            target = rel.get("target", "")
            
            if source and target and G.has_node(source) and G.has_node(target):
                G.add_edge(
                    source,
                    target,
                    relationship=rel.get("relationship", "related_to"),
                    description=rel.get("description", "")
                )
        
        return G
    
    def create_plotly_visualization(self, G: nx.Graph) -> go.Figure:
        """Create an interactive Plotly visualization of the graph."""
        if len(G.nodes()) == 0:
            return go.Figure()
        
        # Use spring layout for node positioning
        pos = nx.spring_layout(G, k=3, iterations=50)
        
        # Extract node information
        node_x = []
        node_y = []
        node_text = []
        node_info = []
        node_colors = []
        
        # Color mapping for different entity types
        color_map = {
            "person": "#FF6B6B",
            "organization": "#4ECDC4", 
            "location": "#45B7D1",
            "concept": "#96CEB4",
            "event": "#FFEAA7",
            "unknown": "#DDA0DD"
        }
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            node_data = G.nodes[node]
            entity_type = node_data.get("type", "unknown")
            description = node_data.get("description", "")
            
            node_text.append(node)
            node_info.append(f"<b>{node}</b><br>Type: {entity_type}<br>Description: {description}")
            node_colors.append(color_map.get(entity_type.lower(), color_map["unknown"]))
        
        # Extract edge information
        edge_x = []
        edge_y = []
        edge_info = []
        
        for edge in G.edges():
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            edge_x.extend([x0, x1, None])
            edge_y.extend([y0, y1, None])
            
            edge_data = G.edges[edge]
            relationship = edge_data.get("relationship", "related_to")
            description = edge_data.get("description", "")
            edge_info.append(f"{edge[0]} → {relationship} → {edge[1]}<br>{description}")
        
        # Create the figure
        fig = go.Figure()
        
        # Add edges
        fig.add_trace(go.Scatter(
            x=edge_x, y=edge_y,
            line=dict(width=2, color='#888'),
            hoverinfo='none',
            mode='lines',
            showlegend=False
        ))
        
        # Add nodes
        fig.add_trace(go.Scatter(
            x=node_x, y=node_y,
            mode='markers+text',
            hoverinfo='text',
            hovertext=node_info,
            text=node_text,
            textposition="middle center",
            textfont=dict(size=10, color="white"),
            marker=dict(
                size=30,
                color=node_colors,
                line=dict(width=2, color='white')
            ),
            showlegend=False
        ))
        
        # Update layout
        fig.update_layout(
            title="Knowledge Graph Visualization",
            showlegend=False,
            hovermode='closest',
            margin=dict(b=20,l=5,r=5,t=40),
            annotations=[ dict(
                text="Hover over nodes and edges to see details",
                showarrow=False,
                xref="paper", yref="paper",
                x=0.005, y=-0.002,
                xanchor='left', yanchor='bottom',
                font=dict(color='gray', size=12)
            )],
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            plot_bgcolor='white',
            height=600
        )
        
        return fig

def main():
    st.title("🧠 AI-Powered Knowledge Graph Generator")
    st.markdown("*Powered by Google Gemini AI*")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # API Key input
    api_key = st.sidebar.text_input(
        "Enter your Google AI Studio API Key:",
        type="password",
        help="Get your API key from Google AI Studio: https://makersuite.google.com/app/apikey"
    )
    
    if not api_key:
        st.warning("⚠️ Please enter your Google AI Studio API key in the sidebar to continue.")
        st.markdown("""
        ### How to get your API Key:
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the key and paste it in the sidebar
        """)
        return
    
    # Initialize the knowledge graph generator
    kg_generator = KnowledgeGraphGenerator(api_key)
    
    # Main interface
    st.header("Input Text")
    
    # Input method selection
    input_method = st.radio(
        "Choose input method:",
        ["Type text directly", "Upload text file"]
    )
    
    text_input = ""
    
    if input_method == "Type text directly":
        text_input = st.text_area(
            "Enter your text:",
            height=200,
            placeholder="Paste or type the text you want to analyze..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a text file:",
            type=['txt'],
            help="Upload a .txt file containing the text to analyze"
        )
        
        if uploaded_file is not None:
            text_input = str(uploaded_file.read(), "utf-8")
            st.text_area("Uploaded text preview:", value=text_input[:500] + "..." if len(text_input) > 500 else text_input, height=150, disabled=True)
    
    # Generate button
    if st.button("🚀 Generate Knowledge Graph", type="primary"):
        if not text_input.strip():
            st.error("Please provide some text to analyze.")
            return
        
        with st.spinner("Analyzing text with Gemini AI..."):
            # Extract entities and relationships
            extracted_data = kg_generator.extract_entities_relationships(text_input)
            
            if not extracted_data.get("entities") and not extracted_data.get("relationships"):
                st.error("No entities or relationships could be extracted from the text.")
                return
            
            # Create graph
            G = kg_generator.create_graph(extracted_data)
            
            if len(G.nodes()) == 0:
                st.error("No valid graph could be created from the extracted data.")
                return
        
        # Display results
        st.success(f"✅ Successfully extracted {len(extracted_data.get('entities', []))} entities and {len(extracted_data.get('relationships', []))} relationships!")
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📊 Graph Visualization", "📋 Extracted Data", "📈 Graph Statistics"])
        
        with tab1:
            st.subheader("Knowledge Graph")
            fig = kg_generator.create_plotly_visualization(G)
            st.plotly_chart(fig, use_container_width=True)
            
            # Legend
            st.subheader("Entity Type Legend")
            legend_data = {
                "Entity Type": ["Person", "Organization", "Location", "Concept", "Event", "Unknown"],
                "Color": ["🔴", "🟢", "🔵", "🟤", "🟡", "🟣"]
            }
            st.table(pd.DataFrame(legend_data))
        
        with tab2:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Entities")
                entities_df = pd.DataFrame(extracted_data.get("entities", []))
                if not entities_df.empty:
                    st.dataframe(entities_df, use_container_width=True)
                else:
                    st.info("No entities extracted.")
            
            with col2:
                st.subheader("Relationships")
                relationships_df = pd.DataFrame(extracted_data.get("relationships", []))
                if not relationships_df.empty:
                    st.dataframe(relationships_df, use_container_width=True)
                else:
                    st.info("No relationships extracted.")
        
        with tab3:
            st.subheader("Graph Statistics")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Nodes", len(G.nodes()))
            
            with col2:
                st.metric("Total Edges", len(G.edges()))
            
            with col3:
                st.metric("Graph Density", f"{nx.density(G):.3f}")
            
            with col4:
                if len(G.nodes()) > 0:
                    avg_degree = sum(dict(G.degree()).values()) / len(G.nodes())
                    st.metric("Avg Degree", f"{avg_degree:.2f}")
                else:
                    st.metric("Avg Degree", "0")
            
            # Entity type distribution
            if extracted_data.get("entities"):
                entity_types = [entity.get("type", "unknown") for entity in extracted_data["entities"]]
                type_counts = pd.Series(entity_types).value_counts()
                
                st.subheader("Entity Type Distribution")
                fig_pie = px.pie(
                    values=type_counts.values,
                    names=type_counts.index,
                    title="Distribution of Entity Types"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with using [Streamlit](https://streamlit.io/) and [Google Gemini AI](https://ai.google.dev/)"
    )

if __name__ == "__main__":
    main()