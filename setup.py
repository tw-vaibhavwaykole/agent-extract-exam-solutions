from setuptools import setup, find_packages

# Define fallback requirements in case requirements.txt is not available
FALLBACK_REQUIREMENTS = [
    "setuptools>=65.0.0",
    "wheel>=0.37.0",
    "python-dotenv",
    "openai",
    "langchain_openai",
    "langchain",
    "PyPDF2>=3.0.0"
]

def read_requirements(filename="requirements.txt"):
    """Read requirements from file, fallback to minimal requirements if file not found"""
    try:
        with open(filename) as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    except FileNotFoundError:
        return FALLBACK_REQUIREMENTS

setup(
    name="ai_exam_paper_generator",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=read_requirements(),
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "exam-generator=main:main",
        ],
    },
    author="Vaibhav Waykole",
    author_email="vaibhavwaykole@gmail.com",
    description="AI-powered exam paper generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-agent-extract-answers",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
)
