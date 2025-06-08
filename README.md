# Shift Optimizer

This repository contains a simple script to create an optimized shift schedule.

## Usage

Prepare two CSV files:

1. `shift.csv` &ndash; availability table. The first column should be member
   names and the following columns indicate availability with `○`.
2. `attribute.csv` &ndash; member attributes with columns `name`, `gender`, and
   `committee` (`〇` when a member belongs to the committee).

Run the optimizer:

```bash
python shift_optimizer.py --shift path/to/shift.csv \
                          --attr path/to/attribute.csv \
                          --out path/to/output.csv
```

If any of the arguments are omitted, the script will prompt for them.
