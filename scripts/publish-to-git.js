#!/usr/bin/env node
// Runs the publish-to-git CLI, working around its `spawn('npm.cmd', ...)` call.
// Since the fix for CVE-2024-27980 (Node 18.20.2 / 20.12.2 and later), Windows
// refuses to spawn .cmd/.bat files without `shell: true` and throws spawn EINVAL.
// publish-to-git 1.2.0 (latest) does not pass it, so add it here for .cmd files.
const childProcess = require('child_process');

if (process.platform === 'win32') {
  const quote = arg => /[\s"]/.test(arg) ? `"${arg.replace(/"/g, '""')}"` : arg;
  const spawn = childProcess.spawn;

  childProcess.spawn = function (command, args, options) {
    if (/\.(cmd|bat)$/i.test(command) && Array.isArray(args)) {
      // one command string, since passing args with shell: true is deprecated (DEP0190)
      const line = [command].concat(args).map(quote).join(' ');
      return spawn.call(this, line, Object.assign({}, options, { shell: true }));
    }
    return spawn.apply(this, arguments);
  };
}

// publish-to-git reads child_process.spawn when it is loaded, so patch first
require('publish-to-git/main.js');
