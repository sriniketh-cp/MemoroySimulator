import streamlit as st
import random
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
import time
import numpy as np

# Initialize session state variables
if 'totalmemory' not in st.session_state:
    st.session_state.totalmemory = 1000  # Total memory in MB
    st.session_state.contiguousmemory = []
    st.session_state.linkedmemory = []
    st.session_state.indexedmemory = []
    st.session_state.allocationhistory = []
    st.session_state.contiguousmemorylog = []
    st.session_state.linkedmemorylog = []
    st.session_state.indexedmemorylog = []
    st.session_state.memoryusedcontiguous = 0
    st.session_state.memoryusedlinked = 0
    st.session_state.memoryusedindexed = 0
    st.session_state.folders = {}
    st.session_state.foldercolors = {}
    st.session_state.automationrunning = False
    st.session_state.tempallocations = []
    st.session_state.fragmentation = 0
    st.session_state.fragmentationhistory = []
    st.session_state.pagetable = {}
    st.session_state.ram = {}
    st.session_state.disk = {}
    st.session_state.protectionviolations = []
    st.session_state.processcolors = {}
    st.session_state.memoryaccesslog = {}

# Existing allocation functions
def allocatecontiguous(size):
    memory = st.session_state.contiguousmemory
    start = 0
    for block in memory:
        if start + size <= block[0]:
            memory.append((start, start + size))
            memory.sort(key=lambda x: x[0])
            return True
        start = block[1]
    if start + size <= st.session_state.totalmemory:
        memory.append((start, start + size))
        return True
    return False

def allocatelinked(size):
    memory = st.session_state.linkedmemory
    totalallocated = sum(block[1] - block[0] for block in memory)
    if totalallocated + size <= st.session_state.totalmemory:
        start = random.randint(0, st.session_state.totalmemory - size)
        memory.append((start, start + size))
        return True
    return False

def allocateindexed(size):
    memory = st.session_state.indexedmemory
    totalallocated = sum(block[1] - block[0] for block in memory)
    if totalallocated + size <= st.session_state.totalmemory:
        start = totalallocated
        memory.append((start, start + size))
        return True
    return False

def deallocatememory(allocationtype, index):
    if allocationtype == 'contiguous':
        memory = st.session_state.contiguousmemory
    elif allocationtype == 'linked':
        memory = st.session_state.linkedmemory
    else:  # indexed
        memory = st.session_state.indexedmemory
    
    if 0 <= index < len(memory):
        del memory[index]
        return True
    return False

# New allocation functions
def allocatememory(method, size):
    if method == "Contiguous":
        if allocatecontiguous(size):
            st.session_state.memoryusedcontiguous += size
            st.session_state.contiguousmemorylog.append(st.session_state.memoryusedcontiguous)
            updatefragmentation()
            return True
    elif method == "Linked":
        if allocatelinked(size):
            st.session_state.memoryusedlinked += size
            st.session_state.linkedmemorylog.append(st.session_state.memoryusedlinked)
            updatefragmentation()
            return True
    elif method == "Indexed":
        if allocateindexed(size):
            st.session_state.memoryusedindexed += size
            st.session_state.indexedmemorylog.append(st.session_state.memoryusedindexed)
            updatefragmentation()
            return True
    return False

def deletememory(method, size):
    if method == "Contiguous":
        if st.session_state.memoryusedcontiguous >= size:
            st.session_state.memoryusedcontiguous -= size
            st.session_state.contiguousmemorylog.append(st.session_state.memoryusedcontiguous)
            updatefragmentation()
            return True
    elif method == "Linked":
        if st.session_state.memoryusedlinked >= size:
            st.session_state.memoryusedlinked -= size
            st.session_state.linkedmemorylog.append(st.session_state.memoryusedlinked)
            updatefragmentation()
            return True
    elif method == "Indexed":
        if st.session_state.memoryusedindexed >= size:
            st.session_state.memoryusedindexed -= size
            st.session_state.indexedmemorylog.append(st.session_state.memoryusedindexed)
            updatefragmentation()
            return True
    return False

# Folder allocation functions
def allocatefoldermemory(foldername, size):
    if foldername in st.session_state.folders:
        st.error(f"Folder '{foldername}' already exists.")
        return
    if st.session_state.totalmemory - sum(st.session_state.folders.values()) >= size:
        st.session_state.folders[foldername] = size
        st.session_state.foldercolors[foldername] = f'rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})'
        st.success(f"Folder '{foldername}' created with {size} MB")
        updatefragmentation()
    else:
        st.error("Not enough memory for folder allocation")

def deletefolder(foldername):
    if foldername in st.session_state.folders:
        del st.session_state.folders[foldername]
        del st.session_state.foldercolors[foldername]
        st.success(f"Folder '{foldername}' deleted")
        updatefragmentation()
    else:
        st.error(f"Folder '{foldername}' does not exist")

