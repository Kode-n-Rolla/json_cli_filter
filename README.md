## About

This tool was originally developed to filter and analyze the results of [ffuf](https://github.com/ffuf/ffuf), but it can work with **any JSON file** that contains an array of objects.

It provides a simple and interactive **CLI interface**, allowing you to explore, narrow down, and investigate anomalies in your data using keyboard navigation and filter conditions.

Filters are **preserved across iterations**, so you can refine your search as you go.

---

## Features

- ✅ Interactive CLI with arrow keys + Enter
- ✅ Live filter editing (fields like `status`, `length`, `words`, etc.)
- ✅ Smart parsing: `> 200`, `== 404`, or even just `200` → automatically treated as `== 200`
- ✅ Page-by-page navigation through results
- ✅ Save filtered results to `.json` with custom filenames
- ✅ Easy to modify: key parameters are marked as `# CHANGE THIS`

---

## How it works

1. The script takes a **JSON file** as input.
2. The file must contain a top-level object with a `"results"` key (i.e. `{"results": [ ... ]}`).
3. All filtering is done on entries inside this `"results"` array.

You can customize:
- The number of entries shown per page
- The fields that are available for filtering
---
## Example of running
![Screenshot-of-work](https://github.com/Kode-n-Rolla/json_cli_filter/blob/main/jcf.png)
---

## Filter Syntax

- Standard comparison operators: `==`, `!=`, `>`, `<`, `>=`, `<=`
- Input like `404` is treated as `== 404`
- Leave a filter empty to skip it

---

## Install requirements
```bash
pip install -r requirements.txt
```
## Usage
```bash
python3 jcf.py results.json
