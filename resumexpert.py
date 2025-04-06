from dotenv import load_dotenv

load_dotenv()

import streamlit as st
#to add extra space to our site in btw the elements
from streamlit_extras import add_vertical_space as avs
import os
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


#in this we are giving some text pdf image with aspecific promt
#to google gemini to get the response as text
def get_gemini_response(input,pdf_content,prompt):
    model=genai.GenerativeModel('gemini-1.5-flash')
    response=model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(upload_file):
    if upload_file is not None:
        # Convert PDF to images
        images = pdf2image.convert_from_bytes(upload_file.read())

        first_page = images[0]
        # Save the first page as a JPEG file

        #convert to bytes
        img_byte_arr=io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        # Return the image as a PIL Image object

        pdf_parts=[
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode() #encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("File not uploaded.")
    



##streamlit app

#page icon is the small image that is shown on the top of the page
st.set_page_config(page_title="ATS Resume Xpert", page_icon=":guardsman:", layout="wide")


#.stApp is the class that is used to add the css to our streamlit app 
#markdown are the synatx that is used to markdown any thing on the site
st.markdown(
    """
    <style>
    .stApp {
        background-color: #4a362f;
    }

    .stTextArea text_area {
        border-radius: 5px;
        padding: 10px;
        background-color: #f0f8ff; /* Light blue background */
        color: #000080; /* Navy text color */
        border: 2px solid #000080; /* Navy border *
    }
    .stFileUploader {
        background-color: #ffe4e1; /* Light pink background */
        border: 2px solid #ff4500; /* Orange border */
        border-radius: 10px; /* Rounded corners */
        padding: 10px;
    }
     
       div.stButton > button {
        background-color: #3b6141; /* Forest green background */
        color: white; /* White text */
        border: 2px solid #228b22; /* Forest green border */
        border-radius: 10px; /* Rounded corners */
        padding: 10px 20px; /* Padding for the button */
        font-size: 5px; /* Font size */
    }
     
     div.stButton > button:hover {
        background-color: #228b22; /* Darker green on hover */
        color: #ffffff; /* White text */
    }

    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<h1 style="text-align:center; color: white; font-family:Arial; font-size:40px;">RESUME Xpert</h1>', unsafe_allow_html=True)


st.markdown('<h4 style="text-align:center;color:red;font-family:Brush Script;">"Be Resume EXpert with KRISH"</h4>', unsafe_allow_html=True)

#avs is the function that is used to add the extra space to our site in btw the elements and
#avs is the streamlit_extras that are install using pip install streamlit-extras
avs.add_vertical_space(4)
input_text=st.text_area("Job Descrption:",key="input")


uploaded_file=st.file_uploader("Upload Your Resume:",type=["pdf"])

if uploaded_file is not None:
    st.write("PDF File is uploaded successfully")

#these are the two button that on clicking give the AI response
#one is for the resume analysis and other is for the match percentage
submit1=st.button("Tell Me About My Resume")
submit2=st.button("Find Out The Match Percentage")



st.warning("Please make sure to upload a PDF file.")




input_prompt1="""
   you are an heighly experienced HR professional with technical knowledge and experience in the 
   feild of any one job role from data science and machine learning,full stack development, and data engineering,
   DEVOPS, data analysis, and data visualization.
   your task has is to review the provided resume against the job description and provide a detailed analysis of the resume.
   please share your professional openion and evalution on wether the candidiate's profile aligns with the role,
   highlighting the strengths and weaknesses of the resume.
   please provide a detailed analysis of the resume, including the following points:
    1. overall impression of the resume
    2. strengths and weaknesses of the resume
    3. skills and experience that are relevant to the job description
    4. any gaps or areas for improvement in the resume
"""
input_prompt2="""
    you are an skilled ATS(Application tracking system ) scanner with a deep understanding of any one job role data science,
      machine learning,full stack development, data engineering,
      DEVOPS, data analysis, data visualization and deep ATS functionality,
      your task is to evaluate the resume against the provided job description.
      give me the percentage match of the resume with the job description.
      first give me the percentage match and then provide a detailed analysis of the resume,
      including the following points: 
      1. overall impression of the resume
      2. strengths and weaknesses of the resume"""


if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file.")

if submit2:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt2,pdf_content,input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("Please upload a PDF file.")


avs.add_vertical_space(3)
st.write("Bored! no worry we have some fun for you")
st.markdown(
    """
    <a href="p.html" target="_blank">
        ClickHere
    </a>
    """,
    unsafe_allow_html=True
)




#adding as slide bar
st.sidebar.title("About:")
st.sidebar.markdown(
    """
    This is a resume analyzer and resume feedback tool designed to help job seekers improve their resumes.
    The tool allows users to upload their resumes in PDF format and provides feedback based on the job description provided.
    The tool helps candidates improve their resumes and increase their chances of getting noticed by recruiters.
    """
)
with st.sidebar.form("sidebar_form"):
    st.write("PLEASE GIVE FEEDBACK")
    st.write("##Your feedback is important to us!##")

    # Add input widgets
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    feedback = st.text_area("Your Feedback")

    # Add a submit button
    submitted = st.form_submit_button("Submit FEEDBACK")

# Handle form submission
if submitted:
    if not  name or not email or not feedback:
        st.sidebar.error("Please fill in all fields.")
    else:
        st.sidebar.success("Thank you for your feedback!")
        st.write(f"Name: {name}")
        st.write(f"Email: {email}")
        st.write(f"Feedback: {feedback}")





# Add footer using HTML and CSS
#target is used to open the link in new tab
#this is the footer that is added to our site using the css and html code
st.markdown(
    """
    <style>
    footer {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #4a362f; /* Dark background */
        color: white; /* White text */
        text-align: center;
        padding: 10px;
        font-size: 14px;
        font-family: Arial, sans-serif;
    }
      footer a {
        color: lightblue; /* Link color */
        text-decoration: none; /* Remove underline */
    }
    footer a:hover {
    background-color: #4a362f;
        color: lightblue; /* Link color on hover */
        text-decoration: underline; /* Underline on hover */
    }
    </style>
    <footer>
        <p>© 2025 ATS Resume Xpert | Developed by Krish Mishra | 
        <a href="https://github.com/krishmishra09" target="_blank">GitHub</a></p>
    </footer>
    """,
    unsafe_allow_html=True
)