# Update fragmentation calculation
def updatefragmentation():
    allocatedmemory = (st.session_state.memoryusedcontiguous +
                        st.session_state.memoryusedlinked +
                        st.session_state.memoryusedindexed +
                        sum(st.session_state.folders.values()))
    freememory = st.session_state.totalmemory - allocatedmemory
    st.session_state.fragmentation = (freememory / st.session_state.totalmemory) * 100
    st.session_state.fragmentationhistory.append(st.session_state.fragmentation)

# Virtual memory functions
def allocatevirtualmemory(processid, size, color):
    if processid not in st.session_state.pagetable:
        st.session_state.pagetable[processid] = {'size': size, 'pageframe': []}
        st.session_state.processcolors[processid] = color
    else:
        st.session_state.pagetable[processid]['size'] += size

    numpages = size // 4  # Assume each page is 4MB
    for page in range(numpages):
        if len(st.session_state.ram) < 4:  # Assuming RAM can hold 4 pages
            st.session_state.ram[processid] = st.session_state.pagetable[processid]
        else:
            swapoutpage(processid)

def swapoutpage(processid):
    for pid in list(st.session_state.ram.keys()):
        if pid != processid:
            st.session_state.disk[pid] = st.session_state.ram[pid]  # Move to disk
            del st.session_state.ram[pid]  # Remove from RAM
            break

def accessmemory(processid, address):
    if processid in st.session_state.pagetable:
        if processid in st.session_state.ram:
            if processid not in st.session_state.memoryaccesslog:
                st.session_state.memoryaccesslog[processid] = {}
            if address not in st.session_state.memoryaccesslog[processid]:
                st.session_state.memoryaccesslog[processid][address] = 0
            st.session_state.memoryaccesslog[processid][address] += 1
            
            return f"Accessing address {address} in process {processid}."
        else:
            st.session_state.protectionviolations.append(
                f"Protection violation for process {processid} accessing address {address}.")
            return f"Protection violation: Process {processid} is not in RAM."

# Visualization functions
def createfragmentationvisualization():
    fig = make_subplots(rows=3, cols=1,
                        subplot_titles=("Contiguous Allocation", "Linked Allocation", "Indexed Allocation"),
                        vertical_spacing=0.1,
                        specs=[[{"type": "xy"}], [{"type": "xy"}], [{"type": "xy"}]])

    for i, (title, memory) in enumerate([("Contiguous", st.session_state.contiguousmemory),
                                         ("Linked", st.session_state.linkedmemory),
                                         ("Indexed", st.session_state.indexedmemory)], 1):
        if title == "Contiguous":
            # Add allocated blocks for Contiguous
            for start, end in memory:
                fig.add_trace(
                    go.Bar(x=[start, end - start], y=[title], orientation='h',
                           name=f'{title} Block', marker_color='rgba(55, 128, 191, 0.7)'),
                    row=i, col=1
                )
            
            # Add free space visualization for Contiguous
            usedspaces = set()
            for start, end in memory:
                usedspaces.update(range(start, end))
            freespaces = sorted(set(range(st.session_state.totalmemory)) - usedspaces)
            for start, end in getcontinuousranges(freespaces):
                fig.add_trace(
                    go.Bar(x=[start, end - start], y=[title], orientation='h',
                           name='Free Space', marker_color='rgba(219, 64, 82, 0.7)'),
                    row=i, col=1
                )
        elif title == "Linked":
            # Add linked list visualization for Linked Allocation
            xnodes = []
            ynodes = []
            for j, (start, end) in enumerate(memory):
                xnodes.extend([start, end])
                ynodes.extend([title, title])
                
                # Add arrow to next node
                if j < len(memory) - 1:
                    next_start = memory[j + 1][0]
                    fig.add_annotation(
                        x=end, y=title,
                        ax=next_start, ay=title,
                        xref="x", yref="y",
                        axref="x", ayref="y",
                        text="",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1.5,
                        arrowwidth=2,
                        arrowcolor="rgba(50, 171, 96, 1)",
                    )
            
            fig.add_trace(
                go.Scatter(x=xnodes, y=ynodes, mode='markers',
                           name='Linked List', 
                           marker=dict(size=20, symbol='square', color='rgba(50, 171, 96, 1)')),
                row=2, col=1
            )
        else:  # Indexed
            if memory:  # Check if there's any indexed memory allocated
                for j, (start, end) in enumerate(memory):
                    fig.add_trace(go.Bar(
                        x=[start],
                        y=[end - start],
                        name=f"Segment {j + 1}",
                        orientation='v',
                        marker=dict(color=f'rgba({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)}, 0.6)')
                    ), row=3, col=1)

                # Add annotations to connect index table to memory blocks
                for j, (start, end) in enumerate(memory):
                    # Adjust y-position to prevent overlap
                    y_position = (end - start) / 2 + 0.5  # Centered with a slight offset
                    fig.add_annotation(
                        x=start,
                        y=y_position,
                        text=f"Segment {j + 1}",
                        showarrow=True,
                        arrowhead=2,
                        arrowsize=1,
                        arrowwidth=2,
                        arrowcolor="black",
                        row=3, col=1
                    )

    fig.update_layout(height=1000, title_text="Memory Allocation and Fragmentation Visualization")
    fig.update_xaxes(title_text="Memory Address", range=[0, st.session_state.totalmemory], row=3, col=1)
    
    for i in range(1, 4):
        fig.update_yaxes(showticklabels=False, row=i, col=1)
    
    fig.update_yaxes(title_text="Segment Size", row=3, col=1)

    return fig


