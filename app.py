# import streamlit as st
# from PIL import Image
# import io
# import zipfile
# import hashlib
# import pandas as pd
# import matplotlib.pyplot as plt
# import torch
# import torch.nn.functional as F
# import torchvision.transforms as transforms
# import timm

# st.set_page_config(page_title="Smart Image Organizer", layout="wide")

# @st.cache_resource
# def load_model():
#     model_path = "best_model.pth"  

#     model = timm.create_model(
#         'efficientnet_b3',
#         pretrained=False,
#         num_classes=5
#     )

#     model.load_state_dict(torch.load(model_path, map_location="cpu"))
#     model.eval()
#     return model

# model = load_model()

# categories = [
#     "Documents",
#     "Educational",
#     "Others",
#     "Personal",
#     "Screenshots"
# ]


# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(
#         [0.485, 0.456, 0.406],
#         [0.229, 0.224, 0.225]
#     )
# ])


# def predict_image(file):
#     image = Image.open(file).convert("RGB")
#     img = transform(image).unsqueeze(0)

#     with torch.no_grad():
#         outputs = model(img)
#         probs = F.softmax(outputs, dim=1)
#         confidence, predicted = torch.max(probs, 1)

#     return categories[predicted.item()], confidence.item()

# def get_hash(file):
#     return hashlib.md5(file.getvalue()).hexdigest()


# if "data" not in st.session_state:
#     st.session_state.data = []

# st.markdown("""
# <style>
# .card {
#     background: rgba(255,255,255,0.05);
#     padding: 10px;
#     border-radius: 15px;
#     backdrop-filter: blur(12px);
#     margin-bottom: 10px;
#     transition: 0.3s;
# }
# .card:hover {
#     transform: scale(1.02);
# }
# .low-conf {
#     border: 2px solid red;
# }

# /* Scrollable columns */
# div[data-testid="column"] {
#     max-height: 80vh;
#     overflow-y: auto;
# }

# /* Column separator lines */
# div[data-testid="column"]:not(:last-child) {
#     border-right: 1px solid rgba(255,255,255,0.1);
#     padding-right: 10px;
# }
# </style>
# """, unsafe_allow_html=True)
# # =========================
# # TITLE
# # =========================
# # st.title("🧠 Smart Image Organizer")

# # # =========================
# # # UPLOAD
# # # =========================
# # uploaded_files = st.file_uploader(
# #     "Upload Images",
# #     type=["png", "jpg", "jpeg"],
# #     accept_multiple_files=True
# # )

# # if uploaded_files:
# #     existing_hashes = {item["hash"] for item in st.session_state.data}

# #     for file in uploaded_files:
# #         file_hash = get_hash(file)

# #         if file_hash in existing_hashes:
# #             continue

# #         category, confidence = predict_image(file)

# #         st.session_state.data.append({
# #             "file": file,
# #             "image": Image.open(file),
# #             "category": category,
# #             "confidence": confidence,
# #             "hash": file_hash
# #         })

# # # =========================
# # # SIDEBAR FILTERS
# # # =========================
# # st.sidebar.header("🔍 Filters")

# # search = st.sidebar.text_input("Search filename")
# # selected_category = st.sidebar.selectbox("Category", ["All"] + categories)
# # low_conf_only = st.sidebar.checkbox("Low Confidence (<70%)")

# # # =========================
# # # FILTER LOGIC
# # # =========================
# # filtered_data = []

# # for item in st.session_state.data:
# #     if search and search.lower() not in item["file"].name.lower():
# #         continue
# #     if selected_category != "All" and item["category"] != selected_category:
# #         continue
# #     if low_conf_only and item["confidence"] >= 0.7:
# #         continue
# #     filtered_data.append(item)

# # # =========================
# # # DISPLAY GRID
# # # =========================
# # st.subheader("📂 Review & Edit")

# # cols = st.columns(5)

# # for i, item in enumerate(filtered_data):
# #     col = cols[i % 5]

# #     with col:
# #         border_class = "low-conf" if item["confidence"] < 0.7 else ""

# #         st.markdown(f'<div class="card {border_class}">', unsafe_allow_html=True)

# #         st.image(item["image"], use_container_width=True)
# #         st.caption(item["file"].name)

# #         new_cat = st.selectbox(
# #             "Category",
# #             categories,
# #             index=categories.index(item["category"]),
# #             key=item["hash"]
# #         )

# #         item["category"] = new_cat

# #         st.write(f"Confidence: {item['confidence']*100:.1f}%")

# #         st.markdown("</div>", unsafe_allow_html=True)

# # # =========================
# # # STATS DASHBOARD
# # # =========================
# # st.subheader("📊 Statistics")

# # if st.session_state.data:
# #     df = pd.DataFrame(st.session_state.data)
# #     counts = df["category"].value_counts()

# #     fig, ax = plt.subplots()
# #     ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
# #     st.pyplot(fig)

