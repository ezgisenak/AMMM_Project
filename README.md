# AMMM Project - Bid Matrix Problem

**Authors:** Ezgi Sena Karabacak, Davide Lamagna

This project consists of two main components: an Instance Generator and Heuristics solvers for the Bid Matrix Problem.

## Project Components

### Core Components
- **Instance Generator**: Generates problem instances with configurable parameters
- **Heuristics**: Implements different solving algorithms for the bid matrix problem

### Key Files and Directories

#### Heuristics Module
- `problem/`: Contains core problem-related classes
  - `instance.py`: Defines the problem instance structure
  - `solution.py`: Implements the solution representation and operations
- `solver.py`: Abstract solver class defining the interface for all solvers
- `ValidateConfig.py`: Validates configuration parameters for solvers
- `validateInputData.py`: Validates input data format and structure

#### Plotting Module
- `plot/`: Contains scripts for visualizing results
  - `main_plot.py`: Generates plots for main results
  - `alpha_tuning_plot.py`: Visualizes GRASP alpha parameter tuning results
  - `img/`: Directory containing generated plots
  - CSV files for storing results and tuning data

## Project Structure

```
.
├── InstanceGenerator/
│   ├── config/           # Configuration files for instance generation
│   ├── output/           # Generated instances
│   └── Main.py          # Main script for instance generation
└── Heuristics/
    ├── config/          # Configuration files for solvers
    ├── solvers/         # Implementation of different solving algorithms
    ├── solutions/       # Generated solutions
    └── Main.py         # Main script for running solvers
```

## Prerequisites

- Python 3.x

## Usage

### 1. Generating Problem Instances

1. Navigate to the InstanceGenerator directory:
   ```bash
   cd InstanceGenerator
   ```

2. Configure the instance generation parameters:
   - Open and modify the configuration file in `config/config.dat`
   - Adjust the parameters according to your needs

3. Run the instance generator:
   ```bash
   python Main.py
   ```
   This will generate problem instances in the `output` directory.

### 2. Running the Solvers

1. Navigate to the Heuristics directory:
   ```bash
   cd Heuristics
   ```

2. Configure the solver parameters:
   - Open and modify the configuration file in `config/config.dat`
   - Set the desired solver type and parameters

3. Run the solver:
   ```bash
   python Main.py
   ```
   The solver will automatically read the generated instances from the correct location and save the solutions in the `solutions` directory.

## Available Solvers

The project includes the following solvers:
- Greedy
- GRASP

## Configuration Files

### Instance Generator Configuration
The configuration file for instance generation (`InstanceGenerator/config/config.dat`) requires the following parameters:

| Parameter | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| instancesDirectory | string | Directory where instances will be saved | Must not be empty |
| fileNamePrefix | string | Prefix for generated instance files | Must not be empty |
| fileNameExtension | string | File extension for instance files | Must not be empty |
| numInstances | integer | Number of instances to generate | Must be positive |
| N | integer | Size of the bid matrix (N x N) | Must be positive |
| maxBid | integer | Maximum bid value | Must be non-negative |

### Solver Configuration
The configuration file for solvers (`Heuristics/config/config.dat`) includes the following parameters:

#### Required Parameters
| Parameter | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| inputDataFile | string | Path to the input data file | Must exist |
| solutionFile | string | Path where solution will be saved | Must not be empty |
| solver | string | Solver to use | Must be one of: 'Greedy', 'GRASP' |

#### Optional Parameters
| Parameter | Type | Description | Default | Constraints |
|-----------|------|-------------|---------|-------------|
| verbose | boolean | Enable verbose output | false | Must be true/false |

#### GRASP Solver Specific Parameters
| Parameter | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| maxExecTime | float | Maximum execution time in seconds | Must be positive |
| alpha | float | GRASP parameter | Must be in range [0,1] |

#### Local Search Parameters (Optional)
| Parameter | Type | Description | Constraints |
|-----------|------|-------------|-------------|
| neighborhoodStrategy | string | Strategy for neighborhood search | Only 'Exchange' is supported |
| policy | string | Policy for improvement selection | Must be one of: 'BestImprovement' |

### Example Configuration Files

#### Instance Generator (config.dat)
```
instancesDirectory = "output"
fileNamePrefix = "instance"
fileNameExtension = "dat"
numInstances = 5
N = 10
maxBid = 100
```

#### Heuristics Solver (config.dat)
```
inputDataFile = "output/instance1.dat"
solutionFile = "solutions/solution1.dat"
solver = "GRASP"
verbose = true
maxExecTime = 60
alpha = 0.5
localSearch = true
neighborhoodStrategy = "Exchange"
policy = "BestImprovement"
```

## Notes

- You don't need to manually copy generated instances from the InstanceGenerator to the Heuristics folder. The code automatically reads the instances from the correct location.
- Solutions are automatically saved in the appropriate directories.
- The project includes validation for both configuration files and input data to ensure correct execution.
