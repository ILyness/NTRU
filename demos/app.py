import streamlit as st
import plotly.graph_objects as go
import numpy as np

def generate_lattice(b1, b2, b3, range_min=-5, range_max=5):
    ns = np.arange(range_min, range_max + 1)
    n1, n2, n3 = np.meshgrid(ns, ns, ns)
    n1, n2, n3 = n1.flatten(), n2.flatten(), n3.flatten()
    
    Rx = n1 * b1[0] + n2 * b2[0] + n3 * b3[0]
    Ry = n1 * b1[1] + n2 * b2[1] + n3 * b3[1]
    Rz = n1 * b1[2] + n2 * b2[2] + n3 * b3[2]
    return Rx, Ry, Rz

st.title("Interactive Lattice Visualization")
st.sidebar.markdown("## Basis Vector Controls")

# --- CHANGE 1 & 2: LaTeX Labels and Integer Inputs ---
# We use st.markdown with raw strings (r"...") for LaTeX.
# We set value=1 (int) and step=1 to enforce integer coordinates.

st.sidebar.markdown(r"### Vector $\vec{a}_1$")
col1, col2, col3 = st.sidebar.columns(3)
a1x = col1.number_input(r"$x$", value=1, step=1, key='a1x')
a1y = col2.number_input(r"$y$", value=0, step=1, key='a1y')
a1z = col3.number_input(r"$z$", value=0, step=1, key='a1z')

st.sidebar.markdown(r"### Vector $\vec{a}_2$")
col4, col5, col6 = st.sidebar.columns(3)
a2x = col4.number_input(r"$x$", value=0, step=1, key='a2x')
a2y = col5.number_input(r"$y$", value=1, step=1, key='a2y')
a2z = col6.number_input(r"$z$", value=0, step=1, key='a2z')

st.sidebar.markdown(r"### Vector $\vec{a}_3$")
col7, col8, col9 = st.sidebar.columns(3)
a3x = col7.number_input(r"$x$", value=0, step=1, key='a3x')
a3y = col8.number_input(r"$y$", value=0, step=1, key='a3y')
a3z = col9.number_input(r"$z$", value=1, step=1, key='a3z')

# 3. Generate Data
b1 = np.array([a1x, a1y, a1z])
b2 = np.array([a2x, a2y, a2z])
b3 = np.array([a3x, a3y, a3z])

x, y, z = generate_lattice(b1, b2, b3)

# 4. Create Plot
fig = go.Figure(data=[go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    marker=dict(size=3, 
                # color=z, 
                # colorscale='Viridis', 
                opacity=0.8)
)])

# --- CHANGE 3: Remove Axis Labels ---
# We set visible=False to hide the axis entirely (lines, ticks, labels).
# If you want to keep the grid lines but hide the text, 
# use dict(showticklabels=False, title='') instead of visible=False.
axis_setting = dict(
    visible=False, 
    showbackground=False # Optional: hides the gray background walls
)

fig.update_layout(
    height=800,
    width=800,
    scene=dict(
        xaxis=axis_setting,
        yaxis=axis_setting,
        zaxis=axis_setting,
        aspectmode='data'
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)