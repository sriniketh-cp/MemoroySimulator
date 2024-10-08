# Memory Management Simulator

An interactive Python-based simulator demonstrating core operating system concepts in memory management. Built with Streamlit, this project visualizes various memory allocation techniques, fragmentation issues, and virtual memory management.

## Features

- Simulates multiple memory allocation strategies:
  - Contiguous memory allocation
  - Linked memory allocation
  - Indexed memory allocation
- Virtual memory management simulation (paging and swapping)
- Fragmentation analysis and solutions
- File and folder allocation simulation
- Advanced visualization of memory usage through graphs, heatmaps, and charts

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/sriniketh-cp/MemoroySimulator.git
   ```

2. Navigate to the project directory:
   ```bash
   cd MemoroySimulator
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Open your browser and go to `http://localhost:8501` to access the simulator.

## Memory Allocation Techniques

- **Contiguous**: Allocates a single, continuous block of memory to each process.
- **Linked**: Allocates memory in scattered blocks linked by pointers.
- **Indexed**: Uses an index table to manage non-contiguous memory blocks.

## Virtual Memory Management

Demonstrates paging and swapping techniques to manage memory overflow and optimize RAM usage.

## Visualization Tools

- Memory Allocation Graphs
- Heatmaps of memory access patterns
- Bar Charts illustrating memory allocation by process

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or suggestions, please open an issue on GitHub.

Project Link: [https://github.com/sriniketh-cp/MemoroySimulator](https://github.com/sriniketh-cp/MemoroySimulator)
