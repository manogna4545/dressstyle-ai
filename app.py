import streamlit as st
from PIL import Image
import requests
import json
import base64
import os
from pathlib import Path
from dotenv import load_dotenv
import fal_client

# ==================================================
# LOAD ENVIRONMENT VARIABLES
# ==================================================

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://localhost:11434/api/generate"
)

FAL_KEY = os.getenv("FAL_KEY", "")

WISHLIST_FILE = BASE_DIR / "wishlist.json"


# ==================================================
# PAGE CONFIG
# IMPORTANT: ONLY ONE set_page_config()
# ==================================================

st.set_page_config(
    page_title="DressStyle AI",
    page_icon="👗",
    layout="wide"
)


# ==================================================
# WISHLIST FUNCTIONS
# ==================================================

def load_wishlist():
    try:
        if WISHLIST_FILE.exists():
            with open(WISHLIST_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

                if isinstance(data, list):
                    return data

        return []

    except Exception:
        return []


def save_wishlist(wishlist):
    try:
        with open(WISHLIST_FILE, "w", encoding="utf-8") as file:
            json.dump(
                wishlist,
                file,
                indent=4,
                ensure_ascii=False
            )

    except Exception as e:
        st.error(f"Could not save wishlist: {e}")


# ==================================================
# OLLAMA CONNECTION CHECK
# ==================================================

def check_ollama():

    try:

        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=5
        )

        return response.status_code == 200

    except requests.exceptions.RequestException:
        return False


# ==================================================
# AI DRESS IMAGE ANALYSIS
# ==================================================

def analyze_dress_image(uploaded_file):

    image_bytes = uploaded_file.getvalue()

    image_base64 = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    prompt = """
You are an AI Fashion Assistant.

Analyze the uploaded dress or outfit image.

Give the answer using exactly these headings:

👗 Outfit Type

Describe the general type of outfit.

🎨 Main Colours

List the main visible colours.

🌸 Pattern and Design

Describe patterns, prints, or general design features.

✨ Style

Describe the general fashion style.

👜 Styling Suggestions

Give practical suggestions for accessories or combinations.

🔎 Search Keywords

Give useful keywords someone could use to search for similar clothing online.

Do not identify the person in the image.

Do not make negative judgments about someone's body or appearance.

Focus only on clothing and visible fashion features.
"""

    payload = {

        "model": "qwen2.5vl:3b",

        "prompt": prompt,

        "images": [image_base64],

        "stream": False

    }

    try:

        response = requests.post(

            OLLAMA_URL,

            json=payload,

            timeout=180

        )

        response.raise_for_status()

        data = response.json()

        return data.get(
            "response",
            "AI could not generate an analysis."
        )

    except requests.exceptions.ConnectionError:

        return """
⚠️ **Ollama is not running.**

Please start Ollama and make sure the required model is installed.

Run:

`ollama serve`

Then check:

`ollama list`
"""

    except requests.exceptions.Timeout:

        return """
⚠️ AI analysis took too long.

Please try again.
"""

    except Exception as e:

        return f"""
⚠️ AI analysis failed.

Error: {str(e)}
"""


# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown(
    """
<style>

/* ================= MAIN BACKGROUND ================= */

.stApp {

    background: linear-gradient(
        135deg,
        #f3edff,
        #e9e0ff
    );

}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {

    background: linear-gradient(
        180deg,
        #fff5fa,
        #f8e8f1
    );

    min-width: 260px !important;

}


section[data-testid="stSidebar"] > div {

    padding-top: 20px;

}


/* ================= SIDEBAR BRAND ================= */

.sidebar-brand {

    font-size: 26px;

    font-weight: 800;

    color: #6b3fa0;

    text-align: center;

    padding: 10px 5px 25px 5px;

}


/* ================= MAIN TITLE ================= */

.main-title {

    text-align: center;

    font-size: 55px;

    font-weight: bold;

    color: #6337b8;

}


/* ================= SUBTITLE ================= */

.subtitle {

    text-align: center;

    font-size: 20px;

    color: #655b75;

}


/* ================= FEATURE CARDS ================= */

.feature-card {

    background: rgba(255, 255, 255, 0.85);

    padding: 25px;

    border-radius: 18px;

    min-height: 140px;

    text-align: center;

    box-shadow:
        0px 6px 20px
        rgba(90, 60, 150, 0.15);

    transition: all 0.3s ease;

}


.feature-card:hover {

    transform: translateY(-5px);

}


.feature-card h2 {

    color: #6b3fa0;

    font-size: 24px;

}


.feature-card p {

    color: #666666;

    font-size: 15px;

}

</style>
""",
    unsafe_allow_html=True
)


# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.markdown(
    '<div class="sidebar-brand">👗 DressStyle AI</div>',
    unsafe_allow_html=True
)


if "page" not in st.session_state:

    st.session_state.page = "🏠 Home"


if st.sidebar.button(
    "🏠 Home",
    use_container_width=True
):

    st.session_state.page = "🏠 Home"


if st.sidebar.button(
    "✨ AI Stylist",
    use_container_width=True
):

    st.session_state.page = "✨ AI Stylist"


if st.sidebar.button(
    "📸 Virtual Try-On",
    use_container_width=True
):

    st.session_state.page = "📸 Virtual Try-On"


if st.sidebar.button(
    "🔍 Dress Search",
    use_container_width=True
):

    st.session_state.page = "🔍 Dress Search"


if st.sidebar.button(
    "💰 Price Comparison",
    use_container_width=True
):

    st.session_state.page = "💰 Price Comparison"


if st.sidebar.button(
    "🔥 Best Deals",
    use_container_width=True
):

    st.session_state.page = "🔥 Best Deals"


if st.sidebar.button(
    "❤️ Wishlist",
    use_container_width=True
):

    st.session_state.page = "❤️ Wishlist"


page = st.session_state.page


# ==================================================
# HOME PAGE
# ==================================================

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">👗 DressStyle AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Find Your Perfect Style Before You Buy ✨'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            """
<div class="feature-card">

<h2>✨ AI Fashion Stylist</h2>

<p>
Get personalized dress recommendations
based on your style, occasion and budget.
</p>

</div>
""",
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            """
<div class="feature-card">

<h2>📸 Virtual Try-On</h2>

<p>
Upload your photo and a dress image
for AI-powered try-on.
</p>

</div>
""",
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            """
<div class="feature-card">

<h2>💰 Compare Prices</h2>

<p>
Search dresses and compare shopping
options within your budget.
</p>

</div>
""",
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.header("✨ What can DressStyle AI do?")

    st.write("""
👗 **Discover fashion styles** based on your preferences

🎨 **Explore colour and outfit ideas**

📸 **Upload a dress image** for AI fashion analysis

🤖 **Get AI fashion suggestions**

💰 **Find dresses within your budget**

❤️ **Save favourite dresses in your wishlist**
""")


# ==================================================
# AI STYLIST
# ==================================================

elif page == "✨ AI Stylist":

    st.title("✨ Find My Perfect Dress")

    st.write(
        "Tell DressStyle AI about your occasion, "
        "colour, style, dress type and budget."
    )

    occasion = st.selectbox(
        "🎉 What is the occasion?",
        [
            "Casual",
            "College",
            "Office",
            "Party",
            "Wedding",
            "Traditional",
            "Vacation",
            "Date"
        ]
    )

    colour = st.text_input(
        "🎨 Preferred Colour",
        placeholder="Example: Pink, Black, Blue"
    )

    style_preference = st.selectbox(
        "✨ Preferred Style",
        [
            "Elegant",
            "Trendy",
            "Simple",
            "Traditional",
            "Modern",
            "Casual",
            "Party Wear"
        ]
    )

    dress_type = st.selectbox(
        "👗 Preferred Dress Type",
        [
            "Any",
            "Midi Dress",
            "Maxi Dress",
            "Mini Dress",
            "Kurti",
            "Saree",
            "Lehenga",
            "Top and Skirt",
            "Jumpsuit"
        ]
    )

    budget = st.selectbox(
        "💰 Maximum Budget",
        [
            "Under ₹200",
            "Under ₹500",
            "Under ₹900",
            "Under ₹1000",
            "Under ₹1500",
            "Under ₹2000"
        ]
    )


    if st.button(
        "✨ Find My Perfect Dress",
        use_container_width=True
    ):

        if not colour.strip():

            st.warning(
                "Please enter your preferred colour."
            )

        elif not check_ollama():

            st.error(
                "⚠️ Ollama is not running. "
                "Please start Ollama first."
            )

        else:

            with st.spinner(
                "🤖 DressStyle AI is creating your recommendation..."
            ):

                try:

                    recommendation_prompt = f"""
