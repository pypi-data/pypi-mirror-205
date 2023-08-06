import setuptools

setuptools.setup(
    name="bp_query_tool",
    version="0.0.6",
    author="Bluepinapple",
    author_email="vivek.sthul@bluepinapple.com",
    description="Query tool to generate query from selection",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.8.10",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.20.0",
    ],
)
