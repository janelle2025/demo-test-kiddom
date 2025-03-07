from dotenv import load_dotenv
import os
import anthropic
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Verify API key
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

def get_response(grade_level, learning_goals):
    """Send user input to the AI model and get a lesson summary using the Messages API."""
    client = anthropic.Anthropic(api_key=api_key)  # Pass the API key
    
    # Construct the prompt for generating a lesson summary from learning targets
    user_content = f"""
    ##CONTEXT##
    I am preparing a lesson plan and have a set of learning targets that outline what the lesson aims to cover. The targets are written for teachers, and I need a summary that encapsulates the essence of the lesson.

    ##OBJECTIVE##
    Please provide:
    Grade level: {grade_level}
    Learning targets:
    {learning_goals}
    Convert these into a concise summary that:
    - Clearly explains what the lesson is about
    - Highlights the key concepts and skills addressed
    - Is accessible to both teachers and students at the specified grade level
    - Uses clear, non-technical language while retaining essential educational terminology

    ##STYLE##
    Clear, concise, and engaging summary that captures the essence of the lesson

    ##TONE##
    Informative, straightforward, and motivating

    ##AUDIENCE##
    Teachers and students at the specified grade level

    ##FORMAT##
    A brief, well-structured summary of the lesson's main focus, key concepts, and skills.
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",  # Use a supported model
        system="You are a helpful assistant that summarizes learning targets into a clear lesson overview.",
        messages=[
            {"role": "user", "content": user_content}
        ],
        max_tokens=500,  # Increase token limit for detailed outputs
        stream=False  # Set to False unless streaming output is desired
    )
    # Extract and return the text content from the response
    return response.content[0].text

# Streamlit app UI
st.title("Lesson Summary Generator")
st.subheader("Generate a concise summary of your lesson based on learning targets.")

# Grade level dropdown
grade_level = st.selectbox(
    "Select a grade level:",
    [
        "Kindergarten", "Grade 1", "Grade 2", "Grade 3", "Grade 4", 
        "Grade 5", "Grade 6", "Grade 7", "Grade 8", 
        "Algebra 1", "Geometry", "Algebra 2"
    ]
)

# Text input for learning targets
learning_goals = st.text_area("Enter the learning targets for the lesson:")

# Generate response when the button is pressed
if st.button("Generate Summary"):
    if grade_level and learning_goals:
        with st.spinner("Generating lesson summary..."):
            try:
                response = get_response(grade_level, learning_goals)
                st.success("Lesson Summary Generated!")
                st.text_area("Lesson Summary", value=response, height=400)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please select a grade level and provide learning targets.")
