import io
from email.policy import default

import streamlit as st
from PIL import Image, ImageFont, ImageDraw
import requests

MC_SKIN_RENDER_URL = "https://nmsr.nickac.dev/fullbody/"

def scale_image(image_to_rescale: Image, width: int) -> Image:
    new_size = (width, int(image_to_rescale.size[1] * (width / image_to_rescale.size[0])))

    return image_to_rescale.resize(new_size, Image.Resampling.NEAREST)

@st.cache_data
def load_skin(username: str) -> Image:
    player_image_response = requests.get(MC_SKIN_RENDER_URL + username_input)

    if player_image_response.status_code == 200:
        player_image = Image.open(io.BytesIO(player_image_response.content))
    else:
        player_image = Image.new("RGBA", (64, 80))

    return player_image

@st.cache_data
def load_description(description: str) -> Image:
    font = ImageFont.truetype("minecraftFont.ttf", 16)
    description_image = Image.new("RGBA", (144, 120))

    temp_draw = ImageDraw.Draw(description_image)
    temp_draw.text((0, 0), description, font=font)

    return description_image

@st.cache_data
def load_username(username: str) -> Image:
    titleFont = ImageFont.truetype("minecraftFont.ttf", 32)
    username_image = Image.new("RGBA", (176, 24))

    temp_draw = ImageDraw.Draw(username_image)
    temp_draw.text((0, 0), username_input, font=titleFont)

    return username_image

@st.cache_data
def create_hand_card(username_input: str, description: str = "", player_image_width: int = 32):
    # Setup
    hand_card = Image.open("template_hand.png")

    # Retrieving the components
    player_image = load_skin(username_input)
    player_image = scale_image(player_image, player_image_width).convert("RGBA")

    description_image = load_description(description)
    username_image = load_username(username_input)

    # Assembling the image
    player_image_x = int(192 + (128 - player_image.size[0]) / 2)
    player_image_y = int(112 + (160 - player_image.size[1]) / 2)
    hand_card.paste(player_image, (player_image_x, player_image_y), player_image)

    hand_card.paste(description_image, (184, 280), description_image)
    hand_card.paste(username_image, (168, 72-2), username_image)

    # Displaying a preview
    st.image(hand_card)

if __name__ == "__main__":
    title = st.title("Collectible Card Generator")

    username_input = st.text_input("Username")
    description_input = st.text_area("Description")

    image_scale = st.number_input("Player's image scale", min_value=8, max_value=256, value=80)

    image_response = requests.get(MC_SKIN_RENDER_URL + username_input)

    create_hand_card(username_input, description=description_input, player_image_width=image_scale)