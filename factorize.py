import multiprocessing
from time import time
    
def factorize(num) -> list[int]:
    result = [n for n in range(1, num + 1) if num % n == 0]
    return result

def parallel_factorize(nums) -> list[list]:
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        result = pool.map(factorize, nums)
    return result

def compare_time(*nums):
    start_factorize_time = time()
    list(map(factorize, nums))
    end_factorize_time = time()
    parallel_factorize(nums)
    end_parallel_factorize_time = time()
    return f"Time factorize: {end_factorize_time - start_factorize_time}; parallel: {end_parallel_factorize_time - end_factorize_time}"
      
    
if __name__ == "__main__":
    numbers = (128, 255, 99999, 10651060, 93003032, 99566294)
    # print(list(map(factorize, numbers)))
    # print(parallel_factorize(numbers))
    print(compare_time(*numbers))