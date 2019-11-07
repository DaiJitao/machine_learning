from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure()
ax = Axes3D(fig)

x1 = np.arange(-20, 20, 1)
x2 = np.arange(-20, 20, 1)
x1, x2 = np.meshgrid(x1, x2)
f = np.power(x1,2) + .5 * np.square(x2) + 3 * x2 + 4.5
print(x1, x2)
plt.xlabel("x")
plt.ylabel("y")
ax.plot_surface(x1,x2,f,rstride=1,cstride=1, cmap="rainbow")
plt.show()