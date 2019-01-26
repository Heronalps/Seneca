python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache

pip uninstall scipy -y
pip uninstall numpy -y
find "$VIRTUAL_ENV/lib/python3.6/site-packages" -name "test" | xargs rm -rf
find "$VIRTUAL_ENV/lib/python3.6/site-packages" -name "tests" | xargs rm -rf
echo "venv size $(du -sh $VIRTUAL_ENV | cut -f1)"