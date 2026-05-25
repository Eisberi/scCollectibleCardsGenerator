import io
import streamlit as st
from PIL import Image
import requests

MC_SKIN_RENDER_URL = "https://nmsr.nickac.dev/fullbody/"

def scale_image(image_to_rescale: Image, width: int) -> Image:
    new_size = (width, int(image_to_rescale.size[1] * (width / image_to_rescale.size[0])))

    return image_to_rescale.resize(new_size, Image.Resampling.NEAREST)

# ziel ist passende width -> factor der verkleinerung auf height anwenden

if __name__ == "__main__":
    title = st.title("Collectible Card Generator")

    username_input = st.text_input("Username")
    description_input = st.text_area("Description")

    image_scale = st.number_input("Image scale", min_value=8, max_value=256)

    image_response = requests.get(MC_SKIN_RENDER_URL + username_input)

    image = None
    if image_response.status_code == 200:
        image = Image.open(io.BytesIO(image_response.content))
        image = scale_image(image, image_scale)
    preview_image = scale_image(image, 256)
    st.image(image)
    st.image(preview_image)