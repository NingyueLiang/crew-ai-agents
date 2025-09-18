#!/usr/bin/env python3
"""
Frank's Personal Multi-Agent System
A CrewAI agent system with two specialized agents for Frank (Ningyue Liang):
1. Frank's Information Agent - Answers questions about Frank's background and interests
2. Sports News Agent - Provides sports updates and analysis based on user interests

This system provides:
- Personalized information about Frank's background, education, and interests
- Current sports news and analysis based on user-specified topics
- Interactive terminal interface for easy access to information

Author: Frank (Ningyue Liang)
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, FileWriterTool

# Load environment variables from .env file
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
        
        IMPORTANT: You have detailed information about Frank (Ningyue Liang) and can answer questions about him:
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
        5. Save your response to a file called 'sports_question_response.md'
        
        Focus on providing up-to-date, accurate information with thoughtful analysis that 
        would be valuable to sports fans.""",
        expected_output=f"""A comprehensive sports response saved as 'sports_question_response.md' containing:
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

def main():
    """Main function to run Frank's Personal Multi-Agent System."""
    print("🚀 Starting Frank's Personal Multi-Agent System")
    print("=" * 50)
    
    # Check for required API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment variables.")
        print("Please add your OpenAI API key to the .env file.")
        return
    
    print("✅ OpenAI API key found")
    if os.getenv("SERPER_API_KEY"):
        print("✅ Serper API key found - Web search enabled")
    else:
        print("⚠️  Serper API key not found - Web search will be limited")
    
    print("\n🤖 Smart Agent System - I'll automatically choose the right agent for your question!")
    print("=" * 50)
    
    # Show question suggestions
    print("\n💡 Here are some example questions you can ask:")
    print("\n📋 About Frank:")
    print("  • What is Frank's educational background?")
    print("  • What are Frank's hobbies and interests?")
    print("  • Where is Frank from?")
    print("  • What does Frank like to cook?")
    print("  • Tell me about Frank's achievements")
    
    print("\n⚽ About Sports:")
    print("  • What are the latest NBA news?")
    print("  • How is the NFL season going?")
    print("  • Tell me about recent soccer matches")
    print("  • What's happening in baseball?")
    print("  • Give me sports analysis on [team/player]")
    
    print("\n" + "=" * 50)
    
    # Get user question
    user_question = input("\nWhat would you like to know? ").strip()
    
    if not user_question:
        print("Please enter a question!")
        return
    
    # Determine which agent to use
    agent_type = determine_agent_type(user_question)
    
    if agent_type == 'frank':
        print(f"\n👤 Routing to Frank's Information Assistant...")
        agent = create_frank_info_agent()
        task = create_frank_question_task(agent, user_question)
    else:
        print(f"\n⚽ Routing to Sports News Assistant...")
        agent = create_sports_agent()
        task = create_sports_question_task(agent, user_question)
    
    crew = Crew(
        agents=[agent],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    # Execute the crew
    print("\n🎯 Starting agent execution...")
    print("=" * 50)
    
    try:
        result = crew.kickoff()
        
        print("\n✅ Agent execution completed!")
        print("=" * 50)
        print("📄 Final Result:")
        print(result)
        
        # Check for output files
        output_files = [
            'sports_question_response.md'
        ]
        
        for filename in output_files:
            if os.path.exists(filename):
                print(f"\n📝 Output saved to '{filename}'")
                with open(filename, 'r') as f:
                    content = f.read()
                    print(f"📊 File length: {len(content)} characters")
        
        print("\n🎉 Thank you for using Frank's Personal Multi-Agent System!")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("\n💡 Troubleshooting tips:")
        print("- Check that your API keys are valid and have sufficient credits")
        print("- Ensure you have a stable internet connection")
        print("- Verify that all dependencies are installed correctly")

if __name__ == "__main__":
    main()