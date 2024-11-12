helpFunction()
{
   echo ""
   echo "Usage: $0 -d path to dump of model -m path to model"
   echo -e "\t-d determine path to saved model"
   echo -e "\t-m determine path to module with model api"
   exit 1 # Exit script after printing help
}

while getopts "d:m:" opt
do
   case "$opt" in
      d ) dump_path="$OPTARG" ;;
      m ) model_api="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done

docker run \
        -v "$dump_path:/local_model_storage:rw" \
        -v "$model_api:/model:rw" \
        -p 8000:8000 \
        --platform linux/amd64 \
        --name model_backend model_backend-img 
      #   /bin/bash # -c 'pip install -r /model/requirements.txt; sudo python & /src/api.py; /bin/bash'
