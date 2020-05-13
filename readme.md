What are the best k hashes and m bits values to store one million n keys (E.g. e52f43cd2c23bb2e6296153748382764) suppose we use the same MD5 hash key from pickle_hash.py and explain why?

Assuming one million keys (N), the best k value can be found with this equation: k: (m/n)ln(2). This, leads to the issue of finding the optimal M.

Let us assume a desired false probability rate of 0.05 (same as professors example). The ideal M can then be modeled as m = -(n * log(p)) / (log(2)^2).

M = -(1000000 * log(0.05)) / log(2)^2 = 14357134.36 ~ 14357135

Thus, K = (14357134.36 / 1000000) * ln(2) = 9.95 ~ 10

