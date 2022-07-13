# deploying

create the requirements from the Pipfile with [jq](https://stedolan.github.io/jq/) like this

$ jq -r '.default  
 | to_entries[]
| .key + .value.version' \
 Pipfile.lock > requirements.txt
