# Operations Research Algorithms

This repository contains implementations of various Operations Research algorithms in Python, specifically using Python 3.12 and the NumPy library.

## Algorithms Included

1. **Simplex Algorithm**: A linear programming algorithm used for solving optimization problems by iteratively improving feasible solutions.

2. **Hungarian Algorithm**: An algorithm for solving the assignment problem in combinatorial optimization, finding an optimal assignment of persons to jobs.

3. **Transportation Algorithms**:
   - **Northwest Corner Method**: A heuristic algorithm for finding an initial feasible solution to the transportation problem, commonly used in logistics.
   - **Lowest Cost Method**: An algorithm that selects the cell with the lowest cost in each iteration, minimizing the overall transportation cost.
   - **Vogel's Approximation Method (VAM)**: A refined approach to finding an initial feasible solution in the transportation problem, known for better accuracy.

## Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python 3.12](https://www.python.org/downloads/release)
- [NumPy](https://numpy.org/)

### Setup Virtual Environment

1. **Clone the repository**
    ```bash
    git clone https://github.com/your-username/operations-research.git
    ```

2. **Navigate to the project directory**
    ```bash
    cd operations-research
    ```

3. **Create a virtual environment**
    ```bash
    python -m venv venv
    ```

4. **Activate the virtual environment**
    - On Windows
    ```cmd
    venv\Scripts\activate
    ```
    - On macOS/Linux
    ```bash
    source venv/bin/activate
    ```

### Install Required Dependencies
```bash
pip install -r requirements.txt
```

## Running the Algorithms
The test file contains several matrices for testing the corectness of the algorithhms. It can be run by using the following command:
```bash
python tests.py
```
