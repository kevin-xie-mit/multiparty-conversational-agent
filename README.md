# Multiparty Conversational Agent: AI-Powered Group Discussion Moderator

## Overview

This project develops an advanced AI moderator system designed to facilitate and enhance group conversations in human-computer interaction (HCI) research contexts. The system uses large language models (LLMs) to provide intelligent, context-aware moderation for multiparty conversations, with a focus on decision-making processes and collaborative problem-solving.

## Research Context

The AI moderator is specifically designed for murder mystery group decision-making scenarios where participants must collaborate to solve a fictional case. This controlled environment allows for systematic study of:

- **Group dynamics** and participation patterns
- **Decision-making processes** in collaborative settings
- **AI intervention effectiveness** in conversation facilitation
- **Information sharing** and consensus building

## System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Chat Parser   │────│   AI Moderator  │────│  Vector Store   │
│                 │    │                 │    │                 │
│ • Message proc. │    │ • GPT-4 LLM     │    │ • Chroma DB     │
│ • Character ID  │    │ • Tool calling  │    │ • Embeddings    │
│ • Format clean  │    │ • Context build │    │ • Similarity    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │ Conversation    │
                    │ Analysis        │
                    │                 │
                    │ • Participation │
                    │ • Long-term ctx │
                    │ • Intervention  │
                    └─────────────────┘
```

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/multiparty-conversational-agent.git
cd multiparty-conversational-agent

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key
```

## Usage

### Basic Usage

```python
from src.main import process_chat

# Process a single conversation
process_chat(1)

# Process multiple conversations
for i in range(0, 10):
    process_chat(i)
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Citation

If you use this work in your research, please cite:

```bibtex
@software{multiparty_conversational_agent,
  title={Multiparty Conversational Agent: AI-Powered Group Discussion Moderator},
  author={Kevin XIe},
  year={2024},
  url={https://github.com/yourusername/multiparty-conversational-agent}
}
```
