import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image


# Write / text
st.title("My First App!")

st.header("This is a Streamlit demo 👨‍💻")

st.markdown("""We can write **text** in **:red[markdown]**  
making use of *custom* :green[styles],  
formulas $\sqrt{x^2+y^4}=z$ and more! 🚀""")


# Data display
st.subheader("Random companies dataframe performance")

np.random.seed(0)
df = pd.DataFrame(np.random.randn(40, 3) + np.array([3, 5, 10]), 
                columns=("Company A", "Company B", "Company C"),
                index=[datetime.today().date() - timedelta(days=x) for x in range(40,0,-1)])

with st.expander("Check data table"):
    st.dataframe(df)


# Charts
st.subheader("Perfomance Chart")

n_days = st.slider("Input: Select the number of days to plot", 1, len(df))  # Input
plot_companies = st.multiselect("Input: Displayed companies", 
                                options=list(df.columns), 
                                default=list(df.columns))

st.line_chart(df.iloc[len(df)-n_days:][plot_companies])


# Media
st.subheader("Media elements")

cols = st.columns(2)

with cols[0]:
    image = Image.open("./landscape.png")
    st.image(image)

with cols[1]:
    # st.button("Click here to see other Zishan's Repositories", on_click=open_website, "https://github.com/zishanyusuf?tab=repositories")
    link = '[Zishan GitHub](https://github.com/zishanyusuf?tab=repositories)'
    st.markdown(link, unsafe_allow_html=True)
    #st.button("Click here to see other Zishan's Repositories", st.markdown(link, unsafe_allow_html=True))