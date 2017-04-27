# red_bird.py
# ----------------
# COMP3620/6320 Artificial Intelligence
# The Australian National University
# For full attributions, see attributions.txt on Wattle at the end of the course

""" This is the main file of the program. It holds the logic for the classic
    red bird game along with the main code to run a game.

    There is nothing you really need to look at in this file.

    For those of you who really want to poke around, try:
        python red_bird.py --help

    to get the full command line arguments of the program.

    ********** YOU SHOULD NOT CHANGE ANYTHING IN THIS FILE **********
"""

import sys, os, random

import layout
from game_rules import ClassicGameRules
import agents, minimax_agent

def default(arg):
    """ A function to prepare an argument string for a default argument.
        (str) -> str
    """
    return arg + ' [Default: %default]'

def parse_agent_args(args):
    """ Parse the arguments for an agent.
        (str) -> { str : str }
    """
    if not args: return {}
    pieces = args.split(',')
    opts = {}
    for p in pieces:
        if '=' in p:
            key, val = p.split('=')
        else:
            key,val = p, 1
        opts[key] = val
    return opts

def read_command( argv ):
    """ Processes the command used to run the program from the command line.
        ([str]) -> { str : object }
    """
    from optparse import OptionParser
    usage_str = """
    USAGE:      python red_bird.py <options>
    EXAMPLES:   (1) python red_bird.py -p MinimaxAgent -l anuAdversarial -a depth=4 -b GreedyBlackBirdAgent --frame_time 0.05
                        will start an adversarial game with your MinimaxAgent vs the GreedyBlackBirdAgent
                        on the anuAdversarial level
                (2) python red_bird.py -l anuAdversarial -p KeyboardAgent -b GreedyBlackBirdAgent
                        will allow you to play with the keyboard on the same level
    """
    parser = OptionParser(usage_str)

    parser.add_option('-n', '--num_games', dest='num_games', type='int',
                      help=default('the number of GAMES to play'), metavar='GAMES', default=1)
    parser.add_option('-l', '--layout', dest='layout',
                      help=default('the LAYOUT_FILE from which to load the map layout'),
                      metavar='LAYOUT_FILE', default='anuMaze')
    parser.add_option('-b', '--black_bird', dest='black_bird',
                      help=default('the black_bird agent TYPE in the agents module to use'),
                      metavar = 'TYPE', default='BlackBirdAgent')
    parser.add_option('-a','--agent_args',dest='agent_args',
                      help='Comma separated values sent to agent. e.g. "opt1=val1,opt2,opt3=val3"')
    parser.add_option('-p', '--red_bird', dest='red_bird',
                      help=default('the agent TYPE in the search_agents module to use'),
                      metavar='TYPE', default='KeyboardAgent')
    parser.add_option('-t', '--text_graphics', action='store_true', dest='text_graphics',
                      help='Display output as text only', default=False)
    parser.add_option('-q', '--quiettext_graphics', action='store_true', dest='quiet_graphics',
                      help='Generate minimal output and no graphics', default=False)
    parser.add_option('-z', '--zoom', type='float', dest='zoom',
                      help=default('Zoom the size of the graphics window'), default=1.0)
    parser.add_option('-f', '--fix_random_seed', action='store_true', dest='fix_random_seed',
                      help='Fixes the random seed to always play the same game', default=False)
    parser.add_option('--frame_time', dest='frame_time', type='float',
                      help=default('Time to delay between frames; <0 means keyboard'), default=0.1)
    parser.add_option('-c', '--catch_exceptions', action='store_true', dest='catch_exceptions',
                      help='Turns on exception handling and timeouts during games', default=False)
    parser.add_option('--timeout', dest='timeout', type='int',
                      help=default('Maximum length of time an agent can spend computing in a single game'), default=30)

    options, otherjunk = parser.parse_args(argv)
    if len(otherjunk) != 0:
        raise Exception('Command line input not understood: ' + str(otherjunk))
    args = dict()

    # Fix the random seed
    if options.fix_random_seed:
        random.seed('comp3620_6320_2014')

    # Choose a layout
    args['layout'] = layout.get_layout( options.layout )
    if args['layout'] == None:
        raise Exception("The layout " + options.layout + " cannot be found")

    # Choose a red_bird agent
    no_keyboard = options.text_graphics or options.quiet_graphics
    red_bird_type = load_agent(options.red_bird, no_keyboard)
    agent_opts = parse_agent_args(options.agent_args)
    
    red_bird = red_bird_type(0, **agent_opts) # Instantiate red_bird with agent_args
    args['red_bird'] = red_bird

    # Choose a black_bird agent
    black_bird_type = load_agent(options.black_bird, no_keyboard)
    if args['layout'].has_black_bird():
        args['black_bird'] = black_bird_type( 1 )
    else:
        args['black_bird'] = None
    
    # Choose a display format
    if options.quiet_graphics:
        import text_display
        args['display'] = text_display.NullGraphics()
    elif options.text_graphics:
        import text_display
        text_display.SLEEP_TIME = options.frame_time
        args['display'] = text_display.RedBirdGraphics()
    else:
        import graphics_display
        args['display'] = graphics_display.RedBirdGraphics(options.zoom,
            frame_time = options.frame_time)
    args['num_games'] = options.num_games
    args['catch_exceptions'] = options.catch_exceptions
    args['timeout'] = options.timeout

    return args

def load_agent(agent, no_graphics):
    """ Attempt to load the specified agent from agents.py.
        (str, bool) -> Agent
    """
    if no_graphics and agent == "KeyboardAgent":
        raise Exception("Using the keyboard requires graphics (not text display)")
    if agent in dir(agents):
        return getattr(agents, agent)
    if agent in dir(minimax_agent):
        return getattr(minimax_agent, agent)
    raise Exception("The agent " + agent + " is not specified in agents.py or minimax_agent.py.")


def run_games(layout, red_bird, black_bird, display, num_games, catch_exceptions=False,
    timeout=30):
    """ Run the given number of games with the specified layout, and agents.
        (Layout, Agent, Agent, RedBirdDisplay, int,  bool, number) -> [Game]
    """
    
    import __main__
    __main__.__dict__['_display'] = display

    rules = ClassicGameRules(timeout)
    games = []

    catch_exceptions = False

    for i in xrange(num_games):
        game_display = display
        game = rules.new_game(layout, red_bird, black_bird, display, False, catch_exceptions)
        game.run()
        games.append(game)

    if num_games > 0:
        scores = [game.state.get_score() for game in games]
        wins = [game.state.score > 0 for game in games]
        win_rate = wins.count(True)/ float(len(wins))
        print 'Average Score:', sum(scores) / float(len(scores))
        print 'Scores:       ', ', '.join([str(score) for score in scores])
        print 'Win Rate:      %d/%d (%.2f)' % (wins.count(True), len(wins), win_rate)
        print 'Record:       ', ', '.join([ ['Loss', 'Win'][int(w)] for w in wins])

    return games

if __name__ == '__main__':
    """
    The main function called when red_bird.py is run
    from the command line:

    > python red_bird.py

    See the usage string for more details.

    > python red_bird.py --help
    """
    
    args = read_command( sys.argv[1:] ) # Get game components based on input
    run_games( **args )