# # # =========================
# # # ZIP EXPORT
# # # =========================
# # def create_zip(data):
# #     zip_buffer = io.BytesIO()
# #     with zipfile.ZipFile(zip_buffer, "w") as z:
# #         for item in data:
# #             z.writestr(
# #                 f"{item['category']}/{item['file'].name}",
# #                 item["file"].getvalue()
# #             )
# #     return zip_buffer

# # if st.button("📦 Download Organized ZIP"):
# #     zip_data = create_zip(st.session_state.data)
# #     st.download_button(
# #         "Download ZIP",
# #         zip_data.getvalue(),
# #         file_name="SortedImages.zip"
# #     )

# # # =========================
# # # CLEAR ALL
# # # =========================
# # if st.button("🗑 Clear All"):
# #     st.session_state.data = []

# # =========================
# # HEADER INFO
# # =========================

# # =========================
# # UPLOAD
# # =========================
# # =========================
# # UPLOAD OPTIONS
# # =========================
# st.markdown("### 📤 Upload Images or Folder")

# MAX_FILES = 100

# uploaded_images = st.file_uploader(
#     "Upload Images",
#     type=["png", "jpg", "jpeg"],
#     accept_multiple_files=True
# )

# uploaded_zip = st.file_uploader(
#     "Upload Folder (ZIP)",
#     type=["zip"]
# )

# new_files = []

# # Handle direct images
# if uploaded_images:
#     new_files.extend(uploaded_images)

# # Handle ZIP folder
# if uploaded_zip:
#     with zipfile.ZipFile(uploaded_zip, "r") as z:
#         for file_name in z.namelist():
#             if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
#                 new_files.append(io.BytesIO(z.read(file_name)))

# # Limit check
# if len(st.session_state.data) + len(new_files) > MAX_FILES:
#     st.warning(f"⚠️ Maximum {MAX_FILES} images allowed")
#     new_files = new_files[:MAX_FILES - len(st.session_state.data)]

# # Process files
# if new_files:
#     existing_hashes = {item["hash"] for item in st.session_state.data}

#     for file in new_files:
#         try:
#             file_bytes = file.getvalue() if hasattr(file, "getvalue") else file.read()
#             file_hash = hashlib.md5(file_bytes).hexdigest()

#             if file_hash in existing_hashes:
#                 continue

#             image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
#             category, confidence = predict_image(io.BytesIO(file_bytes))

#             st.session_state.data.append({
#                 "file": file,
#                 "image": image,
#                 "category": category,
#                 "confidence": confidence,
#                 "hash": file_hash
#             })

#         except:
#             continue

# st.success(f"Total Images: {len(st.session_state.data)}")

# # =========================
# # SIDEBAR FILTERS
# # =========================
# st.sidebar.header("🔍 Filters")

# search = st.sidebar.text_input("Search filename")
# selected_category = st.sidebar.selectbox("Category", ["All"] + categories)
# low_conf_only = st.sidebar.checkbox("Low Confidence (<70%)")

# # =========================
# # FILTER LOGIC
# # =========================
# filtered_data = []

# for item in st.session_state.data:
#     if search and search.lower() not in item["file"].name.lower():
#         continue
#     if selected_category != "All" and item["category"] != selected_category:
#         continue
#     if low_conf_only and item["confidence"] >= 0.7:
#         continue
#     filtered_data.append(item)

# # =========================
# # GROUP BY CATEGORY
# # =========================
# grouped = {cat: [] for cat in categories}
# for item in filtered_data:
#     grouped[item["category"]].append(item)

# # =========================
# # DISPLAY COLUMNS (MAIN FIX)
# # =========================
# st.subheader("📂 Review & Edit")

# cat_cols = st.columns(len(categories))

# for idx, cat in enumerate(categories):
#     with cat_cols[idx]:
#         st.markdown(f"### {cat}")

#         for item in grouped[cat]:
#             border_class = "low-conf" if item["confidence"] < 0.7 else ""

#             st.markdown(f'<div class="card {border_class}">', unsafe_allow_html=True)

#             # IMAGE
#             st.image(item["image"], use_container_width=True)
#             st.caption(item["file"].name)

#             # ACTION ROW
#             col1, col2 = st.columns([3,1])

#             # CATEGORY CHANGE
#             with col1:
#                 new_cat = st.selectbox(
#                     "Move to",
#                     categories,
#                     index=categories.index(item["category"]),
#                     key=item["hash"]
#                 )
#                 item["category"] = new_cat

#             # DELETE BUTTON ❌
#             with col2:
#                 if st.button("🗑", key="del_"+item["hash"], help="Delete Image"):
#                     st.session_state.data = [
#                         i for i in st.session_state.data if i["hash"] != item["hash"]
#                     ]
#                     st.rerun()

#             st.write(f"Confidence: {item['confidence']*100:.1f}%")

#             st.markdown("</div>", unsafe_allow_html=True)

# # =========================
# # STATS (SMALL PIE)
# # =========================
# st.subheader("📊 Statistics")

# if st.session_state.data:
#     df = pd.DataFrame(st.session_state.data)
#     counts = df["category"].value_counts()

