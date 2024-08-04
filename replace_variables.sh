#!/bin/bash

# Function to process a file and replace environment variables
process_file() {
    local file=$1
    local temp_file=$(mktemp)

    local changes_made=false

    # Read the original file and process it line by line
    while IFS= read -r line || [[ -n $line ]]; do
        modified_line=$line
        # Use a while loop to replace all occurrences of #!{VAR_NAME}!# with the value of the environment variable
        while [[ $modified_line =~ (\#\!\{([a-zA-Z_][a-zA-Z_0-9]*)\}\!\#) ]]; do
            var_name=${BASH_REMATCH[2]}
            var_value=${!var_name}

            if [ -z "$var_value" ]; then
                echo "Warning: Environment variable '$var_name' is not set. Skipping replacement."
                var_value=""
            fi

            # Replace all occurrences of #!{VAR_NAME}!# with the value of the environment variable
            modified_line=${modified_line//${BASH_REMATCH[1]}/$var_value}
            changes_made=true
        done
        # Write the modified line to the temporary file
        echo "$modified_line" >> "$temp_file"
    done < "$file"

    # Only replace the original file if changes were made
    if $changes_made; then
        mv "$temp_file" "$file"
    else
        rm "$temp_file"
    fi
}

# Function to recursively traverse directories
process_directory() {
    local dir=$1

    # Traverse all files in the directory
    for entry in "$dir"/*; do
        # Skip if the entry is this script
        if [[ $entry == "$0" ]]; then
            continue
        fi

        if [[ -d $entry ]]; then
            process_directory "$entry"
        elif [[ -f $entry ]]; then
            process_file "$entry"
        fi
    done
}

# If .env file exists, load the environment variables
if [[ -f .env ]]; then
    source .env
fi

# Base directory (default is the current directory)
base_dir=${1:-.}

# Process the base directory
process_directory "$base_dir"

echo "Variable replacement completed."