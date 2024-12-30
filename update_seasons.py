import homdgcat
import time

print("Pulling season information from HomDGCat Wiki...")
start_time = time.perf_counter()
start_time_proc = time.process_time()
homdgcat.seasons_to_csv()
elapsed_time = time.perf_counter() - start_time
elapsed_time_proc = time.process_time() - start_time_proc
elapsed_time_req = elapsed_time - elapsed_time_proc
print("Season information written to seasons.csv")
print(
    f"Request time: {elapsed_time_req:.2f} seconds\n"
    + f"Process time: {elapsed_time_proc:.2f} seconds\n"
    + f"Total time: {elapsed_time:.2f} seconds"
)