#     col1, col2 = st.columns([1,3])

#     with col1:
#         fig, ax = plt.subplots(figsize=(3,3))
#         ax.pie(counts, labels=counts.index, autopct='%1.1f%%')
#         st.pyplot(fig)

# # =========================
# # EXPORT SECTION
# # =========================
# st.subheader("💾 Export")

# def create_zip(data):
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w") as z:
#         for item in data:
#             z.writestr(
#                 f"{item['category']}/{item['file'].name}",
#                 item["file"].getvalue()
#             )
#     return zip_buffer

# col1, col2 = st.columns(2)

# with col1:
#     if st.button("📦 Download ZIP"):
#         zip_data = create_zip(st.session_state.data)
#         st.download_button(
#             "Download Organized Images",
#             zip_data.getvalue(),
#             file_name="SortedImages.zip"
#         )

# with col2:
#     if st.button("🗑 Clear All"):
#         st.session_state.data = []
#         st.rerun()import streamlit as st
# import streamlit as st
# from PIL import Image
# import io
# import zipfile
# import hashlib
# import pandas as pd
# import plotly.express as px
# import torch
# import torch.nn.functional as F
# import torchvision.transforms as transforms
# import timm

# st.set_page_config(
#     page_title="Smart Image Organizer",
#     page_icon="🧠",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # =========================
# # MODEL & UTILS (unchanged)
# # =========================
# @st.cache_resource
# def load_model():
#     model_path = "best_model.pth"
#     model = timm.create_model('efficientnet_b3', pretrained=False, num_classes=5)
#     model.load_state_dict(torch.load(model_path, map_location="cpu"))
#     model.eval()
#     return model

# model = load_model()

# categories = ["Documents", "Educational", "Others", "Personal", "Screenshots"]

# transform = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
# ])

# def predict_image(file_bytes: bytes):
#     image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
#     img = transform(image).unsqueeze(0)
#     with torch.no_grad():
#         outputs = model(img)
#         probs = F.softmax(outputs, dim=1)
#         confidence, predicted = torch.max(probs, 1)
#     return categories[predicted.item()], confidence.item()

# def get_hash(file_bytes: bytes):
#     return hashlib.md5(file_bytes).hexdigest()

# if "data" not in st.session_state:
#     st.session_state.data = []

# # =========================
# # MODERN CSS + MATERIAL ICONS (updated heading sizes)
# # =========================
# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

#     .stApp {
#         background: linear-gradient(135deg, #0f172a 0%, #1e2937 100%);
#         font-family: 'Inter', system-ui, sans-serif;
#     }
    
#     .main .block-container {
#         padding-top: 2rem;
#         padding-bottom: 3rem;
#     }
    
#     h1, h2, h3 {
#         font-weight: 700;
#         letter-spacing: -0.02em;
#     }
    
#     /* Card */
#     .card {
#         background: rgba(255,255,255,0.08);
#         border: 1px solid rgba(255,255,255,0.12);
#         border-radius: 24px;
#         padding: 20px;
#         backdrop-filter: blur(20px);
#         box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.15),
#                     0 4px 6px -4px rgb(0 0 0 / 0.15);
#         transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
#         margin-bottom: 24px;
#         overflow: hidden;
#     }
    
#     .card:hover {
#         transform: translateY(-6px) scale(1.03);
#         box-shadow: 25px 25px 30px -10px rgb(0 0 0 / 0.25),
#                     0 10px 15px -3px rgb(99 102 241);
#         border-color: rgba(99, 102, 241, 0.3);
#     }
    
#     /* Image */
#     div[data-testid="stImage"] img {
#         border-radius: 16px !important;
#         height: 210px !important;
#         object-fit: cover !important;
#         width: 100% !important;
#         transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
#     }
    
#     .card:hover div[data-testid="stImage"] img {
#         transform: scale(1.08);
#     }
    
#     /* Low confidence */
#     .low-conf {
#         border: 3px solid #f43f5e;
#         box-shadow: 0 0 0 6px rgba(244, 63, 94, 0.25);
#     }
    
#     /* Column scroll */
#     div[data-testid="column"] {
#         max-height: 82vh;
#         overflow-y: auto;
#         scrollbar-width: thin;
#         scrollbar-color: #64748b #1e2937;
#     }
    
#     /* Buttons */
#     .stButton > button {
#         background: linear-gradient(90deg, #6366f1, #a855f7);
#         border-radius: 9999px;
#         padding: 14px 28px;
#         font-weight: 600;
#         font-size: 1rem;
#         border: none;
#         box-shadow: 0 10px 15px -3px rgb(99 102 241);
#         transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
#         width: 100%;
#     }
    
#     .stButton > button:hover {
#         transform: translateY(-3px) scale(1.05);
#         box-shadow: 0 20px 25px -5px rgb(99 102 241);
#     }
    
