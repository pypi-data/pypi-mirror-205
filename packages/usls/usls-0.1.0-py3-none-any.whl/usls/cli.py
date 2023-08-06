import sys
import rich
import re
from omegaconf import OmegaConf, DictConfig

from usls import __version__
from usls.run import run
from usls.src.utils import LOGGER, CLI_MSG_TABLE, CONSOLE



SPECIALS = {
	'--help': lambda: CONSOLE.print(CLI_MSG_TABLE()),
	'-H': lambda: CONSOLE.print(CLI_MSG_TABLE()),
	'-h': lambda: CONSOLE.print(CLI_MSG_TABLE()),
	'--version': lambda: rich.print(f"> uselesss version: {__version__}"),
	'-V': lambda: rich.print(f"> uselesss version: {__version__}"),
	'-v': lambda: rich.print(f"> uselesss version: {__version__}"),
}


# support task list
TASKS = (
	'info', 
	'inspect', 'inspect2',
	'dir_combine', 
	'label_combine',
	'spider',
	'clean', 
	'cleanup',
	'v2is',
	'vs2is',
	'play',
	'is2v',
	'classify',
	'deduplicate',
	'class_modify',
)


def cli() -> None:
	args = sys.argv[1:]

	if not args:
		CONSOLE.print(CLI_MSG_TABLE())
		return 

	cmd = {'task': 'untitled'} 	# default  TODO: msg

	# argv[1:]
	for idx, x in enumerate(args):

		# special cmd with `-` or `--`
		if x.startswith('-'):
			if x in SPECIALS.keys():
				SPECIALS[x]()
				return

		else:	# must use '=' to specify args
			if '=' in x:
				try:
					k, v = x.strip().split('=', 1)
					if k == 'task':
						assert v in TASKS, f"> Error: Task support: {TASKS} for now!"
					cmd.update({k: v})
				except Exception as E:
					rich.print(f'{E}')
					sys.exit(1) 

			elif x.lower() in TASKS and idx == 0:
				cmd.update({'task': x.lower()})
			else:
				if idx == 0:
					rich.print(f"> Warning: `{x}` is not in supported TASKS: {TASKS}")
				else:
					rich.print(f"> Warning: `{x}` is not supported, ignored by deault! You can use `sth={x}`")

	rich.print(f"> args: {cmd}")


	# check if has task
	if cmd.get('task') == 'untitled':
		LOGGER.error(f"> `task` not specified!")
	else:
		conf = OmegaConf.create(cmd) 
		run(conf) 	# run




if __name__ == '__main__':
	cli()
