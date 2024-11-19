### PYTHONPATH
You need to export PYTHONPATH so that the updater module can be found.

```bash
# if use bash
echo 'export PYTHONPATH=$PYTHONPATH:$HOME/Interface-Change-Monitor/server/src/updater' >> ~/.bashrc
# if use zsh
echo 'export PYTHONPATH=$PYTHONPATH:$HOME/Interface-Change-Monitor/server/src/updater' >> ~/.zshrc
```