#     /* Compact delete button */
#     .card .stButton > button {
#         background: #ef4444 !important;
#         box-shadow: 0 10px 15px -3px rgb(239 68 68) !important;
#         min-height: 42px !important;
#         width: 42px !important;
#         padding: 0 !important;
#         font-size: 1.55rem !important;
#         border-radius: 50% !important;
#         display: flex;
#         align-items: center;
#         justify-content: center;
#         margin: 4px auto 0 auto;
#     }
    
#     .card .stButton > button:hover {
#         transform: scale(1.12);
#         box-shadow: 0 15px 20px -3px rgb(239 68 68) !important;
#     }
    
#     /* Selectbox */
#     .stSelectbox > div > div {
#         border-radius: 16px !important;
#         border: 1px solid rgba(255,255,255,0.15) !important;
#         background: rgba(255,255,255,0.06) !important;
#     }
    
#     /* Badge */
#     .badge {
#         display: inline-flex;
#         align-items: center;
#         background: rgba(255,255,255,0.1);
#         color: #e2e8f0;
#         padding: 4px 14px;
#         border-radius: 9999px;
#         font-size: 0.875rem;
#         font-weight: 600;
#         letter-spacing: 0.5px;
#     }
    
#     /* Fade-in */
#     @keyframes fadeInUp {
#         from { opacity: 0; transform: translateY(20px); }
#         to { opacity: 1; transform: translateY(0); }
#     }
    
#     .card {
#         animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
#     }
    
#     /* Sidebar */
#     .stSidebar {
#         background: rgba(15, 23, 42, 0.95);
#         border-right: 1px solid rgba(255,255,255,0.1);
#     }
    
#     /* Material Icons */
#     .material-icons {
#         font-family: 'Material Icons';
#         font-weight: normal;
#         font-style: normal;
#         font-size: 24px;
#         line-height: 1;
#         letter-spacing: normal;
#         text-transform: none;
#         display: inline-block;
#         white-space: nowrap;
#         word-wrap: normal;
#         direction: ltr;
#         -webkit-font-feature-settings: 'liga';
#         -webkit-font-smoothing: antialiased;
#     }
# </style>
# """, unsafe_allow_html=True)

# # Load Material Icons font
# st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

# # =========================
# # HEADER
# # =========================
# st.markdown("""
# <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 32px;">
#     <div style="background: linear-gradient(135deg, #6366f1, #a855f7); width: 56px; height: 56px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 32px; box-shadow: 0 10px 15px -3px rgb(99 102 241); flex-shrink: 0;">
#         🧠
#     </div>
#     <div>
#         <h1 style="margin: 0; font-size: 2.75rem; background: linear-gradient(90deg, #e2e8f0, #cbd5e1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
#             Smart Image Organizer
#         </h1>
#         <p style="margin: 0; color: #94a3b8; font-size: 1.1rem; font-weight: 500;">AI-powered • Instant categorization • Zero hassle</p>
#     </div>
#     <div class="badge" style="margin-left: auto; background: #22c55e; color: #052e16;">
#         <span style="margin-right: 6px;">⚡</span> LIVE AI
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # =========================
# # UPLOAD SECTION
# # =========================
# st.markdown("### 📤 Upload Images or Folders")

# col_upload1, col_upload2 = st.columns([3, 2])

# with col_upload1:
#     uploaded_images = st.file_uploader(
#         "📸 Select images",
#         type=["png", "jpg", "jpeg"],
#         accept_multiple_files=True,
#         help="Supports PNG, JPG, JPEG"
#     )

# with col_upload2:
#     uploaded_zip = st.file_uploader(
#         "📁 Upload folder as ZIP",
#         type=["zip"],
#         help="All images inside the ZIP will be extracted"
#     )

# new_files = []

# if uploaded_images:
#     new_files.extend(uploaded_images)

# if uploaded_zip:
#     with zipfile.ZipFile(uploaded_zip, "r") as z:
#         for file_name in z.namelist():
#             if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
#                 file_bytes = z.read(file_name)
#                 bio = io.BytesIO(file_bytes)
#                 bio.name = file_name.split("/")[-1]
#                 new_files.append(bio)

# MAX_FILES = 100
# if len(st.session_state.data) + len(new_files) > MAX_FILES:
#     st.warning(f"⚠️ Maximum {MAX_FILES} images allowed per session")
#     new_files = new_files[:MAX_FILES - len(st.session_state.data)]

# if new_files:
#     existing_hashes = {item["hash"] for item in st.session_state.data}
    
#     with st.spinner("🔍 Analyzing images with AI..."):
#         for file in new_files:
#             try:
#                 file_bytes = file.getvalue() if hasattr(file, "getvalue") else file.read()
#                 file_hash = get_hash(file_bytes)
                
#                 if file_hash in existing_hashes:
#                     continue
                
#                 image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
#                 category, confidence = predict_image(file_bytes)
                
#                 st.session_state.data.append({
#                     "file": file,
#                     "image": image,
#                     "category": category,
#                     "confidence": confidence,
#                     "hash": file_hash
#                 })
#             except Exception:
#                 continue

