import setuptools

setuptools.setup(
    name="streamlit_lang_tts",
    version="0.0.5",
    author="Ryan Rapp",
    author_email="skies_midair0f@icloud.com",
    description="Streamlit extensions for text-to-speech",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 0.63",
    ],
)
