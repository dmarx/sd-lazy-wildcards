import launch

for lib in "openai loguru".split():
    if not launch.is_installed(lib):
        launch.run_pip(f"install {lib}", "requirement for Lazy Wildcard")