# st.markdown(f"""
# <div style="text-align: center; margin: 24px 0;">
#     <div class="badge" style="font-size: 1.25rem; padding: 12px 32px; background: #6366f1; color: white;">
#         📸 {len(st.session_state.data)} images • AI organized
#     </div>
# </div>
# """, unsafe_allow_html=True)

# # =========================
# # SIDEBAR FILTERS
# # =========================
# with st.sidebar:
#     st.markdown("### 🔍 Filters")
#     search = st.text_input("Search by filename", placeholder="e.g. screenshot")
#     selected_category = st.selectbox("Category", ["All"] + categories)
#     low_conf_only = st.checkbox("Only low confidence (< 70%)")

# # =========================
# # FILTER LOGIC
# # =========================
# filtered_data = []
# for item in st.session_state.data:
#     if search and search.lower() not in item["file"].name.lower():
#         continue
#     if selected_category != "All" and item["category"] != selected_category:
#         continue
#     if low_conf_only and item["confidence"] >= 0.7:
#         continue
#     filtered_data.append(item)

# # =========================
# # GROUP BY CATEGORY
# # =========================
# grouped = {cat: [] for cat in categories}
# for item in filtered_data:
#     grouped[item["category"]].append(item)

# # =========================
# # DISPLAY – MODERN CATEGORY COLUMNS (REDUCED HEADING SIZE)
# # =========================
# st.markdown("""
# <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
#     <span style="font-size: 2rem;">📁</span>
#     <h2 style="margin: 0; font-size: 1.75rem; color: #e2e8f0;">Review &amp; Edit</h2>
# </div>
# """, unsafe_allow_html=True)

# cat_cols = st.columns(len(categories))

# # Modern Material UI icons
# icon_map = {
#     "Documents": "description",
#     "Educational": "school",
#     "Others": "widgets",
#     "Personal": "person",
#     "Screenshots": "screenshot"
# }

# for idx, cat in enumerate(categories):
#     with cat_cols[idx]:
#         # Modern category header - count placed UNDER the name
#         st.markdown(f"""
#         <div style="margin-bottom: 20px; text-align: center;">
#             <!-- Icon + Category Name -->
#             <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 8px;">
#                 <span class="material-icons" style="font-size: 1.75rem; color: #a5b4fc;">{icon_map[cat]}</span>
#                 <h2 style="margin: 0; font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">{cat}</h2>
#             </div>
            
#         </div>
#         """, unsafe_allow_html=True)
        
#         for item in grouped[cat]:
#             border_class = "low-conf" if item["confidence"] < 0.7 else ""
            
#             st.markdown(f'<div class="card {border_class}">', unsafe_allow_html=True)
            
#             st.image(item["image"], use_container_width=True)
#             st.caption(f"**{item['file'].name}**")
            
#             # Action row
#             col1, col2 = st.columns([4, 1])
            
#             with col1:
#                 new_cat = st.selectbox(
#                     "Move to",
#                     categories,
#                     index=categories.index(item["category"]),
#                     key=f"cat_{item['hash']}",
#                     label_visibility="collapsed"
#                 )
#                 item["category"] = new_cat
            
#             with col2:
#                 if st.button("🗑️", key=f"del_{item['hash']}", help="Delete this image"):
#                     st.session_state.data = [i for i in st.session_state.data if i["hash"] != item["hash"]]
#                     st.rerun()
            
#             # Confidence badge
#             conf_color = "#10b981" if item["confidence"] >= 0.7 else "#f43f5e"
#             st.markdown(f"""
#             <div style="display: inline-flex; align-items: center; gap: 6px; margin-top: 12px;">
#                 <span style="font-size: 1.1rem;">{item['confidence']*100:.1f}%</span>
#                 <span style="background: {conf_color}20; color: {conf_color}; padding: 2px 10px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600;">CONFIDENCE</span>
#             </div>
#             """, unsafe_allow_html=True)
            
#             st.markdown("</div>", unsafe_allow_html=True)

# # =========================
# # STATS
# # =========================
# st.markdown("### 📊 Statistics")

# if st.session_state.data:
#     df = pd.DataFrame(st.session_state.data)
#     counts = df["category"].value_counts().reset_index()
#     counts.columns = ["category", "count"]
    
#     fig = px.pie(
#         counts,
#         names="category",
#         values="count",
#         title="Distribution by Category",
#         color_discrete_sequence=px.colors.sequential.Viridis,
#         hole=0.4
#     )
    
#     fig.update_traces(
#         textposition="inside",
#         textinfo="percent+label",
#         hovertemplate="<b>%{label}</b><br>%{value} images<br>%{percent:.1%}<extra></extra>"
#     )
    
#     fig.update_layout(
#         showlegend=False,
#         margin=dict(t=40, b=20, l=20, r=20),
#         font=dict(family="Inter"),
#         plot_bgcolor="rgba(0,0,0,0)",
#         paper_bgcolor="rgba(0,0,0,0)"
#     )
    
#     st.plotly_chart(fig, use_container_width=True)

# # =========================
# # EXPORT + CLEAR
# # =========================
# st.markdown("### 💾 Export")

