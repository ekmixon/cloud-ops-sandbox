# SRE Recipes

SRE Recipes is a tool to help users familiarize themselves with finding the root cause of a breakage using monitoring.

## Usage

To view which recipes exist, run the command below in this directory:

```
$ python3 sandboxctl --help
```
To simulate a break in a specific recipe, run:
```
$ python3 sandboxctl break <recipe_name>
```
To restore the original condition after simulating a break in a specific recipe, run:
```
$ python3 sandboxctl restore <recipe_name>
```
To verify the root cause of the breakage in specific recipe, run:
```
$ python3 sandboxctl verify <recipe_name>
```

## Contributing

To contribute a new recipe, create a new folder in the [recipes directory](./recipes). The directory must include a class that extends the abstract base class found in [recipe.py](recipe.py).