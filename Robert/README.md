# Assignment_3
Runtime and Space Complexity in Financial Signal Processing

## How to Run
1.  **Set up your environment**. Make sure you have your Python environment ready.
2.  **Packages needed**. tqdm, timeit, pandas,  matplotlib.pyplot and memory_profiler
3.  **Open the notebook**. Open the `main.py`.
4.  **Run the code**. Run the code in the file.
5.  **See the results**. The notebook will write the results in the file `complexity_report.md`.


## What's Inside? (File Descriptions)
- **data_loader.py**  
  - Handles **CSV parsing** and **dataclass creation**

- **models.py**  
  - Defines **MarketDataPoint** and **Strategy** base classes

- **strategies.py**  
  - Implements **naive** and **optimized strategy** variations

- **profiler.py**  
  - Performs **runtime**,  **memory measurement** and **plotting**

- **main.py**  
  - **Orchestrates** data ingestion, strategy execution, and profiling workflow

- **tests.ipynb/**  
  - Contains **notebook-based validation**

- **complexity_report.md**  
  - Provides a **summary of performance and complexity findings**

- **README.md**  
  - Includes **setup instructions** and **module descriptions**