# def create_zip(data):
#     zip_buffer = io.BytesIO()
#     with zipfile.ZipFile(zip_buffer, "w") as z:
#         for item in data:
#             z.writestr(
#                 f"{item['category']}/{item['file'].name}",
#                 item["file"].getvalue() if hasattr(item["file"], "getvalue") else item["file"].read()
#             )
#     zip_buffer.seek(0)
#     return zip_buffer

# col_export1, col_export2 = st.columns([1, 1])

# with col_export1:
#     if st.button("📦 Download Organized ZIP", use_container_width=True):
#         if st.session_state.data:
#             zip_data = create_zip(st.session_state.data)
#             st.download_button(
#                 label="✅ Download SortedImages.zip",
#                 data=zip_data.getvalue(),
#                 file_name="SortedImages.zip",
#                 mime="application/zip",
#                 use_container_width=True
#             )
#         else:
#             st.warning("No images to export")

# with col_export2:
#     if st.button("🗑️ Clear All Images", use_container_width=True, type="secondary"):
#         st.session_state.data = []
#         st.rerun()


import streamlit as st
from PIL import Image
import io
import zipfile
import hashlib
import pandas as pd
import plotly.express as px
import torch
import torch.nn.functional as F
import torchvision.transforms as transforms
import timm

st.set_page_config(
    page_title="Smart Image Organizer",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# MODEL & UTILS (unchanged)
# =========================
@st.cache_resource
def load_model():
    model_path = "best_model.pth"
    model = timm.create_model('efficientnet_b3', pretrained=False, num_classes=5)
    model.load_state_dict(torch.load(model_path, map_location="cpu"))
    model.eval()
    return model

model = load_model()

categories = ["Documents", "Educational", "Others", "Personal", "Screenshots"]

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

def predict_image(file_bytes: bytes):
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    img = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(img)
        probs = F.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probs, 1)
    return categories[predicted.item()], confidence.item()

def get_hash(file_bytes: bytes):
    return hashlib.md5(file_bytes).hexdigest()

if "data" not in st.session_state:
    st.session_state.data = []

