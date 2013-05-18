(c) 2013 Carson Eisenach, Victor Luo, Caroline Miller, and David Stevens

Code created for Williams College MATH 398 - Independent Study in Linear Programming

The code here depends upon CPLEX and python package PuLP (v 1.5.3) and Python (v 2.7)

Our goal was to solve a real-world problem (described below) that could be phrased as
a binary integer problem.  We took several approaches to solving the problem, and also
explored computationally various aspects of the problem such as whether or not various
solutions were isomorphic (in a graph theoretic sense), and the implications that has 
in terms of solving the problem.  Further, our results had implications on how various
solutions should be "measured" - we only found one schedule up to isomorphism.  Therefore 
a portion of the code randomly generates Team Schedules and then judges them accoding to 
several metrics we created.

A Integer Linear Programming Model using PuLP, a LP modelling interface written in Python
and used in conjunction with either CPLEX or GLPK, to solve "The Judge Problem"

--------------- THE JUDGE PROBLEM -----------------
The judge problem is given as follows: you have a debate tournament among 16
teams.  In each round, groups of 4 teams compete with each other, each group
is judged by 3 judges.  The tournament consists of 5 rounds and each team
plays each other team once.  The assignment of judges to groups of teams is
subject to the following constraints: a judge may see any individual team at 
most once and any pair of judges can work together at most twice.

There are numerous different approaches that we can try to arrive at a solution
of course there is the traditional brute force approach, but we can also
try other things such as meet in the middle and optimizations such as
fixing a given round.  We also want to be able to find the best solution
on a given schedule.