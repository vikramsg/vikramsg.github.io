---
title: 'About me'
layout: single
author_profile: true
---

I am a PostDoc at the Max Planck Institute for Meteorology.
I work at the boundary between mathematics and code development. 
Developing code to solve real world problems require pushing the boundaries of both which is my goal. 
I have increasingly become interested in the mathematics of keeping physics models stable as well as the techniques required to make them efficient. 

I am also interested in how machine learning can be used to improve physics modelling for fluids. 
We already use many different models which need to be tuned. 
Machine learning in theory should be able to make that easier. 

At MPIM, I work on the ocean model ICON-O. 
Keeping climate models stable is a complex problem and requires careful analysis of the numerical method. 
I have been working on improving the structure preserving numerics of ICON-O to push the model towards more accuracy and stability.

I did my PhD at Technion, Israel.
I worked on the Discontinuous Galerkin (DG) method, an arbitrary high-order, unstructured method for the solving the compressible Navier Stokes (CNS) equation. 
High order methods sufferer from aliasing instabilities which leads to robustness issues. 
I showed that we can solve this issue if we used split forms. 
In addition, split forms work well with wall modeling to enable high Reynolds' number flows.
I wrote the solver in C++ making extensive use of the [MFEM](https://github.com/mfem/mfem) library.

