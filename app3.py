import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from mpl_toolkits.mplot3d import Axes3D

# Setup
st.set_page_config(page_title="📊 Student Performance Explorer", layout="wide")
st.title("📚 Student Performance Analysis")

# Optional banner image
try:
    image = Image.open("image1.png")
    # Resize the image (width, height) in pixels
    resized_image = image.resize((600, 600))  # You can adjust the size as needed

    # Display the resized image
    st.image(resized_image, caption="🎓 Student Success Starts with Data", use_container_width=False)
    # st.image(image, caption="Student Success Starts with Data", use_column_width=True)
except:
    st.warning("Optional image not found.")

# Load data
df = pd.read_csv("D:/PROGRAMMING/Python (College)/Python Jupyter/ESE - 3/data.csv")
df['SES_Group'] = pd.cut(df['Socioeconomic_Score'], bins=[0, 0.3, 0.6, 1.0], labels=['Low', 'Medium', 'High'])

# Dataset preview
st.subheader("🔍 Dataset Preview")
st.dataframe(df.head())

# Dataset info
st.subheader("📋 Dataset Summary")
col1, col2 = st.columns(2)

with col1:
    st.write("**Missing Values:**")
    st.dataframe(df.isnull().sum())

with col2:
    st.write("**Data Types:**")
    info_table = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.values,
        'Non-Null Count': df.notnull().sum().values
    })
    st.dataframe(info_table)

st.write("**Descriptive Statistics**")
st.dataframe(df.describe())

# --- Static Visualizations with Insights --- 
st.markdown("## 🔒 Predefined Data Insights")

# Grade Distribution
with st.expander("📊 1. Bar Chart – Grade Distribution"):
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.countplot(x='Grades', data=df, palette='coolwarm', ax=ax1)
    ax1.set_title("Grade Distribution")
    ax1.set_xlabel("Grades")
    ax1.set_ylabel("Number of Students")
    plt.xticks(rotation=90)
    st.pyplot(fig1)
    
    st.write("""
    **Observation:**
    - Most students scored between 30 and 50.
    - Very few students scored extremely high (above 70).
    - The distribution is slightly left-skewed, suggesting many students perform moderately but few achieve high grades.
    
    **Insight:**
    - This indicates that while average performance is stable, interventions could be targeted to help more students reach higher academic levels.
    """)

# SES Pie Chart
with st.expander("🥧 2. Pie Chart – Socioeconomic Status (SES)"):
    ses_counts = df['SES_Group'].value_counts().sort_index()
    fig2, ax2 = plt.subplots()
    ax2.pie(ses_counts, labels=ses_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    ax2.set_title("Socioeconomic Status Groups")
    st.pyplot(fig2)
    
    st.write("""
    **Observation:**
    - The dataset consists of three SES groups: Low, Medium, and High.
    - The Medium SES group forms the majority, followed by High, with a smaller portion from the Low SES category.
    
    **Insight:**
    - Socioeconomic background is skewed towards better-off groups. This could influence access to study resources, leading to better academic performance.
    """)

# Study & Sleep by Grade Line Chart
with st.expander("📈 3. Line Chart – Average Study and Sleep Hours by Grade"):
    avg_hours = df.groupby('Grades')[['Study_Hours', 'Sleep_Hours']].mean().reset_index()
    fig3, ax3 = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=avg_hours, x='Grades', y='Study_Hours', label='Study Hours', marker='o', ax=ax3)
    sns.lineplot(data=avg_hours, x='Grades', y='Sleep_Hours', label='Sleep Hours', marker='o', ax=ax3)
    ax3.set_title("Average Study and Sleep Hours by Grade")
    ax3.set_xlabel("Grades")
    ax3.set_ylabel("Hours")
    ax3.legend()
    st.pyplot(fig3)

    st.write("""
    **Observation:**
    - Study hours increase with higher grades, peaking around the highest grades.
    - Sleep hours decrease slightly as grades improve.
    
    **Insight:**
    - Higher-performing students tend to study more and may sacrifice some sleep. A balanced schedule, however, is still essential for long-term success and mental health.
    """)

