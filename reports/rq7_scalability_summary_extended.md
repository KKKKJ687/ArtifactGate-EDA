# RQ7 Extended Scalability Summary

This benchmark writes and row-parses synthetic ArtifactGate manifest CSV files. Runtime is the measured manifest-processing wall time. Per-phase times are allocated shares of that measured runtime, memory is an estimate, and output size is measured from the generated manifest file. It evaluates package-processing scalability, not EDA algorithm performance or physical design complexity.

- max scale: 100000 manifest rows
- linear-fit R^2: 0.99934
- slope: 0.00304109 s per 1000 manifest rows

| scale | repeats | manifest_rows_processed | median_total_runtime_s | runtime_iqr_s | median_estimated_peak_memory_mb | median_measured_output_size_mb | status |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 1000 | 10 | 10000 | 0.00680964 | 0.00168066 | 32 | 0.14753 | PASS |
| 3000 | 10 | 30000 | 0.0161955 | 0.0058001 | 32 | 0.444122 | PASS |
| 5000 | 10 | 50000 | 0.0152852 | 0.0024742 | 32 | 0.739883 | PASS |
| 10000 | 10 | 100000 | 0.0305318 | 0.0002428 | 32 | 1.49961 | PASS |
| 30000 | 5 | 150000 | 0.0914776 | 0.00057725 | 32 | 4.49952 | PASS |
| 50000 | 5 | 250000 | 0.151844 | 0.001397 | 38.7487 | 7.49946 | PASS |
| 100000 | 3 | 300000 | 0.308181 | 0.002215 | 77.976 | 15.1904 | PASS |
