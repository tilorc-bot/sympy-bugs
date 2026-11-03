# Local sandbox for bugcheck: SymPy master checkout (with .git, for applying fixes),
# plus gcc, g++ and rustc for compiling printed code (checker/lib/codecheck.py).
# Build context must contain ./sympy (a git checkout). Run with --network none.
FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends git gcc g++ libc6-dev rustc && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir mpmath==1.3.0 pytest==8.4.2 pytest-xdist==3.8.0 hypothesis==6.135.0 numpy==2.2.6 \
    scipy==1.15.3 antlr4-python3-runtime==4.11.1 lark==1.2.2
RUN useradd -m runner
COPY --chown=runner sympy /sympy
USER runner
RUN git config --global --add safe.directory /sympy && git config --global user.email bugcheck@localhost \
    && git config --global user.name bugcheck && python -c "import sys; sys.path.insert(0,'/sympy'); import sympy; print(sympy.__version__)"
WORKDIR /work
