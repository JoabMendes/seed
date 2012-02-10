import optparse
import sys

from pythonpackager.baseparser import parser

command_dict = {}

def load_command(name):
    full_name = 'pythonpackager.commands.%s' % name
    if full_name in sys.modules:
        return
    try:
        __import__(full_name)
    except ImportError:
        pass

class Command(object):
    name = None
    usage = None

    def __init__(self):
        assert self.name
        self.parser = optparse.OptionParser(
            usage=self.usage,
            prog='%s %s' % (sys.argv[0], self.name),
            version=parser.version)
        for option in parser.option_list:
            if not option.dest or option.dest == 'help':
                # -h, --version, etc
                continue
            self.parser.add_option(option)
        command_dict[self.name] = self
    
    def main(self, args, initial_options):
        options, args = self.parser.parse_args(args)
        
        # TODO: Pull options for env or settings file (currently ignoring initial_options)
        # TODO: Catch exceptions from command.run()
        # TODO: Setup logging in some way
        
        self.run(args, options)