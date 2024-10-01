# import library
import os
import time
import streamlit as st
from openai import OpenAI

# my_secret = os.environ['OPENAI_API_KEY']
my_secret = st.secrets['OPENAI_API_KEY']
client = OpenAI(api_key=my_secret)


#story generator function
def story_gen(prompt):
  system_prompt = '''You are a world renowned 50 years experience children storyteller. 
  You will be given a concept to generate a short story suitable for ages 5-7 years old.
  '''
  response = client.chat.completions.create(model="gpt-4o-mini",
                                            messages=[{
                                                "role": "system",
                                                "content": system_prompt
                                            }, {
                                                "role": "user",
                                                "content": prompt
                                            }],
                                            temperature=1.3,
                                            max_tokens=350)

  return (response.choices[0].message.content)


# cover gen function
def cover_gen(prompt):
  system_prompt = """ 
  You will be given a children story book.
  Generate a prompt for a cover art that is suitable and shows off the story themes.
  The prompt will be sent to dall-e-2
  """
  response = client.chat.completions.create(model="gpt-4o-mini",
                                            messages=[{
                                                "role": "system",
                                                "content": system_prompt
                                            }, {
                                                "role": "user",
                                                "content": prompt
                                            }],
                                            temperature=1.3,
                                            max_tokens=350)

  return (response.choices[0].message.content)


# image generator function
def image_gen(prompt):
  response = client.images.generate(model="dall-e-2",
                                    prompt=prompt,
                                    size="256x256",
                                    n=1)

  return response.data[0].url


# main function
st.title('Storybook Generator For Children')
st.divider()

prompt = st.text_area('Enter your story concept:')

if st.button("Generate Storybook"):
  with st.spinner("Loading..."):
    time.sleep(5)
    story = story_gen(prompt)
    cover = cover_gen(prompt)
    image = image_gen(cover)

    st.image(image)
    st.write(story)
    st.balloons()
