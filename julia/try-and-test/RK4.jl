"""
# 四阶Runge-Kutta方法（迭代版本）
```math
\\frac{dy}{dx} = f(x , y)\\\\
y(x_0) = y_0\\\\
x\\in [x_0 , x_e]
```
"""
function RK4_iter(f , x::Float64 , y::Float64 , h::Float64 = 0.1)
    k1 = f(x , y);
    k2 = f(x+h/2. , y+k1*h/2.);
    k3 = f(x+h/2. , y+k2*h/2.);
    k4 = f(x+h , y+k3*h);
    x_next = x + h;
    y_next = y + (k1 + 2*k2 + 2*k3 + k4)/6.;
    x_next , y_next;
end


"""
# 四阶Runge-Kutta方法
```math
\\frac{dy}{dx} = f(x , y)\\\\
y(x_0) = y_0\\\\
x\\in [x_0 , x_e]
```
"""
function RK4(f , x0::Float64 , y0::Float64 , xe::Float64 , h::Float64 = 0.1)
    n = Int(floor((xe - x0) / h));
    x = zeros(n);
    y = zeros(n);
    x[1] , y[1] = x0 , y0;
    for i = 1:n-1
        x[i+1] , y[i+1] = RK4_iter(f , x[i] , y[i] , h);
    end
    x , y
end