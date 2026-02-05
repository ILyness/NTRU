import streamlit as st
import plotly.graph_objects as go
import numpy as np

BOX_LIMIT = 5.0 

def generate_filtered_lattice(b1, b2, b3, limit):
    ns = np.arange(-100, 101) 
    n1, n2, n3 = np.meshgrid(ns, ns, ns)
    n1, n2, n3 = n1.flatten(), n2.flatten(), n3.flatten()
    
    Rx = n1 * b1[0] + n2 * b2[0] + n3 * b3[0]
    Ry = n1 * b1[1] + n2 * b2[1] + n3 * b3[1]
    Rz = n1 * b1[2] + n2 * b2[2] + n3 * b3[2]
    
    mask = (np.abs(Rx) <= limit) & (np.abs(Ry) <= limit) & (np.abs(Rz) <= limit)
    
    return Rx[mask], Ry[mask], Rz[mask]

def get_cube_wireframe(limit):
    l = limit
    x = [l, l, -l, -l, l, l, -l, -l, l, l, l, l, -l, -l, -l, -l]
    y = [l, -l, -l, l, l, l, l, -l, -l, l, -l, -l, -l, -l, l, l]
    z = [l, l, l, l, l, -l, -l, -l, -l, -l, -l, l, l, -l, -l, l]
    return x, y, z

st.title("Lattice in a Box")
st.sidebar.markdown("## Basis Vectors")

st.sidebar.markdown(r"### $\vec{a}_1$")
col1, col2, col3 = st.sidebar.columns(3)
a1x = col1.number_input(r"$x$", value=1, step=1, key='a1x')
a1y = col2.number_input(r"$y$", value=0, step=1, key='a1y')
a1z = col3.number_input(r"$z$", value=0, step=1, key='a1z')

st.sidebar.markdown(r"### $\vec{a}_2$")
col4, col5, col6 = st.sidebar.columns(3)
a2x = col4.number_input(r"$x$", value=0, step=1, key='a2x')
a2y = col5.number_input(r"$y$", value=1, step=1, key='a2y')
a2z = col6.number_input(r"$z$", value=0, step=1, key='a2z')

st.sidebar.markdown(r"### $\vec{a}_3$")
col7, col8, col9 = st.sidebar.columns(3)
a3x = col7.number_input(r"$x$", value=0, step=1, key='a3x')
a3y = col8.number_input(r"$y$", value=0, step=1, key='a3y')
a3z = col9.number_input(r"$z$", value=1, step=1, key='a3z')

b1 = np.array([a1x, a1y, a1z])
b2 = np.array([a2x, a2y, a2z])
b3 = np.array([a3x, a3y, a3z])

x, y, z = generate_filtered_lattice(b1, b2, b3, BOX_LIMIT)

distances = np.sqrt(x**2 + y**2 + z**2)

bx, by, bz = get_cube_wireframe(BOX_LIMIT)

fig = go.Figure()

fig.add_trace(go.Scatter3d(
    x=x, y=y, z=z,
    mode='markers',
    name='Lattice Points',
    marker=dict(size=3, color=distances, colorscale='Turbo', opacity=0.8)
))

fig.add_trace(go.Scatter3d(
    x=bx, y=by, z=bz,
    mode='lines',
    name='Boundary',
    line=dict(color='gray', width=4)
))

axis_setting = dict(visible=False, showbackground=False)
fig.update_layout(
    height=800,
    showlegend=False,
    scene=dict(
        xaxis=axis_setting,
        yaxis=axis_setting,
        zaxis=axis_setting,
        xaxis_range=[-BOX_LIMIT-1, BOX_LIMIT+1],
        yaxis_range=[-BOX_LIMIT-1, BOX_LIMIT+1],
        zaxis_range=[-BOX_LIMIT-1, BOX_LIMIT+1],
        aspectmode='cube' 
    ),
    margin=dict(l=0, r=0, b=0, t=0)
)

st.plotly_chart(fig, use_container_width=True)