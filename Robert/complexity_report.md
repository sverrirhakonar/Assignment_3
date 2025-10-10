# Complexity Report

## Tables of runtime and memory metrics

### Data loading

| file                        |   load_time_s |   peak_mem_mb |
|:----------------------------|--------------:|--------------:|
| Robert/market_data_1k.csv   |     0.0052416 |       139.367 |
| Robert/market_data_10k.csv  |     0.0558876 |       143.625 |
| Robert/market_data_100k.csv |     0.481754  |       165.043 |

### Strategies

| strategy                      | file   |   run_time_s |   peak_mem_mb |   signals_count |
|:------------------------------|:-------|-------------:|--------------:|----------------:|
| NaiveMovingAverageStrategy    | 1k     |    0.0100881 |       168.602 |            1001 |
| NaiveMovingAverageStrategy    | 10k    |    0.760158  |       168.617 |           10001 |
| NaiveMovingAverageStrategy    | 100k   |   55.5227    |       175.133 |          100001 |
| WindowedMovingAverageStrategy | 1k     |    0.0004893 |       180.121 |            1001 |
| WindowedMovingAverageStrategy | 10k    |    0.0136695 |       180.254 |           10001 |
| WindowedMovingAverageStrategy | 100k   |    0.0915048 |       183.359 |          100001 |

## Plots of scaling behavior

![Time and memory profile](Robert/profiling_results.png)

## Narrative comparing strategies and optimization impact

Add your analysis here. Compare throughput, latency, and memory across dataset sizes. Note any optimizations and their impact.


## Additional profiling: cProfile

