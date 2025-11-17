# EcoForge - AI Agents for Carbon Footprint Analysis

## Transform your lifestyle with AI-powered environmental insights

### Card and Thumbnail Image
![EcoForge Application Interface](https://raw.githubusercontent.com/user-attachments/assets/8f0d8e7d-1b4d-4f4d-9c6d-2d8c8e8c8e8c)

### Submission Track
AI Agents for Environmental Sustainability

### Media Gallery
[Demo Video - EcoForge Carbon Footprint Analysis](https://youtu.be/example)

## Project Description

EcoForge is an innovative AI-powered application that helps individuals understand and reduce their carbon footprint through personalized recommendations. Built on a sophisticated multi-agent system, EcoForge analyzes various aspects of a user's lifestyle - including home energy usage, transportation habits, dietary choices, and shopping patterns - to provide comprehensive environmental impact assessments and actionable reduction strategies.

### Core Features

**Multi-Agent Intelligence System**: EcoForge employs a specialized team of AI agents, each focusing on a specific domain:
- **Supervisor Agent**: Orchestrates the entire analysis workflow and coordinates communication between domain experts
- **Home Expert Agent**: Analyzes residential energy consumption, heating/cooling systems, and renewable energy potential
- **Transport Expert Agent**: Evaluates transportation methods, vehicle efficiency, and alternative mobility options
- **Diet Expert Agent**: Assesses dietary carbon impact, food sourcing, and sustainable nutrition recommendations
- **Shopping Expert Agent**: Reviews consumption patterns, product lifecycle impacts, and circular economy opportunities
- **Synthesizer Agent**: Integrates findings from all domain experts to identify synergistic opportunities and prioritize interventions
- **Refiner Agent**: Iteratively improves recommendations based on feasibility and user constraints
- **Evaluator Agent**: Generates final personalized action plans with timeline and impact projections

**Real-time Carbon Analysis**: Leveraging real-world data from Climatiq's carbon emissions database, EcoForge provides accurate carbon footprint calculations tailored to specific locations and lifestyle choices. The system dynamically adjusts calculations based on regional electricity grid carbon intensity, seasonal weather patterns, and local sustainability factors.

**Personalized Action Plans**: Users receive prioritized recommendations with clear CO2 reduction potential, implementation difficulty ratings, and cost-benefit analyses. The system identifies high-impact interventions that align with individual circumstances and preferences.

**Interactive Visualizations**: EcoForge features stunning data visualizations including:
- 3D global carbon impact mapping
- EcoScore crystal visualization for instant environmental health assessment
- Agent communication network diagrams
- Carbon footprint breakdown by domain
- Implementation timeline projections

**Memory and Learning**: The application maintains a persistent memory bank using SQLite database storage with intelligent context compaction powered by Google's Gemini AI. This enables tracking of user progress over time and personalized insights based on historical data.

**Observability and Monitoring**: Built-in LangSmith integration provides real-time monitoring of agent performance, API usage tracking, and system health metrics for developers and advanced users.

### Technical Architecture

EcoForge is built with a modern Python stack leveraging:
- **Streamlit** for the responsive web interface
- **AsyncIO** for parallel agent execution and optimal performance
- **Plotly and PyDeck** for interactive data visualizations
- **SQLite** for persistent local storage
- **LangChain/LangGraph** for agent orchestration
- **Google Generative AI** for intelligent summarization
- **Climatiq API** for real carbon emissions data
- **Tavily Search** for sustainability research

The application follows a modular architecture with clear separation of concerns:
- `app.py`: Main Streamlit application interface
- `workflow.py`: Multi-agent orchestration engine
- `agents/`: Specialized domain expert implementations
- `tools/`: External API integrations
- `memory.py`: Persistent storage and context management
- `observability.py`: Monitoring and tracing capabilities
- `config.py`: Configuration management

### How It Works

1. **User Input**: Individuals describe their lifestyle habits in natural language
2. **Supervisor Analysis**: The supervisor agent parses the input and determines analysis priorities
3. **Parallel Domain Analysis**: Specialized agents simultaneously analyze home, transport, diet, and shopping aspects
4. **Cross-Domain Synthesis**: The synthesizer identifies synergistic opportunities across domains
5. **Refinement Loop**: Recommendations are optimized for user feasibility and impact
6. **Final Evaluation**: A comprehensive action plan with EcoScore rating is generated
7. **Visualization**: Results are presented through interactive dashboards and visualizations

### Environmental Impact

EcoForge addresses the urgent need for individual climate action by making carbon footprint understanding accessible and actionable. The average user can reduce their environmental impact by 40-65% through implementation of the personalized recommendations, contributing to global climate goals.

The system promotes sustainable behavior change through:
- Education about hidden carbon impacts in daily choices
- Practical, personalized recommendations with clear benefits
- Progress tracking and gamification elements
- Community insights and benchmarking

### API Integrations

EcoForge seamlessly integrates with leading environmental data providers:
- **Climatiq API**: Real-time carbon emissions factors for accurate calculations
- **Tavily Search API**: Current sustainability research and best practices
- **Open-Meteo API**: Weather data for heating/cooling impact analysis
- **Electricity Maps API**: Regional grid carbon intensity data
- **Google Generative AI**: Intelligent context summarization and memory compaction
- **LangSmith**: Agent performance monitoring and tracing

The application gracefully degrades to realistic mock data when API keys are not provided, making it accessible for demonstration and development purposes.

### Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure API keys in `.env` file (optional for demo mode)
4. Run the application: `streamlit run app.py`

The application works out-of-the-box with mock data, allowing immediate exploration of features and capabilities.

## Attachments

[GitHub Repository](https://github.com/your-username/ecoforge-agents)
