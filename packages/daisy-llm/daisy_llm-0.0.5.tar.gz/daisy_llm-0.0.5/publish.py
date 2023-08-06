import subprocess

# Create distributions
subprocess.run(["py", "-m", 'build'])

# Publish distributions to PyPI
subprocess.run(["poetry", "publish"])
