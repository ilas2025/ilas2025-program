import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Speech Information - ILAS2025",
    page_icon="logomap/favicon.ico",  # Path to your icon file
    layout="wide"
)

# --- Helper: Create URL-safe anchor from TITLE ---
def slugify(title):
    slug = re.sub(r'[^a-zA-Z0-9]+', '-', str(title).lower()).strip('-')
    return slug
def make_clickable(link):
    return f'<a href="{link}">{link[1::]}</a>'
# --- Load Data ---
df = pd.read_csv("srp-full.csv")

minis={
    "MS1":	"Embracing new opportunities in numerical linear algebra",
"MS2": 	"Combinatorial matrix theory",
"MS3":	"Matrix inequalities with applications",
"MS4":	"Linear algebra methods for inverse problems and data assimilation",
"MS5":	"Advances in matrix equations: Theory, computations, and applications",
"MS6":	"Model reduction",
"MS7":	"Linear algebra and quantum information science",
"MS8":	"Tensor and quantum information science",
"MS9":	"Total positivity",
"MS10":	"Matrix means and related topics",
"MS11":	"Structured matrix computations and its applications",
"MS12":	"Preserver problems, I",
"MS13":	"Advances in QR factorizations",
"MS14":	"Pencils, polynomial, and rational matrices",
"MS15":	"Graphs and their eigenvalues: Celebrating the work of Fan Chung Graham",
"MS16":	"Approximations and errors in Krylov-based solvers",
"MS17":	"Graphs and matrices in honor of Leslie Hogben's retirement",
"MS18":	"New methods in numerical multilinear algebra",
"MS19":	"Explicit and hidden asymptotic structures, GLT Analysis, and applications",
"MS20":	"Manifold learning and statistical applications",
"MS21":	"Linear algebra techniques in graph theory",
"MS22":	"Linear algebra applications in computational geometry",
"MS23":	"Advances in Krylov subspace methods and their applications",
"MS24":	"Nonnegative and related families of matrices",
"MS25":	"Enumerative/algebraic combinatorics and matrices",
"MS26":	"Utilizing structure to achieve low-complexity algorithms for data science, engineering, and physics",
"MS27":	"Linear algebra education",
"MS28":	"From matrix theory to Euclidean Jordan algebras, FTvN systems, and beyond",
"MS29":	"Matrix functions and related topics",
"MS30":	"Bohemian matrices: Theory, applications, and explorations",
"MS31":	"Matrix decompositions and applications",
"MS32":	"Advances in matrix manifold optimization",
"MS33":	"Norms of matrices, numerical range, applications of functional analysis to matrix theory",
"MS34":	"Combinatorics, association scheme, and graphs",
"MS35":	"Preserver Problems, II"
}
for key, value in minis.items():
    df["TYPE"][df["TYPE"]==key]=key+" : "+value
# Define columns
summary_columns = ["WEEKDAY", "START_STR", "END_STR", "SESSION", "FULL_NAME", "TYPE", "ROOM"]
detail_columns = summary_columns + ["TITLE", "ABSTRACT"]

# Weekday sort order
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekdays_in_data = df['WEEKDAY'].dropna().unique()
weekdays_sorted = [day for day in weekday_order if day in weekdays_in_data]

# Sidebar Navigation
page = st.sidebar.radio("Select Page", [
    "Filter by Weekday & Time", 
    "Filter by Weekday & Session",
    "Filter by Name",
    "Filter by Type(Topic)",
])
st.title("ILAS2025 Speech Information")

# --- Filtering Logic ---
if page == "Filter by Weekday & Time":    
    selected_weekday = st.sidebar.selectbox("Select Weekday", weekdays_sorted)
    weekday_df = df[df['WEEKDAY'] == selected_weekday]
    show_all_times = st.sidebar.checkbox("Show all times for this weekday", value=True)

    if show_all_times:
        filtered_df = weekday_df
    else:
        times = weekday_df['START_STR'].dropna().unique()
        selected_time = st.sidebar.selectbox("Select Start Time", sorted(times))
        filtered_df = weekday_df[weekday_df['START_STR'] == selected_time]
    filtered_df = filtered_df.sort_values("ROOM").reset_index(drop=True)
    filtered_df = filtered_df.sort_values("SESSION_ORDER").reset_index(drop=True)
    