# Study Hours vs Grades Scatter Plot
with st.expander("⚫ 4. Scatter Plot – Study Hours vs Grades"):
    fig4, ax4 = plt.subplots()
    sns.scatterplot(data=df, x='Study_Hours', y='Grades', hue='SES_Group', palette='Set2', ax=ax4)
    ax4.set_title("Study Hours vs Grades")
    ax4.set_xlabel("Study Hours")
    ax4.set_ylabel("Grades")
    ax4.legend()
    st.pyplot(fig4)

    st.write("""
    **Observation:**
    - There's a positive correlation between study hours and grades.
    - Students from the High SES group tend to have higher study hours and better grades.
    
    **Insight:**
    - Increased study time generally results in better grades. Students from higher SES backgrounds may also benefit from fewer distractions and more study resources.
    """)

# Attendance vs Grades Scatter Plot
with st.expander("🔵 5. Scatter Plot – Attendance vs Grades"):
    fig5, ax5 = plt.subplots()
    sns.scatterplot(data=df, x='Attendance', y='Grades', hue='SES_Group', palette='Set1', ax=ax5)
    ax5.set_title("Attendance vs Grades")
    ax5.set_xlabel("Attendance (%)")
    ax5.set_ylabel("Grades")
    ax5.legend()
    st.pyplot(fig5)

    st.write("""
    **Observation:**
    - A moderate positive trend is seen: students with higher attendance often achieve better grades.
    - Students with lower attendance are mostly clustered in the lower grade range.
    
    **Insight:**
    - Regular attendance plays a crucial role in academic success. It reflects consistent engagement, which likely leads to better performance.
    """)

# --- Interactive Graph Generator ---
st.markdown("## 🎛️ Interactive Chart Generator")

x_col = st.selectbox("Select X-Axis", df.columns)
y_col = st.selectbox("Select Y-Axis", df.columns)
z_col = st.selectbox("Select Z-Axis (for 3D plots)", df.columns)

chart_type = st.selectbox(
    "Choose Chart Type", 
    ["Line Chart", "Bar Chart", "Scatter Chart", "Pie Chart", "3D Line", "3D Scatter", "3D Bar"]
)

fig = plt.figure(figsize=(10, 6))

# 2D Charts
if chart_type == "Line Chart":
    plt.plot(df[x_col], df[y_col], marker='o', label=f"{y_col} vs {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{chart_type}")
    plt.legend()

elif chart_type == "Bar Chart":
    plt.bar(df[x_col], df[y_col], color='skyblue', label=y_col)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{chart_type}")
    plt.legend()

elif chart_type == "Scatter Chart":
    plt.scatter(df[x_col], df[y_col], color='green', label=f"{y_col} vs {x_col}")
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title(f"{chart_type}")
    plt.legend()

elif chart_type == "Pie Chart":
    pie_data = df[y_col].value_counts()
    plt.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%', startangle=90)
    plt.title(f"Pie Chart of {y_col}")
    plt.legend(pie_data.index)

# 3D Charts
elif "3D" in chart_type:
    ax = fig.add_subplot(111, projection='3d')
    if chart_type == "3D Line":
        ax.plot(df[x_col], df[y_col], df[z_col], marker='o', label='3D Line')
    elif chart_type == "3D Scatter":
        ax.scatter(df[x_col], df[y_col], df[z_col], marker='o', label='3D Scatter', c='r')
    elif chart_type == "3D Bar":
        ax.bar3d(df[x_col], df[y_col], 0, 0.1, 0.1, df[z_col], label='3D Bar', color='orange')
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)
    ax.set_title(chart_type)
    ax.legend()

st.pyplot(fig)



# Final Insights
st.markdown("## ✅ Overall Conclusion")

# Create two columns for side-by-side display
col1, col2 = st.columns(2)

# First Image in the first column
with col1:
    try:
        image1 = Image.open("image.png")  # Replace with your first image file path
        resized_image1 = image1.resize((600, 600))  # Resize if needed
        st.image(resized_image1, use_container_width=False)
    except FileNotFoundError:
        st.warning("🚫 Image1 not found. Please check the file path.")

# Second Image in the second column
with col2:
    try:
        image2 = Image.open("image2.png")  # Replace with your second image file path
        resized_image2 = image2.resize((600, 600))  # Resize if needed
        st.image(resized_image2, use_container_width=False)
    except FileNotFoundError:
        st.warning("🚫 Image2 not found. Please check the file path.")

st.success("""
- 📚 Students with higher study hours and attendance generally score better grades.
- 💰 Socioeconomic status impacts access to learning, showing a link to performance.
- 🧠 Balanced sleep, study time, and school attendance are key success factors.
- 📊 This dashboard helps identify patterns and plan targeted interventions for students.
""")
