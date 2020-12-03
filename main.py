import streamlit as st
from PIL import Image
import requests
from PIL import ImageDraw
import io
import os

st.title("Face recognition app")

# Hide key1 and endpoint
# to use this app for your envvronment, please get your own API key and endpoint.
# please check readme how to 
subscription_key =os.environ.get("streamlit_face_api_key1")
assert subscription_key
face_api_url =os.environ.get("streamlit_face_api_url")

upload_file = st.file_uploader("Choose an image(.JPG file type only!.. for now!)...", type="jpg")

if upload_file is not None:
    img = Image.open(upload_file)

    # change images to binary data 
    with io.BytesIO() as output:
        img.save(output,format="JPEG")
        binary_img = output.getvalue()
        
    # set api search details
    headers = {
        'Content-Type':'application/octet-stream', # send images instead of url
        'Ocp-Apim-Subscription-Key': subscription_key}
    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    res = requests.post(face_api_url, params=params,
                            headers=headers, data=binary_img)


    # 'faceRectangle' from "res" outcome means a face-location in the image.
    # "result" is list type. because the image might have a few pepople.
    # "result" returns all faces info
    # this example has only one face, so use result[0]
    # result save in json
    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        
        # define where we draw
        draw = ImageDraw.Draw(img)
        # show rectangle around face-location
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])] ,
                    fill=None,outline="blue",width=5)



    st.image(img,caption="Uploaded Image.", use_column_width=True)

