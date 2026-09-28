# AI-2026-SUT
Solutions for theoretical and practical assignments from the *Artificial Intelligence (AI)* course, **Spring 2026** (بهار ۱۴۰۵),
Computer Engineering Department, **Sharif University of Technology (SUT)**.

## Course Overview
This repository contains my work for the AI course at SUT, which introduces the theoretical and practical
aspects of artificial intelligence — techniques for optimal and near-optimal decision-making across a
variety of problems and environments.

The course covers:

- Introduction to AI and its history; intelligent agents
- **Uninformed search**: BFS, DFS, Iterative Deepening, Uniform Cost Search
- **Informed search**: admissible & consistent heuristics, Greedy Best-First Search, A\* (with optimality proof), automatic heuristic generation
- **Local search**: hill-climbing, simulated annealing, local beam search, genetic algorithms, gradient descent in continuous spaces
- **Constraint Satisfaction Problems (CSPs)**: backtracking search, LCV, MRV, forward checking, MAC, AC-3, local search for CSPs
- **Adversarial search**: minimax, alpha-beta pruning, expectiminimax
- **Markov Decision Processes (MDPs)**: policy evaluation & improvement, value iteration, policy iteration
- **Reinforcement learning**: model-based methods, temporal difference learning, Q-learning
- **Logic**: propositional logic and inference (incl. resolution), first-order logic and inference
- **Bayesian networks**: representation, independence, exact & approximate (sampling-based) inference, parameter estimation; Markov models, Hidden Markov Models (HMM), Naïve Bayes
- **Introduction to Machine Learning**: linear models, neural networks
- Applications: Natural Language Processing (NLP), Computer Vision, Robotics

## Repository Structure
Each `HW-N/` folder contains:
- The assignment PDF and the official solution PDF (as released by the course staff)
- My final submitted PDF (`AI_HWN_403106238.pdf`)
- `LaTeX/` — the LaTeX source for my theoretical answers (`.tex` files, `answers/`, `assets/`). The shared
  style file and fonts are **not** duplicated here; they come from my reusable template repo, see below.
- `Practical/` — Jupyter notebooks and supporting code/data for the practical (عملی) exercises, with large
  IDE/venv/cache files and cell outputs excluded (see notes below)

```
AI-2026-SUT/
├── HW-1/   Uninformed/informed/local search
├── HW-2/   CSP + adversarial search (Practical: Tic-Tac-Toe, Nonogram CSP)
├── HW-3/   Bayesian networks & HMMs (Practical: HMM on DNA data, time-series forecasting)
├── HW-4/   ML foundations (Practical: clustering, neural net / classifier on MNIST)
├── HW-5/   MDPs & reinforcement learning (Practical: value/policy iteration, Q-learning/SARSA)
```

## Notes
- **LaTeX template:** All theoretical answers were typeset with my own reusable Persian/XeLaTeX assignment
  template — see [Persian-LaTeX-Assignment-Template](https://github.com/theQuantaBoy/Persian-LaTeX-Assignment-Template).
  To build any `HW-N/LaTeX/*.tex` here, drop it into a copy of that template (for its `commons/style.sty` and `fonts/`).
- **Notebook outputs:** Per course instructions, cell outputs (including any animations/visualizations) were
  stripped before submission; the notebooks here reflect that same stripped state.
- **HW-4 Practical2 data:** the MNIST dataset used is not committed (see `HW-4/Practical/Practical2/DATA.md`
  for the download link) to keep the repository lightweight.

## Information
**Instructor:** Dr. Marioriyad (ماری‌اوریاد)

**Student:** Mohsen Salah
**Student ID:** 403106238
