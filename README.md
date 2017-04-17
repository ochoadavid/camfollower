# camfollower Library

A simple cam-follower generation library.

**Includes:** 
Some moviment generation functions (genfunc.py, From: {1}) and a simple plate cam generation algoritm for cilindrical (roller) follower with linear moviment (camgen.py).

**Requirements:** 
- Python 3
- Numpy
- For the notebook: matplotlib.

The algoritm starts with a disk and removes the folower geometry for every position.

**To do**:
- Pipy packaging.
- Other follower geometries (flat, curved).
- Other follower moviments (oscilating).
- Automatic calculation of velocity, acceleration, jerk, transmision angle, interference, etc. (some work in progress in the notebook)
- Include speed (rpm?, rad/s?, info)

{1} Mallik, Gosh and Dittrich, *Kinematic analysis and synthesis of mechanisms*, p. 466
