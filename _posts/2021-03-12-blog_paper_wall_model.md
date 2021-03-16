---
layout: single
title:  "Are wall models stable?"
date:   2021-03-16
---

The second paper from my PhD got published recently in 
[Computers and Fluids](https://www.sciencedirect.com/science/article/abs/pii/S0045793021000360).
If you don't have access, there's a free version on
[ResearchGate](https://www.researchgate.net/publication/349396252_Impact_of_wall_modeling_on_kinetic_energy_stability_for_the_compressible_Navier-Stokes_equations)
and the preprint on
[Arxiv](https://arxiv.org/abs/2102.05080).

The idea of the paper was to look at wall models from an angle that
is not usually looked at.
Wall models are a popular way to reduce the cost of simulations.
To see why let us first say something about accurate ways of solving
for flow around walls, such as say the wing of an airplane.
Direct numerical simulation(DNS) is the most
accurate way to solve the Navier Stokes equations,
but if we have a wall then the cost of simulations is crazy expensive.
I think the Channel Flow test case, which is very idealized took
9 months to solve on a supercomputer for a realistic Reynolds' number.
So usually people look at the next most accurate way of doing it,
which is large eddy simulation(LES).
However, the wall still poses a problem since the cost is
still exponenetial.
I recall a talk where people were using billions of grid points
to just solve the flow around a car. And I don't think they were even doing LES. 

Hence wall models. The idea is to do LES away from the wall, 
and use a simple model near it.
The grid need not be so refined then and so we can get away
with doing simulations at much lower cost. 
However, stability is not usually something that is looked at when 
using wall models even though it is very important.
Without stability, you submit a simulation overnight, hoping to see results in the morning
and instead you come back to see that the solver stopped barely after starting.

We looked at kinetic energy $$\frac{1}{2} \rho u^2$$($$\rho$$ being density and $$u$$ being velocity) 
to see the effects of the wall model on it.
We proved that a simple relation at the wall decides the stability.
Using this, we looked at a couple of wall models.
It turns out that the algebraic wall model, which is very popular,
is actually unstable.
Which is surprising, not only because its so popular but because it
often gives fairly accurate results.
We created an idealized test case to demonstrate this issue
on an airfoil.
So next time you simulate flow around a wall, and start seeing
robustness issues, maybe the wall model is the issue.
On the other hand a recently developed slip wall model is actually stable,
but is not accurate.
So, we decided to test one that is a hybrid of the two.
It worked fairly well but we need to push the accuracy forward.

I am happy at how the paper turned out and am really thankful to 
Prof. Nordström for pushing us to investigate this direction 
as well as his detailed revisions of the manuscript
and to Prof. Frankel for all his help.
Have a look at the paper and if you have any questions or suggestions
feel free to send me a message.











































