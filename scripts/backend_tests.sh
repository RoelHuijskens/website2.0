

source test-setup.sh
python -m pytest tests --junit-xml=scripts/test-results.xml
