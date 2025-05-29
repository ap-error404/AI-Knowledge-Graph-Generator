# 🧠 AI-Powered Knowledge Graph Generator

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Google AI](https://img.shields.io/badge/Powered%20by-Google%20Gemini-4285F4.svg)](https://ai.google.dev/)

Transform unstructured text into beautiful, interactive knowledge graphs using Google's Gemini AI. This web application automatically extracts entities and relationships from any text and visualizes them as dynamic network graphs.


## ✨ Features

- 🤖 **AI-Powered Analysis** - Uses Google Gemini AI for intelligent entity and relationship extraction
- 📊 **Interactive Visualizations** - Beautiful, interactive knowledge graphs with Plotly
- 📁 **Multiple Input Methods** - Direct text input or file upload support
- 🎨 **Smart Entity Coloring** - Different colors for people, organizations, locations, concepts, and events
- 📈 **Graph Analytics** - Detailed statistics and insights about your knowledge graphs
- 💾 **Data Export** - View and analyze extracted data in structured tables
- 🌐 **Web Interface** - Easy-to-use Streamlit web application
- 🔒 **Secure** - Your API key stays local, secure processing

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Google AI Studio API key ([Get it free here](https://makersuite.google.com/app/apikey))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ap-error404/AI-Knowledge-Graph-Generator.git
   cd ai-knowledge-graph-generator
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux  
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   - Go to `http://localhost:8501`
   - Enter your Google AI Studio API key
   - Start creating knowledge graphs!

## 🎯 How It Works

1. **Input Text** - Type directly or upload a `.txt` file
2. **AI Analysis** - Gemini AI extracts entities and relationships
3. **Graph Generation** - NetworkX creates the graph structure
4. **Visualization** - Plotly renders an interactive network graph
5. **Explore Results** - Analyze entities, relationships, and graph statistics

## 📊 Demo

### Sample Input:
```
Apple Inc. is a technology company founded by Steve Jobs, Steve Wozniak, and Ronald Wayne in 1976. 
The company is headquartered in Cupertino, California. Tim Cook became CEO after Steve Jobs passed away in 2011. 
Apple is known for products like the iPhone, iPad, and Mac computers.
```

### Generated Output:
- **Entities**: Apple Inc. (Organization), Steve Jobs (Person), Cupertino (Location), iPhone (Product)
- **Relationships**: Steve Jobs → founded → Apple Inc., Apple Inc. → located_in → Cupertino
- **Interactive Graph**: Hover over nodes and edges to see detailed information

## 🎨 Entity Types & Colors

| Entity Type | Color | Description |
|-------------|-------|-------------|
| 🔴 Person | Red | Individual people |
| 🟢 Organization | Teal | Companies, institutions |
| 🔵 Location | Blue | Places, cities, countries |
| 🟤 Concept | Green | Ideas, theories, abstract concepts |
| 🟡 Event | Yellow | Specific events, meetings |
| 🟣 Unknown | Purple | Uncategorized entities |

## 💡 Tips for Best Results

### Optimal Text Types:
- 📰 News articles
- 📚 Research paper abstracts  
- 📋 Business reports
- 📖 Historical accounts
- 👤 Biographical information
- 📄 Technical documentation

### Text Guidelines:
- **Length**: 100-2000 words work best
- **Structure**: Well-formatted, coherent text
- **Content**: Factual content with clear entities and relationships
- **Language**: English text produces optimal results

## 🛠️ Technical Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Interactive web interface
- **AI Engine**: [Google Gemini](https://ai.google.dev/) - Entity and relationship extraction
- **Graph Processing**: [NetworkX](https://networkx.org/) - Graph structure and analysis
- **Visualization**: [Plotly](https://plotly.com/python/) - Interactive graph rendering
- **Data Handling**: [Pandas](https://pandas.pydata.org/) - Data manipulation and export

## 📁 Project Structure

```
ai-knowledge-graph-generator/
│
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies  
├── README.md             # Project documentation
├── LICENSE               # MIT License
├── .gitignore           # Git ignore file
```

## 🔧 Configuration

### Environment Variables (Optional)
Create a `.env` file for default configuration:
```env
GOOGLE_API_KEY=your_api_key_here
DEFAULT_MODEL=gemini-2.5-flash-preview-04-17
```

### Customization Options
- **Entity Colors**: Modify the `color_map` in `create_plotly_visualization()`
- **AI Prompts**: Customize extraction prompts in `create_extraction_prompt()`
- **Graph Layout**: Change NetworkX layout algorithms
- **UI Theme**: Customize Streamlit theme in `.streamlit/config.toml`

## 📈 Performance

- **Processing Time**: 5-30 seconds depending on text length
- **Optimal Text Length**: 100-2000 words
- **Concurrent Users**: Supports multiple users (API rate limits apply)
- **Memory Usage**: Minimal - graphs stored temporarily

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google AI** for providing the Gemini API
- **Streamlit** for the amazing web framework
- **NetworkX** for graph processing capabilities
- **Plotly** for beautiful visualizations
- **Open Source Community** for inspiration and tools

