## ALGO & DATAENG

Create a new environment and install the requirements.txt file.

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

### ALGO

  Running the code is as simple as running the following command in the terminal:

    python3 algo_q2.py

- The first line contains a valid sorted array given as space separated numbers **input1:**. 
- The second line contains a valid sorted array given as space separated numbers **input2:**

Result will be printed in the terminal.
    
    input1: 1 5 10
    input2: 2 7 10
    output: 6.0

### DATAENG

  Running the code is as simple as running the following command in the terminal:

    python3 solution.py --min-date 2021-01-08 --max-date 2021-05-30 --top 5

- "--min-date": start of the date range. type:str, format:"YYYY-MM-DD", default:"2021-01-08"
- "--max-date": end of the date range. type:str, format:"YYYY-MM-DD", default:"2021-05-30"
- "--top": number of rows in the WMAPE output. type:int, default:5

Result will be printed in the terminal.

    Started
    features.csv is created
    mapes.csv is created
    Finished

Then, you can open the `features.csv` and `mapes.csv` files on root dir.