You are DressStyle AI, a helpful personal fashion assistant.

Create a personalized dress-shopping recommendation.

User preferences:

Occasion: {occasion}

Preferred Colour: {colour}

Preferred Style: {style_preference}

Preferred Dress Type: {dress_type}

Maximum Budget: {budget}

Give the response using exactly these sections:

👗 Recommended Dress

🎨 Colour Recommendation

✨ Why This Style

💎 Styling Ideas

🔎 Shopping Search Keywords

💰 Budget Strategy

🛍️ Shopping Checklist

Do not identify or judge the user's appearance.

Focus on clothing, colour, occasion,
comfort, style and shopping preferences.
"""

                    payload = {

                        "model": "qwen2.5:3b",

                        "prompt": recommendation_prompt,

                        "stream": False

                    }

                    response = requests.post(

                        OLLAMA_URL,

                        json=payload,

                        timeout=180

                    )

                    response.raise_for_status()

                    recommendation = response.json().get(
                        "response",
                        "No recommendation generated."
                    )

                    st.success(
                        "✨ Your Personalized Dress Recommendation"
                    )

                    st.markdown(recommendation)

                    st.markdown("---")

                    st.subheader(
                        "🛍️ Find Similar Dresses"
                    )

                    search_query = (
                        f"{colour} "
                        f"{style_preference} "
                        f"{dress_type} "
                        f"{occasion} dress"
                    )

                    search_url = (
                        "https://www.google.com/search?q="
                        + requests.utils.quote(search_query)
                    )

                    st.link_button(
                        "🛍️ Shop Similar Dresses",
                        search_url,
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )


# ==================================================
# VIRTUAL TRY-ON
# ==================================================

elif page == "📸 Virtual Try-On":

    st.title("📸 AI Virtual Try-On")

    st.write(
        "Upload your photo and a dress photo to create "
        "an AI-powered virtual try-on."
    )

    col1, col2 = st.columns(2)

    with col1:

        user_photo = st.file_uploader(
            "👤 Upload Your Photo",
            type=["jpg", "jpeg", "png"],
            key="tryon_user_photo"
        )

        if user_photo:

            st.image(
                user_photo,
                caption="Your Photo",
                use_container_width=True
            )

    with col2:

        dress_photo = st.file_uploader(
            "👗 Upload Dress Photo",
            type=["jpg", "jpeg", "png"],
            key="tryon_dress_photo"
        )

        if dress_photo:

            st.image(
                dress_photo,
                caption="Dress Photo",
                use_container_width=True
            )

    if st.button(
        "✨ Generate Virtual Try-On",
        use_container_width=True
    ):

        if not user_photo or not dress_photo:

            st.warning(
                "Please upload both your photo and the dress photo."
            )

        elif not FAL_KEY:

            st.error(
                "⚠️ FAL API key is not configured."
            )

            st.info(
                "Please add FAL_KEY to your .env file."
            )

        else:

            with st.spinner(
                "🤖 Creating your virtual try-on image... Please wait."
            ):

                try:

                    # Save uploaded images temporarily
                    user_image_path = "temp_user_image.png"
                    dress_image_path = "temp_dress_image.png"

                    with open(user_image_path, "wb") as f:
                        f.write(user_photo.getbuffer())

                    with open(dress_image_path, "wb") as f:
                        f.write(dress_photo.getbuffer())

                    # Upload user image to fal.ai
                    user_image_url = fal_client.upload_file(
                        user_image_path
                    )

                    # Upload dress image to fal.ai
                    dress_image_url = fal_client.upload_file(
                        dress_image_path
                    )

                    # Run fal.ai Virtual Try-On model
                    result = fal_client.subscribe(
                        "fal-ai/image-apps-v2/virtual-try-on",
                        arguments={
                            "human_image_url": user_image_url,
                            "garment_image_url": dress_image_url
                        }
                    )

                    # Get generated image URL
                    result_image_url = result["image"]["url"]

                    st.success(
                        "✨ Virtual Try-On Complete!"
                    )

                    st.subheader(
                        "👗 Your Virtual Try-On Result"
                    )

                    st.image(
                        result_image_url,
                        use_container_width=True
                    )

                    st.link_button(
                        "🖼️ Open Result Image",
                        result_image_url,
                        use_container_width=True
                    )

                except Exception as e:

                    st.error(
                        f"Virtual Try-On Error: {e}"
                    )

                    st.info(
                        "Please check your FAL_KEY and "
                        "make sure your uploaded images are clear."
                    )

                finally:

                    # Remove temporary files
                    if os.path.exists("temp_user_image.png"):
                        os.remove("temp_user_image.png")

                    if os.path.exists("temp_dress_image.png"):
                        os.remove("temp_dress_image.png")
# ==================================================
# DRESS SEARCH
# ==================================================

elif page == "🔍 Dress Search":

    st.title("🔍 AI Dress Search")

    st.write(
        "Upload a dress or outfit image "
        "and let AI analyze its style!"
    )

    uploaded_dress = st.file_uploader(

        "📸 Upload a Dress Image",

        type=["jpg", "jpeg", "png"],

        key="dress_search_upload"

    )


    if uploaded_dress is not None:

        st.image(

            uploaded_dress,

            caption="Uploaded Dress",

            use_container_width=True

        )


        if st.button(
            "🤖 Analyze This Dress",
            use_container_width=True
        ):

            with st.spinner(
                "🤖 AI is analyzing the dress..."
            ):

                analysis = analyze_dress_image(
                    uploaded_dress
                )

                if analysis.startswith("⚠️"):

                    st.warning(analysis)

                else:

                    st.success(
                        "✨ AI Dress Analysis Complete!"
                    )

                    st.markdown(analysis)

    else:

        st.info(
            "📸 Upload a dress image to start AI analysis."
        )


# ==================================================
# PRICE COMPARISON
# ==================================================

elif page == "💰 Price Comparison":

    st.title("💰 Compare Before You Buy")

    st.write(
        "Search for a dress and explore shopping options."
    )


    if "wishlist" not in st.session_state:

        st.session_state.wishlist = load_wishlist()


    if "products" not in st.session_state:

        st.session_state.products = []


    search = st.text_input(

        "🔍 Search for a dress",

        placeholder="Example: Pink floral midi dress"

    )


    budget = st.selectbox(

        "💰 Choose your budget",

        [

            "Any Price",

            "Under ₹500",

            "Under ₹900",

            "Under ₹1000",

            "Under ₹1500",

            "Under ₹2000"

        ]

    )


    if st.button(
        "🔎 Search Dresses",
        use_container_width=True
    ):

        if search.strip():

            products = [

                {

                    "name": f"{search} - Option 1",

                    "store": "Demo Store 1",

                    "price": 799,

                    "rating": 4.3,

                    "link": (
                        "https://www.google.com/search?q="
                        + requests.utils.quote(search)
                    )

                },

                {

                    "name": f"{search} - Option 2",

                    "store": "Demo Store 2",

                    "price": 999,

                    "rating": 4.5,

                    "link": (
                        "https://www.google.com/search?q="
                        + requests.utils.quote(search)
                    )

                },

                {

                    "name": f"{search} - Option 3",

                    "store": "Demo Store 3",

                    "price": 1499,

                    "rating": 4.2,

                    "link": (
                        "https://www.google.com/search?q="
                        + requests.utils.quote(search)
                    )

                }

            ]


            if budget != "Any Price":

                maximum_price = int(
                    budget.replace("Under ₹", "")
                )

                products = [

                    product

                    for product in products

                    if product["price"] < maximum_price

                ]


            st.session_state.products = products


        else:

            st.warning(
                "Please enter a dress name."
            )


    if st.session_state.products:

        st.success(
            f"Results for: {search}"
        )

        st.markdown(
            "### 👗 Available Options"
        )


        for index, product in enumerate(
            st.session_state.products
        ):

            st.markdown("---")

            st.subheader(
                f"👗 {product['name']}"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.write(
                    f"🏪 {product['store']}"
                )

            with col2:

                st.write(
                    f"💰 ₹{product['price']}"
                )

            with col3:

                st.write(
                    f"⭐ {product['rating']}"
                )


            button_col1, button_col2 = st.columns(2)


            with button_col1:

                st.link_button(

                    "🛍️ View Shopping Page",

                    product["link"],

                    use_container_width=True

                )


            with button_col2:

                if st.button(

                    "❤️ Add to Wishlist",

                    key=f"wishlist_product_{index}",

                    use_container_width=True

                ):

                    already_saved = any(

                        item["name"] == product["name"]

                        for item in st.session_state.wishlist

                    )


                    if not already_saved:

                        st.session_state.wishlist.append(

                            {

                                "name": product["name"],

                                "price": product["price"]

                            }

                        )

                        save_wishlist(
                            st.session_state.wishlist
                        )

                        st.success(
                            "❤️ Added to Wishlist!"
                        )

                    else:

                        st.info(
                            "❤️ This dress is already in your Wishlist."
                        )


    elif search.strip():

        st.warning(
            "No dresses found within this budget."
        )


    st.info(
        "⚠️ These are demonstration products and prices. "
        "They are not live retailer prices."
    )


# ==================================================
# BEST DEALS
# ==================================================

elif page == "🔥 Best Deals":

    st.title("🔥 Fashion Within Your Budget")

    st.write(
        "Find fashion options that match your budget."
    )


    budget = st.selectbox(

        "💰 Choose Your Budget",

        [

            "Under ₹200",

            "Under ₹500",

            "Under ₹900",

            "Under ₹1000",

            "Under ₹1500"

        ]

    )


    budget_values = {

        "Under ₹200": 200,

        "Under ₹500": 500,

        "Under ₹900": 900,

        "Under ₹1000": 1000,

        "Under ₹1500": 1500

    }


    maximum_price = budget_values[budget]


    deals = [

        {

            "name": "Floral Casual Dress",

            "price": 199,

            "old_price": 399,

            "discount": "50% OFF",

            "store": "Demo Store"

        },

        {

            "name": "Elegant Midi Dress",

            "price": 799,

            "old_price": 1299,

            "discount": "38% OFF",

            "store": "Demo Store"

        },

        {

            "name": "Party Wear Dress",

            "price": 899,

            "old_price": 1499,

            "discount": "40% OFF",

            "store": "Demo Store"

        },

        {

            "name": "Trendy Maxi Dress",

            "price": 1199,

            "old_price": 1999,

            "discount": "40% OFF",

            "store": "Demo Store"

        }

    ]


    filtered_deals = [

        deal

        for deal in deals

        if deal["price"] < maximum_price

    ]


    st.write(
        f"### ✨ Fashion options for {budget}"
    )


    if filtered_deals:

        for deal in filtered_deals:

            st.markdown("---")

            st.subheader(
                f"👗 {deal['name']}"
            )

            col1, col2, col3 = st.columns(3)


            with col1:

                st.write(
                    f"💰 **₹{deal['price']}**"
                )


            with col2:

                st.write(
                    f"~~₹{deal['old_price']}~~"
                )


            with col3:

                st.success(
                    deal["discount"]
                )


            st.write(
                f"🏪 {deal['store']}"
            )


            search_url = (
                "https://www.google.com/search?q="
                + requests.utils.quote(deal["name"])
            )


            st.link_button(
                "🛍️ Search This Dress",
                search_url,
                use_container_width=True
            )


    else:

        st.warning(
            "No fashion options found within this budget."
        )


    st.info(
        "⚠️ These are demonstration prices and discounts. "
        "They are not live retailer offers."
    )


# ==================================================
# WISHLIST
# ==================================================

elif page == "❤️ Wishlist":

    st.title("❤️ My Wishlist")

    st.write(
        "Your favourite dresses saved from Price Comparison."
    )


    if "wishlist" not in st.session_state:

        st.session_state.wishlist = load_wishlist()


    if st.session_state.wishlist:

        st.subheader(
            "❤️ Saved Dresses"
        )


        for index, item in enumerate(
            st.session_state.wishlist
        ):

            st.markdown("---")

            col1, col2, col3 = st.columns(
                [5, 2, 2]
            )


            with col1:

                st.write(
                    f"👗 **{item['name']}**"
                )


            with col2:

                st.write(
                    f"💰 ₹{item['price']}"
                )


            with col3:

                if st.button(

                    "🗑️ Remove",

                    key=f"remove_wishlist_{index}",

                    use_container_width=True

                ):

                    st.session_state.wishlist.pop(
                        index
                    )

                    save_wishlist(
                        st.session_state.wishlist
                    )

                    st.rerun()


    else:

        st.info(
            "❤️ Your wishlist is empty."
        )

        st.write(
            "Go to 💰 Price Comparison and "
            "click ❤️ Add to Wishlist."
        )
