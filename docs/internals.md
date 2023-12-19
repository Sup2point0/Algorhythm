# Internals

Explaining some of the rationale and design decisions behind *Algorhythm*.


<br>


## Structure


<br>


## Technicalities


<br>


## Learnings

- Git can’t stop tracking a file already being tracked, so you’ve gotta delete it and re-create it.
- VSCode executes code (at least for Python) with the directory open in Explorer as the current working directory.
  - We can configure it to execute from a particular directory with the `PYTHONPATH` variable in a `.env` file.
