

Memory Management Simulator
A Python-based memory management simulator that demonstrates core operating system concepts such as memory allocation techniques (contiguous, linked, indexed), fragmentation, and virtual memory management. Developed using the Streamlit framework, this simulator provides an interactive platform to visualize and understand how operating systems handle memory allocation for processes.


Features
Simulates different memory allocation strategies:
Contiguous memory allocation
Linked memory allocation
Indexed memory allocation
Virtual memory management simulation, including paging and swapping.
Displays internal and external fragmentation and offers solutions.
Provides file and folder allocation, simulating real OS file system operations.
Visualization of memory usage through graphs, heatmaps, and charts.
Demo
You can see a live demo of the Memory Management Simulator by running it locally. Follow the installation and usage instructions below to interact with the simulator.

Installation
To run the simulator on your local machine:

Clone the repository:
git clone https://github.com/sriniketh-cp/MemoroySimulator.git

Navigate to the project directory:


cd MemoroySimulator
Install the required dependencies:

Run the Streamlit app:

streamlit run app.py

Usage
After running the simulator, open your browser and go to http://localhost:8501 to access the application.
Use the interface to select memory allocation techniques, simulate fragmentation, and visualize memory usage.
You can experiment with various allocation strategies and see their impact on memory fragmentation and performance.
Memory Allocation Techniques
Contiguous Memory Allocation
Description: Allocates a single, continuous block of memory to each process.
Advantages: Fast access and simplicity.
Disadvantages: Prone to external fragmentation and limited scalability.
Linked Memory Allocation
Description: Allocates memory in scattered blocks linked by pointers.
Advantages: Avoids external fragmentation, efficient memory use.
Disadvantages: Pointer overhead and slower access due to non-contiguous blocks.
Indexed Memory Allocation
Description: Uses an index table to manage non-contiguous memory blocks.
Advantages: Efficient access and no external fragmentation.
Disadvantages: Index table management requires additional memory and complexity.
Virtual Memory Management
The simulator includes virtual memory management features to show how operating systems use disk storage as an extension of RAM. This is demonstrated through:

Paging: Divides memory into pages and simulates swapping pages between RAM and disk.
Swapping: Handles memory overflow by swapping pages in and out of the disk to free up RAM.
Fragmentation
External Fragmentation
Occurs when free memory is divided into small, non-contiguous blocks, making it difficult to allocate large blocks of memory despite having sufficient free space.
Internal Fragmentation
Happens when memory is allocated in fixed-size blocks, and the process doesn't fully use the block, wasting some memory.
File and Folder Allocation
The simulator also handles file and folder allocation similar to a real OS:

Folder Allocation: Simulates memory allocation for folders, ensuring efficient use of available memory.
File Management: Automates file creation, deletion, and memory management, providing a visualization of the file system structure.
Visualization Tools
The simulator provides detailed visual representations to enhance the learning experience:

Memory Allocation Graphs: Shows how memory is allocated using various strategies (contiguous, linked, indexed).
Heatmaps: Visualizes memory access patterns, highlighting frequently accessed memory regions.
Bar Charts: Illustrates memory allocation by process, showing how much memory is occupied or fragmented.
Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make to this project are greatly appreciated.

Fork the repository.
Create your feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'Add some AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
If you have any questions or suggestions about this project, feel free to reach out via the Issues section on GitHub.
