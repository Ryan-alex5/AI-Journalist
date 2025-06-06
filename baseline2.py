# Import the required libraries
from textwrap import dedent
from agno.agent import Agent
from agno.tools.serpapi import SerpApiTools
from agno.tools.newspaper4k import Newspaper4kTools
import streamlit as st
from agno.models.openai import OpenAIChat

# Set up the Streamlit app
st.title("AI Journalist Agent 🗞️")
st.caption("Generate High-quality articles with AI Journalist by researching, wriritng and editing quality articles on autopilot using GPT-4o")

# Get OpenAI API key from user
openai_api_key = st.text_input("Enter OpenAI API Key to access GPT-4o", type="password")

# Get SerpAPI key from the user
serp_api_key = st.text_input("Enter Serp API Key for Search functionality", type="password")

if openai_api_key and serp_api_key:
    searcher = Agent(
        name="Searcher",
        role="Searches for top URLs based on a topic",
        model=OpenAIChat(id="gpt-3.5-turbo", api_key=openai_api_key),
        description=dedent(
            """\
        You are a world-class journalist for the New York Times. Given a topic, generate a list of 3 search terms
        for writing an article on that topic. Then search the web for each term, analyse the results
        and return the 10 most relevant URLs.
        """
        ),
        instructions=[
            "Given a topic, first generate a list of 3 search terms related to that topic.",
            "For each search term, `search_google` and analyze the results."
            "From the results of all searcher, return the 10 most relevant URLs to the topic.",
            "Remember: you are writing for the New York Times, so the quality of the sources is important.",
        ],
        tools=[SerpApiTools(api_key=serp_api_key)],
        add_datetime_to_instructions=True,
    )
    writer = Agent(
        name="Writer",
        role="Retrieves text from URLs and writes a high-quality article",
        model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
        description=dedent(
            """\
        You are a senior writer for the New York Times. Given a topic and a list of URLs,
        your goal is to write a high-quality NYT-worthy article on the topic.
        """
        ),
        instructions=[
            "Given a topic and a list of URLs, first read the article using `get_article_text`.",
            "Then write a high-quality NYT-worthy article on the topic.",
            "The article should be well-structured, informative, and engaging",
            "Ensure the length is at least as long as a NYT cover story -- at a minimum, 15 paragraphs.",
            "Adapt the writing tone to match the given preference (e.g, Professional, Casual, Persuasive, Neutral)",
            "Adapt the structure and style based on the requested format:",
            " - News Report: Stick to facts, use inverted pyramid structure, avoid opinions.",
            " - Opinion Piece: Take a stance, present arguments and counterarguments with evidence.",
            " - Blog Post: Use a conversational tone, personal stories or analogies, informal structure.",
            " - Executive Summary: Be concise, structured, and analytical. Focus on clarity over storytelling.",
            "Always follow the chosen format while maintaining NYT-level quality.",
            "Ensure the tone is consistent throughout the article",
            "Ensure you provide a nuanced and balanced opinion, quoting facts where possible.",
            "Remember: you are writing for the New York Times, so the quality of the article is important.",
            "Focus on clarity, coherence, and overall quality.",
            "Never make up facts or plagiarize. Always provide proper attribution.",
            "Ensure the article is written in the specified language: {language}.",
            "If translation is needed, do it accurately while preserving tone and format."
            
        ],
        tools=[Newspaper4kTools()],
        add_datetime_to_instructions=True,
        markdown=True,
    )

    editor = Agent(
        name="Editor",
        model=OpenAIChat(id="gpt-4o", api_key=openai_api_key),
        team=[searcher, writer],
        description="You are a senior NYT editor. Given a topic, your goal is to write a NYT worthy article.",
        instructions=[
            "Given a topic, ask the search journalist to search for the most relevant URLs for that topic.",
            "Then pass a description of the topic and URLs to the writer to get a draft of the article.",
            "Edit, proofread, and refine the article to ensure it meets the high standards of the New York Times.",
            "The article should be extremely articulate and well written. ",
            "Focus on clarity, coherence, and overall quality.",
            "Ensure the article is engaging and informative.",
            "After getting the article from the writer, return both:",
            "1. The list of final URLs used",
            "2. The final article",
            "Add the list of URLs to the bottom of this article, in a different section.",
            "This is to show readers where the information was sourced to make this article more professional and worthy of NYT",
            "Format them clearly for the user to see.",
            "Remember: you are the final gatekeeper before the article is published.",
            "Ensure the article is written in the specified language: {language}.",
            "If translation is needed, do it accurately while preserving tone and format."
        ],
        add_datetime_to_instructions=True,
        markdown=True,
    )

    fact_checker = Agent(
    name="FactChecker",
    role="Verifies facts and claims in an article using search.",
    model=OpenAIChat(id="gpt-3.5-turbo", api_key=openai_api_key),
    description="You are a fact verification expert at the New York Times. Your job is to verify the accuracy of claims in an article.",
    instructions=[
        "Read the full article and extract any factual claims (e.g. statistics, dates, events, names, quotes, etc.).",
        "For each claim, use `search_google` to look up credible sources and determine whether it is accurate and up-to-date.",
        "Return your results in a structured markdown table with the following columns:",
        "- **Claim**",
        "- **Status**: Verified ✅, Unverified ⚠️, or False ❌",
        "- **Verification Source**: Include 1–2 source URLs per claim",
        "- **Notes**: Any clarifications, contradictions, or context",
        "Only use reliable sources (e.g. government websites, respected news outlets, peer-reviewed journals).",
        "If a fact cannot be verified, explain why.",
        "Do not speculate or assume. Stick to what you can confirm from search results.",
    ],
    tools=[SerpApiTools(api_key=serp_api_key)],
    add_datetime_to_instructions=True,
    markdown=True
)



with st.form("article_form"):
    query = st.text_input("🧠 What do you want the AI journalist to write an article on?")
    
    tone = st.selectbox(
        "🎨 Select the tone of the article",
        ["Professional", "Casual", "Persuasive", "Neutral"]
    )
    
    article_format = st.selectbox(
        "🗂️ Select the article format",
        ["News Report", "Opinion Piece", "Blog Post", "Executive Summary"]
    )

    language = st.text_input(
        "🌐 Enter the language you want the article in (e.g., English, Spanish, Hindi, etc.)",
        value="English"
    )

    verify_facts = st.checkbox("🔍 Run Fact Verification on the Article")
    
    submit = st.form_submit_button("🚀 Generate Article")

    if submit and not language.strip().isalpha():
        st.warning("❗ Please enter a valid language name.")
        st.stop()

    st.caption("💡 E.g. Blog + Casual, or News Report + Professional are typical combinations.")

# Trigger agent only when the button is clicked and there's input
if submit and query:
    with st.spinner("Processing..."):
        task_description = f"""\
                                    Topic: {query}
                                    Preferred tone: {tone}
                                    Article format: {article_format}
                                    Language: {language}
                                    """
        response = editor.run(task_description, stream=False)
        st.write(response.content)
        

    # 🔍 Optional Fact Check
    if verify_facts:
        with st.spinner("🔍 Verifying facts..."):
            fact_report = fact_checker.run(response.content, stream=False)
            st.markdown("### ✅ Fact Verification Report")
            st.write(fact_report.content)
