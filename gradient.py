'''f(x,y) = 6*(x**6) + 2*(x**4)*(y**2) + 10*(x**2) + 6*x*y + 10*(y**2) - 6*x + 4'''

# Partial derivates.
xder = '36*(x**5) + 8*(x**3)*(y**2) + 20*x + 6*y - 6'
yder = '4*x**4 + 6*x + 20*y'

# Gradient parameters.
step = 2
decrease = 3.0/2
delta = 0.000001

# Start point.
M = [0, 0]

while step > delta:
    # Gradient vector coordinates.
    gradx = eval(xder.replace('x', str(M[0])).replace('y', str(M[1])))
    grady = eval(yder.replace('x', str(M[0])).replace('y', str(M[1])))

    # Gradient vector normalization.
    gradxn = gradx / (gradx**2 + grady**2)**(1/2)
    gradyn = grady / (gradx**2 + grady**2)**(1/2)

    # New spot coordinates.
    X = M[0] - step * gradxn
    Y = M[1] - step * gradyn
    M = [X, Y]
    
    # Step decrease.
    step /= decrease

print(M[0], M[1])
