#!/usr/bin/env python3
"""
Frank's Personal Multi-Agent System
A CrewAI agent system with two specialized agents for Frank:
1. Frank's Information Agent - Answers questions about Frank's background and interests
2. Sports News Agent - Provides sports updates and analysis based on user interests

This system provides:
- Personalized information about Frank's background, education, and interests
- Current sports news and analysis based on user-specified topics
- Interactive terminal interface for easy access to information

Author: Frank
"""

import os
from dotenv import load_dotenv
from nanda_adapter import NANDA
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileWriterTool

# Load env
load_dotenv()

def create_frank_info_agent():
    """
    Create Frank's Information Agent that can answer questions about Frank's background and interests.
    """
    return Agent(
        role="Frank's Personal Information Assistant",
        goal='To provide accurate and helpful information about Frank (Ningyue Liang) based on his background and interests',
        backstory="""You are Frank's personal information assistant with comprehensive knowledge about his background, 
        education, interests, and achievements. You excel at:
        - Answering questions about Frank's educational background and achievements
        - Providing information about his interests and hobbies
        - Sharing details about his professional journey and goals
        - Maintaining a friendly and informative tone
        
        IMPORTANT: You have detailed information about Frank and can answer questions about him:
        - Name: Ningyue Liang (Frank)
        - Education: M.E. candidate in CSE at Harvard University
        - Previous Education: Valedictorian graduate from Washington University in St. Louis with double majors in Computer Science and Statistics
        - Interests: Software engineering, machine learning, and AI
        - Experience: Industrial experience and academic achievements
        - Hobbies: Basketball, Ski, Baldur's Gate 3, League of Legends (LOL), Cooking
        - Hometown: Nanjing
        - Favorite Food: Duck noodles
        - LinkedIn: www.linkedin.com/in/ningyue-liang-frank
        
        You can provide information about Frank's background, achievements, interests, and professional journey.""",
        verbose=True,
        allow_delegation=False,
        tools=[FileWriterTool()]
    )

def create_sports_agent():
    """
    Create a Sports News Agent that provides current sports information based on user interests.
    """
    return Agent(
        role='Sports News Assistant',
        goal='To provide current sports news and analysis based on user-specified topics and interests',
        backstory="""You are a knowledgeable sports assistant with expertise across multiple sports and leagues. 
        You excel at:
        - Finding current sports news and updates using web search
        - Analyzing games, player performances, and team strategies
        - Providing insights about major sports leagues (NFL, NBA, MLB, Premier League, etc.)
        - Explaining sports concepts in an engaging and accessible way
        - Discussing sports trends and predictions
        
        Your personality is enthusiastic and informative, always eager to share the latest sports news 
        and insights. You make sports information accessible to both casual fans and serious enthusiasts.
        
        IMPORTANT: You have access to web search tools and should use them to find the most current 
        sports news and information. When users ask about specific sports topics, teams, players, 
        or events, you should search for the latest information and provide comprehensive, up-to-date 
        analysis based on current web sources.""",
        verbose=True,
        allow_delegation=False,
        tools=[SerperDevTool(), FileWriterTool()]
    )

def create_frank_question_task(agent, user_question):
    """Create a task for Frank's info agent to answer questions about Frank."""
    return Task(
        description=f"""Answer the following question about Frank (Ningyue Liang): "{user_question}"
        
        Your task is to:
        1. Provide accurate information about Frank based on his background
        2. Be friendly and informative in your response
        3. Include relevant details from Frank's profile when appropriate
        4. Maintain a helpful and engaging tone
        5. If the question is not about Frank, politely redirect to Frank-related topics
        
        Frank's Background Information:
        - Name: Ningyue Liang (Frank)
        - Education: M.E. candidate in CSE at Harvard University
        - Previous Education: Valedictorian graduate from Washington University in St. Louis with double majors in Computer Science and Statistics
        - Interests: Software engineering, machine learning, and AI
        - Experience: Industrial experience and academic achievements
        - Hobbies: Basketball, Ski, Baldur's Gate 3, League of Legends (LOL), Cooking
        - Hometown: Nanjing
        - Favorite Food: Duck noodles
        - LinkedIn: www.linkedin.com/in/ningyue-liang-frank""",
        expected_output=f"""A comprehensive and accurate answer to the question about Frank, including:
        - Direct response to the user's question
        - Relevant background information about Frank
        - Friendly and engaging tone
        - Helpful additional context when appropriate""",
        agent=agent
    )

