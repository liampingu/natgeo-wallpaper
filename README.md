Forked from `github.com/atareao/national-geographic-wallpaper`

`run.py` downloads metadata on all the natgeo photo of the day images and pickles them to file.

To use this file start a python3 prompt in `src/`:

```
from run import Picture, Source, NatGeo, use_picture, keyword_list
import pickle

pics = pickle.load(open('natgeo_pic_list', 'rb'))
mongolia_pics = keyword_list(pics, 'mongolia')
use_picture(mongolia_pics[-4])
```