# =========================
# MODERN CSS + MATERIAL ICONS
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e2937 100%);
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }
    
    h1, h2, h3 {
        font-weight: 700;
        letter-spacing: -0.02em;
    }
    
    /* Card */
    .card {
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 24px;
        padding: 20px;
        backdrop-filter: blur(20px);
        box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.15),
                    0 4px 6px -4px rgb(0 0 0 / 0.15);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        margin-bottom: 24px;
        overflow: hidden;
    }
    
    .card:hover {
        transform: translateY(-6px) scale(1.03);
        box-shadow: 25px 25px 30px -10px rgb(0 0 0 / 0.25),
                    0 10px 15px -3px rgb(99 102 241);
        border-color: rgba(99, 102, 241, 0.3);
    }
    
    /* Image */
    div[data-testid="stImage"] img {
        border-radius: 16px !important;
        height: 210px !important;
        object-fit: cover !important;
        width: 100% !important;
        transition: transform 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
    }
    
    .card:hover div[data-testid="stImage"] img {
        transform: scale(1.08);
    }
    
    /* Low confidence */
    .low-conf {
        border: 3px solid #f43f5e;
        box-shadow: 0 0 0 6px rgba(244, 63, 94, 0.25);
    }
    
    /* Column scroll */
    div[data-testid="column"] {
        max-height: 82vh;
        overflow-y: auto;
        scrollbar-width: thin;
        scrollbar-color: #64748b #1e2937;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #6366f1, #a855f7);
        border-radius: 9999px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 1rem;
        border: none;
        box-shadow: 0 10px 15px -3px rgb(99 102 241);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 20px 25px -5px rgb(99 102 241);
    }
    
    /* Compact delete button */
    .card .stButton > button {
        background: #ef4444 !important;
        box-shadow: 0 10px 15px -3px rgb(239 68 68) !important;
        min-height: 42px !important;
        width: 42px !important;
        padding: 0 !important;
        font-size: 1.55rem !important;
        border-radius: 50% !important;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 4px auto 0 auto;
    }
    
    .card .stButton > button:hover {
        transform: scale(1.12);
        box-shadow: 0 15px 20px -3px rgb(239 68 68) !important;
    }
    
    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 16px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        background: rgba(255,255,255,0.06) !important;
    }
    
    /* Badge */
    .badge {
        display: inline-flex;
        align-items: center;
        background: rgba(255,255,255,0.1);
        color: #e2e8f0;
        padding: 4px 14px;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    
    /* Fade-in */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .card {
        animation: fadeInUp 0.5s cubic-bezier(0.4, 0, 0.2, 1) forwards;
    }
    
    /* Sidebar */
    .stSidebar {
        background: rgba(15, 23, 42, 0.95);
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Material Icons */
    .material-icons {
        font-family: 'Material Icons';
        font-weight: normal;
        font-style: normal;
        font-size: 24px;
        line-height: 1;
        letter-spacing: normal;
        text-transform: none;
        display: inline-block;
        white-space: nowrap;
        word-wrap: normal;
        direction: ltr;
        -webkit-font-feature-settings: 'liga';
        -webkit-font-smoothing: antialiased;
    }
</style>
""", unsafe_allow_html=True)

# Load Material Icons font
st.markdown('<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">', unsafe_allow_html=True)

# =========================
# HEADER
# =========================
st.markdown("""
<div style="display: flex; align-items: center; gap: 16px; margin-bottom: 32px;">
    <div style="background: linear-gradient(135deg, #6366f1, #a855f7); width: 56px; height: 56px; border-radius: 20px; display: flex; align-items: center; justify-content: center; font-size: 32px; box-shadow: 0 10px 15px -3px rgb(99 102 241); flex-shrink: 0;">
        🧠
    </div>
    <div>
        <h1 style="margin: 0; font-size: 2.75rem; background: linear-gradient(90deg, #e2e8f0, #cbd5e1); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
            Smart Image Organizer
        </h1>
        <p style="margin: 0; color: #94a3b8; font-size: 1.1rem; font-weight: 500;">AI-powered • Instant categorization • Zero hassle</p>
    </div>
    <div class="badge" style="margin-left: auto; background: #22c55e; color: #052e16;">
        <span class="material-icons" style="margin-right: 6px; font-size: 1.1rem;">bolt</span> LIVE AI
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# UPLOAD SECTION - TWO CLEAR OPTIONS (Material Icons)
# =========================
st.markdown("### 📤 Choose Upload Method")

upload_col1, upload_col2 = st.columns(2)

new_files = []

with upload_col1:
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; text-align: center; 
                padding: 28px 20px; background: rgba(255,255,255,0.06); border-radius: 24px; 
                border: 2px solid rgba(99,102,241,0.25); transition: all 0.3s ease;">
        <span class="material-icons" style="font-size: 3.8rem; color: #6366f1; margin-bottom: 16px;">photo_library</span>
        <h3 style="margin: 0 0 8px 0; color: #e2e8f0; font-size: 1.4rem;">Individual Images</h3>
        <p style="color: #94a3b8; margin-bottom: 20px;">Upload multiple PNG, JPG, or JPEG files</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_images = st.file_uploader(
        "Select images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        help="Supports PNG, JPG, JPEG",
        label_visibility="collapsed"
    )
    
    if uploaded_images:
        new_files.extend(uploaded_images)

with upload_col2:
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; text-align: center; 
                padding: 28px 20px; background: rgba(255,255,255,0.06); border-radius: 24px; 
                border: 2px solid rgba(99,102,241,0.25); transition: all 0.3s ease;">
        <span class="material-icons" style="font-size: 3.8rem; color: #6366f1; margin-bottom: 16px;">folder_zip</span>
        <h3 style="margin: 0 0 8px 0; color: #e2e8f0; font-size: 1.4rem;">Entire Folder (ZIP)</h3>
        <p style="color: #94a3b8; margin-bottom: 20px;">Upload a ZIP file containing images</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_zip = st.file_uploader(
        "Upload folder as ZIP",
        type=["zip"],
        help="All images inside the ZIP will be extracted automatically",
        label_visibility="collapsed"
    )
    
    if uploaded_zip:
        with zipfile.ZipFile(uploaded_zip, "r") as z:
            for file_name in z.namelist():
                if file_name.lower().endswith((".png", ".jpg", ".jpeg")):
                    file_bytes = z.read(file_name)
                    bio = io.BytesIO(file_bytes)
                    bio.name = file_name.split("/")[-1]
                    new_files.append(bio)

# =========================
# PROCESS UPLOADED FILES
# =========================
MAX_FILES = 100
if len(st.session_state.data) + len(new_files) > MAX_FILES:
    st.warning(f"⚠️ Maximum {MAX_FILES} images allowed per session")
    new_files = new_files[:MAX_FILES - len(st.session_state.data)]

if new_files:
    existing_hashes = {item["hash"] for item in st.session_state.data}
    
    with st.spinner("🔍 Analyzing images with AI..."):
        for file in new_files:
            try:
                file_bytes = file.getvalue() if hasattr(file, "getvalue") else file.read()
                file_hash = get_hash(file_bytes)
                
                if file_hash in existing_hashes:
                    continue
                
                image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
                category, confidence = predict_image(file_bytes)
                
                st.session_state.data.append({
                    "file": file,
                    "image": image,
                    "category": category,
                    "confidence": confidence,
                    "hash": file_hash
                })
            except Exception:
                continue

st.markdown(f"""
<div style="text-align: center; margin: 24px 0;">
    <div class="badge" style="font-size: 1.25rem; padding: 12px 32px; background: #6366f1; color: white;">
        <span class="material-icons" style="margin-right: 8px; font-size: 1.4rem;">photo_camera</span>
        {len(st.session_state.data)} images • AI organized
    </div>
</div>
""", unsafe_allow_html=True)

# =========================
# SIDEBAR FILTERS
# =========================
with st.sidebar:
    st.markdown("### 🔍 Filters")
    search = st.text_input("Search by filename", placeholder="e.g. screenshot")
    selected_category = st.selectbox("Category", ["All"] + categories)
    low_conf_only = st.checkbox("Only low confidence (< 70%)")

# =========================
# FILTER LOGIC
# =========================
filtered_data = []
for item in st.session_state.data:
    if search and search.lower() not in item["file"].name.lower():
        continue
    if selected_category != "All" and item["category"] != selected_category:
        continue
    if low_conf_only and item["confidence"] >= 0.7:
        continue
    filtered_data.append(item)

# =========================
# GROUP BY CATEGORY
# =========================
grouped = {cat: [] for cat in categories}
for item in filtered_data:
    grouped[item["category"]].append(item)

# =========================
# DISPLAY – REVIEW & EDIT (Material Icon)
# =========================
st.markdown("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
    <span class="material-icons" style="font-size: 2.5rem; color: #a5b4fc;">folder_open</span>
    <h2 style="margin: 0; font-size: 1.75rem; color: #e2e8f0;">Review &amp; Edit</h2>
</div>
""", unsafe_allow_html=True)

cat_cols = st.columns(len(categories))

icon_map = {
    "Documents": "description",
    "Educational": "school",
    "Others": "widgets",
    "Personal": "person",
    "Screenshots": "screenshot"
}

for idx, cat in enumerate(categories):
    with cat_cols[idx]:
        # Category header with count UNDER the name
        st.markdown(f"""
        <div style="margin-bottom: 20px; text-align: center;">
            <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 8px;">
                <span class="material-icons" style="font-size: 1.75rem; color: #a5b4fc;">{icon_map[cat]}</span>
                <h2 style="margin: 0; font-size: 1.1rem; color: #e2e8f0; font-weight: 600;">{cat}</h2>
            </div>
            <div style="background: rgba(255,255,255,0.1); 
                        color: #e2e8f0; 
                        padding: 4px 14px; 
                        border-radius: 9999px; 
                        font-size: 0.85rem; 
                        font-weight: 600; 
                        display: inline-block;">
                {len(grouped[cat])} images
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        for item in grouped[cat]:
            border_class = "low-conf" if item["confidence"] < 0.7 else ""
            
            st.markdown(f'<div class="card {border_class}">', unsafe_allow_html=True)
            
            st.image(item["image"], use_container_width=True)
            st.caption(f"**{item['file'].name}**")
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                new_cat = st.selectbox(
                    "Move to",
                    categories,
                    index=categories.index(item["category"]),
                    key=f"cat_{item['hash']}",
                    label_visibility="collapsed"
                )
                item["category"] = new_cat
            
            with col2:
                if st.button("🗑️", key=f"del_{item['hash']}", help="Delete this image"):
                    st.session_state.data = [i for i in st.session_state.data if i["hash"] != item["hash"]]
                    st.rerun()
            
            conf_color = "#10b981" if item["confidence"] >= 0.7 else "#f43f5e"
            st.markdown(f"""
            <div style="display: inline-flex; align-items: center; gap: 6px; margin-top: 12px;">
                <span style="font-size: 1.1rem;">{item['confidence']*100:.1f}%</span>
                <span style="background: {conf_color}20; color: {conf_color}; padding: 2px 10px; border-radius: 9999px; font-size: 0.8rem; font-weight: 600;">CONFIDENCE</span>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)

# =========================
# STATS
# =========================
st.markdown("### 📊 Statistics")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)
    counts = df["category"].value_counts().reset_index()
    counts.columns = ["category", "count"]
    
    fig = px.pie(
        counts,
        names="category",
        values="count",
        title="Distribution by Category",
        color_discrete_sequence=px.colors.sequential.Viridis,
        hole=0.4
    )
    
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>%{value} images<br>%{percent:.1%}<extra></extra>"
    )
    
    fig.update_layout(
        showlegend=False,
        margin=dict(t=40, b=20, l=20, r=20),
        font=dict(family="Inter"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    st.plotly_chart(fig, use_container_width=True)

# =========================
# EXPORT + CLEAR
# =========================
st.markdown("### 💾 Export")

def create_zip(data):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as z:
        for item in data:
            z.writestr(
                f"{item['category']}/{item['file'].name}",
                item["file"].getvalue() if hasattr(item["file"], "getvalue") else item["file"].read()
            )
    zip_buffer.seek(0)
    return zip_buffer

col_export1, col_export2 = st.columns([1, 1])

with col_export1:
    if st.button("📦 Download Organized ZIP", use_container_width=True):
        if st.session_state.data:
            zip_data = create_zip(st.session_state.data)
            st.download_button(
                label="✅ Download SortedImages.zip",
                data=zip_data.getvalue(),
                file_name="SortedImages.zip",
                mime="application/zip",
                use_container_width=True
            )
        else:
            st.warning("No images to export")

with col_export2:
    if st.button("🗑️ Clear All Images", use_container_width=True, type="secondary"):
        st.session_state.data = []
        st.rerun()