elif page == "Filter by Weekday & Session":
    selected_weekday = st.sidebar.selectbox("Select Weekday", weekdays_sorted)
    weekday_df = df[df['WEEKDAY'] == selected_weekday]
    sessions = weekday_df['SESSION'].dropna().unique()
    selected_session = st.sidebar.selectbox("Select Session", sorted(sessions))
    filtered_df = weekday_df[weekday_df['SESSION'] == selected_session]
    filtered_df = filtered_df.sort_values("START_STR").reset_index(drop=True)
    filtered_df = filtered_df.sort_values("S_ORDER").reset_index(drop=True)

elif page == "Filter by Name":
    name_query = st.sidebar.text_input("Enter part of a name", "").strip()
    if name_query:
        filtered_df = df[df['FULL_NAME'].str.contains(name_query, case=False, na=False)]
    else:
        st.info("Please enter a name to search.")
        filtered_df = pd.DataFrame(columns=df.columns)
        filtered_df = filtered_df.sort_values("START_STR").reset_index(drop=True)
elif page == "Filter by Type(Topic)":
    selected_weekday = st.sidebar.selectbox("Select Weekday", weekdays_sorted)
    weekday_df = df[df['WEEKDAY'] == selected_weekday]
    
    selected_type = st.sidebar.selectbox("Select Type(Topic)", sorted(df['TYPE'].dropna().unique()))
    weekday_df = weekday_df[weekday_df['TYPE'] == selected_type]
    show_all_times = st.sidebar.checkbox("Show all times for this weekday", value=True)
    if show_all_times:
        filtered_df = weekday_df
    else:
        times = weekday_df['START_STR'].dropna().unique()
        selected_time = st.sidebar.selectbox("Select Start Time", sorted(times))
        filtered_df = weekday_df[weekday_df['START_STR'] == selected_time]
    
    filtered_df = filtered_df.sort_values("ROOM").reset_index(drop=True)
    filtered_df = filtered_df.sort_values("SESSION_ORDER").reset_index(drop=True)

# --- Sort and Generate Anchors ---

# Generate anchor slugs from titles
slugs = {}
anchor_links = []

for title in filtered_df["TITLE"]:
    base_slug = slugify(title)
    slug = base_slug
    count = 1
    while slug in slugs:
        slug = f"{base_slug}-{count}"
        count += 1
    slugs[slug] = True
    anchor_links.append(slug)

filtered_df["ANCHOR"] = anchor_links
show_table = st.checkbox("Show Schedule Overview Table", value=True)

# --- Display Table ---
if not filtered_df.empty:
    if show_table:

        st.subheader("Schedule Overview")
        st.markdown("<div id='schedule-overview'></div>", unsafe_allow_html=True)

        summary_table = filtered_df[summary_columns + ["ANCHOR"]].copy()
        summary_table["ANCHOR"] = summary_table["ANCHOR"].apply(lambda x: f"#{x}")
        summary_table['ANCHOR'] = summary_table['ANCHOR'].apply(make_clickable)
        summary_table = summary_table.rename(columns={
            "WEEKDAY": "Day",
            "START_STR": "Start Time",
            "END_STR": "End Time",
            "SESSION": "Session",
            "FULL_NAME": "Presenter",
            "TYPE": "Type",
            "ROOM": "Room",
            "Link": "Details"
        })

        st.write(summary_table.to_html(escape=False), unsafe_allow_html=True)
        st.markdown("---")
    st.subheader("Detailed Information")

    for _, row in filtered_df.iterrows():
        st.markdown(f"<div id='{row['ANCHOR']}'></div>", unsafe_allow_html=True)
        st.markdown(f"### {row['TITLE']}")
        st.write(f"**Session:** {row['SESSION']}, **Type:** {row['TYPE']}, **Time:** {row['START_STR']}–{row['END_STR']}, **Room:** {row['ROOM']}")
        st.write(f"**Presenter:** {row['FULL_NAME']}")
        st.markdown("**Abstract:**")
        st.markdown(row['ABSTRACT'], unsafe_allow_html=True)
        st.markdown("[🔝](#schedule-overview)")
        st.markdown("---")
else:
    if page != "Filter by Name" or name_query:
        st.warning("No results found.")
