## Chart prompt

```python
def answer_to_chart(question: str, results: str) -> str:
    # write a prompt to generate a chart, execute it and save the results
    # to a file with a random filename
    prompt = f"""Given this question:

{question}

and these results:

{results}

write some Python code with matplotlib.pyplot to create a chart 
which illustrates this data.

Only return the Python code. DON'T explain your work. 
Don't use plt.show(), use plt.save('image.png')."""

question = "show me pings in 2022, broken down by month"
results = """month         total_pings\n----------  -------------\n2022-01-01           4237\n2022-02-01           4819\n2022-03-01           4873\n2022-04-01           1527\n2022-05-01           5564\n2022-06-01           9915\n2022-07-01          12931\n2022-08-01          20464\n2022-09-01          22462\n2022-10-01          16082\n2022-11-01          17473\n2022-12-01           9940"""
```
