# AI Game Purchase Assistant

A powerful AI-powered assistant that helps you find and purchase games at the best prices across multiple gaming platforms. The application features both voice and text-based interactions using LiveKit for real-time communication and LangGraph for intelligent decision-making.

## Features

### 🎮 Multi-Platform Game Search
- **Epic Games Store** integration via [`game_site.epic`](backend/game_site/epic.py)
- **Steam** platform support via [`game_site.steam`](backend/game_site/steam.py)
- **GOG** (Good Old Games) integration via [`game_site.gog`](backend/game_site/gog.py)

### 🤖 Intelligent Price Comparison
- Automatic price fetching from all supported platforms
- Smart comparison algorithm in [`logic.compare`](backend/logic/compare.py)
- Best deal recommendation based on price and availability

### 🎙️ Voice Interface (LiveKit)
- Real-time voice conversations using Google's Realtime Model
- Enhanced noise cancellation for clear audio
- Natural language processing for game name extraction
- Voice commands for game purchasing

### 💬 Text Interface (LangGraph)
- Chat-based interaction using Google Gemini
- Structured conversation flow with state management
- Tool-based architecture for modular functionality

## Architecture

```
backend/
├── agent.py          # LiveKit voice agent implementation
├── main.py           # LangGraph text-based agent
├── tool.py           # Shared game purchasing tool
├── game_site/        # Platform integrations
│   ├── epic.py
│   ├── steam.py
│   └── gog.py
├── logic/
│   └── compare.py    # Price comparison logic
└── llm/
    └── agent.py      # Game name extraction
```

## Setup

### Prerequisites
- Python 3.9+
- Google API Key for Gemini
- LiveKit Cloud account (for voice features)

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd aiagent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   Create a [`.env`](backend/.env) file in the backend directory:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   LIVEKIT_URL=your_livekit_url
   LIVEKIT_API_KEY=your_livekit_api_key
   LIVEKIT_API_SECRET=your_livekit_api_secret
   ```

## Usage

### Voice Interface

Start the LiveKit voice agent:

```bash
cd backend
python agent.py
```

The voice agent uses the [`Assistant`](backend/agent.py) class with:
- Google Realtime Model with "puck" voice
- Enhanced noise cancellation via [`noise_cancellation.BVC()`](backend/agent.py)
- Integrated [`buy_game_tool`](backend/tool.py) for game purchasing

**Voice Commands:**
- "I want to buy [game name]"
- "Find me the best price for [game name]"
- "Purchase [game name] for me"

### Text Interface

Start the LangGraph text agent:

```bash
cd backend
python main.py
```

The text interface provides:
- Interactive chat session
- State management with [`StateGraph`](backend/main.py)
- Multiple tools: [`extract_game_name`](backend/main.py), [`best_options`](backend/main.py), and [`buy_game`](backend/main.py)

**Text Commands:**
- Type any message about wanting to buy a game
- The agent will extract the game name and find the best deal
- Automatic purchase execution after price comparison

## How It Works

### Game Purchase Flow

1. **Input Processing**: User provides game name via voice or text
2. **Name Extraction**: [`extract_game_name`](backend/llm/agent.py) function processes the input
3. **Price Fetching**: Parallel queries to Epic, Steam, and GOG via respective modules
4. **Comparison**: [`choose_best`](backend/logic/compare.py) algorithm selects optimal option
5. **Purchase**: Automatic execution through the selected platform's API

### Core Components

- **[`buy_game_tool`](backend/tool.py)**: Main function tool that orchestrates the entire purchase process
- **[`Assistant`](backend/agent.py)**: LiveKit Agent class for voice interactions
- **[`State`](backend/main.py)**: TypedDict managing conversation state and purchase status
- **Platform modules**: Individual integrations for each gaming platform

## API Integration

The application integrates with:

- **Google Gemini**: For natural language processing and conversation
- **Google Realtime Model**: For voice synthesis and recognition
- **LiveKit**: For real-time voice communication
- **Gaming Platforms**: Epic Games, Steam, and GOG APIs

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue on GitHub or contact the development team.

---

**Note**: This application requires valid API keys and proper configuration for all integrated services. Make sure to review the platform-specific terms of service before using their APIs for automated purchases.
