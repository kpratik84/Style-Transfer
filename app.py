import streamlit as st
from PIL import Image,ImageSequence

import numpy as np
from PIL import Image
from style_transfer.learn import StyleTransfer

from style_transfer.learn import StyleTransfer
from style_transfer.dissolve import create_dissolve
import imageio
import numpy as np
import glob
import cv2

#from post_processing import load_mask, mask_content
from scipy.misc import imread, imresize, imsave
import os
from io import BytesIO
import base64

def get_image_download_link(img):
	"""Generates a link allowing the PIL image to be downloaded
	in:  PIL image
	out: href string
	"""
	buffered = BytesIO()
	img.save(buffered, format="JPEG")
	img_str = base64.b64encode(buffered.getvalue()).decode()
	href = f'<a href="data:file/jpg;base64,{img_str}" download ="result.jpg">Download result</a>'
	return href


st.set_page_config(
    page_title="AI Style App",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.image('https://streamlit.io/images/brand/streamlit-mark-color.png', width=50)
st.title("MaskAI Style Transfer Demo")

Choose_Mask, Choose_Style = st.columns(2)
# %%
# enable the end user to upload a csv file:
#st.sidebar.write("_" * 30)
# >>>>>>>>>>>>>>>>
#st.sidebar.write("**Choose a Mask:**")

img = st.sidebar.selectbox(
  'Sample Masks',
  ('test33.jpg','mod.jpg')
)

style_name = st.sidebar.selectbox(
  'Sample Styles',
  ('exp3.jpg','exp6.jpg','exp9.jpg'),
)
#style_iter = st.sidebar.selectbox(
#  'Select_Iterations',
#  (100,200,300,400,500)
#)

input_image = "images/content_images/"+img
style_image = "images/style_images/"+style_name

output_image = "images/" + "artwork.jpg"

#Select_Image, Select_Style = st.columns(2)
#with Choose_Mask:
#  st.write("### Mask Image:")
#  image_ms = Image.open(input_image)
#  st.image(image_ms, width=300)

#with Choose_Style:
#  st.write("### Style Image:")
#  image_st = Image.open(style_image)
#  st.image(image_st, width=300)

st.sidebar.write("-" * 20 + "OR" + "-" * 20)

with Choose_Mask:
  st.write("### Mask Image:")
  #image_ms = Image.open(input_image)
  #st.image(image_ms, width=300)

  uploaded_mask = st.sidebar.file_uploader(
      label="Upload your own Mask or any Image:",
      type="jpg",
      accept_multiple_files=False,
      help='''Upload any Content Image
          ''')
  #if uploaded_file is not None:
  #    df = pd.read_csv(uploaded_file)

  if uploaded_mask is not None:
    image_ms = Image.open(uploaded_mask)
    #st.write("### Input Invoice:")
    #imsave("static/image_raw.jpg", image)
    #st.image(image, caption='Uploaded Mask.', width=500)
    #c_image = Image.open(image_ms)
    st.image(image_ms, width=300,caption='Mask Image')
  else:
    image_ms = Image.open(input_image)
    st.image(image_ms, width=300)

#st.sidebar.write("_" * 30)


with Choose_Style:
  st.write("### Style Image:")
  #image_st = Image.open(style_image)
  #st.image(image_st, width=300)
  uploaded_style = st.sidebar.file_uploader(
      label="Upload your own Style:",
      type="jpg",
      accept_multiple_files=False,
      help='''Upload any Style Image
          ''')
  #if uploaded_file is not None:
  #    df = pd.read_csv(uploaded_file)

  if uploaded_style is not None:
    image_st = Image.open(uploaded_style)
    #st.write("### Input Invoice:")
    #imsave("static/image_raw.jpg", image)
    #st.image(image, caption='Uploaded Mask.', width=500)
    #c_image = Image.open(image_ms)
    st.image(image_st, width=300,caption='Style Image')
  else:
    image_st = Image.open(style_image)
    st.image(image_st, width=300)

st.sidebar.write("_" * 30)

#model = "saved_models/" + style_name + ".pth"

clicked = st.button("Stylize")

style_transfer = StyleTransfer(style_weight = 1000, content_weight = 1)

if clicked:

  trans_images = [image_ms]
  for i in [0,10, 20, 30, 40, 50, 60 , 70 , 80, 90, 100, 150,300,500, 500, 500]:
    #artwork_int = self.postprocess(artwork)
    #artwork_int.save("/content/gdrive/MyDrive/Prism/prism/images/Interim_images/"  + str(i) +".jpg")
    trans_images.append("images/Interim_images/" + str(i) +".jpg")


  artwork = style_transfer(image_ms, image_st,iter = 500)
  #artwork.save("/content/gdrive/MyDrive/Prism/prism/images/output_images/" + img.replace(".jpg","") + "--" + style_name.replace(".jpg","") + ".jpg")

  st.write("### Stylized Image:")
  #image = Image.open("/content/gdrive/MyDrive/Prism/prism/images/output_images/" + img.replace(".jpg","") + "--" + style_name.replace(".jpg","") + ".jpg")
  st.image(artwork, width=500)

  artwork.save("artwork.png")

  #st.download_button(label="Download Image",data = artwork, file_name='df.csv',mime='text/csv')

  #st.image(img, caption=f"Image Predicted")
  #result = Image.fromarray(artwork)
  #st.markdown(get_image_download_link(artwork), unsafe_allow_html=True)
  with open("artwork.png","rb") as file:
    st.download_button(label="Download image",data=file,file_name="result.png",mime="image/png")


  ##### GIF ######

  #output_path = "/content/gdrive/MyDrive/Prism/prism/images/output_images/" + img.replace(".jpg","") + "--" + style_name.replace(".jpg","") + ".jpg"
  #images = []
  #filenames = [input_image, style_image,output_path]

  ## to include masked image in GIF ###
  #trans_images.append("/content/gdrive/MyDrive/Prism/prism/images/masked_output/masked.jpg")
  #trans_images.append("/content/gdrive/MyDrive/Prism/prism/images/masked_output/masked.jpg")
  #trans_images.append("/content/gdrive/MyDrive/Prism/prism/images/masked_output/masked.jpg")
  #trans_images.append("/content/gdrive/MyDrive/Prism/prism/images/masked_output/masked.jpg")

  #for filename in trans_images:
  #  img1 = imageio.imread(filename)
  #  img1 = Image.fromarray(img1).resize(artwork.size)
  #  images.append(np.array(img1))

  #imageio.mimsave('/content/gdrive/MyDrive/Prism/prism/result.gif', images, duration=0.35)
  #Image(open('/content/gdrive/MyDrive/Prism/prism/images/GIFs/movie.gif','rb').read())
  #st.write("### GIF:")
  #st.image('/content/gdrive/MyDrive/Prism/prism/result.gif')





#output_image = "images/output-images/"+ style_name+ "-" + img
