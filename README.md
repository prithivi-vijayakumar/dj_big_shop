To generate a `requirements.txt` file with the dependencies currently installed in your environment, you can run the following command:

```bash
pip freeze > requirements.txt
```

This will create a `requirements.txt` file in your current directory, listing all installed Python packages along with their versions.

If you need to install these dependencies in another environment, you can use the following command:

```bash
pip install -r requirements.txt
