import pandas as pd
import logging
from pathlib import Path
import sys
from typing import Union, List, Optional, Annotated

project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from src.ingest_strategy import *


def ingest_df(
    source_path: Union[str, Path],
    sep: str = "\t",
    header: Optional[int] = None,
    names: Optional[List[str]] = None,
    encoding: Optional[str] = None
) -> pd.DataFrame:
    """
    ZenML step: ingest given file into DataFrame using explicit parameters.
    Chooses strategy based on file extension via IngestContext.
    """
    context = IngestContext(source_path)
    read_kwargs = {"sep": sep}
    
    if header is not None:
        read_kwargs["header"] = header
        
    if names is not None:
        read_kwargs["names"] = names
        
    if encoding is not None:
        read_kwargs["encoding"] = encoding
        
    return context.read(**read_kwargs)