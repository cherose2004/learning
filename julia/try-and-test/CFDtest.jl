using QuadGK
using Plots

#mesh parameter
L = 1
div = 100
dx = L/div

#time parameter
t0 = 0.0
T = 5

#physics constants
g = 1.0

#initial height profile
function u0(x)
    return 0.1+0.1*exp(-64*(x-0.25)*(x-0.25))
end

#initial height vector
ini_h = [u0(i*dx-0.5dx) for i in 1:(div)]
#initial velocity vector
ini_m = [0 for i in 0:(div-1)]

ini_U=[ini_h ini_m]

function f(H,M,i)
     return (M[i], M[i]*M[i]/H[i]+(g/2)*H[i]*H[i])
end

function flux(H,M,L,R)
    if L==0
        return (0,f(H,M,R)[2])
    end
    if R==div+1
        return (0,f(H,M,L)[2])
    end
    fl = f(H,M,L)
    fr = f(H,M,R)
    d = 0.2
    return ((fl[1]+fr[1])/2+d*(H[L]-H[R])/2, (fl[2]+fr[2])/2+d*(M[L]-M[R])/2)
end

function dUdt(U,t)
    curr_dhdt = []
    curr_dmdt = []
    curr_h = U[1:div]
    curr_m = U[(div+1):(2div)]
    for i in 1:div
        flux_l = flux(curr_h,curr_m,i-1,i)
        flux_r = flux(curr_h,curr_m,i,i+1)
        push!(curr_dhdt, (flux_l[1]-flux_r[1])/dx)
        push!(curr_dmdt, (flux_l[2]-flux_r[2])/dx)
    end
    return vcat(curr_dhdt, curr_dmdt)
end


function rk4(f,t0,t1,y0,h)
    t=[t0]
    y=reshape(y0,1,length(y0))
    for tm in (t0+h):h:t1
        k1=f(y[end,:], tm)
        k2=f(y[end,:]+0.5h*k1, tm+0.5h)
        k3=f(y[end,:]+0.5h*k2, tm+0.5h)
        k4=f(y[end,:]+h*k3, tm+h)
        y=[y; transpose(y[end,:]+h*(k1+2k2+2k3+k4)/6)]
        push!(t,tm)
    end
    return t,y
end

t,y = rk4(dUdt,t0,T,ini_U,0.01)


@gif for i in 1:500
    plot([dx*i for i in 1:div],y[i,1:div],ylims=(0,0.3),label="t="*string(round(i*0.01; digits=2)))
    title!("The Wave")
end every 2

println("=============")