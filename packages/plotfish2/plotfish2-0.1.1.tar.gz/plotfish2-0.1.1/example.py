import plotfish
import time

plotfish.api_key = "my-api_key"

for i in range(1000):
    plotfish.line("hello", i)
    plotfish.progress_bar("bar", i, 10)
    plotfish.counter("count_me", 1)

print("done but still waiting")

time.sleep(1)