```
         6223190 function calls (6205838 primitive calls) in 353.602 seconds

   Ordered by: cumulative time
   List reduced from 1738 to 50 due to restriction <50>

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    434/2    0.009    0.000  352.416  176.208 C:\Users\Lenovo\anaconda3\Lib\site-packages\matplotlib\text.py:926(get_window_extent)
       34    0.012    0.000  258.286    7.597 C:\Users\Lenovo\anaconda3\Lib\threading.py:641(wait)
       21    0.001    0.000  219.946   10.474 c:\Users\Lenovo\Documents\FinMath UChicago\Coursework\FINM 32500 1 Computing for Finance in Python\Assignment 3\Assignment_3\Robert\profiler.py:11(profile_memory)
       21    0.333    0.016  212.401   10.114 C:\Users\Lenovo\anaconda3\Lib\site-packages\memory_profiler.py:269(memory_usage)
        6    0.225    0.037  188.391   31.399 c:\Users\Lenovo\Documents\FinMath UChicago\Coursework\FINM 32500 1 Computing for Finance in Python\Assignment 3\Assignment_3\Robert\profiler.py:21(run_strategies_memory_check)
      255    0.003    0.000  180.911    0.709 C:\Users\Lenovo\anaconda3\Lib\multiprocessing\connection.py:246(recv)
      255    0.005    0.000  180.905    0.709 C:\Users\Lenovo\anaconda3\Lib\multiprocessing\connection.py:310(_recv_bytes)
      170  180.895    1.064  180.895    1.064 {built-in method _winapi.WaitForMultipleObjects}
       34    0.378    0.011  154.353    4.540 C:\Users\Lenovo\anaconda3\Lib\threading.py:327(wait)
   222035    1.064    0.000  128.234    0.001 c:\Users\Lenovo\Documents\FinMath UChicago\Coursework\FINM 32500 1 Computing for Finance in Python\Assignment 3\Assignment_3\Robert\strategies.py:12(generate_signals)
   224210  126.992    0.001  127.276    0.001 {built-in method builtins.sum}
    523/2    0.041    0.000  114.092   57.046 C:\Users\Lenovo\anaconda3\Lib\site-packages\matplotlib\text.py:358(_get_layout)
      139   29.983    0.216   29.993    0.216 {method 'acquire' of '_thread.lock' objects}
      722    0.036    0.000   10.028    0.014 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:102(acquire)
       59    0.000    0.000   10.017    0.170 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:110(__enter__)
        6    0.127    0.021    8.680    1.447 c:\Users\Lenovo\Documents\FinMath UChicago\Coursework\FINM 32500 1 Computing for Finance in Python\Assignment 3\Assignment_3\Robert\profiler.py:56(run_strategies_time_check)
       85    0.001    0.000    6.238    0.073 C:\Users\Lenovo\anaconda3\Lib\multiprocessing\process.py:142(join)
      204    0.002    0.000    6.237    0.031 C:\Users\Lenovo\anaconda3\Lib\multiprocessing\popen_spawn_win32.py:105(wait)
      204    6.235    0.031    6.235    0.031 {built-in method _winapi.WaitForSingleObject}
       10    0.832    0.083    3.130    0.313 c:\Users\Lenovo\Documents\FinMath UChicago\Coursework\FINM 32500 1 Computing for Finance in Python\Assignment 3\Assignment_3\Robert\data_loader.py:11(read_csv_to_immutable_list)
   235020    1.051    0.000    1.711    0.000 C:\Users\Lenovo\anaconda3\Lib\csv.py:174(__next__)
        3    0.000    0.000    1.226    0.409 c:\Users\Lenovo\Documents\FinMath UChicago\Coursework\FINM 32500 1 Computing for Finance in Python\Assignment 3\Assignment_3\Robert\profiler.py:48(run_data_loader_time_check)
   222012    0.209    0.000    0.988    0.000 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:1160(__iter__)
   222037    0.646    0.000    0.883    0.000 c:\Users\Lenovo\Documents\FinMath UChicago\Coursework\FINM 32500 1 Computing for Finance in Python\Assignment 3\Assignment_3\Robert\strategies.py:36(generate_signals)
      657    0.017    0.000    0.751    0.001 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:1198(update)
      663    0.007    0.000    0.731    0.001 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:1325(refresh)
      669    0.005    0.000    0.708    0.001 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:1464(display)
       85    0.002    0.000    0.483    0.006 C:\Users\Lenovo\anaconda3\Lib\multiprocessing\process.py:110(start)
       85    0.001    0.000    0.462    0.005 C:\Users\Lenovo\anaconda3\Lib\multiprocessing\context.py:222(_Popen)
       85    0.002    0.000    0.462    0.005 C:\Users\Lenovo\anaconda3\Lib\multiprocessing\context.py:334(_Popen)
       85    0.005    0.000    0.460    0.005 C:\Users\Lenovo\anaconda3\Lib\multiprocessing\popen_spawn_win32.py:46(__init__)
238795/238439    0.356    0.000    0.427    0.000 {built-in method builtins.next}
       85    0.411    0.005    0.411    0.005 {built-in method _winapi.CreateProcess}
   235010    0.397    0.000    0.397    0.000 <string>:2(__init__)
     2007    0.004    0.000    0.386    0.000 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\utils.py:378(disp_len)
     2007    0.006    0.000    0.375    0.000 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\utils.py:374(_text_width)
   907924    0.357    0.000    0.357    0.000 {method 'append' of 'list' objects}
      669    0.008    0.000    0.352    0.001 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:1150(__str__)
      669    0.005    0.000    0.350    0.001 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:457(print_status)
      132    0.010    0.000    0.348    0.003 C:\Users\Lenovo\anaconda3\Lib\site-packages\matplotlib\axis.py:1287(_update_ticks)
1143533/1143481    0.340    0.000    0.340    0.000 {built-in method builtins.len}
      669    0.056    0.000    0.334    0.000 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\std.py:464(format_meter)
   370862    0.185    0.000    0.269    0.000 C:\Users\Lenovo\anaconda3\Lib\site-packages\tqdm\utils.py:375(<genexpr>)
        1    0.000    0.000    0.212    0.212 C:\Users\Lenovo\anaconda3\Lib\site-packages\matplotlib\image.py:1508(imsave)
        1    0.000    0.000    0.212    0.212 C:\Users\Lenovo\anaconda3\Lib\site-packages\PIL\Image.py:2509(save)
        1    0.000    0.000    0.207    0.207 C:\Users\Lenovo\anaconda3\Lib\site-packages\PIL\PngImagePlugin.py:1300(_save)
        1    0.000    0.000    0.207    0.207 C:\Users\Lenovo\anaconda3\Lib\site-packages\PIL\ImageFile.py:535(_save)
        1    0.000    0.000    0.207    0.207 C:\Users\Lenovo\anaconda3\Lib\site-packages\PIL\ImageFile.py:563(_encode_tile)
        3    0.206    0.069    0.206    0.069 {method 'encode' of 'ImagingEncoder' objects}
   1127/5    0.007    0.000    0.183    0.037 C:\Users\Lenovo\anaconda3\Lib\site-packages\matplotlib\text.py:65(_get_text_metrics_with_cache)



```
