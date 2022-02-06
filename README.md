# HOW TO USE

To use this project, you need a installation of python, and run the main.py in a terminal/console using:

```console
py main.py
```
This will run the main.py script, but it needs parameters to work well.

## KS model checker

To use the model checker you'll need to give 3 parameters:

Firstly, you need to specify what the script should execute. Here we want to run the model checker, here's how to do it:

```
py main.py --action=run
```

or

```
py main.py -a run
```

Then we need a ctl formula:

```
py main.py --action=run --ctl="A ( X busy )"
```

or

```
py main.py -a run -c "A ( X busy )"
```

and a path to a json containing a kripke structure:

```
py main.py --action=run --ctl="A ( X busy )" --ksfile="test_models/ks3.json"
```

or

```
py main.py -a run -c "A ( X busy )" -k "test_models/ks3.json"
```

Then press enter to execute the script.

## CTL Abstract Syntax Tree

We can execute a command to show the AST that the script will use for a CTL formula

```
py main.py --action=showAST --ctl="A ( X busy )"
```

This command will show the AST for the fomula AX busy.

We can also see all the operations that the script will use to check a CTL formula.

```
py main.py --action=showOperation --ctl="A ( X busy )"
```

## Kripke structure generator - Python

The script can also generate kripke structures.

```
py main.py --label=[a,b] --ksfile=test2.json --nbstate=6 --action=generateKS 
```

where:
`--label` is the list of all the labels you want
`--ksfile` is the destination file
`--nbstate` is the number of state
`--action=generateKS ` specified the use of the generator

## Kripke Structure Generator

There is a more user friendly way of generating structures, using the executable in the "Csharp ks gen" folder

Run it either on its own, or using a command line interpreter

Follow then the instructions, considering default mode generates without any setup from the user, and custom mode allows inputting how many states you want, and what atomic propositions you need

The resulting structure will be stored in a json file in the "Generation Result" folder
