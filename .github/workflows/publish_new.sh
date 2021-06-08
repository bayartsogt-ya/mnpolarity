# get all the tags
git fetch --prune --unshallow --tags

# get latest minor version
VERSION=$(git tag | tail -1 | tr "." "\n" | tail -1)
((VERSION++))

# get last trained model dir
LATEST_OUTPUT_DIR=$(ls output | tail -1)

echo version 0.0.$VERSION
echo output dir $LATEST_OUTPUT_DIR

# compress
cd output
zip -r $LATEST_OUTPUT_DIR.zip $LATEST_OUTPUT_DIR
cd ..

# release
gh release create 0.0.$VERSION output/$LATEST_OUTPUT_DIR.zip -t 0.0.$VERSION -F train_log.txt
