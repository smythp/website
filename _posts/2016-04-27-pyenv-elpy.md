---
layout: post
title:  "Using Elpy with pyenv in Emacs"
short: "Elpy and pyenv in Emacs"
date:   2016-04-27
image:
  feature: elpy.png
categories: emacs python
---

I use [Emacs](https://www.gnu.org/software/emacs/) to write code in Python. As someone who prefers to use the keyboard over the mouse and who doesn't mind memorizing key combinations, I've found that Emacs is great for managing both small scripts and large projects. Until recently, I'd used the built-in Python mode that comes with Emacs, which did a decent job of handling indentation, whitespace, and some syntax highlighting. While I didn't have fancy code completion, the built-in dabbrev-expand command in Emacs, which completes words based on context, did a decent job in lieu of real completion. However, I always knew there were good libraries for syntax highlighting, linting, completion, refactoring, project management, and navigation out there, and recently I decided to take the plunge and get a proper Python programming environment set up in Emacs.

I use [pyenv](https://github.com/yyuu/pyenv) to manage Python versions, allowing me to quickly switch between 2.7, 3.5, and Anaconda on a project-by-project basis. Any solution I came up with, therefore, would have to work seamlessly with pyenv. I'd also had the Elpy framework recommended to me as a good library for managing IDE features in Emacs. This post will walk you through the steps of getting Elpy to work with pyenv, and by the end you'll be able to switch between Python versions while also taking advantage of the cool IDE features afforded by Elpy.

### Installing pyenv and Elpy

First, [install pyenv](https://github.com/yyuu/pyenv#installation), if you haven't already. I also recommend the [pyenv-virtualenv plugin](https://github.com/yyuu/pyenv-virtualenv#installation), which lets you manage virtual environments using pyenv.

Once you have pyenv set up and have installed a new version of Python with the `pyenv install <version>` command, you're ready to [install elpy](https://github.com/jorgenschaefer/elpy#quick-installation):

In the command line:

```
pip install jedi flake8 yapf autopep8 importmagic
```

(You can also Install Rope instead of Jedi.)

Paste this code into your scratch buffer and evaluate it:

```
(require 'package)
(add-to-list 'package-archives
						 '("elpy" . "https://jorgenschaefer.github.io/packages/"))
```

And run:

```
M-x package-refresh-contents
M-x package-install RET elpy RET
```

To complete the elpy installation, add this code to your .emacs:

```
(package-initialize)
(elpy-enable)
```

### Getting Elpy to play nice with pyenv

You have Elpy and pyenv installed, but Elpy is still going to try to use your system Python, which isn't what you want. We're going to install a package called pyenv-mode that will force Emacs to recognize our pyenv installation. Run

```
M-x package-install RET pyenv-mode
```

and add

```
(pyenv-mode)
```

to your .emacs file. Now you can run

```
M-x elpy-config
```

To check that Flask is using the correct version and path for pyenv.

If you'd like to go one step further and have Elpy switch to a local version of pyenv when you enter a project folder, put this function in your .emacs:

```
(defun ssbb-pyenv-hook ()
"Automatically activates pyenv version if .python-version file exists."
(f-traverse-upwards
(lambda (path)
  (let ((pyenv-version-path (f-expand ".python-version" path)))
		(if (f-exists? pyenv-version-path)
				(pyenv-mode-set (s-trim (f-read-text pyenv-version-path 'utf-8))))))))

(add-hook 'find-file-hook 'ssbb-pyenv-hook)
```

Finally, to clean up whitespace on a save, add:

```
(add-hook 'before-save-hook 'whitespace-cleanup)
```

Note that this setup runs into trouble if you use the same instance of Emacs to visit local projects that have incompatible versions. If you run Emacs from a server or frequently work across different versions in this way, you may want to manually control which pyenv version is active to avoid this problem. Instead of using the function above, just call

```
M-x pyenv-mode-set
```

and type the version of Python you'd like Emacs to use. This isn't as convenient, but it's more stable.
