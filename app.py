import streamlit as st
import pandas as pd
import torch
from transformers import AutoTokenizer, BertForSequenceClassification

logo_url = "https://img.freepik.com/free-vector/colorful-bird-illustration-gradient_343694-1741.jpg?size=626&ext=jpg&ga=GA1.1.733875022.1726100029&semt=ais_hybrid.png"
background_image_url = "https://images.unsplash.com/photo-1524758631624-e2822e304c36?crop=entropy&cs=tinysrgb&w=1080&fit=max"

st.set_page_config(page_title="Bangla Sentiment Analysis", page_icon=logo_url, layout="wide")

# Custom CSS for the background image and text styling
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .stButton>button {{
        background-color: #3498db;
        color: white;
        border-radius: 10px;
    }}
    .stButton>button:hover {{
        background-color: #2980b9;
    }}
    .stSidebar {{
        background-color: rgba(0, 0, 0, 0.5);
    }}
    .stTextInput, .stTextArea {{
        background-color: rgba(255, 255, 255, 0.8);
    }}
    h1, h2, h3 {{
        color: white;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.image(logo_url, width=100)

# Load the fine-tuned model and tokenizer
model_path = "F://Bangla Sentiment project//Bangla_sentiment_bert_model"
model = BertForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
df=pd.read_csv("F://Bangla Sentiment project//bangla_sentiment_data (5).csv")
# Define label mapping
label_mapping = {0: "happy", 1: "sad", 2: "angry"}

# Define preprocessing function
def preprocess_text(text):
    stopwords = ['আমি', 'আপনি', 'সে', 'তুমি', 'আমরা', 'আপনারা', 'তারা', 'এর', 'এই', 'ওই', 'তার', 'তাদের', 'আমাদের', 'আপনার', 'তোমার', 'আপনারা', 'আমরা', 'যে', 'যত', 'সব', 'কিছু', 'বহু', 'কোনো', 'কোন', 'একটি', 'এটি', 'তিন', 'চার', 'এখানে', 'যেখানে', 'এখানে', 'কিভাবে', 'কীভাবে', 'কেন', 'কেননা', 'যখন', 'যদি', 'তবে', 'কিন্তু', 'তবে', 'আর', 'তিন', 'চার', 'অথবা', 'নাহলে', 'যত', 'যেমন', 'কিন্তু', 'নিশ্চিত', 'সবাই', 'অনেক', 'কিছু', 'কেননা', 'অন্য', 'নতুন', 'পুরানো', 'বেশি', 'কম', 'অন্তত', 'বেশি', 'কম', 'এবং', 'অথবা', 'নির্বাচন', 'এই', 'ওই', 'ফিরে', 'তারপর', 'পরে', 'আগে', 'তখন', 'নতুন', 'পুরানো', 'যে', 'তবে', 'অথবা', 'একটি', 'অথবা', 'অবশ্য', 'এরপর', 'আমরা', 'বিভিন্ন', 'সকল', 'যেখানে', 'এখানে', 'কি', 'মাঝে', 'মধ্যে', 'মধ্যবর্তী', 'যে', 'শুধু', 'উল্লেখযোগ্য', 'অধিক', 'যেমন', 'বিভিন্ন', 'অপর', 'অন্য', 'কিছু', 'অন্যান্য', 'আর', 'যাওয়া', 'আসা', 'কী', 'যখন', 'এটি', 'কারণে', 'তারপর', 'তাদের', 'আমাদের', 'আরও', 'অবশ্যই', 'এবং', 'অথবা', 'বিশেষ', 'কি', 'ব্যাপারে', 'অথবা', 'দ্বারা', 'তারা', 'এক', 'মধ্যে', 'কিছু', 'তবে', 'এছাড়া', 'মধ্যে', 'কোনো', 'অন্য', 'প্রতিটি', 'একটি', 'যেখানে', 'যত', 'যে', 'যদি', 'আর', 'অনেক', 'যেমন', 'যেমন', 'তার', 'ভেতরে', 'দ্বারা', 'এর', 'আছে', 'দিয়ে', 'যাওয়া', 'আসা', 'যে', 'নতুন', 'পুরানো', 'যেমন', 'ফিরে', 'পরের', 'সকল', 'তাদের', 'সব', 'অন্যান্য', 'আরও', 'কোন', 'এখানে', 'যখন', 'তবে', 'তাদের', 'ফিরে', 'যেখানে', 'আরও', 'আমরা', 'কিছু', 'অন্য', 'নতুন', 'কিছু', 'অন্য', 'সবার', 'অপর', 'মাঝে', 'বিভিন্ন', 'এই', 'তাদের', 'আমাদের', 'এই', 'যেমন', 'অতএব', 'এরপর', 'নতুন', 'সর্বোচ্চ', 'সর্বনিম্ন', 'মাঝে', 'আমি', 'আপনি', 'সে', 'তুমি', 'আমরা', 'আপনারা', 'তারা', 'এর', 'এই', 'ওই', 'তার', 'তাদের', 'আমাদের', 'আপনার', 'তোমার', 'আপনারা', 'আমরা', 'যে', 'যত', 'সব', 'কিছু', 'বহু', 'কোনো', 'কোন', 'একটি', 'এটি', 'তিন', 'চার', 'এখানে', 'যেখানে', 'এখানে', 'কিভাবে', 'কীভাবে', 'কেন', 'কেননা', 'যখন', 'যদি', 'তবে', 'কিন্তু', 'তবে', 'আর', 'তিন', 'চার', 'অথবা', 'নাহলে', 'যত', 'যেমন', 'কিন্তু', 'নিশ্চিত', 'সবাই', 'অনেক', 'কিছু', 'কেননা', 'অন্য', 'নতুন', 'পুরানো', 'বেশি', 'কম', 'অন্তত', 'বেশি', 'কম', 'এবং', 'অথবা', 'নির্বাচন', 'এই', 'ওই', 'ফিরে', 'তারপর', 'পরে', 'আগে', 'তখন', 'নতুন', 'পুরানো', 'যে', 'তবে', 'অথবা', 'একটি', 'অথবা', 'অবশ্য', 'এরপর', 'আমরা', 'বিভিন্ন', 'সকল', 'যেখানে', 'এখানে', 'কি', 'মাঝে', 'মধ্যে', 'মধ্যবর্তী', 'যে', 'শুধু', 'উল্লেখযোগ্য', 'অধিক', 'যেমন', 'বিভিন্ন', 'অপর', 'অন্য', 'কিছু', 'অন্যান্য', 'আর', 'যাওয়া', 'আসা', 'কী', 'যখন', 'এটি', 'কারণে', 'তারপর', 'তাদের', 'আমাদের', 'আরও', 'অবশ্যই', 'এবং', 'অথবা', 'বিশেষ', 'কি', 'ব্যাপারে', 'অথবা', 'দ্বারা', 'তারা', 'এক', 'মধ্যে', 'কিছু', 'তবে', 'এছাড়া', 'মধ্যে', 'কোনো', 'অন্য', 'প্রতিটি', 'একটি', 'যেখানে', 'যত', 'যে', 'যদি', 'আর', 'অনেক', 'যেমন', 'যেমন', 'তার', 'ভেতরে', 'দ্বারা', 'এর', 'আছে', 'দিয়ে', 'যাওয়া', 'আসা', 'যে', 'নতুন', 'পুরানো', 'যেমন', 'ফিরে', 'পরের', 'সকল', 'তাদের', 'সব', 'অন্যান্য', 'আরও', 'কোন', 'এখানে', 'যখন', 'তবে', 'তাদের', 'ফিরে', 'যেখানে', 'আরও', 'আমরা', 'কিছু', 'অন্য', 'নতুন', 'কিছু', 'অন্য', 'সবার', 'অপর', 'মাঝে', 'বিভিন্ন', 'এই', 'তাদের', 'আমাদের', 'এই', 'যেমন', 'অতএব', 'এরপর', 'নতুন', 'সর্বোচ্চ', 'সর্বনিম্ন', 'মাঝে', 'আমি', 'আপনি', 'সে', 'তুমি', 'আমরা', 'আপনারা', 'তারা', 'এর', 'এই', 'ওই', 'তার', 'তাদের', 'আমাদের', 'আপনার', 'তোমার', 'আপনারা', 'আমরা', 'যে', 'যত', 'সব', 'কিছু', 'বহু', 'কোনো', 'কোন', 'একটি', 'এটি', 'তিন', 'চার', 'এখানে', 'যেখানে', 'এখানে', 'কিভাবে', 'কীভাবে', 'কেন', 'কেননা', 'যখন', 'যদি', 'তবে', 'কিন্তু', 'তবে', 'আর', 'তিন', 'চার', 'অথবা', 'নাহলে', 'যত', 'যেমন', 'কিন্তু', 'নিশ্চিত', 'সবাই', 'অনেক', 'কিছু', 'কেননা', 'অন্য', 'নতুন', 'পুরানো', 'বেশি', 'কম', 'অন্তত', 'বেশি', 'কম', 'এবং', 'অথবা', 'নির্বাচন', 'এই', 'ওই', 'ফিরে', 'তারপর', 'পরে', 'আগে', 'তখন', 'নতুন', 'পুরানো', 'যে', 'তবে', 'অথবা', 'একটি', 'অথবা', 'অবশ্য', 'এরপর', 'আমরা', 'বিভিন্ন', 'সকল', 'যেখানে', 'এখানে', 'কি', 'মাঝে', 'মধ্যে', 'মধ্যবর্তী', 'যে', 'শুধু', 'উল্লেখযোগ্য', 'অধিক', 'যেমন', 'বিভিন্ন', 'অপর', 'অন্য', 'কিছু', 'অন্যান্য', 'আর', 'যাওয়া', 'আসা', 'কী', 'যখন', 'এটি', 'কারণে', 'তারপর', 'তাদের', 'আমাদের', 'আরও', 'অবশ্যই', 'এবং', 'অথবা', 'বিশেষ', 'কি', 'ব্যাপারে', 'অথবা', 'দ্বারা', 'তারা', 'এক', 'মধ্যে', 'কিছু', 'তবে', 'এছাড়া', 'মধ্যে', 'কোনো', 'অন্য', 'প্রতিটি', 'একটি', 'যেখানে', 'যত', 'যে', 'যদি', 'আর', 'অনেক', 'যেমন', 'যেমন', 'তার', 'ভেতরে', 'দ্বারা', 'এর', 'আছে', 'দিয়ে', 'যাওয়া', 'আসা', 'যে', 'নতুন', 'পুরানো', 'যেমন', 'ফিরে', 'পরের', 'সকল', 'তাদের', 'সব', 'অন্যান্য', 'আরও', 'কোন', 'এখানে', 'যখন', 'তবে', 'তাদের', 'ফিরে', 'যেখানে', 'আরও', 'আমরা', 'কিছু', 'অন্য', 'নতুন', 'কিছু', 'অন্য', 'সবার', 'অপর', 'মাঝে', 'বিভিন্ন', 'এই', 'তাদের', 'আমাদের', 'এই', 'যেমন', 'অতএব', 'এরপর', 'নতুন', 'সর্বোচ্চ', 'সর্বনিম্ন', 'মাঝে', 'অতএব', 'অথচ', 'অথবা', 'অনুযায়ী', 'অনেক', 'অনেকে', 'অনেকেই', 'অন্তত', 'অন্য', 'অবধি', 'অবশ্য', 'অর্থাত', 'আই', 'আগামী', 'আগে', 'আগেই', 'আছে', 'আজ', 'আদ্যভাগে', 'আপনার', 'আপনি', 'আবার', 'আমরা', 'আমাকে', 'আমাদের', 'আমার', 'আমি', 'আর', 'আরও', 'ই', 'ইত্যাদি', 'ইহা', 'উচিত', 'উত্তর', 'উনি', 'উপর', 'উপরে', 'এ', 'এঁদের', 'এঁরা', 'এই', 'একই', 'একটি', 'একবার', 'একে', 'এক্', 'এখন', 'এখনও', 'এখানে', 'এখানেই', 'এটা', 'এটাই', 'এটি', 'এত', 'এতটাই', 'এতে', 'এদের', 'এব', 'এবং', 'এবার', 'এমন', 'এমনকী', 'এমনি', 'এর', 'এরা', 'এল', 'এস', 'এসে', 'ঐ', 'ও', 'ওঁদের', 'ওঁর', 'ওঁরা', 'ওই', 'ওকে', 'ওখানে', 'ওদের', 'ওর', 'ওরা', 'কখনও', 'কত', 'কবে', 'কমনে', 'কয়েক', 'কয়েকটি', 'করছে', 'করছেন', 'করতে', 'করবে', 'করবেন', 'করলে', 'করলেন', 'করা', 'করাই', 'করায়', 'করার', 'করি', 'করিতে', 'করিয়া', 'করিয়ে', 'করে', 'করেই', 'করেছিলেন', 'করেছে', 'করেছেন', 'করেন', 'কাউকে', 'কাছ', 'কাছে', 'কাজ', 'কাজে', 'কারও', 'কারণ', 'কি', 'কিংবা', 'কিছু', 'কিছুই', 'কিন্তু', 'কী', 'কে', 'কেউ', 'কেউই', 'কেখা', 'কেন', 'কোটি', 'কোন', 'কোনও', 'কোনো', 'ক্ষেত্রে', 'কয়েক', 'খুব', 'গিয়ে', 'গিয়েছে', 'গিয়ে', 'গুলি', 'গেছে', 'গেল', 'গেলে', 'গোটা', 'চলে', 'চান', 'চায়', 'চার', 'চালু', 'চেয়ে', 'চেষ্টা', 'ছাড়া', 'ছাড়াও', 'ছিল', 'ছিলেন', 'জন', 'জনকে', 'জনের', 'জন্য', 'জন্যওজে', 'জানতে', 'জানা', 'জানানো', 'জানায়', 'জানিয়ে', 'জানিয়েছে', 'জে', 'জ্নজন', 'টি', 'ঠিক', 'তখন', 'তত', 'তথা', 'তবু', 'তবে', 'তা', 'তাঁকে', 'তাঁদের', 'তাঁর', 'তাঁরা', 'তাঁাহারা', 'তাই', 'তাও', 'তাকে', 'তাতে', 'তাদের', 'তার', 'তারপর', 'তারা', 'তারৈ', 'তাহলে', 'তাহা', 'তাহাতে', 'তাহার', 'তিনঐ', 'তিনি', 'তিনিও', 'তুমি', 'তুলে', 'তেমন', 'তো', 'তোমার', 'থাকবে', 'থাকবেন', 'থাকা', 'থাকায়', 'থাকে', 'থাকেন', 'থেকে', 'থেকেই', 'থেকেও', 'দিকে', 'দিতে', 'দিন', 'দিয়ে', 'দিয়েছে', 'দিয়েছেন', 'দিলেন', 'দু', 'দুই', 'দুটি', 'দুটো', 'দেওয়া', 'দেওয়ার', 'দেওয়া', 'দেখতে', 'দেখা', 'দেখে', 'দেন', 'দেয়', 'দ্বারা', 'ধরা', 'ধরে', 'ধামার', 'নতুন', 'নয়', 'না', 'নাই', 'নাকি', 'নাগাদ', 'নানা', 'নিজে', 'নিজেই', 'নিজেদের', 'নিজের', 'নিতে', 'নিয়ে', 'নিয়ে', 'নেই', 'নেওয়া', 'নেওয়ার', 'নেওয়া', 'নয়', 'পক্ষে', 'পর', 'পরে', 'পরেই', 'পরেও', 'পর্যন্ত', 'পাওয়া', 'পাচ', 'পারি', 'পারে', 'পারেন', 'পি', 'পেয়ে', 'পেয়্র্', 'প্রতি', 'প্রথম', 'প্রভৃতি', 'প্রযন্ত', 'প্রাথমিক', 'প্রায়', 'প্রায়', 'ফলে', 'ফিরে', 'ফের', 'বক্তব্য', 'বদলে', 'বন', 'বরং', 'বলতে', 'বলল', 'বললেন', 'বলা', 'বলে', 'বলেছেন', 'বলেন', 'বসে', 'বহু', 'বা', 'বাদে', 'বার', 'বি', 'বিনা', 'বিভিন্ন', 'বিশেষ', 'বিষয়টি', 'বেশ', 'বেশি', 'ব্যবহার', 'ব্যাপারে', 'ভাবে', 'ভাবেই', 'মতো', 'মতোই', 'মধ্যভাগে', 'মধ্যে', 'মধ্যেই', 'মধ্যেও', 'মনে', 'মাত্র', 'মাধ্যমে', 'মোট', 'মোটেই', 'যখন', 'যত', 'যতটা', 'যথেষ্ট', 'যদি', 'যদিও', 'যা', 'যাঁর', 'যাঁরা', 'যাওয়া', 'যাওয়ার', 'যাওয়া', 'যাকে', 'যাচ্ছে', 'যাতে', 'যাদের', 'যান', 'যাবে', 'যায়', 'যার', 'যারা', 'যিনি', 'যে', 'যেখানে', 'যেতে', 'যেন', 'যেমন', 'র', 'রকম', 'রয়েছে', 'রাখা', 'রেখে', 'লক্ষ', 'শুধু', 'শুরু', 'সঙ্গে', 'সঙ্গেও', 'সব', 'সবার', 'সমস্ত', 'সম্প্রতি', 'সহ', 'সহিত', 'সাধারণ', 'সামনে', 'সি', 'সুতরাং', 'সে', 'সেই', 'সেখান', 'সেখানে', 'সেটা', 'সেটাই', 'সেটাও', 'সেটি', 'স্পষ্ট', 'স্বয়ং', 'হইতে', 'হইবে', 'হইয়া', 'হওয়া', 'হওয়ায়', 'হওয়ার', 'হচ্ছে', 'হত', 'হতে', 'হতেই', 'হন', 'হবে', 'হবেন', 'হয়', 'হয়তো', 'হয়নি', 'হয়ে', 'হয়েই', 'হয়েছিল', 'হয়েছে', 'হয়েছেন', 'হল', 'হলে', 'হলেই', 'হলেও', 'হলো', 'হাজার', 'হিসাবে', 'হৈলে', 'হোক', 'হয়']
    emoji_dict = {
        "😊": "হাসি", "😢": "কান্না", "😠": "রাগ", "😔": "মন খারাপ", "👍": "দারুণ",
        "😎": "ঠান্ডা", "😭": "অশ্রু", "😁": "মুচকি হাসি", "😅": "হালকা হাসি", "😍": "ভালবাসা",
        "😒": "অসন্তুষ্ট", "😞": "হতাশা", "😡": "রাগান্বিত", "😃": "খুশি", "😉": "চোখ মারা",
        "😋": "স্বাদ আস্বাদন", "😐": "নির্বিকার", "😤": "অসন্তুষ্ট", "😴": "ঘুম", "😜": "মজার",
        "😩": "ক্লান্ত", "😯": "আশ্চর্য", "😆": "হাসি", "😷": "মাস্ক", "🙄": "গুর্গুরানি",
        "😳": "বিস্মিত", "😬": "চিন্তিত", "😚": "চুম্বন", "😰": "উদ্বিগ্ন", "🤗": "আলিঙ্গন",
        "🤔": "চিন্তাশীল", "🤐": "মুখ বন্ধ", "😇": "পুণ্যবান"
    }
    
    for emoji, meaning in emoji_dict.items():
        text = text.replace(emoji, meaning)
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return " ".join(words).strip()

# Define sentiment prediction function
def predict_sentiment(text):
    text = preprocess_text(text)
    inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    
    with torch.no_grad():
        model.eval()
        outputs = model(**inputs)
        logits = outputs.logits
        prediction = torch.argmax(logits, dim=1).item()
    
    return label_mapping.get(prediction, "Unknown")

# Streamlit App
st.title("Bangla Sentiment Analysis")
st.write("Enter Bangla text below to predict its sentiment:")

user_input = st.text_area("Enter text:")
if st.button("Predict Sentiment"):
    if user_input:
        sentiment = predict_sentiment(user_input)
        st.write(f"Predicted Sentiment: **{sentiment}**")
    else:
        st.warning("Please enter some text.")
with st.sidebar:
    st.write("### Input Text Example:")
    st.code("আমি খুব খারাপ আছি 😢", language="plain")
    st.code("তুমি কেন এমন করলে? 😡", language="plain")
    st.code("তুমি আমাকে রাগিয়ে দিচ্ছ 😠", language="plain")
    st.code("আজকে সবকিছুই বিরক্তিকর 😡", language="plain")
    st.code("আজ আমার খুব মন খারাপ।", language="plain")
    st.code("আমি খুব একা বোধ করছি।", language="plain")
    st.code("জীবনটা কেন এত কঠিন!", language="plain")
    st.code("কিছুই যেন আর ভালো লাগছে না।", language="plain")
    st.code("মনে হচ্ছে সব কিছু ভেঙে পড়ছে।", language="plain")
    st.code("আজ আমি খুব আনন্দিত!", language="plain")
    st.code("এটা আমার জীবনের সেরা মুহূর্ত!", language="plain")
    st.code("সবকিছু এত সুন্দর লাগছে!", language="plain")
    st.code("আজকের দিনটা সত্যিই অসাধারণ!", language="plain")
st.markdown("""
    <div style='display: flex; justify-content: center;'>
        <h2>Dataset Preview</h2>
    </div>
""", unsafe_allow_html=True)
# Centered Dataset Preview
st.markdown("""
    <style>
    .centered-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    </style>
    <div class='centered-container'>
        <div>
""", unsafe_allow_html=True)

st.dataframe(df, height=200)  # Ensure 'df' is defined elsewhere in the script

st.markdown("</div></div>", unsafe_allow_html=True)

st.markdown(
    """
    <hr style="border: 1px solid #e74c3c;">
    <div style="text-align:center;">
        <p style="color:yellow;font-weight:bold;">Bangla Sentiment Analysis App | Powered by BanglaNLP</p>
    </div>
    """, 
    unsafe_allow_html=True
)