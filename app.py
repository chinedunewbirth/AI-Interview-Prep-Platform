import streamlit as st
import openai
import json
import time
import pandas as pd
import plotly.express as px
from datetime import datetime
import random
import os
from typing import Dict, List, Tuple

# Set page configuration
st.set_page_config(
    page_title="AI Interview Prep Platform",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state variables
if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "interview_started" not in st.session_state:
    st.session_state.interview_started = False
if "current_question" not in st.session_state:
    st.session_state.current_question = ""
if "question_count" not in st.session_state:
    st.session_state.question_count = 0
if "feedback" not in st.session_state:
    st.session_state.feedback = []
if "interview_type" not in st.session_state:
    st.session_state.interview_type = "Behavioral"
if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Medium"

# Mock API key for demonstration (in production, use st.secrets or environment variables)
API_KEY_PLACEHOLDER = "your-api-key-here"

# Application title and description
st.title("💼 AI Interview Preparation Platform")
st.markdown("""
    <style>
    .main-header {font-size: 2.5rem; color: #1E3A8A; margin-bottom: 1rem;}
    .sub-header {font-size: 1.5rem; color: #374151; margin-bottom: 1rem;}
    .highlight {background-color: #F3F4F6; padding: 1rem; border-radius: 0.5rem;}
    </style>
""", unsafe_allow_html=True)

# Sidebar for configuration
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1256/1256650.png", width=100)
    st.title("Interview Settings")
    
    # API key input
    api_key = st.text_input("OpenAI API Key", type="password", value=API_KEY_PLACEHOLDER)
    
    # Interview type selection
    interview_type = st.selectbox(
        "Interview Type",
        ["Behavioral", "Technical", "System Design", "Leadership", "Mock Interview"],
        index=0
    )
    st.session_state.interview_type = interview_type
    
    # Difficulty level
    difficulty = st.select_slider(
        "Difficulty Level",
        options=["Easy", "Medium", "Hard", "Expert"],
        value="Medium"
    )
    st.session_state.difficulty = difficulty
    
    # Job role
    job_role = st.selectbox(
        "Target Job Role",
        ["Software Engineer", "Data Scientist", "Product Manager", "UX Designer", 
         "Business Analyst", "DevOps Engineer", "Full Stack Developer", "Other"]
    )
    
    # Experience level
    experience = st.selectbox(
        "Experience Level",
        ["Entry Level", "Mid Level", "Senior", "Executive"]
    )
    
    # Number of questions
    num_questions = st.slider("Number of Questions", 1, 15, 5)
    
    # Start/Reset buttons
    col1, col2 = st.columns(2)
    with col1:
        start_interview = st.button("Start Interview", type="primary", use_container_width=True)
    with col2:
        reset_interview = st.button("Reset", use_container_width=True)
    
    if reset_interview:
        st.session_state.conversation = []
        st.session_state.interview_started = False
        st.session_state.current_question = ""
        st.session_state.question_count = 0
        st.session_state.feedback = []
        st.rerun()
    
    # Resources section
    st.divider()
    st.markdown("### 📚 Resources")
    st.markdown("""
    - [Common Interview Questions](https://example.com)
    - [Technical Interview Guide](https://example.com)
    - [Behavioral Interview Tips](https://example.com)
    """)
    
    # About section
    st.divider()
    st.markdown("### About This Platform")
    st.markdown("""
    This AI Interview Prep Platform helps you practice for interviews
    with realistic questions and instant feedback. 
    
    **Features:**
    - Multiple interview types
    - Difficulty customization
    - Performance analytics
    - Real-time feedback
    """)

# Mock function for generating questions (in production, replace with actual OpenAI API call)
def generate_question(interview_type, difficulty, job_role, experience):
    """Generate an interview question based on parameters"""
    
    # Question banks for different interview types
    behavioral_questions = [
        "Tell me about a time you faced a significant challenge at work and how you handled it.",
        "Describe a situation where you had to work with a difficult team member.",
        "Give an example of a goal you didn't meet and how you handled it.",
        "Tell me about a time you showed leadership skills.",
        "Describe a situation where you had to make a decision with incomplete information."
    ]
    
    technical_questions = {
        "Software Engineer": [
            "Explain the concept of polymorphism in object-oriented programming.",
            "How would you design a URL shortening service like bit.ly?",
            "What's the difference between SQL and NoSQL databases?",
            "Explain how HTTP/2 improves upon HTTP/1.1.",
            "Describe how a hash table works and its time complexity."
        ],
        "Data Scientist": [
            "Explain the bias-variance tradeoff in machine learning.",
            "How would you handle missing data in a dataset?",
            "What's the difference between L1 and L2 regularization?",
            "Describe how a random forest algorithm works.",
            "Explain what cross-validation is and why it's important."
        ],
        "Product Manager": [
            "How would you prioritize features for a new product?",
            "Describe how you would conduct user research for a new feature.",
            "How do you measure the success of a product feature?",
            "Explain the difference between OKRs and KPIs.",
            "How would you handle a situation where engineering says a feature will take twice as long as expected?"
        ]
    }
    
    # Select question based on interview type
    if interview_type == "Behavioral":
        questions = behavioral_questions
    elif interview_type == "Technical":
        # Default to Software Engineer questions if job role not in dict
        questions = technical_questions.get(job_role, technical_questions["Software Engineer"])
    elif interview_type == "System Design":
        questions = [
            "Design a ride-sharing service like Uber or Lyft.",
            "How would you design Twitter's feed system?",
            "Design a global video streaming platform like Netflix.",
            "How would you architect a real-time collaborative document editor like Google Docs?",
            "Design a distributed key-value store."
        ]
    elif interview_type == "Leadership":
        questions = [
            "How do you motivate a team that's facing repeated setbacks?",
            "Describe your approach to conflict resolution between team members.",
            "How do you balance innovation with maintaining existing systems?",
            "Describe your strategy for managing remote or distributed teams.",
            "How do you measure and improve team productivity?"
        ]
    else:  # Mock Interview - mix of questions
        questions = behavioral_questions + technical_questions.get(job_role, [])
    
    # Select a random question
    question = random.choice(questions)
    
    # Adjust question difficulty by adding complexity
    if difficulty == "Hard":
        question += " Provide specific examples and metrics if possible."
    elif difficulty == "Expert":
        question += " Discuss edge cases and alternative approaches."
    
    return question

# Mock function for evaluating answers (in production, replace with actual OpenAI API call)
def evaluate_answer(question, answer, interview_type, difficulty):
    """Evaluate the user's answer and provide feedback"""
    
    # Simulate API call delay
    time.sleep(1)
    
    # Generate mock feedback based on answer length and content
    answer_length = len(answer)
    
    if answer_length < 50:
        rating = 2
        feedback = "Your answer is quite brief. Try to expand with specific examples and details."
        suggestions = ["Provide a specific example", "Explain the impact of your actions", "Mention what you learned"]
    elif answer_length < 150:
        rating = 3
        feedback = "Good start, but could use more detail and structure."
        suggestions = ["Use the STAR method (Situation, Task, Action, Result)", "Add quantifiable results", "Explain your thought process"]
    else:
        rating = 4
        feedback = "Well-structured answer with good detail."
        suggestions = ["Consider mentioning alternative approaches", "Tie back to the job requirements", "Highlight transferable skills"]
    
    # Adjust based on difficulty
    if difficulty == "Expert" and rating > 3:
        rating = min(4, rating - 0.5)
        feedback += " For expert level, consider discussing more nuanced aspects."
    
    # Add interview-type specific feedback
    if interview_type == "Technical":
        feedback += " For technical roles, ensure you're precise with terminology."
    elif interview_type == "Behavioral":
        feedback += " Remember to focus on your specific role and actions."
    
    # Generate sample answer
    sample_answers = {
        "Behavioral": "In my previous role as a project lead, I faced a challenge when our main database went down during peak hours. I quickly assembled the team, delegated tasks based on expertise, implemented a temporary solution to restore partial functionality, and communicated transparently with stakeholders about the timeline for full restoration. This resulted in 80% service restoration within 2 hours and taught me the importance of having a disaster recovery plan.",
        "Technical": "Polymorphism in object-oriented programming allows objects of different classes to be treated as objects of a common superclass. There are two main types: compile-time polymorphism (method overloading) and runtime polymorphism (method overriding). This enables writing more flexible and reusable code. For example, a 'Shape' superclass can have a 'calculateArea()' method that is implemented differently by 'Circle' and 'Rectangle' subclasses, but code can work with any 'Shape' object without knowing its specific type.",
        "System Design": "When designing Twitter's feed system, I'd consider: 1) Two types of feeds: home timeline (mixed from followed accounts) and user timeline (single user's tweets). 2) For the home timeline, use a fan-out approach where tweets are pushed to followers' caches when published. 3) Implement caching with Redis or Memcached for fast retrieval. 4) Use a message queue like Kafka for asynchronous processing. 5) Database sharding for user data. 6) Consider hybrid approach for celebrity users with many followers to avoid overloading the system."
    }
    
    sample_answer = sample_answers.get(interview_type, "A good answer would include specific examples, clear structure, and relevance to the question asked.")
    
    return {
        "rating": rating,
        "feedback": feedback,
        "suggestions": suggestions,
        "sample_answer": sample_answer
    }

# Performance tracking function
def track_performance(feedback_data):
    """Track and visualize user performance"""
    if not feedback_data:
        return None
    
    df = pd.DataFrame(feedback_data)
    
    # Calculate average rating
    avg_rating = df['rating'].mean()
    
    # Calculate improvement over time
    df['question_number'] = range(1, len(df) + 1)
    
    return df, avg_rating

# Main application logic
def main():
    # Header with current settings
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Interview Type", st.session_state.interview_type)
    with col2:
        st.metric("Difficulty", st.session_state.difficulty)
    with col3:
        st.metric("Questions Asked", st.session_state.question_count)
    
    # Initialize interview if start button is pressed
    if start_interview and not st.session_state.interview_started:
        st.session_state.interview_started = True
        st.session_state.question_count = 0
        st.session_state.conversation = []
        st.session_state.feedback = []
        
        # Generate first question
        question = generate_question(
            st.session_state.interview_type,
            st.session_state.difficulty,
            job_role,
            experience
        )
        st.session_state.current_question = question
        st.session_state.conversation.append(("AI", question))
        st.session_state.question_count += 1
        st.rerun()
    
    # Main interview area
    if st.session_state.interview_started:
        st.divider()
        st.markdown(f"### 🎯 Question {st.session_state.question_count} of {num_questions}")
        
        # Display current question
        st.info(f"**Question:** {st.session_state.current_question}")
        
        # User answer input
        user_answer = st.text_area(
            "Your Answer:",
            height=150,
            placeholder="Type your answer here...",
            key=f"answer_{st.session_state.question_count}"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            submit_answer = st.button("Submit Answer", type="primary", use_container_width=True)
        with col2:
            next_question = st.button("Skip Question", use_container_width=True)
        
        # Process answer submission
        if submit_answer and user_answer:
            # Add user answer to conversation
            st.session_state.conversation.append(("User", user_answer))
            
            # Evaluate answer
            with st.spinner("Analyzing your answer..."):
                evaluation = evaluate_answer(
                    st.session_state.current_question,
                    user_answer,
                    st.session_state.interview_type,
                    st.session_state.difficulty
                )
            
            # Store feedback
            feedback_entry = {
                "question": st.session_state.current_question,
                "answer": user_answer,
                "rating": evaluation["rating"],
                "feedback": evaluation["feedback"],
                "suggestions": evaluation["suggestions"],
                "sample_answer": evaluation["sample_answer"],
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }
            st.session_state.feedback.append(feedback_entry)
            
            # Display feedback
            st.divider()
            st.markdown("### 📊 Feedback")
            
            # Rating visualization
            rating_col1, rating_col2, rating_col3 = st.columns([1, 2, 1])
            with rating_col2:
                rating_value = evaluation["rating"]
                st.markdown(f"#### Rating: **{rating_value:.1f}/5**")
                st.progress(rating_value/5)
            
            # Detailed feedback
            st.markdown(f"**Analysis:** {evaluation['feedback']}")
            
            # Suggestions
            st.markdown("**Suggestions for improvement:**")
            for suggestion in evaluation["suggestions"]:
                st.markdown(f"- {suggestion}")
            
            # Sample answer (collapsible)
            with st.expander("View sample answer"):
                st.markdown(evaluation["sample_answer"])
        
        # Process next question
        if next_question or (submit_answer and user_answer):
            if st.session_state.question_count < num_questions:
                # Generate next question
                question = generate_question(
                    st.session_state.interview_type,
                    st.session_state.difficulty,
                    job_role,
                    experience
                )
                st.session_state.current_question = question
                st.session_state.conversation.append(("AI", question))
                st.session_state.question_count += 1
                st.rerun()
            else:
                # Interview completed
                st.session_state.interview_started = False
                st.balloons()
                st.success("🎉 Interview completed! Check your performance in the Analytics tab.")
                st.rerun()
    
    else:
        # Welcome screen when interview hasn't started
        st.divider()
        st.markdown("""
        ## Welcome to AI Interview Prep!
        
        This platform helps you practice for job interviews with AI-powered feedback.
        
        **How it works:**
        1. Configure your interview settings in the sidebar
        2. Click 'Start Interview' to begin
        3. Answer questions as they appear
        4. Receive instant feedback on your responses
        5. Review your performance analytics
        
        **Available Features:**
        - Multiple interview types (Behavioral, Technical, System Design, etc.)
        - Adjustable difficulty levels
        - Real-time answer evaluation
        - Performance tracking and analytics
        - Sample answers for comparison
        
        Get started by setting your preferences in the sidebar and clicking 'Start Interview'!
        """)
        
        # Feature highlights
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            <div class='highlight'>
            <h4>🤖 AI-Powered Practice</h4>
            <p>Practice with realistic interview questions generated by AI</p>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div class='highlight'>
            <h4>📊 Instant Feedback</h4>
            <p>Get detailed feedback on your answers immediately</p>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div class='highlight'>
            <h4>📈 Performance Analytics</h4>
            <p>Track your progress and identify areas for improvement</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Performance analytics tab (always visible when there's data)
    if st.session_state.feedback:
        st.divider()
        st.markdown("## 📈 Performance Analytics")
        
        # Calculate performance metrics
        df, avg_rating = track_performance(st.session_state.feedback)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Average Rating", f"{avg_rating:.1f}/5")
        with col2:
            st.metric("Questions Answered", len(st.session_state.feedback))
        with col3:
            completion_rate = (len(st.session_state.feedback) / num_questions) * 100
            st.metric("Completion", f"{completion_rate:.0f}%")
        
        # Create visualizations
        if len(st.session_state.feedback) > 1:
            tab1, tab2, tab3 = st.tabs(["Rating Progress", "Feedback Summary", "Conversation History"])
            
            with tab1:
                # Rating trend chart
                fig = px.line(df, x='question_number', y='rating', 
                              title='Rating Progress Over Questions',
                              markers=True)
                fig.update_layout(yaxis_range=[0, 5])
                st.plotly_chart(fig, use_container_width=True)
            
            with tab2:
                # Display all feedback
                for i, fb in enumerate(st.session_state.feedback):
                    with st.expander(f"Question {i+1}: {fb['question'][:50]}..."):
                        st.markdown(f"**Your Answer:** {fb['answer']}")
                        st.markdown(f"**Rating:** {fb['rating']}/5")
                        st.markdown(f"**Feedback:** {fb['feedback']}")
            
            with tab3:
                # Display conversation history
                st.markdown("### Conversation History")
                for speaker, text in st.session_state.conversation:
                    if speaker == "AI":
                        st.markdown(f"**🤖 Interviewer:** {text}")
                    else:
                        st.markdown(f"**👤 You:** {text}")
                    st.divider()
        
        # Download feedback option
        if st.session_state.feedback:
            st.download_button(
                label="Download Feedback Report",
                data=json.dumps(st.session_state.feedback, indent=2),
                file_name=f"interview_feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

# Run the main function
if __name__ == "__main__":
    main()