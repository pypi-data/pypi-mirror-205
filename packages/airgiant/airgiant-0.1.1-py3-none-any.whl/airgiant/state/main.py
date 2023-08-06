from imports import *

# GLOBAL variables 

person1 = [0,0,0]           # xyz of detected person > see SkelCoord()
rwristperson = [0,0,0]
lwristperson = [0,0,0]
finalstate = 0              # confident state > see decision()
i = 1                       # true condition
p = 0                       # person detected (0 not, 1 detected)
ac=3


from behavior import *
from .make_decision import *


logging.basicConfig(
    format="%(asctime)s %(message)s",
    level=logging.CRITICAL #.DEBUG,
)
asyncio.run(auto())


