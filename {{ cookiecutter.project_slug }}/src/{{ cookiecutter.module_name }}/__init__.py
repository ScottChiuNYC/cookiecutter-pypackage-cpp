from .{{ cookiecutter.module_name }}_core import Point

A = Point(0, 0)
B = Point(0, 1)
C = Point(1, 1)
D = Point(1, 0)

A.SetTarget(B)
B.SetTarget(C)
C.SetTarget(D)
D.SetTarget(A)

# Simulate
for i in range(1000):
    A.Step()
    B.Step()
    C.Step()
    D.Step()

# Fetch curves
ax, ay = A.GetPursuitCurve()
bx, by = B.GetPursuitCurve()
cx, cy = C.GetPursuitCurve()
dx, dy = D.GetPursuitCurve()