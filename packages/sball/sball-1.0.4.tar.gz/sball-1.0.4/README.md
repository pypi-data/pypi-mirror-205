# sball

`sball` facilitates submitting multiple scripts in Slurm job arrays using Yale's dSQ module. "sball" is short for "sbatch all".

## Usage

After installing using `pip`, you can run `sball` as a command. It takes a few arguments, which are the following. Any additional arguments not provided here are passed along to `sbatch` when the job array is submitted. Arguments must be specified as `key=value` pairs, with the exception of the `pattern` argument, which should always be passed as the final argument. Additional arguments should be specified in the usual way for `sbatch`; i.e., `--$argument_name $argument_value`.

If you need to include spaces in arguments, make sure to escape them by using single quotes. If you do not escape `pattern` using single quotes, make sure to escape any `*` in the glob expression with a backslash, since otherwise they will be expanded by the shell before sball gets them.

- `name`: (required) the name to give the job array.
- `regex`: (optional) only scripts with filenames matching `regex` will be included in any arrays.
- `log_dir`: (optional) the directory where log files for the job array should be stored. Default is `joblogs`.
- (`pattern`): (required, not named) a glob expression that matches scripts to include in job arrays. Only files ending in `.sh` that match the glob will be included. If a glob expression is insufficient to filter to just the scripts you want, you should use the `regex` argument.
- Additional arguments are passed to the underlying calls to `sbatch`. This allows you to, e.g., set up job dependencies. They should be inserted _before_ the final, pattern argument.

## Description

`sball` finds all `.sh` scripts matching `pattern` (and `regex`, if provided). If scripts are found, it sorts them into bins with unique sets of SBATCH options (since job arrays must all be run with the same SBATCH options). For each bin, the scripts are added to a job file, where the contents of each script takes up a single line. These files are named `$name.txt`, and are saved in the deepest directory common to all scripts in a bin. In case there is more than one bin, the file is suffixed with their bin number. Then, `dsq` called to create a job script from this file with the SBATCH options for that bin. Finally, the created job script is submitted to the queue with `sbatch`, and the (now unnecessary) job script is removed. The `$name.txt` files must be present when the job actually procs in the queue, so they are not removed (and should not be removed until after the jobs finish).

In case a bin contains only one script, that script is just submitted in the usual way with `sbatch`, as a fallback.

## Examples

Sample directory structure:
```
main-project-directory/
├── ...
│
└── scripts/
	├── script1.sh
	├── script2.sh
	├── script3.sh
	└── ...
```

To submit all the scripts in `main-project-directory/scripts` in a job array named `my-job-array`, from `main-project-directory` you would run:
```bash
module load dSQ # if not already loaded
sball name=my-job-array scripts/\*
```

Note that the `*` in the glob expression in `pattern` is escaped. After running this, your job array will be created, and you will have a new file in `main-project-directory/scripts` that Slurm references to find the jobs.
```
main-project-directory/
├── ...
│
└── scripts/
	├── script1.sh
	├── script2.sh
	├── script3.sh
	├── ...
	└── my-job-array.txt
```
After your job array finishes running, you can safely remove `my-job-array.txt`. You can make further refinements of which scripts to run by changing the glob expression, or by using the `regex=` argument.