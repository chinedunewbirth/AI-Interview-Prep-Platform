# 🎯 AI Interview Prep Platform

An AI-powered platform to help you ace your job interviews with personalized questions, real-time feedback, and resume analysis.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- **🎯 Question Generation**: AI-generated interview questions tailored to your role
- **💬 Mock Interviews**: Practice with an AI interviewer and get real-time feedback
- **📄 Resume Analysis**: Comprehensive resume review with actionable insights
- **📊 Progress Tracking**: Monitor your improvement over time
- **💾 Export Results**: Download all feedback and analysis

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com))

### Installation

#### Option 1: Using pip (traditional)
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-interview-prep.git
cd ai-interview-prep

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e .

# Or install from requirements.txt
pip install -r requirements.txt
```

#### Option 2: Using Poetry (recommended)
```bash
# Clone the repository
git clone https://github.com/yourusername/ai-interview-prep.git
cd ai-interview-prep

# Install dependencies with Poetry
poetry install

# Activate virtual environment
poetry shell
```

#### Option 3: Using uv (fastest)
```bash
# Install uv if you haven't
pip install uv

# Create environment and install
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
```

### Configuration

1. Copy the environment template:
```bash
cp .env.example .env
```

2. Add your Anthropic API key to `.env`:
```bash
ANTHROPIC_API_KEY=your_api_key_here
```

### Run Locally
```bash
# With standard Python
streamlit run app.py

# With Poetry
poetry run streamlit run app.py
```

Visit `http://localhost:8501` in your browser.

## 🌐 Deploy to Production

### Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Add `ANTHROPIC_API_KEY` to secrets
5. Deploy!

### Docker
```bash
# Build image
docker build -t ai-interview-prep .

# Run container
docker run -p 8501:8501 -e ANTHROPIC_API_KEY=your_key ai-interview-prep
```

### Railway
```bash
railway init
railway add
railway up
```

## 📖 Usage Guide

### 1. Generate Questions

1. Navigate to "Generate Questions"
2. Enter your job role (e.g., "Senior Software Engineer")
3. Select experience level
4. Click "Generate Questions"

### 2. Mock Interview

1. Generate questions first
2. Go to "Mock Interview"
3. Click "Start Interview"
4. Answer each question
5. Receive detailed feedback
6. Export your results

### 3. Resume Analysis

1. Navigate to "Resume Analysis"
2. Paste your resume text
3. Click "Analyze Resume"
4. Review strengths, improvements, and keywords
5. Export the analysis report

## 🛠️ Development

### Setup Development Environment
```bash
# Install with dev dependencies
poetry install --with dev

# Or with pip
pip install -e ".[dev]"
```

### Code Quality
```bash
# Format code
black .

# Lint code
ruff check .

# Type checking
mypy .

# Run tests
pytest

# Run tests with coverage
pytest --cov
```

### Pre-commit Hooks
```bash
# Install pre-commit
pip install pre-commit

# Setup hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

## 📊 Project Statistics

- **Lines of Code**: ~500
- **Dependencies**: 3 main, 7 dev
- **Python Version**: 3.9+
- **Test Coverage**: 80%+

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io)
- Powered by [Anthropic Claude](https://anthropic.com)
- Inspired by modern interview preparation needs

## 📧 Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter)

Project Link: [https://github.com/yourusername/ai-interview-prep](https://github.com/yourusername/ai-interview-prep)

---

**Made with ❤️ and AI**