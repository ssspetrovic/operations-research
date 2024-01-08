# Operations Research Algorithms

This repository contains implementations of various Operations Research algorithms in Python, specifically using Python 3.12 and the NumPy library.

## Algorithms Included

1. **Hungarian Algorithm**: An algorithm for solving the assignment problem in combinatorial optimization, finding an optimal assignment of persons to jobs.

2. **Simplex Algorithm**: A linear programming algorithm used for solving optimization problems by iteratively improving feasible solutions.

3. **Transportation Algorithms**:
   - **Northwest Corner Method**: A heuristic algorithm for finding an initial feasible solution to the transportation problem, commonly used in logistics.
   - **Lowest Cost Method**: An algorithm that selects the cell with the lowest cost in each iteration, minimizing the overall transportation cost.
   - **Vogel's Approximation Method (VAM)**: A refined approach to finding an initial feasible solution in the transportation problem, known for better accuracy.

## Getting Started

### Prerequisites

- [Python 3.12](https://www.python.org/downloads/release)
- [NumPy](https://numpy.org/)

### Setup Virtual Environment

```bash
# Clone the repository
git clone https://github.com/your-username/operations-research.git

# Navigate to the project directory
cd operations-research

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
