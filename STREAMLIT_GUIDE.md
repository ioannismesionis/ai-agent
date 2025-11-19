# Career Advisor Streamlit UI

A beautiful, interactive web interface for your AI Career Advisor agent.

## Features

✅ **Clean Interface** - User-friendly chat-like experience
✅ **Real-time Processing** - See research and mentoring in action
✅ **Conversation History** - Track your career planning journey
✅ **Customizable Display** - Toggle research/mentor outputs
✅ **Session Management** - Start fresh conversations anytime
✅ **Memory Integration** - Remembers context across conversations

## Quick Start

### 1. Ensure Dependencies are Installed

```bash
# If using uv (recommended)
uv pip install streamlit

# Or using pip
pip install streamlit
```

### 2. Make Sure Your .env File is Set Up

Ensure your `.env` file contains:
```
GOOGLE_API_KEY=your_api_key_here
```

### 3. Run the Streamlit App

```bash
streamlit run app.py
```

### 4. Open Your Browser

Streamlit will automatically open your browser to `http://localhost:8501`

If it doesn't open automatically, navigate to that URL manually.

## How to Use

1. **Enter Your Career Query**
   - Describe your current role, experience, target role, and time commitment
   - Example: "I'm a Product Manager with 5 years of experience. I want to transition to Data Science and can dedicate 10 hours per week."

2. **Click "Get Career Advice"**
   - The agent will research your career transition
   - Then create a personalized action plan

3. **Review the Results**
   - **Research Findings**: Detailed information about your target career
   - **Personalized Career Plan**: Step-by-step transition roadmap

4. **Continue the Conversation**
   - Ask follow-up questions in the same session
   - Or start a new session for a different career path

## Sidebar Options

- **Show Research Output**: Toggle research findings display
- **Show Mentor Plan**: Toggle action plan display
- **New Session**: Start fresh with a clean conversation

## Tips for Best Results

💡 **Be Specific**: Include your current role, years of experience, target role, and available time

💡 **Ask Follow-ups**: Continue the conversation to refine your plan

💡 **Use New Sessions**: Start fresh when exploring different career paths

## Troubleshooting

**Error: "No module named 'streamlit'"**
```bash
pip install streamlit
```

**Error: "GOOGLE_API_KEY not found"**
- Make sure your `.env` file exists in the project root
- Verify the API key is correctly set

**App is slow or hanging**
- Check your internet connection
- Verify your API key is valid
- Check API rate limits

## Deployment Options

### Deploy to Streamlit Cloud (Free)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add `GOOGLE_API_KEY` as a secret
5. Deploy!

### Deploy to Other Platforms

- **Heroku**: Use Procfile with `web: streamlit run app.py`
- **Google Cloud Run**: Containerize with Docker
- **AWS**: Use EC2 or ECS

## Project Structure

```
ai-agent/
├── app.py                 # Streamlit UI (main file)
├── ai-agent.ipynb        # Original Jupyter notebook
├── .env                  # API keys (don't commit!)
├── requirements.txt      # Python dependencies
└── STREAMLIT_GUIDE.md   # This file
```

## Next Steps

- 🎨 Customize the UI styling in the CSS section
- 📊 Add analytics/metrics tracking
- 💾 Implement persistent storage (database)
- 🔐 Add user authentication
- 📧 Add email notifications for completed plans

---

Built with ❤️ using Google ADK and Streamlit
