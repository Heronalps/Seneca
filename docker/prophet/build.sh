python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --no-cache

pip uninstall -y matplotlib
find "$VIRTUAL_ENV/lib/python3.6/site-packages" -name "test" | xargs rm -rf
find "$VIRTUAL_ENV/lib/python3.6/site-packages" -name "tests" | xargs rm -rf
rm -rf "$VIRTUAL_ENV/lib/python3.6/site-packages/pystan/stan/src"
rm -rf "$VIRTUAL_ENV/lib/python3.6/site-packages/pystan/stan/lib/stan_math/lib"
echo "venv size $(du -sh $VIRTUAL_ENV | cut -f1)"