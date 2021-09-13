using Pkg;
ls = ["IJulia" , "GR" , "PyCall" , "PyPlot" , "Plots" , "JuMP" , "LinearAlgebra" , "Distributions" , "XLSX" , "Gadfly"];
for package in ls
    println(package);
    println("Start");    
    Pkg.add(package);
    Pkg.build(package);
    println(package);
    println("Finished");
    println("---------------------------------------------------------------------------------")
end