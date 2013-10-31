# a number of constants

from custom_types import ForceFactor

# scaling between pixels and metres
SCALE = 100.0


# scaling factors the social force model
SF_FACTORS = ForceFactor(
    social = 2.1, 
    desired = 1.0, 
    obstacle = 1.0, 
    lookahead = 1.0
    )


SIGN = lambda x: (1, -1)[x < 0.0]