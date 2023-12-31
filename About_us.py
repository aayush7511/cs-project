import streamlit as st

st.set_page_config(page_title="About Us", layout="centered")

with st.container():
    c1, c2 = st.columns(2)
    with c1:
        st.title(":rainbow[At Stratton Oakmont, we're changing the way people think about banking] ")

    with c2:
        st.image("https://pics.craiyon.com/2023-10-19/b6313e9dc310438382783ca5a1e8ff60.webp")
st.divider()
with st.container():
    c3, c4, c5 = st.columns(3)
    with c4:
        st.title(":rainbow[Our Vision]")

with st.container():
    c6, c7, c8 = st.columns([0.2, 0.7, 0.1])

    with c7:
        st.subheader(
            "To be the preferred financial partner, driving prosperity and growth for our customers and communities.")

st.divider()
with st.container():
    st.title(":rainbow[Our Core Values]")
    st.write(
        "****Customer-Centric****: Our customers are at the heart of everything we do. We are committed to understanding their needs and exceeding their expectations.")
    st.write(
        "****Integrity****: We operate with the highest standards of honesty and transparency. Trust is earned, and we work diligently to maintain it.")
    st.write(
        "****Innovation****: Embracing change and technology allows us to offer modern, efficient, and secure banking solutions.")
    st.write(
        "****Teamwork****: Collaborative efforts drive our success. We encourage a supportive and inclusive environment that values the diversity of our team.")

st.divider()

with st.container():
    c12, c13, c14 = st.columns(3)

    with c13:
        st.title(":rainbow[Services]")
with st.container():
    c9, c10, c11 = st.columns(3)

    with c9:
        with st.container(border=True):
            st.title(":orange[Personal Banking]")
    with c10:
        with st.container(border=True):
            st.title(":orange[Loans and Mortgages]")
    with c11:
        with st.container(border=True):
            st.title(":orange[Online Banking]")

st.divider()

with st.container():
    c15, c16 = st.columns(2)

    with c15:
        st.image("https://freeurcloset.files.wordpress.com/2013/09/suits-6.jpg?w=584", caption="Harvey Specter")
        c17, c18 = st.columns([0.25, 0.75])
        with c18:
            st.write(":gray[**Chief Executive Officer**]")

        st.image("https://i.pinimg.com/736x/a2/cf/5b/a2cf5bab90b5372a010e81d2be7c808e.jpg",caption="Mike Ross")

        c22,c23 = st.columns([0.2, 0.8])

        with c23:
            st.write(":gray[Assistant General Manager]")



    with c16:
        st.image("https://hips.hearstapps.com/hmg-prod/images/gina-torre-suits-64f216a1c7c44.jpg?crop=0.670xw:1.00xh;0.202xw,0&resize=640:*", caption="Jessica Pearson")



        c19, c20 = st.columns([0.25, 0.75])

        with c20:
            st.write(":gray[**Chief Operating Officer**]")

            with st.container():
                st.title(":rainbow[The Team]")
                st.write("")

        st.image("https://bloximages.chicago2.vip.townnews.com/auburnpub.com/content/tncms/assets/v3/editorial/0/c4/0c42141a-2357-11e4-9bbe-0019bb2963f4/53ec18f466499.image.jpg",caption="Louis Litt")

        c20, c21 = st.columns([0.3, 0.8])

        st.image("https://people.com/thmb/AXI_Rfd2WAKfhY-wnsDkWBBN2s0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc():focal(1053x367:1055x369)/meghan-markle-suits-1-263be702444549fe853ef9d1201952be.jpg",caption="Rachel Zane")

        c23,c24 = st.columns([0.3, 0.7])
        with c24:
            st.write(":grey[Principal Officer]")

        with c21:
            st.write(":gray[General Manager]")



