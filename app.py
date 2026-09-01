import streamlit as st
from PIL import Image
import requests
import json
import base64
from dotenv import load_dotenv
import os

WISHLIST_FILE = "wishlist.json"


def load_wishlist():

    if os.path.exists(WISHLIST_FILE):

        try:
            with open(
                WISHLIST_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:
            return []

    return []


def save_wishlist(wishlist):

    with open(
        WISHLIST_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            wishlist,
            file,
            indent=4,
            ensure_ascii=False
        )

load_dotenv()

TRYON_API_KEY = os.getenv("TRYON_API_KEY")

OLLAMA_URL = "http://localhost:11434/api/generate"

def analyze_dress_image(uploaded_file):
    image_bytes = uploaded_file.getvalue()

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

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
    Focus only on the clothing and general visible fashion features.
    """

    try:
    payload = {
        "model": "qwen2.5vl:3b",
        "prompt": prompt,
        "images": [image_base64],
        "stream": False
    }

    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        timeout=10
    )

    response.raise_for_status()

    return response.json()["response"]

except Exception:

    return """
✨ AI Fashion Recommendation

Based on your selected preferences, here are some fashion suggestions:

👗 Choose an outfit that matches your preferred style and occasion.

🎨 Use colours that complement your personal preferences.

✨ Add suitable accessories to complete your look.

💡 For the best results, consider your comfort, budget, and the occasion.

👠 Try combining simple pieces with one stylish statement item for a balanced outfit.
"""
    # ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="DressStyle AI",
    page_icon="👗",
    layout="wide"
)

# ---------------- CUSTOM STYLE ----------------

st.markdown("""
<style>

/* ================= MAIN BACKGROUND ================= */

.stApp {
    background: linear-gradient(135deg, #f3edff, #e9e0ff);
}


/* ================= SIDEBAR ================= */

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff5fa, #f8e8f1);
    min-width: 260px !important;
}


/* SIDEBAR SPACING */

section[data-testid="stSidebar"] > div {
    padding-top: 20px;
}


/* ================= SIDEBAR LOGO ================= */

.sidebar-logo {
    font-size: 26px;
    font-weight: 800;
    color: #6b3fa0;
    text-align: center;
    padding: 10px 5px 25px 5px;
}


/* ================= NAVIGATION ================= */

section[data-testid="stSidebar"] [data-testid="stRadio"] {
    width: 100%;
}


/* ================= NAVIGATION BUTTONS ================= */

section[data-testid="stSidebar"] [role="radio"] {

    width: 100% !important;

    min-height: 55px !important;

    background: linear-gradient(135deg, #ffdce9, #f8c8dc);

    border-radius: 30px !important;

    padding: 12px 18px !important;

    margin-bottom: 12px !important;

    display: flex !important;

    align-items: center !important;

    box-shadow: 0px 4px 10px rgba(180, 100, 140, 0.18);

    border: 1px solid #f2b6cf !important;

    transition: all 0.25s ease;

}


/* ================= HIDE RADIO CIRCLE ================= */

section[data-testid="stSidebar"] [role="radio"] > div:first-child {
    display: none !important;
}


/* ================= BUTTON TEXT ================= */

section[data-testid="stSidebar"] [role="radio"] p {

    color: #6b3fa0 !important;

    font-size: 16px !important;

    font-weight: 600 !important;

    margin: 0 !important;

}


/* ================= HOVER EFFECT ================= */

section[data-testid="stSidebar"] [role="radio"]:hover {

    transform: translateX(5px);

    background: linear-gradient(135deg, #ffc9df, #f5b5d1);

    box-shadow: 0px 7px 15px rgba(180, 100, 140, 0.25);

}


/* ================= SELECTED BUTTON ================= */

section[data-testid="stSidebar"] [role="radio"][aria-checked="true"] {

    background: linear-gradient(135deg, #e9b6d0, #d99abc) !important;

    border: 1px solid #c97ca5 !important;

    box-shadow: 0px 6px 18px rgba(180, 80, 130, 0.30);

}


section[data-testid="stSidebar"] [role="radio"][aria-checked="true"] p {

    color: #5a2850 !important;

    font-weight: 700 !important;

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

    box-shadow: 0px 6px 20px rgba(90, 60, 150, 0.15);

    transition: all 0.3s ease;

}


.feature-card:hover {

    transform: translateY(-5px);

    box-shadow: 0px 10px 25px rgba(90, 60, 150, 0.25);

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

""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------

st.sidebar.markdown(
    '<div class="sidebar-brand">👗 DressStyle AI</div>',
    unsafe_allow_html=True
)

if "page" not in st.session_state:
    st.session_state.page = "🏠 Home"


if st.sidebar.button("🏠  Home", use_container_width=True):
    st.session_state.page = "🏠 Home"

if st.sidebar.button("✨  AI Stylist", use_container_width=True):
    st.session_state.page = "✨ AI Stylist"

if st.sidebar.button("📸  Virtual Try-On", use_container_width=True):
    st.session_state.page = "📸 Virtual Try-On"

if st.sidebar.button("🔍  Dress Search", use_container_width=True):
    st.session_state.page = "🔍 Dress Search"

if st.sidebar.button("💰  Price Comparison", use_container_width=True):
    st.session_state.page = "💰 Price Comparison"

if st.sidebar.button("🔥  Best Deals", use_container_width=True):
    st.session_state.page = "🔥 Best Deals"

if st.sidebar.button("❤️  Wishlist", use_container_width=True):
    st.session_state.page = "❤️ Wishlist"


page = st.session_state.page



# ---------------- HOME PAGE ----------------

if page == "🏠 Home":

    st.markdown(
        '<div class="main-title">👗 DressStyle AI</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Find Your Perfect Style Before You Buy ✨</div>',
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="feature-card">
            <h2>✨ AI Fashion Stylist</h2>
            <p>Get personalized dress recommendations based on your style, occasion and budget.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="feature-card">
            <h2>📸 Virtual Try-On</h2>
            <p>Upload your photo and a dress image to get AI-powered style matching advice.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="feature-card">
            <h2>💰 Compare Prices</h2>
            <p>Search dresses and compare available shopping options within your budget.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    st.header("✨ What can DressStyle AI do?")

    st.write("""
    👗 **Discover fashion styles** based on your preferences

    🎨 **Explore colour and outfit ideas**

    📸 **Upload a dress image** for AI fashion analysis

    🤖 **Get AI fashion suggestions**

    💰 **Find dresses within your budget**

    🔗 **Open supported shopping links**
    """)

# ---------------- AI STYLIST ----------------

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

    if st.button("✨ Find My Perfect Dress"):

        if not colour.strip():

            st.warning(
                "Please enter your preferred colour."
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

Suggest the most suitable dress style based on
the user's occasion, preferred colour, style,
dress type and budget.

🎨 Colour Recommendation

Explain the selected colour and suggest
2 or 3 alternative colours that may also work
with the chosen style.

✨ Why This Style

Explain why this dress style matches the
occasion and the user's preferences.

💎 Styling Ideas

Suggest suitable:
- Shoes
- Handbag
- Jewellery
- Hairstyle
- Optional layering

🔎 Shopping Search Keywords

Give 5 useful search phrases that could be used
to find similar dresses online.

💰 Budget Strategy

Explain what type of dress, fabric or design
the customer could look for within the stated
budget.

🛍️ Shopping Checklist

Give 5 things the customer should check before
buying the dress, such as size, material,
return policy and reviews.

Do not identify or judge the user's appearance.
Do not make assumptions about race, ethnicity
or sensitive personal characteristics.

Focus on clothing, colour, occasion, comfort,
style and shopping preferences.
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

                    recommendation = response.json()["response"]

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
                        search_url
                    )

                    st.caption(
                        "This opens a shopping search using "
                        "your selected preferences."
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )

# ---------------- VIRTUAL TRY-ON ----------------
elif page == "📸 Virtual Try-On":

    st.title("📸 AI Virtual Try-On")

    st.write(
        "Upload your photo and a dress photo to see an AI-generated try-on."
    )

    col1, col2 = st.columns(2)

    with col1:
        user_photo = st.file_uploader(
            "👤 Upload Your Photo",
            type=["jpg", "jpeg", "png"],
            key="user_tryon_photo"
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
            key="dress_tryon_photo"
        )

        if dress_photo:
            st.image(
                dress_photo,
                caption="Dress Photo",
                use_container_width=True
            )

    st.write("")

    if st.button("✨ Generate Virtual Try-On"):

        if not user_photo or not dress_photo:

            st.warning(
                "Please upload both your photo and the dress photo."
            )

        elif not TRYON_API_KEY:

            st.error(
                "Try-On API key was not found. "
                "Please check your .env file."
            )

        else:

            with st.spinner(
                "🤖 Creating your virtual try-on image... This may take a little while."
            ):

                try:

                    api_url = (
                        "https://www.tryoncloud.com/api/v1/generate"
                    )

                    headers = {
                        "X-API-KEY": TRYON_API_KEY
                    }

                    files = {
                        "garment_image": (
                            dress_photo.name,
                            dress_photo.getvalue(),
                            dress_photo.type
                        ),
                        "person_image": (
                            user_photo.name,
                            user_photo.getvalue(),
                            user_photo.type
                        )
                    }

                    response = requests.post(
                        api_url,
                        headers=headers,
                        files=files,
                        timeout=180
                    )

                    if response.status_code == 200:

                        st.success(
                            "✨ Virtual Try-On Complete!"
                        )

                        st.subheader(
                            "👗 Your Virtual Try-On Result"
                        )

                        st.image(
                            response.content,
                            caption="AI Virtual Try-On Result",
                            use_container_width=True
                        )

                        st.download_button(
                            label="⬇️ Download Try-On Image",
                            data=response.content,
                            file_name="virtual_tryon_result.png",
                            mime="image/png"
                        )

                    else:

                        try:
                            error_data = response.json()

                            error_code = error_data.get(
                                "code",
                                "UNKNOWN_ERROR"
                            )

                            error_message = error_data.get(
                                "error",
                                "Virtual try-on failed."
                            )

                            st.error(
                                f"Try-On Error: {error_code} - "
                                f"{error_message}"
                            )

                        except Exception:

                            st.error(
                                f"Try-on failed with HTTP "
                                f"status {response.status_code}."
                            )

                except requests.exceptions.Timeout:

                    st.error(
                        "The virtual try-on took too long to respond. "
                        "Please try again with clear JPG/PNG images."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Connection error: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )
# ---------------- DRESS SEARCH ----------------

elif page == "🔍 Dress Search":

    st.title("🔍 AI Dress Search")

    st.write(
        "Upload a dress or outfit image and let AI analyze its style!"
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
            key="analyze_dress_button"
        ):

            with st.spinner(
                "🤖 AI is analyzing the dress..."
            ):

                try:

                    analysis = analyze_dress_image(
                        uploaded_dress
                    )

                    st.success(
                        "✨ AI Dress Analysis Complete!"
                    )

                    st.markdown(analysis)

                except Exception as e:

                    st.error(
                        f"AI analysis error: {e}"
                    )

                    st.info(
                        "Make sure Ollama is running correctly."
                    )

    else:

        st.info(
            "📸 Upload a dress image to start AI analysis."
        )
# ---------------- PRICE COMPARISON ----------------
elif page == "💰 Price Comparison":

    st.title("💰 Compare Before You Buy")

    st.write(
        "Search for a dress and explore shopping options."
    )

    # Load wishlist once
    if "wishlist" not in st.session_state:
        st.session_state.wishlist = load_wishlist()

    # Store search results in session state
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

    if st.button("🔎 Search Dresses"):

        if search.strip():

            products = [
                {
                    "name": f"{search} - Option 1",
                    "store": "Demo Store 1",
                    "price": 799,
                    "rating": 4.3,
                    "link": "https://www.google.com/search?q=dress"
                },
                {
                    "name": f"{search} - Option 2",
                    "store": "Demo Store 2",
                    "price": 999,
                    "rating": 4.5,
                    "link": "https://www.google.com/search?q=dress"
                },
                {
                    "name": f"{search} - Option 3",
                    "store": "Demo Store 3",
                    "price": 1499,
                    "rating": 4.2,
                    "link": "https://www.google.com/search?q=dress"
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

            # Save search results
            st.session_state.products = products

        else:

            st.warning(
                "Please enter a dress name."
            )

    # Display saved search results
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
                    product["link"]
                )

            with button_col2:

                if st.button(
                    "❤️ Add to Wishlist",
                    key=f"wishlist_product_{index}"
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
# ---------------- BEST DEALS ----------------

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
        },
        {
            "name": "Classic Party Dress",
            "price": 1499,
            "old_price": 2499,
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

            st.link_button(
                "🛍️ Search This Dress",
                "https://www.google.com/search?q=dress"
            )

    else:

        st.warning(
            "No fashion options found within this budget."
        )

    st.info(
        "⚠️ These are demonstration prices and discounts. "
        "They are not live retailer offers."
    )

# ---------------- WISHLIST ----------------
elif page == "❤️ Wishlist":

    st.title("❤️ My Wishlist")

    st.write(
        "Your favourite dresses saved from Price Comparison."
    )

    # Create wishlist if it does not exist
    if "wishlist" not in st.session_state:
        st.session_state.wishlist = load_wishlist()

    # Show saved dresses
    if st.session_state.wishlist:

        st.subheader("❤️ Saved Dresses")

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
                    key=f"remove_wishlist_{index}"
                ):

                    st.session_state.wishlist.pop(
                        index
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
# ==========================================
# VIRTUAL TRY-ON
# ==========================================

elif page == "📸 Virtual Try-On":

    st.title("📸 AI Virtual Try-On")

    st.write(
        "Upload your photo and a dress photo to create "
        "an AI-generated virtual try-on."
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

    st.write("")

    if st.button("✨ Generate Virtual Try-On"):

        if not user_photo or not dress_photo:

            st.warning(
                "Please upload both your photo "
                "and the dress photo."
            )

        elif not TRYON_API_KEY:

            st.error(
                "Try-On API key was not found. "
                "Please check your .env file."
            )

        else:

            with st.spinner(
                "🤖 Creating your virtual try-on image..."
            ):

                try:

                    api_url = (
                        "https://www.tryoncloud.com/api/v1/generate"
                    )

                    headers = {
                        "X-API-KEY": TRYON_API_KEY
                    }

                    files = {

                        "garment_image": (
                            dress_photo.name,
                            dress_photo.getvalue(),
                            dress_photo.type
                        ),

                        "person_image": (
                            user_photo.name,
                            user_photo.getvalue(),
                            user_photo.type
                        )
                    }

                    response = requests.post(
                        api_url,
                        headers=headers,
                        files=files,
                        timeout=180
                    )

                    response.raise_for_status()

                    st.success(
                        "✨ Virtual Try-On Complete!"
                    )

                    st.subheader(
                        "👗 Your Virtual Try-On Result"
                    )

                    st.image(
                        response.content,
                        caption="AI Virtual Try-On Result",
                        use_container_width=True
                    )

                    st.download_button(
                        "⬇️ Download Try-On Image",
                        data=response.content,
                        file_name="virtual_tryon_result.png",
                        mime="image/png"
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "The virtual try-on took too long. "
                        "Please try again."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(
                        f"Virtual Try-On connection error: {e}"
                    )

                except Exception as e:

                    st.error(
                        f"Something went wrong: {e}"
                    )
