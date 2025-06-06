## 🗞️ AI Journalist Agent 
This Streamlit app is an AI-powered journalist agent that generates high-quality articles using OpenAI GPT-4o. It automates the process of researching, writing, and editing articles, allowing you to create compelling content on any topic with ease.

### Features
- Searches the web for relevant information on a given topic
- Writes well-structured, informative, and engaging articles
- Edits and refines the generated content to meet the high standards of the New York Times

### How to get Started?

1. Clone the GitHub repository

```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git
cd advanced_ai_agents/single_agent_apps/ai_journalist_agent
```
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```
3. Get your OpenAI API Key

- Sign up for an [OpenAI account](https://platform.openai.com/) (or the LLM provider of your choice) and obtain your API key.

4. Get your SerpAPI Key

- Sign up for an [SerpAPI account](https://serpapi.com/) and obtain your API key.

5. Run the Streamlit App
```bash
streamlit run journalist_agent.py
```

### How it Works?

The AI Journalist Agent utilizes three main components:
- Searcher: Responsible for generating search terms based on the given topic and searching the web for relevant URLs using the SerpAPI.
- Writer: Retrieves the text from the provided URLs using the NewspaperToolkit and writes a high-quality article based on the extracted information.
- Editor: Coordinates the workflow between the Searcher and Writer, and performs final editing and refinement of the generated article.


### Changes I made to the project
1. Tone Selector: Allows user to choose the tone the article is written in.
2. Article Format Selector: Allows the user to choose the format of the article(blog, news, report, opinion piece).
3. Fact Verification Agent: An agent that finds the facts written in the article and verifies the facts. Also provides the links from where they are found.
4. Sources and Citations: Shows a list of the URLs used to write the article at the bottom of the page. Allows the user to read up on where the information has come from.
5. Multilingual Support: Allows user to choose what language they want the article to be written in.

