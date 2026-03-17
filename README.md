# LRU Cache Toy Project

A small project to build and benchmark a **simple Least-Recently-Used (LRU) cache** implementation in Python.

This repo is a learning exercise: it re-implements an LRU cache in Python (linked list + manual eviction) and compares it to Python's built-in `functools.lru_cache`, which is implemented in C and is much faster.

---

## 🧠 What this project contains

- `main.py`: A toy LRU cache implementation (linked list + manual eviction) wrapped as a decorator.
- A benchmark comparison of the custom cache vs. `functools.lru_cache`.

---

## ▶️ How to run

From the project root:

```bash
python main.py
```

This prints timings for:
- `test_func_myCache` (your custom cache)
- `test_func_pyLRU` (Python's `functools.lru_cache`)
- `test_func_no_cache` (no caching, just baseline)

---

## 💡 What you can experiment with

- Change `cache_size` in `main()`.
- Adjust the workload (number of calls, input range, or sleep duration) to see how caching affects performance.
- Improve the implementation (e.g., use a dict for O(1) lookups, or `collections.OrderedDict`).

---

## 🛠 Notes / Next steps

- The current cache implementation uses a linear scan through a linked list for lookups, which is `O(n)` per access. That’s why `functools.lru_cache` is usually faster.
- A faster pure-Python implementation may be possible by combining a dict (for fast lookups) with a linked list (for eviction order).