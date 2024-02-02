# Whats this
- automatic pandas data profiling from tables and views of a specific SQL Server Connection.
- basically its a quick wrap-up over pandas profiling library for quick & automatic table and views output.

# Structures
- data-profiles: pandas profiling html exports. Here's where your output html profilings will be created.
- scripts: python based script.

# Scripts
- dataprofile.py: connects to db, get list of tables and views, and for each one it generates and export pandas profiling html on output folder

## Parameteres:

- dataprofiles = "data-profiles/" # folder to save the profiles
- type = 'tables' # 'tables' or 'views
- dataobject_prefix = 'stg_nv' # prefix of the data objects to be profiled
- file_prefix = 'rd' # prefix for the profile file names

# Instructions
- create virtualenv (python -m venv venv)
- access / activate virtualenv (source venv/scripts/activate or bash script for linux based)
- install libraries from requirements.txt (pip install -r requirements.txt)
- edit .env.example file, rename or copy to .env, just for sql conn
- execute script from root path (python scripts/dataprofile.py)
- enjoy your auto profiling!
