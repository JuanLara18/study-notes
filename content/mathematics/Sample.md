---
title: "Introduction to Derivatives"
date: 2024-01-15
category: mathematics
tags: [calculus, derivatives, limits]
author: Example Author
---

# Introduction to Derivatives

The derivative of a function represents its rate of change at any given point. This fundamental concept in calculus has numerous applications in physics, economics, and other fields.

## Definition

The derivative of a function $f(x)$ at a point $x$ is defined as:

$$
f'(x) = \lim_{h \to 0} \frac{f(x + h) - f(x)}{h}
$$

## Basic Rules

Here are some fundamental derivative rules:

1. Power Rule: For any function $f(x) = x^n$, its derivative is:
   $$\frac{d}{dx}(x^n) = nx^{n-1}$$

2. Sum Rule: $\frac{d}{dx}(f(x) + g(x)) = f'(x) + g'(x)$

## Implementation in Python

We can implement a basic derivative calculator for polynomials:

```python
def power_rule_derivative(coefficient, power):
    return (coefficient * power, power - 1)

def derive_polynomial(terms):
    """
    Takes a list of (coefficient, power) tuples
    Returns the derivative as a list of terms
    """
    return [power_rule_derivative(coef, pow) 
            for coef, pow in terms 
            if pow > 0]

# Example usage
polynomial = [(2, 3), (-1, 1), (5, 0)]  # 2x³ - x + 5
derivative = derive_polynomial(polynomial)
# Result: [(6, 2), (-1, 0)]  # 6x² - 1
```

## Applications

One common application is finding local maxima and minima by solving $f'(x) = 0$. This is particularly useful in optimization problems, such as:

- Finding the optimal price point in economics
- Calculating the maximum height of a projectile
- Minimizing cost functions in machine learning