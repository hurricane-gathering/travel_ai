#!/usr/bin/env python
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scripts.init_vector_store import init_vector_store
import asyncio

if __name__ == "__main__":
    asyncio.run(init_vector_store())