def getcontinuousranges(numbers):
    ranges = []
    start = end = numbers[0]
    for n in numbers[1:]:
        if n == end + 1:
            end = n
        else:
            ranges.append((start, end + 1))
            start = end = n
    ranges.append((start, end + 1))
    return ranges

def creatememoryallocationgraph():
    processes = list(st.session_state.pagetable.keys())
    sizes = [st.session_state.pagetable[p]['size'] for p in processes]
    colors = [st.session_state.processcolors[p] for p in processes]

    fig = go.Figure(data=[
        go.Bar(name=process, x=['Memory Allocation'], y=[size], marker_color=color)
        for process, size, color in zip(processes, sizes, colors)
    ])

    fig.update_layout(
        barmode='stack',
        title="Memory Allocation by Process",
        xaxis_title="",
        yaxis_title="Memory Allocated (MB)",
        showlegend=True
    )

    return fig

def creatememoryaccessheatmap():
    processes = list(st.session_state.memoryaccesslog.keys())
    maxaddress = max(max(addresses.keys()) for addresses in st.session_state.memoryaccesslog.values())
    
    heatmapdata = np.zeros((len(processes), maxaddress + 1))
    
    for i, process in enumerate(processes):
        for address, count in st.session_state.memoryaccesslog[process].items():
            heatmapdata[i][address] = count
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmapdata,
        x=list(range(maxaddress + 1)),
        y=processes,
        colorscale='Viridis'
    ))
    
    fig.update_layout(
        title="Memory Access Heatmap",
        xaxis_title="Memory Address",
        yaxis_title="Process ID",
        height=400 + (len(processes) * 30)  # Adjust height based on number of processes
    )
    
    return fig

# Add this function to create the folder allocation chart
def createfolderallocationchart():
    folders = list(st.session_state.folders.keys())
    sizes = list(st.session_state.folders.values())
    colors = [st.session_state.foldercolors[folder] for folder in folders]

    fig = go.Figure(data=[
        go.Bar(name=folder, x=['Folder Allocation'], y=[size], marker_color=color)
        for folder, size, color in zip(folders, sizes, colors)
    ])

    fig.update_layout(
        barmode='stack',
        title="Folder Allocation",
        xaxis_title="",
        yaxis_title="Memory Allocated (MB)",
        showlegend=True
    )

    return fig

# Add this function to create the memory allocation heatmap
def creatememoryheatmap():
    processes = list(st.session_state.pagetable.keys())
    sizes = [st.session_state.pagetable[p]['size'] for p in processes]
    colors = [st.session_state.processcolors[p] for p in processes]
    
    fig = go.Figure(data=[go.Bar(
        x=processes,
        y=sizes,
        marker_color=colors,
        text=sizes,
        textposition='auto',
    )])
    
    fig.update_layout(
        title="Memory Allocation Heatmap",
        xaxis_title="Process ID",
        yaxis_title="Memory Allocated (MB)",
        height=400 + (len(processes) * 30)  # Adjust height based on number of processes
    )
    
    return fig

# Streamlit app
st.title("Memory Allocation and Management Simulator")

# Sidebar menu
st.sidebar.title("Menu")
menu = st.sidebar.radio("Choose an operation:",
                        ["File Allocation", "Folder Allocation", "Automate File Creation and Deletion", "Advanced Memory Management"])

