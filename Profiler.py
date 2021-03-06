import cProfile
import pstats
import io


def profile(fcn):

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fcn(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    
    return inner