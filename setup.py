from cx_Freeze import setup, Executable

# Define the executables
executables = [Executable("visual-2d-line.py", target_name="visual-2d-line")]

# Define the setup options
setup(
    name="visual-2d-line-tool",
    version="0.1",
    description="polynomial time algorithms visualisation",
    executables=executables,
)
