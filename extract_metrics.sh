#!/bin/bash
# CK Tool ile her sürüm için metrik çıkarımı

VERSIONS=("1.0.0.0" "1.1.0.0" "1.3.0.0" "2.0.0.0" "2.2.0.0" "2.4.0.0" "2.7.0.0" "2.10.0.0" "2.13.0.0" "2.16.0.0" "2.19.0.0" "3.0.0.0")
REPO_DIR="/Users/bilgem/software_design_project/anomaly-detection"
OUTPUT_DIR="/Users/bilgem/software_design_project/metrics"
CK_JAR="/Users/bilgem/software_design_project/ck-0.7.0-jar-with-dependencies.jar"

mkdir -p "$OUTPUT_DIR"

for VERSION in "${VERSIONS[@]}"; do
    echo "=== Processing version $VERSION ==="

    # Checkout the tag
    cd "$REPO_DIR"
    git checkout "$VERSION" --quiet 2>/dev/null

    # Create output directory for this version
    VERSION_DIR="$OUTPUT_DIR/$VERSION"
    mkdir -p "$VERSION_DIR"

    # Count Java files
    JAVA_COUNT=$(find src/main/java -name "*.java" 2>/dev/null | wc -l | tr -d ' ')
    echo "  Java files: $JAVA_COUNT"

    # Run CK Tool
    java -jar "$CK_JAR" "$REPO_DIR/src/main/java" false 0 false "$VERSION_DIR/" 2>/dev/null

    if [ -f "$VERSION_DIR/class.csv" ]; then
        LINE_COUNT=$(wc -l < "$VERSION_DIR/class.csv" | tr -d ' ')
        echo "  Classes analyzed: $((LINE_COUNT - 1))"
    else
        echo "  ERROR: No output generated"
    fi
done

# Return to main branch
cd "$REPO_DIR"
git checkout main --quiet 2>/dev/null

echo ""
echo "=== All versions processed ==="
