from sympy import symbols, exp, sin, integrate, laplace_transform, simplify

# 1. Define the mathematical symbols
t, tau, s = symbols('t tau s', positive=True)

# 2. Define the continuous-time functions
f = exp(-2*t)
g = sin(3*t)

# 3. Compute individual Laplace transforms
# noconds=True tells sympy to return just the formula, ignoring convergence conditions
F = laplace_transform(f, t, s, noconds=True)
G = laplace_transform(g, t, s, noconds=True)

# 4. Calculate their convolution in the time domain: integral from 0 to t of f(tau)*g(t-tau) d_tau
# We use .subs() to substitute the variables appropriately
conv_fg = integrate(f.subs(t, tau) * g.subs(t, t - tau), (tau, 0, t))

# 5. Compute the Laplace transform of the resulting convolution
L_conv = laplace_transform(conv_fg, t, s, noconds=True)

# 6. Compute the product of the individual Laplace transforms
product_FG = F * G

# 7. Prove the validity of the Convolution Theorem
# If L{(f*g)} == F(s)*G(s), then subtracting them should equal 0.
# We use simplify() to force sympy to resolve the algebra.
is_valid = simplify(L_conv - product_FG) == 0

# --- Print the Results ---
print(f"f(t) = {f}")
print(f"g(t) = {g}\n")

print(f"F(s) = L{{f(t)}} = {F}")
print(f"G(s) = L{{g(t)}} = {G}\n")

print(f"Convolution (f * g)(t) = \n{conv_fg}\n")

print(f"L{{(f * g)(t)}} = \n{L_conv}")
print(f"F(s) * G(s) = \n{product_FG}\n")

print(f"Does L{{(f * g)(t)}} equal F(s) * G(s)? --> {is_valid}")
