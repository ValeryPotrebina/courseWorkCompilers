import numpy as np
import matplotlib.pyplot as plt

# Уравнение круга
x = np.linspace(-1.5, 1.5, 400)
y = np.linspace(-1.5, 1.5, 400)
x, y = np.meshgrid(x, y)
circle = x**2 + y**2 - 1

plt.contour(x, y, circle, [0])
plt.title('Круг: $x^2 + y^2 = 1$')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

# Уравнение гиперболы
hyperbola = x**2 - y**2 - 1

plt.contour(x, y, hyperbola, [0])
plt.title('Гипербола: $x^2 - y^2 = 1$')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()

# Уравнение эллипса
ellipse = x**2 + 2*y**2 - 1

plt.contour(x, y, ellipse, [0])
plt.title('Эллипс: $x^2 + 2y^2 = 1$')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.show()