import launch

if not launch.is_installed("openai"):
    launch.run_pip("install openai", "requirement for Lazy Wildcard")
