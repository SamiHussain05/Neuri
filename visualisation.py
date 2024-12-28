# Importing required modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Defining the function
def func(x):
    return x*x*x

# Defining the integral function
def integral_func(start, end):
    result,_ = quad(func, start, end)
    return 2 * np.pi * result

# Defining the X, Y for the function and its integral
x = np.linspace(0, 2, 1000)
y_func = func(x)
y_integ = [integral_func(0, i) for i in x]

# Creating the plots
plt.figure(figsize=(10, 5))

# Plotting the function
plt.subplot(1, 2, 1)
plt.plot(x, y_func)
plt.title('Function Plot')
plt.grid(True)

# Plotting the integral
plt.subplot(1, 2, 2)
plt.plot(x, y_integ)
plt.title('Integral Plot')
plt.grid(True)

# Displaying the plots
plt.show()