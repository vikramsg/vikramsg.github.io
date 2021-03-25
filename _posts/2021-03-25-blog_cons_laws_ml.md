---
layout: single
title:  "Can we make machine learning more efficient using conservation laws?"
date:   2021-03-25
---


There are many differen ways to do machine learning. 
The most popular methods use neural networks.
We are usually given some data and we train the neural network to
fit this data. 
In this post I will review an interesting way to look at this problem
that converts the training problem to an ordinary differential equation.
We will look at a property of this ODE that indicates a 
possible way to optimize the training process.


The training of machine learning models require optimizing 
an objective function.
For example, using Tensorflow, you could define a loss function
in the following manner. 
This is simply least squares.

```
import keras.backend as K

def loss(y_true,y_pred):
      return K.mean( K.square( y_pred - y_true) )
```

Then you select an optimization function such as ADAM and 
then wait for the learning to happen.
But what is really happening when you do this.
Well, most popular optimization functions are really stochastic gradient descent.
Maybe I will talk of stochastic gradient descent in a future post,
but right now I am more interested in discussing gradient descent
and its connections to differential equations and conservation laws.

Let us first look at how gradient descent works.
First, define the parameters of the neural network, 
namely the weights and biases as the vector $$x$$,
and the loss function, for example the one above, as $$V$$.
What we want to do is find the minimum of this function $$V$$
and we use gradient descent for this.
Then gradient descent is simply 

$$
x^{n + 1} = x^{n} - \gamma \nabla V(x^n).
$$

Here $$\nabla V$$ is the gradient of $$V$$.
This is an iterative algorithm that states how the parameters
at step $$n+1$$ should be updated using parameters at step $$n$$
and $$\gamma$$ is called learning rate for machine learning.
The gradients in packages such as Tensorflow are done using 
automatic differentiation. The iterations in general go on until the loss function
is sufficiently small.
However, an interesting way to look at this algorithm is
to think of Euler time stepping.
You are given an equation

$$
\dot{x} = - \nabla V(x).
$$

Here $$\dot{x}$$ is the time derivative of the parameters.
This is called gradient flow.
There's an excellent blog post[^1]
that goes into more detail.
This is now simply an ordinary differential equation(ODE)
although a very big one!

But once we realize it is an ODE there are
some new ways to think of this problem.
First, we realize that we are doing Euler time stepping
and to people familiar with numerical methods 
that is usually a strict no-no.
Its usually not stable and restricts you to
using very small sized steps.
Therefore, it is possible that gradient descent is not 
very efficient especially for large problems.
Second, this suggests that we could come up
with some kind of convergence proof for the algorithm.
Of course then we have to start making assumptions about
the function $$V$$ but I guess having guarantees
on how efficiently we can do learning for a machine learning problem
would be a sort of Holy Grail.
So this is a very active area of research.
And third, we can start thinking about conservation laws
that the ODE may satisfy and investigate whether the algorithm
satisfies this law.
The second and third point is interconnected but I have separated them
because I want to talk more about this third point.


In computational fluid dynamics(CFD) which is what I work on,
conservation laws are everywhere.
In CFD, we want to conserve mass, momentum and energy,
which is what the conservation laws tell you to do.
However, when approximating the equations, we often
don't guarantee conservation resulting in bad results or the solver 
crashing. 
However, even if you do satisfy conservation, it turns out 
that the flow satisfies additional laws.
For example, the compressible Navier Stokes satisfy entropy 
conservation and it turns out if you satisfy them in your approximation
your solver becomes much more stable in general. 
My last post on wall models explored one such stability aspect.
Similarly for gradient flows there's a conservation law,
or rather a stability law that is satisfied.
To see this, we just multiply $$\nabla V$$ to the ODE to get

$$
\nabla V \cdot \dot{x} = - (\nabla V)^2. 
$$

Now we simply use the chain rule $$\frac{dV}{dx}\frac{dx}{dt} = \frac{dV}{dt}$$
to get

$$
\dot{V} = - (\nabla V)^2.
$$

Notice that the right hand side is always negative, meaning
that $$V$$ will always decrease which is what we want since
we want its minimum.
But does gradient descent do this?
We multiply $$\nabla V(x^n)$$ with the gradient descent equation to get

$$
\nabla V(x^n)
\frac{x^{n + 1} - x^{n}}{\gamma} = - ( \nabla V(x^n) )^2.
$$

Notice that the left hand side is only an approximation
for $$\dot{V}$$.
As $$\gamma$$ becomes bigger this approximation gets worse
(using Taylor series)
and so you cannot have large learning rates.



One way to solve this issue would be to define
the gradient in a different way.
This approach is called the discrete gradient approach and 
the earliest reference I found was a paper from the 70's[^2].
The first two authors of the paper are 2 giants of CFD
and of course I should not have been surprised.
Recent studies I have found usually  explore
applications in image[^3] regularization[^4]. 
In this approach we define the gradient in the following manner. 

$$
\bar{\nabla} V(x, y)
(x - y)= V(x) - V(y).
$$

Now, if we use this definition of the gradient, then 
our iterative algorithm will in fact satisfy the stability condition.
Some people familiar with CFD will recognize that this condition
looks very similar to the famous Tadmor shuffle condition [^5].
There also, we define a function such that we can satisfy a conservation law.
However, there are 2 issues that makes this new definition difficult 
to use.
First, we cannot use automatic differentiation anymore which could affect efficiency.
And second, this then becomes an implicit equation.
For example, gradient descent will look like the following 

$$
x^{n + 1} = x^{n} - \gamma \bar{\nabla} V(x^n, x^{n+1}).
$$

So, we have an implicit equation, which looks like
implicit time stepping used in CFD. 
Obviously we don't have something as simple as Euler time stepping,
but here's something that CFD tells us. 
If we do implicit time stepping, we can usually get away with much larger 
time steps. I suspect the same is true for this problem as well.
So, if we come up with efficient ways to do the implicit time stepping,
we can do training with a much larger learning rate. 
This would make it much more efficient.


So that is it. 
My aim with the post was to summarize some of the ideas 
in literature that allows people from the numerical analysis community
to get familiar with the problem. 
I think this is an interesting direction to attack the problem
and come up with solutions to make training more efficient.
Don't hesistate to contact me if you have any questions or suggestions.





### References

[^1]: [https://francisbach.com/gradient-flows/](https://francisbach.com/gradient-flows/) 
[^2]: [https://doi.org/10.1002/cpa.3160310205](https://doi.org/10.1002/cpa.3160310205)   
[^3]: [https://doi.org/10.1088/1751-8121/aa747c](https://doi.org/10.1088/1751-8121/aa747c)
[^4]: [https://arxiv.org/pdf/1805.06444.pdf](https://arxiv.org/pdf/1805.06444.pdf)   
[^5]: [https://doi.org/10.2307/2008251](https://doi.org/10.2307/2008251)












