def create_sports_question_task(agent, user_question):
    """Create a task for the sports agent to answer sports-related questions using web search."""
    return Task(
        description=f"""Answer the following sports-related question: "{user_question}"
        
        Your task is to:
        1. Use web search to find the most current and accurate information
        2. Provide comprehensive analysis and insights
        3. Include relevant statistics, news, or updates
        4. Present information in an engaging and accessible way
        5. Save your response to a file called 'response.md'
        
        Focus on providing up-to-date, accurate information with thoughtful analysis that 
        would be valuable to sports fans.""",
        expected_output=f"""A comprehensive sports response saved as 'response.md' containing:
        - Direct answer to the user's question
        - Current information from web search
        - Relevant statistics and insights
        - Engaging presentation of information
        - Proper formatting in Markdown""",
        agent=agent
    )

def determine_agent_type(question):
    """
    Determine which agent should handle the question based on keywords and context.
    Returns 'frank' for Frank-related questions, 'sports' for sports-related questions.
    """
    question_lower = question.lower()
    
    # Frank-related keywords
    frank_keywords = [
        'frank', 'ningyue', 'liang', 'harvard', 'washington university', 'valedictorian',
        'computer science', 'statistics', 'cse', 'master', 'engineering', 'education',
        'hobbies', 'basketball', 'ski', 'baldur', 'gate', 'league of legends', 'lol',
        'cooking', 'nanjing', 'duck noodles', 'linkedin', 'background', 'interests',
        'experience', 'achievements', 'hometown', 'favorite food'
    ]
    
    # Sports-related keywords
    sports_keywords = [
        'sports', 'basketball', 'football', 'soccer', 'baseball', 'tennis', 'nba', 'nfl',
        'mlb', 'premier league', 'championship', 'game', 'player', 'team', 'score',
        'match', 'tournament', 'league', 'season', 'playoff', 'draft', 'trade',
        'injury', 'news', 'update', 'analysis', 'statistics', 'stats', 'performance'
    ]
    
    # Count keyword matches
    frank_matches = sum(1 for keyword in frank_keywords if keyword in question_lower)
    sports_matches = sum(1 for keyword in sports_keywords if keyword in question_lower)
    
    # Special case: if question contains "basketball" but also Frank-related terms, prioritize Frank
    if 'basketball' in question_lower and any(keyword in question_lower for keyword in ['frank', 'ningyue', 'liang', 'hobby', 'hobbies']):
        return 'frank'
    
    # Return the agent with more keyword matches, default to Frank if tied
    if sports_matches > frank_matches:
        return 'sports'
    else:
        return 'frank'

def create_frank_multi_agent_service():
    """Create a callable that routes questions to the appropriate agent."""
    frank_agent = create_frank_info_agent()
    sports_agent = create_sports_agent()

    def frank_multi_agent(user_question: str) -> str:
        question = (user_question or "").strip()
        if not question:
            return "Please provide a question about Frank or sports."

        agent_type = determine_agent_type(question)

        if agent_type == 'frank':
            selected_agent = frank_agent
            task = create_frank_question_task(selected_agent, question)
        else:
            selected_agent = sports_agent
            task = create_sports_question_task(selected_agent, question)

        crew = Crew(
            agents=[selected_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )

        try:
            result = crew.kickoff()
            return str(result)
        except Exception as exc:
            return f"Agent execution failed: {exc}"

    return frank_multi_agent


nanda = NANDA(create_frank_multi_agent_service())
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
domain = os.getenv("DOMAIN_NAME")

if __name__ == "__main__":
    nanda.start_server_api(anthropic_key, domain)
