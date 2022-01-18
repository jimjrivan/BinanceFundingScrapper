from cx_Freeze import setup, Executable

base = None

executables = [Executable(script='FundingHistory.py', base=base, icon='robot.ico')]

packages = ["idna"]
options = {
    'build_exe': {
        'packages':packages,
    },
}

setup(
    name = "FundingHistory",
    options = options,
    version = "1.0",
    description = 'Extract Funding History from Binance',
    author = 'José Ivan Marciano Junior',
    executables = executables
)