import werkzeug

# Monkey-patching the __version__ attribute for compatibility with Flask's test client.
# Newer versions of Werkzeug (>=3.0) remove this attribute.
werkzeug.__version__ = "2.2.2" # A version that is known to be compatible.
