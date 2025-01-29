import streamlit as st
from phi.agent import Agent
from phi.tools.dalle import Dalle
from phi.model.openai import OpenAIChat
import os
from dotenv import load_dotenv
from typing import Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_bg_from_url():
    """Add a background and custom styling."""
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(45deg, #0f2027, #203a43, #2c5364);
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
        }}
        
        @keyframes gradient {{
            0% {{
                background-position: 0% 50%;
            }}
            50% {{
                background-position: 100% 50%;
            }}
            100% {{
                background-position: 0% 50%;
            }}
        }}
        
        .big-font {{
            font-size: 24px !important;
            font-weight: bold;
        }}
        .medium-font {{
            font-size: 18px !important;
        }}
        .stButton>button {{
            background: linear-gradient(45deg, #3498db, #2980b9);
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: bold;
            border: none;
            transition: all 0.3s ease;
        }}
        .stButton>button:hover {{
            background: linear-gradient(45deg, #2980b9, #3498db);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }}
        .stTextArea>div>div>textarea {{
            background-color: rgba(255,255,255,0.95);
            border-radius: 10px;
            border: 2px solid #3498db;
        }}
        .custom-card {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(4px);
            border: 1px solid rgba(255, 255, 255, 0.18);
            margin: 10px 0;
        }}
        .title-text {{
            background: -webkit-linear-gradient(45deg, #3498db, #2980b9);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: bold;
        }}
        .stSpinner > div {{
            border-color: #3498db transparent transparent transparent;
        }}
        .stAlert {{
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def load_environment() -> None:
    """Load environment variables and set up API key."""
    try:
        load_dotenv()
        api_key = st.secrect['OPENAI_API_KEY']
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        os.environ['OPENAI_API_KEY'] = api_key
    except Exception as e:
        logger.error(f"Error loading environment: {str(e)}")
        st.error("Failed to load API key. Please check your .env file.")
        st.stop()

def create_image_agent() -> Agent:
    """Create and configure the image generation agent."""
    return Agent(
        model=OpenAIChat(id="gpt-4"),
        tools=[Dalle()],
        description="You are an AI agent that can generate images using DALL-E.",
        instructions="""
        When the user asks you to create an image:
        1. Analyze the prompt for clarity and completeness
        2. Use the `create_image` tool to generate the image
        3. Provide feedback about the generation process
        """,
        markdown=True,
        show_tool_calls=True,
    )

def generate_image(agent: Agent, prompt: str) -> Optional[List]:
    """Generate image using the provided agent and prompt."""
    try:
        agent.print_response(f"Generate an image of {prompt}")
        images = agent.get_images()
        if not images or not isinstance(images, list):
            raise ValueError("No images generated")
        return images
    except Exception as e:
        logger.error(f"Error generating image: {str(e)}")
        return None

def main():
    st.set_page_config(
        page_title="Dream Canvas",
        page_icon="✨",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Add custom background and styles
    add_bg_from_url()

    # Custom title with styling
    st.markdown("""
        <div style='text-align: center; padding: 20px;'>
            <h1 style='font-size: 3em; margin-bottom: 10px;' class='title-text'>
                ✨ Dream Canvas
            </h1>
            <p style='color: white; font-size: 1.2em; margin-bottom: 30px;'>
                Where Imagination Becomes Reality
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Load environment variables
    load_environment()

    # Create the image agent
    image_agent = create_image_agent()

    # Create two columns for layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
            <div class='custom-card'>
            <p class='big-font' style='color: #3498db;'>Create Your Masterpiece</p>
            </div>
        """, unsafe_allow_html=True)
        
        prompt = st.text_area(
            "Enter your image prompt:",
            height=100,
            placeholder="Describe your dream image here..."
        )

        if st.button("🎨 Create Magic", use_container_width=True):
            if not prompt:
                st.warning("✨ Please share your vision before we begin...")
                return

            with st.spinner("🎨 Bringing your dreams to life..."):
                images = generate_image(image_agent, prompt)
                
                if images:
                    st.success("✨ Your masterpiece is ready!")
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    for image_response in images:
                        st.image(
                            image_response.url,
                            caption=prompt,
                            use_column_width=True
                        )
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error("💫 Let's try a different approach. Adjust your prompt and try again.")

    with col2:
        st.markdown("""
            <div class='custom-card'>
            <p class='big-font' style='color: #3498db;'>✨ Inspiration Guide</p>
            <p class='medium-font'><strong>Creative Tips:</strong></p>
            <ul class='medium-font'>
                <li>Paint with words - be vivid and descriptive</li>
                <li>Set the mood with lighting and atmosphere</li>
                <li>Choose an artistic style</li>
                <li>Include color preferences</li>
            </ul>
            <p class='medium-font'><strong>✨ Magical Examples:</strong></p>
            <ul class='medium-font'>
                <li>"An ethereal floating city among iridescent clouds at sunset, digital art"</li>
                <li>"A magical library with floating books and glowing crystals, fantasy style"</li>
                <li>"A bioluminescent underwater garden with merfolk, ethereal lighting"</li>
            </ul>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()