if menu == "File Allocation":
    st.sidebar.header("File Allocation")
    operation = st.sidebar.radio("Select operation:", ["Create File", "Delete File"])

    if operation == "Create File":
        filesize = st.sidebar.number_input("Enter file size (MB)", min_value=1, max_value=1000, value=50)
        allocationmethod = st.sidebar.selectbox("Select allocation method", ["Contiguous", "Linked", "Indexed"])

        if st.sidebar.button("Create File"):
            if allocatememory(allocationmethod, filesize):
                st.success(f"File created with {filesize} MB using {allocationmethod} Allocation")
            else:
                st.error(f"Not enough memory for {allocationmethod} Allocation")

    elif operation == "Delete File":
        deletesize = st.sidebar.number_input("Enter file size to delete (MB)", min_value=1, max_value=1000, value=50)
        deletemethod = st.sidebar.selectbox("Select deletion method", ["Contiguous", "Linked", "Indexed"])

        if st.sidebar.button("Delete File"):
            if deletememory(deletemethod, deletesize):
                st.success(f"File deleted, {deletesize} MB freed from {deletemethod} Allocation")
            else:
                st.error(f"Invalid size for deletion in {deletemethod} Allocation")

elif menu == "Folder Allocation":
    st.sidebar.header("Folder Allocation")
    operation = st.sidebar.radio("Select operation:", ["Create Folder", "Delete Folder"])

    if operation == "Create Folder":
        foldername = st.sidebar.text_input("Enter folder name")
        foldersize = st.sidebar.number_input("Enter folder size (MB)", min_value=1, max_value=1000, value=100)

        if st.sidebar.button("Create Folder"):
            allocatefoldermemory(foldername, foldersize)

    elif operation == "Delete Folder":
        foldertodelete = st.sidebar.selectbox("Select folder to delete", list(st.session_state.folders.keys()))

        if st.sidebar.button("Delete Folder"):
            deletefolder(foldertodelete)

elif menu == "Automate File Creation and Deletion":
    st.sidebar.header("Automation")
    if not st.session_state.automationrunning:
        if st.sidebar.button("Start Automation"):
            st.session_state.automationrunning = True
    else:
        if st.sidebar.button("Stop Automation"):
            st.session_state.automationrunning = False

    if st.session_state.automationrunning:
        for _ in range(5):  # Simulate 5 operations
            operation = random.choice(["create", "delete"])
            method = random.choice(["Contiguous", "Linked", "Indexed"])
            size = random.randint(10, 100)

            if operation == "create":
                if allocatememory(method, size):
                    st.session_state.tempallocations.append((method, size))
                    st.info(f"Created file of {size} MB using {method} Allocation")
            else:
                if st.session_state.tempallocations:
                    deletemethod, deletesize = st.session_state.tempallocations.pop()
                    if deletememory(deletemethod, deletesize):
                        st.info(f"Deleted file of {deletesize} MB from {deletemethod} Allocation")

            time.sleep(0.5)
        
        # Trigger a rerun using st.rerun()
        st.rerun()

elif menu == "Advanced Memory Management":
    st.sidebar.header("Virtual Memory Management")
    operation = st.sidebar.radio("Select operation:", ["Allocate Virtual Memory", "Access Memory"])

    if operation == "Allocate Virtual Memory":
        processid = st.sidebar.text_input("Enter process ID")
        memorysize = st.sidebar.number_input("Enter memory size (MB)", min_value=1, max_value=1000, value=50)
        color = st.sidebar.color_picker("Choose process color", "#00FFAA")

        if st.sidebar.button("Allocate Virtual Memory"):
            allocatevirtualmemory(processid, memorysize, color)
            st.success(f"Virtual memory allocated for process {processid}")

    elif operation == "Access Memory":
        processid = st.sidebar.selectbox("Select process ID", list(st.session_state.pagetable.keys()))
        address = st.sidebar.number_input("Enter memory address to access", min_value=0, max_value=999)

        if st.sidebar.button("Access Memory"):
            result = accessmemory(processid, address)
            st.info(result)

# Display visualizations
st.header("Memory Allocation Visualization")
st.plotly_chart(createfragmentationvisualization())

st.header("Memory Usage")
col1, col2, col3 = st.columns(3)
col1.metric("Contiguous", f"{st.session_state.memoryusedcontiguous} MB")
col2.metric("Linked", f"{st.session_state.memoryusedlinked} MB")
col3.metric("Indexed", f"{st.session_state.memoryusedindexed} MB")

st.header("Folder Allocation")
if st.session_state.folders:
    st.plotly_chart(createfolderallocationchart())
else:
    st.info("No folders allocated yet.")

st.header("Fragmentation")
st.line_chart(st.session_state.fragmentationhistory)

if st.session_state.pagetable:
    st.header("Virtual Memory Allocation")
    st.plotly_chart(creatememoryallocationgraph())

if st.session_state.memoryaccesslog:
    st.header("Memory Access Heatmap")
    st.plotly_chart(creatememoryaccessheatmap())

if st.session_state.protectionviolations:
    st.header("Protection Violations")
    for violation in st.session_state.protectionviolations:
        st.warning(violation)

if st.session_state.pagetable:
    st.header("Memory Allocation Heatmap")
    st.plotly_chart(creatememoryheatmap())