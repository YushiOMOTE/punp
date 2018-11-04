from dataclasses import dataclass
from pypp import pypp
from typing import List, Tuple, Dict, Optional

import json
import yaml


@pypp
@dataclass
class SubTest:
    p: int
    q: int
    r: float


@pypp
@dataclass
class Test:
    i: int
    j: float
    k: complex
    l: SubTest
    m: List[int]
    x: Tuple[int, str, str, float]
    y: Dict[float, str]
    z: Optional[int]


def main():
    j = Test(json.loads('''
    {"i": 3,
     "j": 0.5,
     "k": 3.5,
     "l": {"p": 3, "q": 4, "r": 3.3},
     "m": [1,2,3],
     "x": [3, "key", "val", 1.5],
     "y": {"1.0": "ittenzero"}}
    '''))

    print(f'parse json: {j}')

    y = Test(yaml.load('''
    i: 3
    j: 0.5
    k: 3.5
    l:
      p: 3
      q: 4
      r: 3.3
    m: [1,2,3]
    x:
      - 3
      - "key"
      - "val"
      - 1.5
    y:
      1.0: ittenzero
    '''))

    print(f'parse yaml: {y}')


if __name__ == '__main__':
    main()
