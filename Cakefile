fs = require 'fs'
path = require 'path'
util = require 'util'
{print} = require 'sys'
{spawn, exec} = require 'child_process'

defaults =
	
	output: '~/WorkspaceTest'
	project: 'bsdproject'
	bare: false

out =

	flags:
		header: '\033[95m'
		blue: '\033[94m'
		green: '\033[92m'
		yellow: '\033[93m'
		red: '\033[91m'
		end: '\033[0m'
		
		wrap: (message, flag) ->
			return flag+message+@end

	say: (module, message) ->
		util.log '['+@flags.wrap(module, @flags.blue)+']: '+message

	shout: (module, message) ->
		util.log ''
		util.log @flags.wrap('[############### ===== '+message+' ===== ###############]', @flags.yellow)
		
	error: (module, message) ->
		util.log '\n'
		util.log @flags.wrap('[############### ERROR: '+module+' ###############]', @flags.red)
		util.log message
		util.log '\n'
		util.log ''
		
	spawn: (name, command, flags, callback) ->
		
		if not command?
			command = name
		else
			if typeof command == 'function'
				command = name
				callback = command
			
		if not flags?
			flags = []
		else
			if typeof flags == 'function'
				callback = flags
				flags = []
		
		op = spawn command, flags || []
		
		op.stderr.on 'data', (data) =>
			out.error name, data.toString()
		
		op.stdout.on 'data', (data) =>
			out.say name, data.toString()
		
		op.on 'exit', (code) =>
			callback?() if code is 0
			
	exec: (command, callback) ->
		return exec command, (error, stdout, stderr) =>
			if error is null
				callback?(stdout)
			else
				@error('execute', 'Problem encountered executing the command: "'+command+'". Error details: '+error)
			
			
## Script Options
option 'o', '--output [DIR]', 'output directory for new project'
option 'c', '--config [CFG]', 'path to project feature/skeleton config'
option 'p', '--project [STR]', 'name of the project being operated on'
option 'b', '--bare', 'don\'t create a folder to wrap the project in'


######### =======  Utils  ========== #########
f_escape = (path) =>
	reg = new RegExp(' ','gi')
	return path.replace(reg, '\\ ')
	
getpath = (options) =>
	## Choose whether or not to wrap
	bare = options.bare || defaults.bare
	if not bare
		## If wrap, create a project directory
		out.say 'skeleton', 'Creating project directory...'
		project_dir = (options.output || defaults.output)
		if project_dir[-1] != '/'
			project_dir += '/'
	
		project_dir = project_dir+(options.project || defaults.project)
		out.exec 'mkdir '+project_dir
	else
		## Else just use it
		out.say 'skeleton', 'Entering project directory...'
		project_dir = (options.output || defaults.output)
	return project_dir


######### =======  Project Tools  ========== #########	
task 'newproject', 'start a new project', (options) =>

	out.shout 'install', 'Starting Installation'

	## 1: Copy skeleton over first
	install_skeleton = (callback) =>
		out.say 'skeleton', 'Copying project skeleton...'

		project_dir = getpath(options)
		sk = fs.readdirSync __dirname+'/resources/skeleton' 
		for entry in sk
			if entry in ['.DS_Store']
				continue
			cp_cmd = 'cp -R '+f_escape(__dirname+'/resources/skeleton/'+entry)+' '+f_escape(project_dir)
			out.say 'skeleton', 'Copying: '+entry
			out.exec cp_cmd

		out.exec 'chmod -R 755 '+f_escape(project_dir)
		out.say 'skeleton', 'Finished skeleton copy.'
		out.shout 'install', 'Installation complete at: '+project_dir
				
	install_skeleton()


task 'install:bootstrap', 'generate a buildout executable', (options) =>

	bootstrap_buildout = (project_dir) =>
	
		## 2: Run bootstrap		
		out.say 'install', 'Running bootstrap...'
		out.exec 'ls '+project_dir
		out.spawn 'bootstrap', '/usr/local/bin/python', [project_dir+'/bootstrap.py'], () =>
			out.say 'install', out.flags.wrap('Bootstrap complete.', out.flags.green)+' From now on, you can use `'+out.flags.wrap('cake make', out.flags.green)+'` to update dependencies.'
			out.say 'install', 'Running buildout...'
			out.spawn 'buildout', 'sh', [project_dir+'/bin/buildout'], () =>
				out.say 'install', out.flags.wrap('Buildout complete.', out.flags.green)+' Installation is complete.'
				out.shout 'install', 'Installation complete.'
				
	project_dir = getpath(options)
	bootstrap_buildout(project_dir)
	
	
task 'install:skeleton', 'copy basic project files to project destination', (options) =>
	return project_dir
	

task 'install:services', 'copy services files to project destination', (options) =>
	
	
task 'install:coffeescript', 'enable coffeescript integration in target project', (options) =>
	
	
task 'install:compass', 'enable compass integration in target project', (options) =>
	
		
task 'project:buildout', 'download and install GAE environment, supporting libraries, etc', (options) =>