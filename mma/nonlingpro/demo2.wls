#!/usr/bin/env wolframscript
(* ::Package:: *)

Clear["Global`*"];
f=a^2+b^2+c^2+8;
lim1=a^2-b+c^2>=0;
lim2=a+b^2+c^2<=20;
lim3=-a-b^2+2==0;
lim4=b+2c^2==3;
lim5=a>=0;
lim6=b>=0;
lim7=c>=0;
lim=lim1&&lim2&&lim3&&lim4&&lim5&&lim6&&lim7;
result=Minimize[{f,lim},{a,b,c}]


N[result][[2]]
