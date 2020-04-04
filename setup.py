import setuptools

setuptools.setup(
    name="amzfresh", 
    version="0.0.1",
    author="Obxino",
    author_email="qguo43@gmail.com",
    description="Amazon fresh delivery time availability",
    url="https://github.com/guo43/fresh_delivery",
    entry_points={'console_scripts':['fresh_deliver=fresh:main']}
)
